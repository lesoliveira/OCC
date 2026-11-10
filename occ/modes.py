"""MODES (Fragoso et al., KBS 2021) como família de OCC por classe.

Para uma classe:
  1. Índices de validação de cluster avaliam k = 2..10 e cada um indica
     o seu melhor k; o conjunto D de valores distintos define as
     segmentações.
  2. Para cada k em D, k-means segmenta a classe e um OCC base é treinado
     por cluster (clusters com 1 amostra são descartados, como no artigo).
  3. No teste, para cada segmentação, seleciona-se o OCC do cluster de
     centróide mais próximo; o escore da classe é a média dos selecionados.

Diferenças em relação ao artigo original, todas deliberadas:
  - Índices: usamos 4 dos 13 do NbClust (silhueta, Calinski-Harabasz,
    Davies-Bouldin e Dunn), que cobrem os mais robustos segundo
    Arbelaitz et al. (2013) e rodam rápido em Python.
  - Agregação: no artigo, os OCCs do dd_tools devolvem probabilidades.
    Aqui cada OCC de cluster é padronizado pela média e desvio dos seus
    próprios escores de treino antes da média, para que clusters
    diferentes fiquem na mesma escala. A calibração conforme por
    classe (calibration.py) é aplicada depois, sobre o escore final.
  - A seleção por região de competência entre classes (vizinhança k = 3|C|
    com poda de 10%) não é usada por padrão: em mundo aberto, a vizinhança
    de uma amostra nova só contém classes conhecidas, e a poda forçaria a
    escolha entre elas. Ela pode ser ligada em ClassWiseScorer.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import (calinski_harabasz_score, davies_bouldin_score,
                             silhouette_score)
from scipy.spatial.distance import cdist

from .base import BaseOCC
from .families import make_occ


def dunn_index(X, labels):
    """Menor distância entre clusters / maior diâmetro de cluster."""
    ks = np.unique(labels)
    groups = [X[labels == k] for k in ks]
    diam = max(cdist(g, g).max() if len(g) > 1 else 0.0 for g in groups)
    if diam == 0:
        return 0.0
    sep = min(cdist(groups[i], groups[j]).min()
              for i in range(len(groups)) for j in range(i + 1, len(groups)))
    return sep / diam


def cvi_ks(X, k_min=2, k_max=10, random_state=0, max_eval=2000):
    """Conjunto de k sugeridos pelos 4 índices (cada índice vota em 1 k)."""
    n = len(X)
    k_max = min(k_max, n - 1)
    if k_max < k_min:
        return [1]
    rng = np.random.default_rng(random_state)
    Xe = X[rng.choice(n, max_eval, replace=False)] if n > max_eval else X
    scores = {"sil": {}, "ch": {}, "db": {}, "dunn": {}}
    for k in range(k_min, k_max + 1):
        lab = KMeans(k, n_init=5, random_state=random_state).fit_predict(Xe)
        if len(np.unique(lab)) < 2:
            continue
        scores["sil"][k] = silhouette_score(Xe, lab)
        scores["ch"][k] = calinski_harabasz_score(Xe, lab)
        scores["db"][k] = -davies_bouldin_score(Xe, lab)  # menor é melhor
        scores["dunn"][k] = dunn_index(Xe, lab)
    if not scores["sil"]:
        return [1]
    return sorted({max(s, key=s.get) for s in scores.values()})


class _ECDF:
    """Padroniza escores pela média e desvio dos escores de treino do cluster.

    (Uma ECDF limitada a [0, 1] saturaria em 0 para amostras distantes e
    perderia a ordem entre elas, o que prejudica a rejeição.)
    """

    def __init__(self, ref):
        self.mu = float(np.mean(ref))
        self.sd = float(np.std(ref)) or 1.0

    def __call__(self, s):
        return (s - self.mu) / self.sd


class MODESOCC(BaseOCC):
    def __init__(self, base="gauss", base_kwargs=None, k_min=2, k_max=10,
                 min_cluster=2, random_state=0):
        self.base = base
        self.base_kwargs = base_kwargs or {}
        self.k_min = k_min
        self.k_max = k_max
        self.min_cluster = min_cluster
        self.random_state = random_state

    def fit(self, X):
        X = self._check(X)
        self.ks_ = cvi_ks(X, self.k_min, self.k_max, self.random_state)
        self.partitions_ = []  # lista de (centroides, [(occ, ecdf) por cluster])
        for k in self.ks_:
            if k == 1:
                lab = np.zeros(len(X), int)
                cent = X.mean(axis=0, keepdims=True)
            else:
                km = KMeans(k, n_init=5, random_state=self.random_state).fit(X)
                lab, cent = km.labels_, km.cluster_centers_
            members, keep = [], []
            for j in range(len(cent)):
                Xj = X[lab == j]
                if len(Xj) < self.min_cluster:
                    continue  # cluster unitário: tratado como outlier
                occ = make_occ(self.base, **self.base_kwargs).fit(Xj)
                members.append((occ, _ECDF(occ.score(Xj))))
                keep.append(j)
            if members:
                self.partitions_.append((cent[keep], members))
        if not self.partitions_:  # classe minúscula: um OCC só
            occ = make_occ(self.base, **self.base_kwargs).fit(X)
            self.partitions_ = [(X.mean(0, keepdims=True),
                                 [(occ, _ECDF(occ.score(X)))])]
        return self

    def score(self, X):
        X = self._check(X)
        total = np.zeros(len(X))
        for cent, members in self.partitions_:
            nearest = cdist(X, cent).argmin(axis=1)
            s = np.empty(len(X))
            for j, (occ, ecdf) in enumerate(members):
                m = nearest == j
                if m.any():
                    s[m] = ecdf(occ.score(X[m]))
            total += s
        return total / len(self.partitions_)
