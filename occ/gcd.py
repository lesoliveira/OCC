"""Pipeline OCC para GCD: rejeição -> descoberta -> incorporação.

Uso típico (cenário C2, transdutivo):

    model = OCCDiscovery(family="gauss").fit(X_l, y_l)
    y_hat = model.discover(X_u)            # K_new estimado pela silhueta
    model.incorporate(X_u, y_hat)          # cenário C4: classes novas viram OCCs

Rótulos de classe devem ser inteiros >= 0; -1 é reservado para rejeição.
"""
import numpy as np
from .calibration import ClassWiseOCC
from .kest import estimate_k  # noqa: F401  (reexportado)
from .baselines import cluster_rejected
from .fragments import corrected_discovery, fragment_size



class OCCDiscovery:
    def __init__(self, family="gauss", occ_kwargs=None, alpha=0.05,
                 cal_size=0.2, k_max_factor=2, min_new_size=5,
                 dic_kwargs=None, random_state=0, cal_mode="cv",
                 assign="kmeans", k_est="silhouette", frag_c=2.0, priority=False):
        self.priority = priority
        self.k_est = k_est
        self.frag_c = frag_c
        self.cal_mode = cal_mode
        self.assign = assign
        self.family = family
        self.occ_kwargs = occ_kwargs or {}
        self.alpha = alpha
        self.cal_size = cal_size
        self.k_max_factor = k_max_factor
        self.min_new_size = min_new_size
        self.dic_kwargs = dic_kwargs or {}
        self.random_state = random_state

    def fit(self, X_l, y_l):
        self.model_ = ClassWiseOCC(self.family, self.occ_kwargs, self.cal_size,
                                   self.dic_kwargs, self.random_state,
                                   cal_mode=self.cal_mode).fit(X_l, y_l)
        self.n_old_ = len(self.model_.classes_)
        self.X_l_, self.y_l_ = np.asarray(X_l, float), np.asarray(y_l)
        # médias por classe (usadas na reatribuição do ruído); atualizadas
        # no incorporate, sem guardar as amostras das classes novas
        self.means_ = {c: self.X_l_[self.y_l_ == c].mean(0) for c in self.model_.classes_}
        self.radius_ = {c: self._radius(self.X_l_[self.y_l_ == c], self.means_[c])
                        for c in self.model_.classes_}
        return self

    @staticmethod
    def _radius(Xc, mu):
        return float(np.median(np.linalg.norm(Xc - mu, axis=1)))

    def merge_duplicates(self, X, y, ratio=1.0):
        """C4: um cluster novo cujo centróide cai dentro do raio típico de uma
        classe existente (mediana das distâncias das amostras dessa classe
        ao seu centro, vezes ratio) é rotulado como essa classe, em vez de
        virar uma classe nova. Evita redescobrir, numa sessão seguinte, uma
        classe já descoberta (ou um pedaço de uma classe antiga).
        """
        X, y = np.asarray(X, float), np.asarray(y).copy()
        C = list(self.model_.classes_)
        M = np.array([self.means_[c] for c in C])
        R = np.array([self.radius_[c] for c in C])
        merged = 0
        for c in np.unique(y):
            if c in self.means_:
                continue
            mu = X[y == c].mean(0)
            q = np.linalg.norm(M - mu, axis=1) / np.maximum(R, 1e-12)
            j = int(q.argmin())
            if q[j] <= ratio:
                y[y == c] = C[j]
                merged += 1
        self.last_merged_ = merged
        return y

    def novelty_score(self, X):
        return self.model_.novelty_score(X)

    def discover(self, X_u, k_new=None, calibrated=True, return_info=False):
        """Rotula D_U: aceitos recebem a classe conhecida; rejeitados são
        agrupados em k_new classes novas (estimado se None).

        assign="kmeans": k-means só nos rejeitados (tudo vira classe nova).
        assign="ssk": SS-k-means nos rejeitados com os centróides das
        antigas ancorados em D_L; um rejeitado por engano pode voltar
        para a sua classe antiga.
        """
        X_u = np.asarray(X_u, float)
        self.last_tau_ = None
        y = self.model_.predict(X_u, self.alpha, calibrated, priority=self.priority)
        rej = y == -1
        info = {"n_rejected": int(rej.sum()), "k_new": 0}
        corr = (k_new is None and self.assign == "kmeans"
                and self.k_est in ("sil-size", "hdbscan", "hdbscan-leaf"))
        if corr and rej.sum() >= 2:
            C = self.model_.classes_
            P = self.model_.pvalues(X_u[rej])
            acc = [(y == c).sum() for c in C]
            tau = fragment_size(acc, self.alpha, self.frag_c, self.min_new_size)
            lab, k_new = corrected_discovery(
                X_u[rej], C[P.argmax(axis=1)], int(C.max()) + 1, tau, self.k_est,
                self.k_max_factor * self.n_old_, self.random_state,
                old_means=np.array([self.means_[c] for c in C]),
                old_ids=C)
            y[rej] = lab
            self.last_tau_ = tau
            info.update({"k_new": k_new, "tau": tau,
                         "n_back_to_old": int(np.isin(lab, C).sum())})
        elif rej.sum() >= 2:
            lab, k_new = cluster_rejected(
                X_u[rej], k_new, self.assign, self.X_l_, self.y_l_,
                int(self.model_.classes_.max()) + 1,
                self.k_max_factor * self.n_old_, self.random_state)
            y[rej] = lab
            info["k_new"] = k_new
            info["n_back_to_old"] = int(np.isin(lab, self.model_.classes_).sum())
        elif rej.any():
            y[rej] = int(self.model_.classes_.max()) + 1
            info["k_new"] = 1
        return (y, info) if return_info else y

    def incorporate(self, X, y, min_size=None):
        """Cria OCCs para as classes descobertas (as que ainda não existem).

        Classes conhecidas não são re-treinadas. Clusters menores que
        min_size (padrão min_new_size) são ignorados. No C4, usar
        min_size = last_tau_ (tamanho de um fragmento de classe antiga)
        evita que fragmentos virem classes permanentes.
        """
        X, y = np.asarray(X, float), np.asarray(y)
        thr = self.min_new_size if min_size is None else max(self.min_new_size, min_size)
        self.model_.next_tier_ = getattr(self.model_, "next_tier_", 0) + 1
        known = set(self.model_.classes_.tolist())
        added = []
        for c in np.unique(y):
            if c == -1 or c in known:
                continue
            Xc = X[y == c]
            if len(Xc) >= thr:
                self.model_.add_class(c, Xc)
                self.means_[c] = Xc.mean(0)
                self.radius_[c] = self._radius(Xc, self.means_[c])
                added.append(int(c))
        self.n_old_ = len(self.model_.classes_)
        return added
