"""Escolha da família de OCC só com D_L (sem rótulos de D_U).

Dois critérios, ambos simulando classes novas com classes conhecidas
escondidas:

- "auroc" (padrão, loco_auroc): esconde uma classe conhecida por vez;
  OCCs treinados nas demais (fração train_frac de cada uma); AUROC do
  escore de novidade entre a classe escondida e as amostras restantes das
  demais. Mede só a rejeição.

- "acc" (loco_eval; pior que "auroc" nos testes do PBN, results_v5/): simula o GCD inteiro. Em cada repetição,
  esconde n_hidden classes conhecidas (2 se houver ao menos 4, senão 1);
  D_L' = train_frac das demais; D_U' = o resto das demais + todas as
  escondidas. Roda o pipeline completo (rejeição, HDBSCAN, reatribuição)
  e mede a ACC All húngara em D_U'. Captura também o que vem depois da
  rejeição: duas famílias com o mesmo AUROC podem deixar conjuntos
  rejeitados mais ou menos fáceis de agrupar. Empates (diferença menor
  que tie_tol) são decididos pelo AUROC simulado.
"""
import numpy as np
from sklearn.metrics import roc_auc_score

from .calibration import ClassWiseOCC
from .metrics import gcd_acc


SVM_GRID = (0.1, 0.3, 1.0, 3.0, 10.0)  # multiplicadores do gamma "scale"


def parse_spec(spec):
    """'svm@3' -> ('svm', {'gamma_mult': 3.0}); outras famílias sem mudança."""
    fam, _, val = spec.partition("@")
    if fam == "svm" and val:
        return "svm", {"gamma_mult": float(val)}
    return fam, None


def loco_auroc(family, X_l, y_l, occ_kwargs=None, n_hold=5, train_frac=0.7,
               random_state=0):
    X_l, y_l = np.asarray(X_l, float), np.asarray(y_l)
    rng = np.random.default_rng(random_state)
    classes = np.unique(y_l)
    if len(classes) < 3:  # sobraria uma classe só para treinar
        return np.nan
    hold = rng.permutation(classes)[:min(n_hold, len(classes))]
    aucs = []
    for c in hold:
        rest = y_l != c
        tr = np.zeros(len(y_l), bool)
        for k in classes[classes != c]:  # divisão estratificada das demais
            idx = rng.permutation(np.flatnonzero(y_l == k))
            tr[idx[:max(2, int(round(train_frac * len(idx))))]] = True
        te = rest & ~tr
        if not te.any():
            continue
        m = ClassWiseOCC(family, occ_kwargs or {}, random_state=random_state,
                         cal_mode="cv").fit(X_l[tr], y_l[tr])
        Xt = np.vstack([X_l[y_l == c], X_l[te]])
        lab = np.r_[np.ones((y_l == c).sum()), np.zeros(te.sum())]
        aucs.append(roc_auc_score(lab, m.novelty_score(Xt)))
    return float(np.mean(aucs)) if aucs else np.nan


def _splits(y_l, n_rep, n_hidden, train_frac, rng):
    """Gera (hidden, tr, te) com conjuntos de classes escondidas distintos."""
    classes = np.unique(y_l)
    seen, out, tries = set(), [], 0
    while len(out) < n_rep and tries < 50 * n_rep:
        tries += 1
        hidden = tuple(sorted(rng.choice(classes, n_hidden, replace=False).tolist()))
        if hidden in seen:
            continue
        seen.add(hidden)
        rest = ~np.isin(y_l, hidden)
        tr = np.zeros(len(y_l), bool)
        for k in classes[~np.isin(classes, hidden)]:
            idx = rng.permutation(np.flatnonzero(y_l == k))
            tr[idx[:max(2, int(round(train_frac * len(idx))))]] = True
        out.append((np.array(hidden), tr, rest & ~tr))
    return out


def loco_eval(family, X_l, y_l, occ_kwargs=None, n_rep=5, n_hidden=None,
              train_frac=0.7, random_state=0, alpha=0.1, k_est="hdbscan-leaf",
              frag_c=2.0):
    """GCD simulado em D_L. Devolve {'acc': ACC All média, 'auroc': AUROC médio}."""
    from .gcd import OCCDiscovery  # evita import circular
    X_l, y_l = np.asarray(X_l, float), np.asarray(y_l)
    rng = np.random.default_rng(random_state)
    n_cls = len(np.unique(y_l))
    if n_cls < 2:
        return {"acc": np.nan, "auroc": np.nan}
    if n_hidden is None:
        n_hidden = 2 if n_cls >= 4 else 1
    accs, aucs = [], []
    for hidden, tr, te in _splits(y_l, n_rep, n_hidden, train_frac, rng):
        is_new = np.isin(y_l, hidden)
        U = te | is_new
        if not te.any():
            continue
        m = OCCDiscovery(family, occ_kwargs or {}, alpha=alpha, random_state=random_state,
                         cal_mode="cv", k_est=k_est, frag_c=frag_c).fit(X_l[tr], y_l[tr])
        y_hat = m.discover(X_l[U], k_new=None)
        old = np.unique(y_l[tr])
        accs.append(gcd_acc(y_l[U], y_hat, old)["all"])
        aucs.append(roc_auc_score(is_new[U], m.novelty_score(X_l[U])))
    if not accs:
        return {"acc": np.nan, "auroc": np.nan}
    return {"acc": float(np.mean(accs)), "auroc": float(np.mean(aucs))}


def select_family(X_l, y_l, families=("gauss", "knn", "mst", "dic"),
                  occ_kwargs=None, random_state=0, criterion="auroc", tie_tol=0.005,
                  **kw):
    """Devolve (família escolhida, {chave: valor}) com os escores de cada candidata.

    Uma candidata pode ser uma variante, como 'svm@3' (gamma_mult = 3).
    criterion="acc": ACC All do GCD simulado, desempate pelo AUROC simulado.
    criterion="auroc": o critério original (só rejeição).
    kw: alpha, k_est, frag_c (repassados ao GCD simulado).
    """
    occ_kwargs = occ_kwargs or {}
    acc, auc = {}, {}
    for f in families:
        fam, kws = parse_spec(f)
        kk = kws if kws is not None else occ_kwargs.get(fam)
        if criterion == "acc":
            r = loco_eval(fam, X_l, y_l, kk, random_state=random_state, **kw)
            acc[f], auc[f] = r["acc"], r["auroc"]
        else:
            auc[f] = loco_auroc(fam, X_l, y_l, kk, random_state=random_state)
    main = acc if criterion == "acc" else auc
    valid = {f: v for f, v in main.items() if v == v}
    if not valid:
        best = families[0]
    else:
        top = max(valid.values())
        tied = [f for f, v in valid.items() if v >= top - (tie_tol if criterion == "acc" else 0)]
        best = max(tied, key=lambda f: (auc.get(f, -1) if auc.get(f) == auc.get(f) else -1, valid[f]))
    scores = {**{f"auc_{f}": v for f, v in auc.items()}, **{f"acc_{f}": v for f, v in acc.items()}}
    return best, scores
