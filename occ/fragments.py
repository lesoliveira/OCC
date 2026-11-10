"""Correção da superestimativa de K causada pelas antigas rejeitadas por engano.

Com C_old classes antigas e taxa de falsa rejeição ~alpha, o conjunto
rejeitado contém, além das classes novas, um "fragmento" de cada classe
antiga, com cerca de alpha/(1-alpha) x (aceitos da classe) amostras. Um
estimador de K aplicado aos rejeitados conta esses fragmentos como classes
novas; o viés cresce com o número de classes antigas (no letter, ~30 em vez
de 7). O tamanho esperado de um fragmento é estimado só com quantidades
disponíveis sem rótulos de D_U: alpha e o número de aceitos por classe.

- sil-size: silhueta + k-means nos rejeitados; clusters menores que
  tau = frag_c x mediana(tamanho esperado dos fragmentos) voltam para a
  classe antiga de maior escore; repete nos restantes até estabilizar.
- hdbscan: HDBSCAN (Campello et al., 2013) com min_cluster_size = tau;
  pontos marcados como ruído vão para o centróide mais próximo entre as
  classes antigas (médias de D_L) e os clusters novos. Não precisa de K:
  o número de clusters sai da densidade.
- hdbscan-leaf: igual, com cluster_selection_method="leaf": escolhe as
  folhas da árvore de clusters (clusters mais finos) em vez dos clusters
  mais estáveis ("eom"); separa classes vizinhas que o "eom" funde.
"""
import numpy as np
from sklearn.cluster import KMeans

from .kest import estimate_k


def fragment_size(accepted_counts, alpha, frag_c=2.0, floor=5):
    s = alpha / (1.0 - alpha) * np.asarray(accepted_counts, float)
    s = s[s > 0]
    tau = frag_c * (np.median(s) if len(s) else 0.0)
    return max(float(floor), tau)


def _sqd(A, C):
    return np.maximum((A**2).sum(1)[:, None] - 2 * A @ C.T + (C**2).sum(1)[None], 0)


def corrected_discovery(Xr, best_old, base, tau, method="sil-size", k_max=20,
                        random_state=0, max_iter=5, old_means=None, old_ids=None):
    """Devolve (rótulos dos rejeitados, k_new). Rótulos: antigos ou base+j."""
    Xr, best_old = np.asarray(Xr, float), np.asarray(best_old)
    out = best_old.copy()
    if method in ("hdbscan", "hdbscan-leaf"):
        from sklearn.cluster import HDBSCAN
        if len(Xr) < 2 * tau:
            return out, 0
        sel = "leaf" if method == "hdbscan-leaf" else "eom"
        lab = HDBSCAN(min_cluster_size=int(round(tau)),
                      cluster_selection_method=sel).fit_predict(Xr)
        keep = lab >= 0
        ids = np.unique(lab[keep])
        if len(ids) == 0:  # densidade sem estrutura (ex.: pixels): usa sil-size
            return corrected_discovery(Xr, best_old, base, tau, "sil-size", k_max,
                                       random_state, max_iter)
        out[keep] = base + np.searchsorted(ids, lab[keep])
        noise = ~keep
        if noise.any() and len(ids) and old_means is not None:
            # ruído: centróide mais próximo entre antigas (médias de D_L) e novas
            C = np.vstack([old_means] + [Xr[lab == i].mean(0) for i in ids])
            L = np.r_[old_ids, base + np.arange(len(ids))]
            out[noise] = L[_sqd(Xr[noise], C).argmin(1)]
        return out, len(ids)
    if method != "sil-size":
        raise ValueError(method)
    idx = np.arange(len(Xr))
    lab = None
    for _ in range(max_iter):
        if len(idx) < max(2, tau):
            idx, lab = idx[:0], None
            break
        k = estimate_k(Xr[idx], 2, min(k_max, len(idx) - 1), random_state)
        lab = KMeans(k, n_init=10, random_state=random_state).fit_predict(Xr[idx])
        small = np.bincount(lab, minlength=k)[lab] < tau
        if not small.any():
            break
        idx, lab = idx[~small], None
    if lab is None and len(idx) >= 2:  # última remoção: reagrupa o que sobrou
        k = estimate_k(Xr[idx], 2, min(k_max, len(idx) - 1), random_state)
        lab = KMeans(k, n_init=10, random_state=random_state).fit_predict(Xr[idx])
    if lab is None:
        return out, 0
    ids = np.unique(lab)
    out[idx] = base + np.searchsorted(ids, lab)
    return out, len(ids)
