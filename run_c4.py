"""Cenário C4: GCD incremental (contínuo), em sessões.

Protocolo (inspirado no Continual GCD de MetaGCD/Happy, adaptado às bases
do PBN):

- Sessão 0: D_L com metade das amostras de cada classe conhecida (divisão
  de classes do PBN). Nenhum rótulo depois disso.
- As classes novas são sorteadas (pela semente) e divididas igualmente em
  T sessões (--sessions, padrão 3).
- Sessão t = 1..T: chega um lote não rotulado U_t com
    * 1/T da metade restante de cada classe conhecida;
    * 60% das amostras das classes novas que estreiam em t;
    * o resto das classes novas de sessões anteriores, em partes iguais
      nas sessões seguintes (uma classe descoberta precisa ser
      reconhecida depois, não descoberta de novo).
  As sessões são disjuntas: nenhuma amostra aparece duas vezes.
- Padronização: média e desvio de D_L da sessão 0 apenas (o futuro não é
  conhecido); desvios abaixo de 10% da mediana são elevados a esse piso,
  para não criar valores extremos em atributos quase constantes.

Métodos:
- OCC (gauss, knn, mst, dic, svm, svm@g, svm-cv, auto, auto-auroc): família
  escolhida na sessão 0 (só D_L); em cada sessão, discover() e depois
  incorporate(): cada cluster descoberto vira um OCC novo; os OCCs antigos
  não são re-treinados e nenhuma amostra bruta de sessões anteriores é
  guardada (kNN e MST guardam as amostras da própria classe, que são o
  modelo).
- rf_msp: Random Forest + MSP re-treinada a cada sessão com D_L e as
  amostras das classes descobertas (pseudorrótulos), que precisam ficar
  guardadas.
- sskmeans: SS-k-means a cada sessão, com D_L + amostras pseudorrotuladas
  das classes descobertas como parte rotulada.

Métricas por sessão (CSV, uma linha por método × semente × sessão):
- acc_all/acc_old/acc_new: o casamento entre ids previstos e classes
  verdadeiras é FIXO depois de feito: um cluster descoberto na sessão t é
  casado (húngaro) com uma classe ainda não casada nessa sessão e mantém
  esse casamento nas seguintes. Assim, um erro de descoberta se propaga,
  como na prática. Old = classes vistas antes de t (conhecidas e
  descobertas antes); New = classes que estreiam em t.
- acc_s0: acurácia nas classes da sessão 0 (esquecimento = queda entre a
  sessão 1 e a última).
- acc_all_hung: ACC All com casamento húngaro refeito na sessão, como no
  C2 (para comparação).
- n_model_classes, t_session_s.
- Diagnóstico dos clusters espúrios (os criados na sessão que não casam
  com nenhuma classe): spur_from_s0 / spur_from_prev / spur_from_new contam
  quantos têm como classe majoritária uma classe da sessão 0, uma classe
  já descoberta antes ou uma classe que estreia na sessão; spur_size_mean
  é o tamanho médio deles.

Incorporação (--inc-min): por padrão, só vira classe um cluster com pelo
menos tau amostras, o tamanho esperado de um fragmento de classe antiga
(o mesmo limiar usado pelo HDBSCAN); com 'fixed', basta 5 amostras. O
mesmo limiar vale para os pseudorrótulos guardados pelo rf_msp. O
sskmeans não tem rejeição nem tau e usa 5.

Uso:
    python run_c4.py --data data/pendigits --seeds 0 1 2 3 4 \\
        --families mst svm-cv auto-auroc rf_msp sskmeans --out results_c4/pendigits_c4.csv
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

from occ import (ClosedMSP, OCCDiscovery, SSKMeans, SVM_GRID, parse_spec,
                 select_family)
from occ.metrics import gcd_acc


# --------------------------------------------------------------------- dados
def load(path, no_preproc=False):
    X = np.load(os.path.join(path, "X_train.npy"))
    y_raw = np.load(os.path.join(path, "y_train.npy"))
    with open(os.path.join(path, "split.json")) as f:
        known_raw = json.load(f)["known"]
    l2 = False
    pp = os.path.join(path, "preproc.json")
    if os.path.exists(pp) and not no_preproc:
        with open(pp) as f:
            cfg = json.load(f)
        if cfg.get("drop_cols"):
            X = np.delete(X, cfg["drop_cols"], axis=1)
        if cfg.get("l2"):
            X = X / np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)
            l2 = True
        print(f"pré-processamento {cfg}")
    classes, y = np.unique(y_raw, return_inverse=True)
    known = np.flatnonzero(np.isin(classes, known_raw))
    return X.astype(float), y, known, l2


def sessions_split(y, known, T, seed):
    """Devolve (idx_l, [idx_1..idx_T], estreia) com estreia[c] = sessão."""
    rng = np.random.default_rng(seed)
    classes = np.unique(y)
    novel = rng.permutation(classes[~np.isin(classes, known)])
    groups = np.array_split(novel, T)
    debut = {int(c): 0 for c in known}
    for t, g in enumerate(groups, start=1):
        for c in g:
            debut[int(c)] = t
    idx_l, sess = [], [[] for _ in range(T)]
    for c in classes:
        idx = rng.permutation(np.flatnonzero(y == c))
        if debut[int(c)] == 0:
            n_l = len(idx) // 2
            idx_l.append(idx[:n_l])
            for t, part in enumerate(np.array_split(idx[n_l:], T)):
                sess[t].append(part)
        else:
            t0 = debut[int(c)]
            if t0 == T:
                sess[T - 1].append(idx)
            else:
                n0 = int(round(0.6 * len(idx)))
                sess[t0 - 1].append(idx[:n0])
                for k, part in enumerate(np.array_split(idx[n0:], T - t0)):
                    sess[t0 + k].append(part)
    return (np.concatenate(idx_l), [np.concatenate(s) for s in sess], debut)


def scaler_s0(X_l):
    mu = X_l.mean(0)
    sd = X_l.std(0)
    floor = 0.1 * np.median(sd[sd > 0]) if (sd > 0).any() else 1.0
    return mu, np.maximum(sd, floor)


# ------------------------------------------------------------------ métodos
class OCCStream:
    def __init__(self, family, alpha, k_est, seed, auto_families, criterion, inc_min="tau",
                 merge=True):
        self.inc_min, self.merge = inc_min, merge
        self.family, self.alpha, self.k_est, self.seed = family, alpha, k_est, seed
        self.auto_families, self.criterion = auto_families, criterion
        self.chosen = None

    def start(self, X_l, y_l):
        fam = self.family
        if fam in ("auto", "auto-auroc", "svm-cv"):
            cands = [f"svm@{g:g}" for g in SVM_GRID] if fam == "svm-cv" else self.auto_families
            crit = "auroc" if fam == "auto-auroc" else self.criterion
            fam, _ = select_family(X_l, y_l, cands, {}, self.seed, criterion=crit,
                                   alpha=self.alpha, k_est=self.k_est)
            self.chosen = fam
        base, kws = parse_spec(fam)
        self.m = OCCDiscovery(base, kws, alpha=self.alpha, random_state=self.seed,
                              cal_mode="nested", k_est=self.k_est).fit(X_l, y_l)
        return self

    def session(self, X_u, fresh):
        y = self.m.discover(X_u)
        if self.merge:
            y = self.m.merge_duplicates(X_u, y, ratio=self.merge)
        y = fresh(y, self.m.model_.classes_)
        tau = getattr(self.m, "last_tau_", None) if self.inc_min == "tau" else None
        self.m.incorporate(X_u, y, min_size=tau)
        return y

    def n_classes(self):
        return len(self.m.model_.classes_)


class MSPStream:
    """Classificador fechado re-treinado a cada sessão (guarda os dados)."""

    def __init__(self, alpha, k_est, seed, inc_min="tau"):
        self.alpha, self.k_est, self.seed = alpha, k_est, seed
        self.inc_min = inc_min

    def start(self, X_l, y_l):
        self.Xm, self.ym = X_l.copy(), y_l.copy()
        return self

    def session(self, X_u, fresh):
        m = ClosedMSP("rf", alpha=self.alpha, random_state=self.seed,
                      k_est=self.k_est).fit(self.Xm, self.ym)
        y = fresh(m.discover(X_u), m.classes_)
        tau = getattr(m, "last_tau_", None) if self.inc_min == "tau" else None
        self._remember(X_u, y, m.classes_, tau)
        self.k = len(np.unique(self.ym))
        return y

    def _remember(self, X_u, y, old, min_size=None):
        thr = 5 if min_size is None else max(5, min_size)
        new = ~np.isin(y, old)
        keep = np.zeros(len(y), bool)
        for c in np.unique(y[new]):
            if (y == c).sum() >= thr:
                keep |= y == c
        self.Xm = np.vstack([self.Xm, X_u[keep]])
        self.ym = np.r_[self.ym, y[keep]]

    def n_classes(self):
        return len(np.unique(self.ym))


class SSKStream(MSPStream):
    def session(self, X_u, fresh):
        old = np.unique(self.ym)
        y = SSKMeans(random_state=self.seed).fit_predict(self.Xm, self.ym, X_u, None)
        y = fresh(y, old)
        self._remember(X_u, y, old)
        return y


# ----------------------------------------------------------------- avaliação
class Matcher:
    """Casamento fixo id previsto -> classe verdadeira, construído sessão a sessão."""

    def __init__(self, known):
        self.map = {int(c): int(c) for c in known}  # conhecidas: id = classe

    def update(self, y_true, y_pred):
        claimed = set(self.map.values())
        new_pred = [p for p in np.unique(y_pred) if int(p) not in self.map]
        free_true = [c for c in np.unique(y_true) if int(c) not in claimed]
        if new_pred and free_true:
            W = np.zeros((len(new_pred), len(free_true)))
            for i, p in enumerate(new_pred):
                for j, c in enumerate(free_true):
                    W[i, j] = np.sum((y_pred == p) & (y_true == c))
            r, c = linear_sum_assignment(-W)
            for i, j in zip(r, c):
                if W[i, j] > 0:
                    self.map[int(new_pred[i])] = int(free_true[j])
        for p in new_pred:  # sem par: nunca acerta
            self.map.setdefault(int(p), -999)

    def hits(self, y_true, y_pred):
        return np.array([self.map.get(int(p), -999) == int(t) for p, t in zip(y_pred, y_true)])


def run(args):
    X, y, known, l2 = load(args.data, args.no_preproc)
    rows = []
    for seed in args.seeds:
        idx_l, sess, debut = sessions_split(y, known, args.sessions, seed)
        if l2:
            Xs = X
        else:
            mu, sd = scaler_s0(X[idx_l])
            Xs = (X - mu) / sd
        X_l, y_l = Xs[idx_l], y[idx_l]
        for fam in args.families:
            if fam == "rf_msp":
                st = MSPStream(args.alpha, args.k_est, seed, args.inc_min)
            elif fam == "sskmeans":
                st = SSKStream(args.alpha, args.k_est, seed, args.inc_min)
            else:
                st = OCCStream(fam, args.alpha, args.k_est, seed,
                               args.auto_families, args.auto_criterion, args.inc_min,
                               0 if args.no_merge else args.merge_ratio)
            t0 = time.perf_counter()
            st.start(X_l, y_l)
            t_start = time.perf_counter() - t0
            matcher = Matcher(known)
            counter = [int(y.max()) + 1000]

            def fresh(yp, model_classes):
                """Ids novos -> ids globais únicos (evita colisão entre sessões)."""
                yp = np.asarray(yp).copy()
                mc = set(int(c) for c in model_classes)
                for p in np.unique(yp):
                    if int(p) not in mc:
                        counter[0] += 1
                        yp[yp == p] = counter[0]
                return yp

            for t, idx in enumerate(sess, start=1):
                Xu, yu = Xs[idx], y[idx]
                t1 = time.perf_counter()
                yp = st.session(Xu, fresh)
                dt = time.perf_counter() - t1
                seen_before = set(matcher.map)
                matcher.update(yu, yp)
                hit = matcher.hits(yu, yp)
                # diagnóstico: clusters novos desta sessão que não casaram com
                # nenhuma classe (espúrios) — de que tipo de classe vêm?
                spur = {"s0": 0, "prev": 0, "new": 0}
                sizes = []
                for p_ in np.unique(yp):
                    if int(p_) in seen_before or matcher.map.get(int(p_)) != -999:
                        continue
                    tc = np.bincount(yu[yp == p_]).argmax()
                    s_ = debut[int(tc)]
                    spur["s0" if s_ == 0 else ("prev" if s_ < t else "new")] += 1
                    sizes.append(int((yp == p_).sum()))
                d = np.array([debut[int(c)] for c in yu])
                old_cls = [c for c, s in debut.items() if s < t and s >= 0]
                r = {"family": fam, "seed": seed, "session": t,
                     "acc_all": hit.mean(),
                     "acc_old": hit[d < t].mean() if (d < t).any() else np.nan,
                     "acc_new": hit[d == t].mean() if (d == t).any() else np.nan,
                     "acc_s0": hit[d == 0].mean(),
                     "acc_all_hung": gcd_acc(yu, yp, old_cls)["all"],
                     "n_model_classes": st.n_classes(),
                     "n_spurious": sum(1 for p in np.unique(yp) if matcher.map.get(int(p)) == -999),
                     "n_true_classes": len([c for c, s in debut.items() if s <= t]),
                     "spur_from_s0": spur["s0"], "spur_from_prev": spur["prev"],
                     "spur_from_new": spur["new"],
                     "spur_size_mean": float(np.mean(sizes)) if sizes else np.nan,
                     "t_session_s": dt, "t_start_s": t_start,
                     "chosen": getattr(st, "chosen", None)}
                rows.append(r)
                print(f"seed={seed} {fam:11s} S{t} all={r['acc_all']:.3f} "
                      f"old={r['acc_old']:.3f} new={r['acc_new']:.3f} s0={r['acc_s0']:.3f} "
                      f"classes={r['n_model_classes']}/{r['n_true_classes']} t={dt:.1f}s",
                      flush=True)
    df = pd.DataFrame(rows)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        df.to_csv(args.out, index=False)
        print(f"Resultados salvos em {args.out}")
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--sessions", type=int, default=3)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--alpha", type=float, default=0.1)
    ap.add_argument("--k-est", default="hdbscan-leaf",
                    choices=["silhouette", "sil-size", "hdbscan", "hdbscan-leaf"])
    ap.add_argument("--families", nargs="+",
                    default=["mst", "gauss", "svm-cv", "auto-auroc", "rf_msp", "sskmeans"])
    ap.add_argument("--auto-families", nargs="+",
                    default=["gauss", "knn", "mst", "dic"] + [f"svm@{g:g}" for g in SVM_GRID])
    ap.add_argument("--auto-criterion", choices=["acc", "auroc"], default="auroc")
    ap.add_argument("--inc-min", choices=["tau", "fixed"], default="tau",
                    help="tamanho mínimo de um cluster para virar classe: 'tau' "
                         "(padrão; o tamanho esperado de um fragmento de classe "
                         "antiga, o mesmo limiar do HDBSCAN) ou 'fixed' (5 amostras)")
    ap.add_argument("--no-merge", action="store_true",
                    help="OCC: não junta clusters novos a classes existentes "
                         "(OCCDiscovery.merge_duplicates)")
    ap.add_argument("--merge-ratio", type=float, default=0.0,
                    help="OCC: junta um cluster novo a uma classe existente se a "
                         "distância entre os centros for <= ratio x o raio típico "
                         "dessa classe (padrão 0 = desligado; no digits não "
                         "ajudou)")
    ap.add_argument("--no-preproc", action="store_true")
    ap.add_argument("--out", default=None)
    run(ap.parse_args())


if __name__ == "__main__":
    main()
