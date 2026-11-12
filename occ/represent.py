"""Representações alternativas, aplicadas depois da padronização e iguais
para todos os métodos.

- "qpca": transformação quantílica para a normal + PCA com branqueamento
  (95% da variância). Não usa rótulos; ajustada em D_L ∪ D_U (transdutivo).
- "pcaN" / "pcawN": PCA para N dimensões (sem / com branqueamento), sem
  rótulos, ajustada em D_L ∪ D_U. Para características de imagem (768
  dimensões), em que há poucas amostras por classe para a dimensão.
- "rfleaf": floresta aleatória treinada só em D_L; cada amostra vira o vetor
  das folhas em que cai (one-hot), reduzido por SVD truncado. A distância
  euclidiana nesse espaço é a distância de proximidade da floresta. Risco
  conhecido: a floresta aprende a separar as classes conhecidas e pode
  juntar as novas.
"""
import numpy as np


def transform(kind, X_l, y_l, X_u, random_state=0, n_comp=64):
    if kind == "raw":
        return X_l, X_u
    if kind == "qpca":
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import QuantileTransformer
        A = np.vstack([X_l, X_u])
        qt = QuantileTransformer(n_quantiles=min(1000, len(A)), output_distribution="normal",
                                 random_state=random_state).fit(A)
        pca = PCA(0.95, whiten=True, random_state=random_state).fit(qt.transform(A))
        return pca.transform(qt.transform(X_l)), pca.transform(qt.transform(X_u))
    if kind.startswith("pca"):  # "pca64": PCA sem rótulos em D_L ∪ D_U; "pcaw64": branqueada
        from sklearn.decomposition import PCA
        white = kind.startswith("pcaw")
        k = int(kind[4:] if white else kind[3:])
        A = np.vstack([X_l, X_u])
        pca = PCA(min(k, A.shape[1], len(A) - 1), whiten=white, random_state=random_state).fit(A)
        return pca.transform(X_l), pca.transform(X_u)
    if kind == "rfleaf":
        from sklearn.decomposition import TruncatedSVD
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        rf = RandomForestClassifier(300, min_samples_leaf=3, n_jobs=-1,
                                    random_state=random_state).fit(X_l, y_l)
        L_l, L_u = rf.apply(X_l), rf.apply(X_u)
        oh = OneHotEncoder(handle_unknown="ignore").fit(np.vstack([L_l, L_u]))
        S_l, S_u = oh.transform(L_l), oh.transform(L_u)
        k = int(min(n_comp, S_l.shape[1] - 1, len(X_l) + len(X_u) - 1))
        from scipy.sparse import vstack
        svd = TruncatedSVD(k, random_state=random_state).fit(vstack([S_l, S_u]))
        Z_l, Z_u = svd.transform(S_l), svd.transform(S_u)
        sc = StandardScaler().fit(np.vstack([Z_l, Z_u]))
        return sc.transform(Z_l), sc.transform(Z_u)
    raise ValueError(kind)
