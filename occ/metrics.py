"""Métricas do protocolo: ACC com casamento húngaro (All/Old/New) e rejeição."""
import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import roc_auc_score


def _hungarian_map(y_true, y_pred):
    """Mapeia rótulos previstos para verdadeiros maximizando acertos."""
    t = np.unique(y_true)
    p = np.unique(y_pred)
    W = np.zeros((len(p), len(t)), int)
    ti = {v: i for i, v in enumerate(t)}
    pi = {v: i for i, v in enumerate(p)}
    for a, b in zip(y_pred, y_true):
        W[pi[a], ti[b]] += 1
    r, c = linear_sum_assignment(-W)
    return {p[i]: t[j] for i, j in zip(r, c)}


def cluster_acc(y_true, y_pred):
    """ACC de clustering (NCD / C1): casamento húngaro em todo o conjunto."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    m = _hungarian_map(y_true, y_pred)
    return float(np.mean([m.get(a, None) == b for a, b in zip(y_pred, y_true)]))


def gcd_acc(y_true, y_pred, old_classes):
    """ACC All/Old/New (C2/C3), na versão 'v2' de Vaze et al.

    O casamento húngaro é feito uma vez sobre todas as classes de D_U;
    Old e New são as acurácias, sob esse mesmo casamento, nas amostras
    de classes Old e New. É a versão usada pelo SimGCD.
    """
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    m = _hungarian_map(y_true, y_pred)
    hit = np.array([m.get(a, None) == b for a, b in zip(y_pred, y_true)])
    old = np.isin(y_true, list(old_classes))
    return {
        "all": float(hit.mean()),
        "old": float(hit[old].mean()) if old.any() else float("nan"),
        "new": float(hit[~old].mean()) if (~old).any() else float("nan"),
    }


def rejection_metrics(novelty, is_new, alpha_reject=None):
    """AUROC Old×New, FPR@95%TPR e taxa de falsa rejeição de Old.

    novelty: escore de novidade (maior = mais provável classe nova)
    is_new:  1 para amostras de classes novas
    alpha_reject: máscara booleana das amostras rejeitadas (opcional)
    """
    novelty, is_new = np.asarray(novelty), np.asarray(is_new).astype(bool)
    out = {"auroc": float(roc_auc_score(is_new, novelty))}
    # FPR@95: fração de New ACEITA como Old quando 95% das Old são aceitas
    thr = np.quantile(novelty[~is_new], 0.95)
    out["fpr95"] = float(np.mean(novelty[is_new] <= thr))
    if alpha_reject is not None:
        rej = np.asarray(alpha_reject, bool)
        out["old_false_reject"] = float(rej[~is_new].mean())
        out["new_reject"] = float(rej[is_new].mean())
    return out
