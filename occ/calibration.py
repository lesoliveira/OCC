"""Decomposição one-class com calibração conforme.

Cada classe c tem seu OCC e um conjunto de calibração separado do treino.
O escore bruto s_c(x) vira um p-valor conforme

    p_c(x) = (1 + #{z em Cal_c : s_c(z) <= s_c(x)}) / (|Cal_c| + 1)

Assim, escores de OCCs diferentes ficam na mesma escala (p-valores), e
aceitar x quando p_c(x) >= alpha garante cobertura de aproximadamente
1 - alpha para as amostras da classe c (troca de amostras intercambiáveis).
"""
import warnings

import numpy as np
from sklearn.model_selection import train_test_split

from .dichotomy import Dichotomizer, DichotomyOCC
from .families import make_occ
from .modes import MODESOCC


def build_occ(family, label=None, dichotomizer=None, **kwargs):
    if family == "modes":
        return MODESOCC(**kwargs)
    if family == "dic":
        return DichotomyOCC(dichotomizer, label)
    return make_occ(family, **kwargs)


class ClassWiseOCC:
    """Um OCC calibrado por classe, com rejeição e incorporação de classes.

    family: 'gauss' | 'knn' | 'svm' | 'mst' | 'modes' | 'dic'
    occ_kwargs: parâmetros da família (ex.: {'k': 5} para knn,
                {'base': 'mst'} para modes)
    cal_mode: 'cv' (padrão), 'split' ou 'nested' (ver add_class)
    cal_size: fração reservada para calibração quando cal_mode='split'
    family_map: {classe: (família, kwargs)} para dar a cada classe a sua
                própria família (seleção por classe, occ/select.py). Classes
                fora do mapa usam family/occ_kwargs. Os p-valores conformes
                deixam OCCs de famílias diferentes na mesma escala.
    """

    def __init__(self, family="gauss", occ_kwargs=None, cal_size=0.2,
                 dic_kwargs=None, random_state=0, cal_mode="cv", n_folds=5,
                 family_map=None):
        self.family_map = family_map or {}
        self.family = family
        self.occ_kwargs = occ_kwargs or {}
        self.cal_size = cal_size
        self.cal_mode = cal_mode
        self.n_folds = n_folds
        self.dic_kwargs = dic_kwargs or {}
        self.random_state = random_state

    # ------------------------------------------------------------------ treino
    def fit(self, X, y):
        X = np.asarray(X, float)
        y = np.asarray(y)
        self.occs_, self.cal_ = {}, {}
        self.tier_ = {}  # "idade" da classe: 0 = D_L; t = incorporada no lote t
        self.dic_ = None
        if self.family == "dic" or any(f == "dic" for f, _ in self.family_map.values()):
            # no modo 'split', o dichotomizer usa só a parte de treino; no
            # modo 'cv', usa todo D_L (as referências de cada fold excluem
            # a amostra calibrada, mas o classificador de pares já a viu:
            # vazamento leve, a medir na ablação A3)
            if self.cal_mode == "split":
                Xtr, _, ytr, _ = train_test_split(
                    X, y, test_size=self.cal_size, stratify=y,
                    random_state=self.random_state)
            else:
                Xtr, ytr = X, y
            self.dic_ = Dichotomizer(random_state=self.random_state,
                                     **self.dic_kwargs).fit(Xtr, ytr)
            if self.cal_mode == "nested" and not self.family_map:
                return self._fit_dic_nested(X, y)
        for c in np.unique(y):
            self.add_class(c, X[y == c])
        return self

    def _fit_dic_nested(self, X, y):
        """Calibração do OCC-Dic sem vazamento (cal_mode='nested').

        Para cada fold f, um dichotomizer é treinado com D_L sem o fold f; as
        amostras do fold f são pontuadas contra as referências da própria
        classe fora do fold. Nenhum escore de calibração vem de um
        classificador que viu a amostra. O dichotomizer final (self.dic_)
        usa todo D_L. Custo: n_folds + 1 florestas.
        """
        rng = np.random.default_rng(self.random_state)
        fold = np.empty(len(y), int)
        for c in np.unique(y):  # folds estratificados por classe
            idx = np.flatnonzero(y == c)
            fold[idx] = rng.permutation(len(idx)) % self.n_folds
        cal = {c: [] for c in np.unique(y)}
        cal_idx = {c: [] for c in np.unique(y)}
        for f in range(self.n_folds):
            tr = fold != f
            dic_f = Dichotomizer(random_state=self.random_state,
                                 **self.dic_kwargs).fit(X[tr], y[tr])
            for c in np.unique(y):
                ref = tr & (y == c)
                test = (~tr) & (y == c)
                if ref.sum() == 0 or test.sum() == 0:
                    continue
                dic_f.add_class(c, X[ref])
                cal[c].append(dic_f.score_class(c, X[test]))
                cal_idx[c].append(np.flatnonzero(test))
        self.cal_raw_ = {}
        for c in np.unique(y):
            occ = build_occ("dic", c, self.dic_).fit(X[y == c])
            self.occs_[c] = occ
            self.cal_[c] = np.sort(np.concatenate(cal[c]))
            # ordem das amostras de c em X (para o limiar da posteriori)
            pos = np.searchsorted(np.flatnonzero(y == c), np.concatenate(cal_idx[c]))
            raw = np.empty(len(pos))
            raw[pos] = np.concatenate(cal[c])
            self.cal_raw_[c] = raw
            self.tier_.setdefault(c, 0)
        return self

    def add_class(self, label, Xc):
        """Treina e calibra o OCC de uma classe; não toca nas demais.

        cal_mode='cv' (padrão): validação cruzada em n_folds dentro da
        classe; cada amostra recebe o escore de um OCC treinado sem ela, e
        o OCC final é treinado com TODAS as amostras. Assim o conjunto de
        calibração tem o tamanho da classe inteira. Isso importa: com n
        pontos de calibração, o menor p-valor possível é 1/(n+1), e só há
        rejeição se 1/(n+1) < alpha (n >= 20 para alpha = 0,05).

        cal_mode='split': reserva cal_size da classe para calibração.

        cal_mode='nested': igual a 'cv' aqui. Só muda o fit inicial do
        OCC-Dic (ver _fit_dic_nested). Para uma classe incorporada depois,
        o dichotomizer nunca viu essa classe, então o 'cv' já é honesto.
        """
        Xc = np.asarray(Xc, float)
        n = len(Xc)
        family, kwargs = self.family_map.get(label, (self.family, self.occ_kwargs))
        kwargs = kwargs or {}
        if self.cal_mode in ("cv", "nested") and n >= 2 * self.n_folds:
            rng = np.random.default_rng(self.random_state)
            fold = rng.permutation(n) % self.n_folds
            cal = np.empty(n)
            for f in range(self.n_folds):
                occ_f = build_occ(family, ("__cv__", label, f), self.dic_,
                                  **kwargs).fit(Xc[fold != f])
                cal[fold == f] = occ_f.score(Xc[fold == f])
            if self.dic_ is not None:  # limpa referências temporárias
                for f in range(self.n_folds):
                    self.dic_.refs_.pop(("__cv__", label, f), None)
            occ = build_occ(family, label, self.dic_, **kwargs).fit(Xc)
        else:
            if n >= 10:
                Xtr, Xcal = train_test_split(Xc, test_size=self.cal_size,
                                             random_state=self.random_state)
            else:  # classe muito pequena: calibra no próprio treino (otimista)
                Xtr = Xcal = Xc
            occ = build_occ(family, label, self.dic_, **kwargs).fit(Xtr)
            cal = occ.score(Xcal)
        if 1.0 / (len(cal) + 1) >= 0.05:
            warnings.warn(f"classe {label}: só {len(cal)} pontos de calibração; "
                          "com alpha <= 1/(n+1) nenhuma amostra é rejeitada")
        self.occs_[label] = occ
        self.cal_[label] = np.sort(cal)
        if not hasattr(self, "cal_raw_"):
            self.cal_raw_ = {}
        cv_ok = self.cal_mode in ("cv", "nested") and n >= 2 * self.n_folds
        self.cal_raw_[label] = cal if cv_ok else None
        self.tier_.setdefault(label, self.next_tier_ if hasattr(self, "next_tier_") else 0)
        return self

    @property
    def classes_(self):
        return np.array(list(self.occs_))

    # ------------------------------------------------------------------ escores
    def raw_scores(self, X):
        """Matriz (n, C) de escores brutos, na ordem de classes_."""
        X = np.asarray(X, float)
        return np.column_stack([self.occs_[c].score(X) for c in self.classes_])

    def pvalues(self, X):
        """Matriz (n, C) de p-valores conformes."""
        S = self.raw_scores(X)
        P = np.empty_like(S)
        for j, c in enumerate(self.classes_):
            cal = self.cal_[c]
            P[:, j] = (1 + np.searchsorted(cal, S[:, j], side="right")) / (len(cal) + 1)
        return P

    # ------------------------------------------------------- posteriori (ablação)
    # decision_ = 'pvalue' (padrão), 'post' ou 'hybrid'.
    #   'post':   a densidade do escore em cada classe, f_c(s), é estimada por
    #             KDE nos escores de calibração (fora da amostra) da própria
    #             classe. P(c|x) ∝ pi_c f_c(s_c(x)), com pi_c proporcional ao
    #             tamanho da classe. Aceita pela classe de maior posteriori e
    #             rejeita se ela ficar abaixo de um limiar global t, o quantil
    #             alpha da maior posteriori das amostras de D_L (calculado uma
    #             vez no fit). O escore é truncado na mediana da calibração para
    #             que a verossimilhança seja monótona no escore (uma amostra mais
    #             típica que a mediana não é penalizada).
    #   'hybrid': p-valor para aceitar/rejeitar (como no padrão) e posteriori
    #             para escolher entre as classes que aceitam.
    def _loglik(self, S):
        """Matriz (n, C) de log pi_c + log f_c(s_c(x))."""
        L = np.empty_like(S)
        sizes = np.array([len(self.cal_[c]) for c in self.classes_], float)
        logpi = np.log(sizes / sizes.sum())
        for j, c in enumerate(self.classes_):
            cal = self.cal_[c]
            med = np.median(cal)
            sd = cal.std()
            iqr = np.subtract(*np.percentile(cal, [75, 25]))
            h = 0.9 * min(sd, iqr / 1.34 if iqr > 0 else sd) * len(cal) ** -0.2
            h = max(h, 1e-12 + 1e-6 * (abs(med) + 1))
            s = np.minimum(S[:, j], med)
            # log da média de núcleos gaussianos, estável (log-sum-exp), em blocos
            out = np.empty(len(s))
            for a in range(0, len(s), 2048):
                z = (s[a:a + 2048, None] - cal[None, :]) / h
                q = -0.5 * z ** 2
                m = q.max(axis=1, keepdims=True)
                out[a:a + 2048] = (m[:, 0] + np.log(np.exp(q - m).mean(axis=1))
                                   - np.log(h * np.sqrt(2 * np.pi)))
            L[:, j] = out + logpi[j]
        return L

    def posteriors(self, X=None, S=None):
        if S is None:
            S = self.raw_scores(X)
        L = self._loglik(S)
        L -= L.max(axis=1, keepdims=True)
        E = np.exp(L)
        return E / E.sum(axis=1, keepdims=True)

    def _fit_posterior_threshold(self, X, y):
        """t = quantil alpha_post_ da maior posteriori em D_L, com o escore da
        própria classe fora da amostra (cal_raw_) e os das outras classes
        dados pelos OCCs finais (que não viram a amostra)."""
        self.post_scores_ = None
        raw = getattr(self, "cal_raw_", {})
        if any(raw.get(c) is None for c in self.classes_):
            return
        S = self.raw_scores(X)
        for j, c in enumerate(self.classes_):
            S[y == c, j] = raw[c]
        self.post_maxes_ = self.posteriors(S=S).max(axis=1)

    def predict(self, X, alpha=0.05, calibrated=True, priority=False):
        """Rótulos previstos; -1 = rejeitado (candidato a classe nova).

        calibrated=False usa o escore bruto (ablação A3): aceita pela
        classe de maior escore bruto e rejeita se esse escore estiver
        abaixo do quantil alpha da calibração daquela classe.

        priority=True (cenário C4): entre as classes que aceitam a amostra
        (p >= alpha), vence a mais antiga (menor tier_); dentro da mesma
        idade, a de maior p-valor. Uma classe descoberta só recebe o que as
        classes mais antigas rejeitam, como quando foi descoberta.
        """
        decision = getattr(self, "decision_", "pvalue")
        if calibrated and decision == "post":
            S = self.raw_scores(X)
            Q = self.posteriors(S=S)
            t = np.quantile(self.post_maxes_, alpha)
            best = Q.argmax(axis=1)
            accept = Q.max(axis=1) >= t
            labels = self.classes_[best].copy()
            labels[~accept] = -1
            return labels
        if calibrated:
            P = self.pvalues(X)
            # desempate entre as classes que aceitam: p-valor (padrão) ou posteriori
            R = self.posteriors(X) if decision == "hybrid" else P
            if priority:
                tiers = np.array([self.tier_.get(c, 0) for c in self.classes_], float)
                # alpha_disc_ (opcional): limiar mais estrito para as classes
                # descobertas (tier > 0), que foram ajustadas em clusters
                a_disc = getattr(self, "alpha_disc_", None)
                a_vec = np.where(tiers > 0, a_disc, alpha) if a_disc else alpha
                ok = P >= a_vec
                # chave: idade primeiro (menor é melhor), p-valor depois
                key = np.where(ok, -tiers[None, :] * 10.0 + R, -np.inf)
                best = key.argmax(axis=1)
                accept = ok.any(axis=1)
                best = np.where(accept, best, P.argmax(axis=1))
            else:
                accept = P.max(axis=1) >= alpha
                best = np.where(P >= alpha, R, -np.inf).argmax(axis=1)
                best = np.where(accept, best, P.argmax(axis=1))
        else:
            S = self.raw_scores(X)
            best = S.argmax(axis=1)
            thr = np.array([np.quantile(self.cal_[c], alpha) for c in self.classes_])
            accept = S[np.arange(len(S)), best] >= thr[best]
        labels = self.classes_[best].copy()
        labels[~accept] = -1
        return labels

    def novelty_score(self, X):
        """Escore de novidade: 1 - max_c p_c(x). Maior = mais provável nova."""
        if getattr(self, "decision_", "pvalue") == "post":
            return 1.0 - self.posteriors(X).max(axis=1)
        return 1.0 - self.pvalues(X).max(axis=1)
