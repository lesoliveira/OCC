"""Baselines do protocolo, com a mesma saída do OCCDiscovery.

- SSKMeans: k-means semi-supervisionado do GCD (Vaze et al., CVPR 2022).
  Usa D_L, mas não tem rejeição explícita.
- ClosedMSP: classificador fechado + rejeição pela probabilidade máxima
  (MSP) + k-means dos rejeitados. O limiar é escolhido em probabilidades
  de validação cruzada em D_L, para rejeitar uma fração alpha das antigas,
  com a mesma semântica de alpha dos OCCs.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict

from .kest import estimate_k


def _sqdist(A, C):
    """|a - c|^2 sem materializar (n, k, d): cabe na memória no CIFAR-100."""
    d = (A ** 2).sum(1)[:, None] - 2 * A @ C.T + (C ** 2).sum(1)[None, :]
    return np.maximum(d, 0.0)


class SSKMeans:
    """k-means em D_L ∪ D_U com as atribuições de D_L fixas na própria classe.

    Os centróides das classes antigas começam nas médias das classes; os das
    novas, por k-means++ em D_U, como no NCD k-means do PBN. Rótulos de
    D_U: classes antigas mantêm o rótulo original; novas começam em
    max(antigas) + 1.
    """

    def __init__(self, n_iter=100, random_state=0, k_max_factor=2):
        self.n_iter = n_iter
        self.random_state = random_state
        self.k_max_factor = k_max_factor

    def fit_predict(self, X_l, y_l, X_u, k_new=None):
        X_l, X_u, y_l = np.asarray(X_l, float), np.asarray(X_u, float), np.asarray(y_l)
        old = np.unique(y_l)
        if k_new is None:  # estimativa sem rótulos de D_U (silhueta em D_U)
            # K total entre n_old + 1 e k_max_factor * n_old: as classes
            # conhecidas estão em D_U por construção (antes o mínimo era 2, o
            # que deixava escolher menos grupos que classes conhecidas)
            k_new = estimate_k(X_u, len(old) + 1,
                               max(len(old) + 2, self.k_max_factor * len(old)),
                               self.random_state) - len(old)
        rng = np.random.default_rng(self.random_state)
        C = [X_l[y_l == c].mean(axis=0) for c in old]
        for _ in range(k_new):  # k-means++ a partir dos centróides existentes
            d2 = _sqdist(X_u, np.array(C)).min(axis=1)
            p = d2 / d2.sum() if d2.sum() > 0 else None
            C.append(X_u[rng.choice(len(X_u), p=p)])
        C = np.array(C)
        lab_l = np.searchsorted(old, y_l)  # índice fixo do centróide de cada rotulada
        X = np.vstack([X_l, X_u])
        prev = None
        for _ in range(self.n_iter):
            d = _sqdist(X_u, C)
            lab_u = d.argmin(axis=1)
            if prev is not None and np.array_equal(lab_u, prev):
                break
            prev = lab_u
            lab = np.r_[lab_l, lab_u]
            for j in range(len(C)):
                if (lab == j).any():
                    C[j] = X[lab == j].mean(axis=0)
        base = int(old.max()) + 1
        ids = np.r_[old, base + np.arange(k_new)]
        self.k_new_ = k_new
        return ids[lab_u]


def cluster_rejected(Xr, k_new, assign, X_l, y_l, base, k_max, random_state=0):
    """Rotula os rejeitados. Devolve (rótulos, k_new usado).

    assign="kmeans": k-means isolado; rótulos base, base+1, ...
    assign="ssk":    SS-k-means com as antigas ancoradas em (X_l, y_l);
                     rótulos podem ser antigos ou base+j.
    """
    if k_new is None and assign == "kmeans":
        k_new = estimate_k(Xr, 2, k_max, random_state)
    if assign == "kmeans":
        k_new = int(min(k_new, len(Xr)))
        lab = KMeans(k_new, n_init=10, random_state=random_state).fit_predict(Xr)
        return base + lab, k_new
    if assign == "ssk":
        if k_new is not None:
            k_new = int(min(k_new, len(Xr)))
        m = SSKMeans(random_state=random_state)
        lab = m.fit_predict(X_l, y_l, Xr, k_new)
        return lab, m.k_new_
    raise ValueError(f"assign desconhecido: {assign}")


class ClosedMSP:
    def __init__(self, clf="rf", alpha=0.05, k_max_factor=2, n_folds=5,
                 random_state=0, assign="kmeans", k_est="silhouette", frag_c=2.0):
        self.assign = assign
        self.k_est = k_est
        self.frag_c = frag_c
        self.clf = clf
        self.alpha = alpha
        self.k_max_factor = k_max_factor
        self.n_folds = n_folds
        self.random_state = random_state

    def _make(self):
        if self.clf == "rf":
            return RandomForestClassifier(n_estimators=300, n_jobs=-1,
                                          random_state=self.random_state)
        return LogisticRegression(max_iter=2000, C=1.0)

    def fit(self, X_l, y_l):
        X_l, y_l = np.asarray(X_l, float), np.asarray(y_l)
        # MSP de validação cruzada em D_L: escores "honestos" das antigas
        k = min(self.n_folds, np.bincount(np.unique(y_l, return_inverse=True)[1]).min())
        self.model_ = self._make().fit(X_l, y_l)
        if k >= 2:
            P = cross_val_predict(self._make(), X_l, y_l, cv=k, method="predict_proba")
        else:  # alguma classe com 1 amostra: limiar no treino (otimista)
            P = self.model_.predict_proba(X_l)
        self.thr_ = np.quantile(P.max(axis=1), self.alpha)
        self.classes_ = self.model_.classes_
        self.X_l_, self.y_l_ = X_l, y_l
        return self

    def novelty_score(self, X):
        return 1.0 - self.model_.predict_proba(np.asarray(X, float)).max(axis=1)

    def discover(self, X_u, k_new=None, return_info=False):
        X_u = np.asarray(X_u, float)
        P = self.model_.predict_proba(X_u)
        y = self.classes_[P.argmax(axis=1)].copy()
        rej = P.max(axis=1) < self.thr_
        info = {"n_rejected": int(rej.sum()), "k_new": 0}
        corr = (k_new is None and self.assign == "kmeans"
                and self.k_est in ("sil-size", "hdbscan", "hdbscan-leaf"))
        if corr and rej.sum() >= 2:
            from .fragments import corrected_discovery, fragment_size
            acc = [(y[~rej] == c).sum() for c in self.classes_]
            tau = fragment_size(acc, self.alpha, self.frag_c)
            lab, k_new = corrected_discovery(
                X_u[rej], y[rej], int(self.classes_.max()) + 1, tau, self.k_est,
                self.k_max_factor * len(self.classes_), self.random_state,
                old_means=np.array([self.X_l_[self.y_l_ == c].mean(0) for c in self.classes_]),
                old_ids=self.classes_)
            y[rej] = lab
            self.last_tau_ = tau
            info.update({"k_new": k_new, "tau": tau,
                         "n_back_to_old": int(np.isin(lab, self.classes_).sum())})
        elif rej.sum() >= 2:
            lab, k_new = cluster_rejected(
                X_u[rej], k_new, self.assign, self.X_l_, self.y_l_,
                int(self.classes_.max()) + 1,
                self.k_max_factor * len(self.classes_), self.random_state)
            y[rej] = lab
            info["k_new"] = k_new
            info["n_back_to_old"] = int(np.isin(lab, self.classes_).sum())
        return (y, info) if return_info else y
