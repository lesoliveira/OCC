"""OCC-Dic: escore por classe no espaço de dissimilaridade (dichotomizer).

Diferente das outras famílias, o dichotomizer é UM classificador binário
global, treinado em pares de amostras: vetor |a - b|, rótulo 1 se a e b
são da mesma classe e 0 caso contrário. O escore de x para a classe c é a
média de P(mesma classe | |x - r|) sobre as k referências r de c mais
próximas de x.

Propriedade importante para mundo aberto: incorporar uma classe nova é só
guardar suas referências; o dichotomizer não é re-treinado.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors


class Dichotomizer:
    def __init__(self, n_pairs=20000, k_ref=5, n_estimators=200,
                 n_jobs=-1, random_state=0):
        self.n_pairs = n_pairs
        self.k_ref = k_ref
        self.n_estimators = n_estimators
        self.n_jobs = n_jobs
        self.random_state = random_state

    def _pairs(self, X, y, rng):
        classes = np.unique(y)
        idx = {c: np.flatnonzero(y == c) for c in classes}
        half = self.n_pairs // 2
        # positivos: mesma classe, classe sorteada uniformemente
        cp = rng.choice(classes, half)
        a = np.array([rng.choice(idx[c]) for c in cp])
        b = np.array([rng.choice(idx[c]) for c in cp])
        pos = np.abs(X[a] - X[b])
        # negativos: classes diferentes
        a = rng.integers(0, len(X), half * 3)
        b = rng.integers(0, len(X), half * 3)
        keep = y[a] != y[b]
        a, b = a[keep][:half], b[keep][:half]
        neg = np.abs(X[a] - X[b])
        Z = np.vstack([pos, neg])
        t = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
        return Z, t

    def fit(self, X, y):
        """Treina o dichotomizer com as classes conhecidas (precisa de >= 2)."""
        X = np.asarray(X, float)
        y = np.asarray(y)
        if len(np.unique(y)) < 2:
            raise ValueError("o dichotomizer precisa de pelo menos 2 classes")
        rng = np.random.default_rng(self.random_state)
        Z, t = self._pairs(X, y, rng)
        self.clf_ = RandomForestClassifier(
            n_estimators=self.n_estimators, min_samples_leaf=2,
            n_jobs=self.n_jobs, random_state=self.random_state).fit(Z, t)
        self.refs_ = {}
        return self

    def add_class(self, label, X):
        """Guarda as referências de uma classe (conhecida ou descoberta)."""
        X = np.asarray(X, float)
        k = min(self.k_ref, len(X))
        self.refs_[label] = (X, NearestNeighbors(n_neighbors=k).fit(X), k)
        return self

    def score_class(self, label, X):
        """Escore de x para uma classe; maior = mais típico."""
        R, nn, k = self.refs_[label]
        X = np.asarray(X, float)
        _, ind = nn.kneighbors(X, n_neighbors=k)
        Z = np.abs(X[:, None, :] - R[ind]).reshape(-1, X.shape[1])
        p = self.clf_.predict_proba(Z)[:, 1].reshape(len(X), k)
        return p.mean(axis=1)


class DichotomyOCC:
    """Adaptador: o escore de UMA classe, com a interface fit/score.

    O dichotomizer compartilhado é passado pronto; fit só guarda as
    referências da classe-alvo.
    """

    def __init__(self, dichotomizer, label):
        self.dic = dichotomizer
        self.label = label

    def fit(self, X):
        self.dic.add_class(self.label, X)
        return self

    def score(self, X):
        return self.dic.score_class(self.label, X)
