"""Executa as famílias de OCC no cenário C1 (NCD) ou C2 (GCD transdutivo).

Entrada: atributos fixos em .npy (ou .npz/.csv) e rótulos inteiros ou texto.

Exemplos:
    python run_gcd.py --X feats.npy --y labels.npy --scenario c2
    python run_gcd.py --X feats.npy --y labels.npy --families gauss knn modes \
        --seeds 0 1 2 3 4 --out results/cub_dino.csv
    python run_gcd.py --demo            # base digits do scikit-learn
    python run_gcd.py --data data/pendigits --seeds 0   # divisão do PBN

Nada aqui usa rótulos de D_U para escolher parâmetros: alpha é fixo e
K_new é estimado em D_L ∪ D_U pelo critério de Vaze et al. (--k-est labeled,
padrão), pela silhueta (--k-est silhouette) ou dado com --k-known.
Com --k-est labeled, a mesma estimativa vale para todos os métodos.

Sufixo "+ssk" em uma família (ex.: mst+ssk, rf_msp+ssk): os rejeitados
são agrupados pelo SS-k-means com as classes antigas ancoradas em D_L.
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from occ import (BASELINE_NAMES, FAMILY_NAMES, SSK_NAMES, ClosedMSP, OCCDiscovery,
                 SSKMeans, cluster_acc, estimate_k, estimate_k_labeled, gcd_acc,
                 rejection_metrics, select_family, select_per_class, parse_spec,
                 SVM_GRID)
from splits import gcd_split, ncd_split


def load(path):
    if path.endswith(".npy"):
        return np.load(path)
    if path.endswith(".npz"):
        d = np.load(path)
        return d[d.files[0]]
    return pd.read_csv(path, header=None).values


def run_one(family, X_l, y_l, X_u, y_u, old_classes, scenario, alpha, k_known,
            occ_kwargs, seed, cal_mode="cv", k_est="silhouette", frag_c=2.0,
            auto_families=("gauss", "knn", "mst", "dic"), auto_criterion="auroc"):
    """family: nome da família, uma variante ('svm@3'), 'svm-cv' (gamma do
    SVM escolhido em D_L), 'auto' (família escolhida em D_L pelo critério
    auto_criterion), 'auto-auroc' (o mesmo, sempre com o critério AUROC,
    para comparar os dois critérios na mesma rodada) ou 'auto-pc' (seleção
    por classe: cada classe conhecida com a sua própria família)."""
    t0 = time.perf_counter()
    novelty = None
    family, _, assign = family.partition("+")
    assign = assign or "kmeans"
    extra = {}
    family_map = None
    if family == "auto-pc":  # seleção por classe (occ/select.py: select_per_class)
        spec, chosen, sc = select_per_class(X_l, y_l, auto_families, occ_kwargs, seed)
        family_map = {}
        for k, f in chosen.items():
            fam_k, kws_k = parse_spec(f)
            family_map[k] = (fam_k, kws_k if kws_k is not None else occ_kwargs.get(fam_k))
        extra = {"chosen": spec, "t_select_s": time.perf_counter() - t0,
                 "chosen_pc": ";".join(f"{k}:{f}" for k, f in chosen.items()),
                 "n_switched": sum(f != spec for f in chosen.values())}
        extra.update({f"loco_{f}": v for f, v in sc.items()})
        family = spec
    elif family in ("auto", "auto-auroc", "svm-cv"):  # escolha só com D_L (occ/select.py)
        cands = [f"svm@{g:g}" for g in SVM_GRID] if family == "svm-cv" else auto_families
        crit = "auroc" if family == "auto-auroc" else auto_criterion
        spec, sc = select_family(X_l, y_l, cands, occ_kwargs, seed,
                                 criterion=crit, alpha=alpha,
                                 k_est=k_est if k_est in ("sil-size", "hdbscan", "hdbscan-leaf")
                                 else "hdbscan-leaf", frag_c=frag_c)
        extra = {"chosen": spec, "t_select_s": time.perf_counter() - t0}
        extra.update({f"loco_{f}": v for f, v in sc.items()})
        family = spec
    family, kws = parse_spec(family)
    if kws is not None:
        occ_kwargs = {**occ_kwargs, family: kws}
    if family == "kmeans":  # piso sem D_L: k-means sobre D_U, K total = n_old + k_new
        n_old_u = len(old_classes) if scenario == "c2" else 0  # C1: D_U só tem novas
        k = n_old_u + k_known if k_known else \
            estimate_k(X_u, n_old_u + 1 if n_old_u else 2,
                       max(n_old_u + 2, 3 * len(old_classes)), seed)
        y_hat = KMeans(k, n_init=10, random_state=seed).fit_predict(X_u)
        res = {"n_rejected": np.nan, "k_new": k - n_old_u}
    elif family == "sskmeans":  # piso com D_L, sem rejeição
        m = SSKMeans(random_state=seed)
        y_hat = m.fit_predict(X_l, y_l, X_u, k_new=k_known)
        res = {"n_rejected": np.nan, "k_new": m.k_new_}
    elif family in ("rf_msp", "lr_msp"):  # classificador fechado + MSP
        m = ClosedMSP(family[:2], alpha=alpha, random_state=seed,
                      assign=assign, k_est=k_est, frag_c=frag_c).fit(X_l, y_l)
        y_hat, res = m.discover(X_u, k_new=k_known, return_info=True)
        novelty = m.novelty_score(X_u)
    else:
        m = OCCDiscovery(family, occ_kwargs.get(family), alpha=alpha,
                         random_state=seed, cal_mode=cal_mode,
                         assign=assign, k_est=k_est, frag_c=frag_c,
                         family_map=family_map).fit(X_l, y_l)
        t_fit = time.perf_counter() - t0
        y_hat, res = m.discover(X_u, k_new=k_known, return_info=True)
        novelty = m.novelty_score(X_u)
        res["t_fit_s"] = t_fit
    res.update(extra)
    res["t_total_s"] = time.perf_counter() - t0
    is_new = ~np.isin(y_u, old_classes)
    if scenario == "c1":
        res["acc"] = cluster_acc(y_u, y_hat)
    else:
        a = gcd_acc(y_u, y_hat, old_classes)
        res.update({"acc_all": a["all"], "acc_old": a["old"], "acc_new": a["new"]})
        if novelty is not None:
            res.update(rejection_metrics(novelty, is_new, y_hat_rejected(y_hat, old_classes)))
    res["k_true_new"] = int(is_new.any() and len(np.unique(y_u[is_new])))
    return res


def y_hat_rejected(y_hat, old_classes):
    """Máscara de amostras que NÃO receberam uma classe Old."""
    return ~np.isin(y_hat, old_classes)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", help="pasta gerada por prepare_pbn_datasets.py "
                    "(usa X_train/y_train e as classes conhecidas de split.json)")
    ap.add_argument("--X")
    ap.add_argument("--y")
    ap.add_argument("--demo", action="store_true", help="usa a base digits")
    ap.add_argument("--scenario", choices=["c1", "c2"], default="c2")
    ap.add_argument("--families", nargs="+",
                    default=BASELINE_NAMES + FAMILY_NAMES,
                    help="OCCs: " + " ".join(FAMILY_NAMES) +
                         "; baselines: " + " ".join(BASELINE_NAMES) +
                         "; opcional: sufixo +ssk (ex.: mst+ssk, " + " ".join(SSK_NAMES) + ")")
    ap.add_argument("--old-frac", type=float, default=0.5)
    ap.add_argument("--labeled-frac", type=float, default=0.5)
    ap.add_argument("--old-classes", nargs="+", default=None,
                    help="classes Old fixas (ex.: divisão do PBN); senão sorteia")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0])
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--k-known", action="store_true",
                    help="usa o número verdadeiro de classes novas")
    ap.add_argument("--k-est", choices=["labeled", "silhouette", "sil-size", "hdbscan", "hdbscan-leaf"],
                    default="labeled",
                    help="estimativa de K_new quando --k-known não é usado: "
                         "'labeled' (Vaze et al., em D_L ∪ D_U, a mesma para "
                         "todos os métodos); 'silhouette' (cada método estima "
                         "nos seus rejeitados); 'sil-size', 'hdbscan' e 'hdbscan-leaf' (nos "
                         "rejeitados, com correção dos fragmentos de classes "
                         "antigas; ver occ/fragments.py). Sem rejeição "
                         "(kmeans, sskmeans), as três últimas usam a silhueta.")
    ap.add_argument("--auto-families", nargs="+",
                    default=["gauss", "knn", "mst", "dic"] + [f"svm@{g:g}" for g in SVM_GRID],
                    help="candidatas da família 'auto' (escolha por deixa-uma-"
                         "classe-de-fora em D_L); 'svm@g' é o SVM com gamma = "
                         "g x o 'scale' do scikit-learn")
    ap.add_argument("--auto-criterion", choices=["acc", "auroc"], default="auroc",
                    help="critério do auto/svm-cv: 'auroc' (padrão; esconde uma "
                         "classe por vez, AUROC da rejeição) ou 'acc' (GCD simulado "
                         "em D_L, ACC All; pior nos testes: results_v5/)")
    ap.add_argument("--frag-c", type=float, default=2.0,
                    help="sil-size/hdbscan*: tau = frag_c x tamanho esperado de "
                         "um fragmento")
    ap.add_argument("--scale", choices=["all", "labeled", "none"], default="all",
                    help="padronização: 'all' usa D_L ∪ D_U (só atributos, sem "
                         "rótulos; padrão no cenário transdutivo); 'labeled' usa "
                         "só D_L; 'none' não padroniza")
    ap.add_argument("--cal-mode", choices=["cv", "split", "nested"], default="cv",
                    help="calibração dos OCCs; 'nested' remove o vazamento do Dic")
    ap.add_argument("--modes-base", default="knn", choices=["gauss", "knn", "mst", "svm"])
    ap.add_argument("--repr", default="raw",
                    help="representação (occ/represent.py): raw, pcaN, pcawN, 'qpca' quantílica + PCA "
                         "branqueada (sem rótulos); 'rfleaf' folhas de uma floresta "
                         "treinada em D_L")
    ap.add_argument("--no-preproc", action="store_true",
                    help="ignora data/<base>/preproc.json")
    ap.add_argument("--out", default=None, help="CSV de resultados")
    args = ap.parse_args()

    if args.demo:
        from sklearn.datasets import load_digits
        X, y_raw = load_digits(return_X_y=True)
    elif args.data:
        X = np.load(os.path.join(args.data, "X_train.npy"))
        y_raw = np.load(os.path.join(args.data, "y_train.npy"))
        pp = os.path.join(args.data, "preproc.json")
        if os.path.exists(pp) and not args.no_preproc:
            # pré-processamento da base, o mesmo para todos os métodos:
            #   drop_cols: colunas removidas; l2: normaliza cada linha (a
            #   distância euclidiana vira função do cosseno) e desliga a
            #   padronização, que destruiria essa normalização
            with open(pp) as f:
                cfg = json.load(f)
            if cfg.get("drop_cols"):
                X = np.delete(X, cfg["drop_cols"], axis=1)
            if cfg.get("l2"):
                X = X / np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)
                args.scale = "none"
            print(f"pré-processamento {cfg}: X {X.shape}, scale={args.scale}")
        if not args.old_classes:
            with open(os.path.join(args.data, "split.json")) as f:
                args.old_classes = [str(c) for c in json.load(f)["known"]]
    else:
        X, y_raw = load(args.X), load(args.y).ravel()
    names, y = np.unique(y_raw, return_inverse=True)
    old_fixed = None
    if args.old_classes:
        old_fixed = np.flatnonzero(np.isin(names.astype(str), args.old_classes))

    occ_kwargs = {"modes": {"base": args.modes_base}}
    rows = []
    for seed in args.seeds:
        if args.scenario == "c2":
            il, iu, old = gcd_split(y, args.old_frac, args.labeled_frac, old_fixed, seed)
        else:
            il, iu, old = ncd_split(y, args.old_frac, old_fixed, seed)
        X_l, y_l, X_u, y_u = X[il], y[il], X[iu], y[iu]
        if args.scale != "none":
            # 'labeled': só D_L. Pode criar valores extremos quando um atributo
            # quase não varia nas classes antigas mas varia nas novas (no
            # digits chega a 90 desvios e derruba o k-means de 0,78 para 0,59).
            # 'all': D_L ∪ D_U, legítimo no transdutivo (nenhum rótulo usado).
            sc = StandardScaler().fit(X_l if args.scale == "labeled"
                                      else np.vstack([X_l, X_u]))
            X_l, X_u = sc.transform(X_l), sc.transform(X_u)
        if args.repr != "raw":
            from occ.represent import transform
            X_l, X_u = transform(args.repr, X_l, y_l, X_u, random_state=seed)
        k_true = len(np.unique(y_u[~np.isin(y_u, old)]))
        if args.k_known:
            k_new, k_mode = k_true, "known"
        elif args.k_est == "labeled" and args.scenario == "c2":
            t = time.perf_counter()
            k_new = estimate_k_labeled(X_l, y_l, X_u, random_state=seed)
            k_mode = "labeled"
            print(f"seed={seed} K_new estimado (Vaze) = {k_new} "
                  f"(verdadeiro {k_true}) em {time.perf_counter() - t:.0f}s", flush=True)
        else:
            k_new, k_mode = None, args.k_est
        for fam in args.families:
            r = run_one(fam, X_l, y_l, X_u, y_u, old, args.scenario, args.alpha,
                        k_new, occ_kwargs, seed, args.cal_mode, args.k_est,
                        args.frag_c, tuple(args.auto_families), args.auto_criterion)
            r.update({"family": fam, "seed": seed, "k_mode": k_mode})
            rows.append(r)
            show = (f"acc={r['acc']:.3f}" if args.scenario == "c1" else
                    f"all={r['acc_all']:.3f} old={r['acc_old']:.3f} new={r['acc_new']:.3f}"
                    + (f" auroc={r['auroc']:.3f}" if "auroc" in r else ""))
            print(f"seed={seed} {fam:11s} {show} k_new={r['k_new']} "
                  f"t={r['t_total_s']:.1f}s", flush=True)

    df = pd.DataFrame(rows)
    metric_cols = [c for c in ["acc", "acc_all", "acc_old", "acc_new", "auroc",
                               "fpr95", "old_false_reject", "k_new", "t_total_s"]
                   if c in df]
    print("\nMédia por família:")
    print(df.groupby("family")[metric_cols].mean().round(3).to_string())
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        df.to_csv(args.out, index=False)
        print(f"\nResultados salvos em {args.out}")


if __name__ == "__main__":
    main()
