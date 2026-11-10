"""Estimativa do número de classes novas.

- estimate_k: silhueta em um único conjunto (sem rótulos).
- estimate_k_labeled: método de Vaze et al. (CVPR 2022). Roda k-means em
  D_L ∪ D_U para cada K total candidato e escolhe o K que maximiza a ACC
  húngara nas amostras ROTULADAS. Com K pequeno, classes antigas se fundem
  com novas; com K grande, as antigas se partem: os dois erros aparecem em
  D_L, que tem rótulo. Nenhum rótulo de D_U é usado.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from .metrics import cluster_acc


def estimate_k(X, k_min=2, k_max=20, random_state=0, max_eval=3000):
    """K pela silhueta (o índice que melhor foi no PBN)."""
    n = len(X)
    k_max = min(k_max, n - 1)
    if k_max < k_min:
        return 1
    rng = np.random.default_rng(random_state)
    Xe = X[rng.choice(n, max_eval, replace=False)] if n > max_eval else X
    best_k, best_s = k_min, -np.inf
    for k in range(k_min, k_max + 1):
        lab = KMeans(k, n_init=5, random_state=random_state).fit_predict(Xe)
        if len(np.unique(lab)) < 2:
            continue
        s = silhouette_score(Xe, lab)
        if s > best_s:
            best_k, best_s = k, s
    return best_k


def estimate_k_labeled(X_l, y_l, X_u, k_max_new=None, random_state=0,
                       max_eval=5000, n_init=3, return_curve=False):
    """Número de classes NOVAS pelo critério de Vaze et al.

    Devolve k_new = K_total* - n_old, com K_total* = argmax_K ACC(D_L).
    Em caso de empate, fica o menor K.
    """
    X_l, X_u, y_l = np.asarray(X_l, float), np.asarray(X_u, float), np.asarray(y_l)
    rng = np.random.default_rng(random_state)
    n_old = len(np.unique(y_l))
    k_max_new = k_max_new or 2 * n_old
    # subamostra mantendo a proporção D_L : D_U
    n = len(X_l) + len(X_u)
    if n > max_eval:
        f = max_eval / n
        il = rng.choice(len(X_l), max(n_old, int(f * len(X_l))), replace=False)
        iu = rng.choice(len(X_u), int(f * len(X_u)), replace=False)
        X_l, y_l, X_u = X_l[il], y_l[il], X_u[iu]
    X = np.vstack([X_l, X_u])
    curve = {}
    for k_new in range(1, k_max_new + 1):
        K = n_old + k_new
        if K >= len(X):
            break
        lab = KMeans(K, n_init=n_init, random_state=random_state).fit_predict(X)
        curve[k_new] = cluster_acc(y_l, lab[:len(X_l)])
    best = max(curve, key=lambda k: (curve[k], -k))
    return (best, curve) if return_curve else best
