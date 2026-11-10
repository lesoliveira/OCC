"""Famílias de OCC do protocolo: Gauss, kNN, SVM, MST (base do MODES).

Todas rodam em CPU com numpy/scipy/scikit-learn.
"""
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import cdist
from sklearn.covariance import LedoitWolf
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import OneClassSVM

from .base import BaseOCC


class GaussOCC(BaseOCC):
    """OCC-Gauss / GaussianDD: log-verossimilhança gaussiana.

    Covariância estimada por Ledoit-Wolf (encolhimento automático), o que
    evita matrizes singulares em alta dimensão (ex.: 768 atributos DINO
    com poucas centenas de amostras por classe).
    """

    def __init__(self, reg=0.0):
        self.reg = reg  # regularização extra na diagonal, além do Ledoit-Wolf

    def fit(self, X):
        X = self._check(X)
        lw = LedoitWolf().fit(X)
        cov = lw.covariance_ + self.reg * np.eye(X.shape[1])
        self.mean_ = X.mean(axis=0)
        # inversa estável por autovalores; atributos constantes (variância
        # zero) geram autovalores ~0, limitados por baixo
        w, V = np.linalg.eigh(cov)
        w = np.maximum(w, 1e-6 * max(w.max(), 1e-12))
        self.prec_ = (V / w) @ V.T
        return self

    def score(self, X):
        # -0.5 * Mahalanobis^2. O termo log|Sigma| é omitido: é constante
        # por classe e a calibração conforme (p-valores por classe) o anula.
        D = self._check(X) - self.mean_
        maha = np.einsum("ij,jk,ik->i", D, self.prec_, D)
        return -0.5 * maha


class KNNOCC(BaseOCC):
    """OCC-kNN: menos a distância média aos k vizinhos da classe.

    No treino, cada amostra exclui a si mesma (k+1 vizinhos), para que os
    escores de calibração não fiquem otimistas.
    """

    def __init__(self, k=5, metric="euclidean"):
        self.k = k
        self.metric = metric

    def fit(self, X):
        X = self._check(X)
        self.k_ = min(self.k, len(X) - 1) if len(X) > 1 else 1
        self.nn_ = NearestNeighbors(n_neighbors=self.k_, metric=self.metric).fit(X)
        self.X_ = X
        return self

    def score(self, X):
        d, _ = self.nn_.kneighbors(self._check(X), n_neighbors=self.k_)
        return -d.mean(axis=1)


class SVMOCC(BaseOCC):
    """OCC-SVM: One-class SVM (Schölkopf) com kernel RBF.

    gamma = gamma_mult / (d * var(X)), calculado nos dados da própria
    classe; gamma_mult = 1 é o "scale" do scikit-learn. Sem negativos, o
    gamma não se ajusta por validação cruzada comum; a família "svm-cv"
    (occ/select.py) escolhe gamma_mult pelo protocolo deixa-uma-classe-de-
    fora em D_L.
    """

    def __init__(self, nu=0.05, gamma_mult=1.0):
        self.nu = nu
        self.gamma_mult = gamma_mult

    def fit(self, X):
        X = self._check(X)
        var = X.var()
        gamma = self.gamma_mult / (X.shape[1] * (var if var > 0 else 1.0))
        self.svm_ = OneClassSVM(kernel="rbf", nu=self.nu, gamma=gamma)
        self.svm_.fit(X)
        return self

    def score(self, X):
        return self.svm_.decision_function(self._check(X))


class MSTOCC(BaseOCC):
    """MSTDD (Juszczak et al.), reimplementado do dd_tools.

    Constrói a árvore geradora mínima dos dados de treino; o escore é menos
    a distância da amostra à aresta mais próxima da árvore (projeção sobre
    o segmento, ou o vértice mais próximo quando a projeção cai fora).
    Equivale ao MSTDD com max_path = none, como no artigo do MODES.

    Custo: O(n^2) memória no treino; em classes com milhares de amostras,
    use max_train para subamostrar.
    """

    def __init__(self, max_train=2000, random_state=0):
        self.max_train = max_train
        self.random_state = random_state

    def fit(self, X):
        X = self._check(X)
        if len(X) > self.max_train:
            rng = np.random.default_rng(self.random_state)
            X = X[rng.choice(len(X), self.max_train, replace=False)]
        self.X_ = X
        if len(X) < 2:
            self.a_ = self.b_ = X
            return self
        mst = minimum_spanning_tree(cdist(X, X)).tocoo()
        self.a_ = X[mst.row]
        self.b_ = X[mst.col]
        return self

    def score(self, X, batch=512):
        X = self._check(X)
        out = np.empty(len(X))
        ab = self.b_ - self.a_                          # (m, d)
        ab2 = np.maximum((ab ** 2).sum(axis=1), 1e-12)  # (m,)
        for s in range(0, len(X), batch):
            Q = X[s:s + batch]                          # (q, d)
            # t = <q - a, b - a> / |b - a|^2, recortado em [0, 1]
            t = (Q @ ab.T - (self.a_ * ab).sum(axis=1)) / ab2
            t = np.clip(t, 0.0, 1.0)                    # (q, m)
            # |q - (a + t ab)|^2 expandido para não materializar (q, m, d)
            qa = (Q ** 2).sum(1)[:, None] - 2 * Q @ self.a_.T + (self.a_ ** 2).sum(1)[None, :]
            qab = Q @ ab.T - (self.a_ * ab).sum(axis=1)[None, :]
            d2 = qa - 2 * t * qab + t ** 2 * ab2[None, :]
            out[s:s + batch] = -np.sqrt(np.maximum(d2.min(axis=1), 0.0))
        return out


FAMILIES = {
    "gauss": GaussOCC,
    "knn": KNNOCC,
    "svm": SVMOCC,
    "mst": MSTOCC,
}


def make_occ(name, **kwargs):
    """Cria um OCC pelo nome usado no protocolo."""
    if name not in FAMILIES:
        raise ValueError(f"família desconhecida: {name}; use {list(FAMILIES)}")
    return FAMILIES[name](**kwargs)
