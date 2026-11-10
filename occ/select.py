"""Escolha da família de OCC só com D_L (sem rótulos de D_U).

Protocolo "deixa uma classe de fora" (leave-one-class-out): para cada classe
conhecida c de um subconjunto, finge que c é nova. Os OCCs são treinados nas
demais classes com uma parte das amostras (fração train_frac); o escore de
novidade é medido nas amostras de c (positivas) e nas amostras restantes das
demais classes (negativas, nunca vistas no treino). O critério é o AUROC
médio sobre as classes deixadas de fora; vence a família de maior AUROC.

O AUROC mede só a separação antigas × novas, que é o que a família muda no
pipeline; a calibração e o agrupamento são os mesmos para todas.
"""
import numpy as np
from sklearn.metrics import roc_auc_score

from .calibration import ClassWiseOCC


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


def select_family(X_l, y_l, families=("gauss", "knn", "mst", "dic"),
                  occ_kwargs=None, random_state=0, **kw):
    """Devolve (família escolhida, {família: AUROC})."""
    occ_kwargs = occ_kwargs or {}
    scores = {f: loco_auroc(f, X_l, y_l, occ_kwargs.get(f), random_state=random_state, **kw)
              for f in families}
    valid = {f: s for f, s in scores.items() if s == s}
    best = max(valid, key=valid.get) if valid else families[0]
    return best, scores
