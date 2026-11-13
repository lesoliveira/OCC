"""PBN (Projection-Based NCD; Troisemaine et al., DMKD 2024), reimplementado.

Segue o código oficial (github.com/Orange-OpenSource/PracticalNCD,
models/PBN_model.py e Full_notebook*.ipynb):

  - codificador: Linear(d, 3d/4) -> [ReLU, BatchNorm, Dropout, Linear] ->
    (2d/4) -> [ReLU, BatchNorm, Dropout, Linear] -> latent_dim; no treino, z é
    normalizado por L2 antes do decodificador e do classificador;
  - decodificador espelhado; classificador linear sobre z (classes conhecidas);
  - perda w * CE(conhecidas do lote) + (1 - w) * MSE(soma por amostra, todas);
  - AdamW, 200 épocas, lote 512;
  - agrupamento: k-means (n_init = 10) na saída do codificador SEM a
    normalização, como em predict_new_data;
  - K estimado: silhueta do k-means (3 repetições por k) no espaço latente
    normalizado, k de 2 a 30, como em estimate_k_with_silhouette.

Diferença em relação ao código oficial: os lotes são embaralhados a cada
época (o oficial percorre os dados na ordem em que foram embaralhados uma vez).
Precisa de PyTorch (pip install torch).
"""
import math

import numpy as np

# hiperparâmetros publicados (hyperparameters.json do repositório oficial)
PBN_HPARAMS = {
    "GT k": {
        "har": {"lr": 0.0001387, "w": 0.8814, "p_dropout": 0.5526, "latent_dim": 276},
        "letter": {"lr": 0.006142, "w": 0.8605, "p_dropout": 0.0808, "latent_dim": 13},
        "pendigits": {"lr": 0.00284, "w": 0.4606, "p_dropout": 0.02538, "latent_dim": 11},
        "census": {"lr": 0.000495, "w": 0.9715, "p_dropout": 0.138, "latent_dim": 28},
        "mfeat": {"lr": 0.0002768, "w": 0.4283, "p_dropout": 0.1264, "latent_dim": 123},
        "optdigits": {"lr": 0.0008756, "w": 0.0637, "p_dropout": 0.08648, "latent_dim": 58},
        "cnae9": {"lr": 0.004836, "w": 0.9006, "p_dropout": 0.01101, "latent_dim": 768},
    },
    "Estimated k": {
        "har": {"lr": 0.0001014, "w": 0.4671, "p_dropout": 0.5098, "latent_dim": 504},
        "letter": {"lr": 0.0005889, "w": 0.7224, "p_dropout": 0.02746, "latent_dim": 22},
        "pendigits": {"lr": 0.001077, "w": 0.1067, "p_dropout": 0.01126, "latent_dim": 12},
        "census": {"lr": 0.002112, "w": 0.9609, "p_dropout": 0.1678, "latent_dim": 13},
        "mfeat": {"lr": 0.004675, "w": 0.6703, "p_dropout": 0.2393, "latent_dim": 172},
        "optdigits": {"lr": 0.0003646, "w": 0.1892, "p_dropout": 0.06607, "latent_dim": 53},
        "cnae9": {"lr": 0.0044, "w": 0.6982, "p_dropout": 0.08132, "latent_dim": 579},
    },
}


def _torch():
    import torch
    return torch


class PBN:
    """fit(X, y_known, is_labeled) treina; embed(X) devolve o espaço latente."""

    def __init__(self, lr, w, p_dropout, latent_dim, epochs=200, batch_size=512,
                 random_state=0, device="cpu"):
        self.lr, self.w, self.p_dropout = float(lr), float(w), float(p_dropout)
        self.latent_dim = int(latent_dim)
        self.epochs, self.batch_size = int(epochs), int(batch_size)
        self.random_state, self.device = random_state, device

    def _build(self, d, n_classes):
        torch = _torch()
        nn = torch.nn
        dims = [math.floor(3 * d / 4), math.floor(2 * d / 4), self.latent_dim]
        dims = [max(1, x) for x in dims]

        def block(a, b, last_linear=True):
            layers = [nn.ReLU(), nn.BatchNorm1d(a)]
            if self.p_dropout > 0:
                layers.append(nn.Dropout(self.p_dropout))
            layers.append(nn.Linear(a, b))
            return layers

        enc = [nn.Linear(d, dims[0])]
        for i in range(1, len(dims)):
            enc += block(dims[i - 1], dims[i])
        dec_dims = list(reversed(dims))
        dec = []
        for i in range(1, len(dec_dims)):
            dec += [nn.Linear(dec_dims[i - 1], dec_dims[i]), nn.ReLU(),
                    nn.BatchNorm1d(dec_dims[i])]
            if self.p_dropout > 0:
                dec.append(nn.Dropout(self.p_dropout))
        dec.append(nn.Linear(dec_dims[-1], d))
        self.enc_ = nn.Sequential(*enc).to(self.device)
        self.dec_ = nn.Sequential(*dec).to(self.device)
        self.cls_ = nn.Linear(self.latent_dim, n_classes).to(self.device)

    def fit(self, X, y, labeled):
        """X: todas as amostras de treino; y: rótulo 0..C-1 onde labeled é True."""
        torch = _torch()
        F = torch.nn.functional
        torch.manual_seed(self.random_state)
        rng = np.random.default_rng(self.random_state)
        X = np.asarray(X, np.float32)
        labeled = np.asarray(labeled, bool)
        yy = np.where(labeled, np.asarray(y), -1).astype(np.int64)
        n_classes = int(yy[labeled].max()) + 1
        self._build(X.shape[1], n_classes)
        params = list(self.enc_.parameters()) + list(self.dec_.parameters()) + \
            list(self.cls_.parameters())
        opt = torch.optim.AdamW(params, lr=self.lr)
        Xt = torch.tensor(X, device=self.device)
        yt = torch.tensor(yy, device=self.device)
        for m in (self.enc_, self.dec_, self.cls_):
            m.train()
        n = len(X)
        for _ in range(self.epochs):
            perm = torch.tensor(rng.permutation(n), device=self.device)
            for s in range(0, n, self.batch_size):
                idx = perm[s:s + self.batch_size]
                if len(idx) < 2:
                    continue
                xb, yb = Xt[idx], yt[idx]
                z = F.normalize(self.enc_(xb), p=2, dim=1)
                mse = ((self.dec_(z) - xb) ** 2).sum() / len(xb)
                known = yb >= 0
                if known.any():
                    ce = F.cross_entropy(self.cls_(z[known]), yb[known])
                    loss = self.w * ce + (1 - self.w) * mse
                else:
                    loss = (1 - self.w) * mse
                opt.zero_grad()
                loss.backward()
                opt.step()
        for m in (self.enc_, self.dec_, self.cls_):
            m.eval()
        return self

    def embed(self, X, normalize=False):
        torch = _torch()
        with torch.no_grad():
            z = self.enc_(torch.tensor(np.asarray(X, np.float32), device=self.device))
            if normalize:
                z = torch.nn.functional.normalize(z, p=2, dim=1)
        return z.cpu().numpy().astype(float)


def kmeans_labels(Z, k, random_state):
    from sklearn.cluster import KMeans
    return KMeans(k, init="k-means++", n_init=10, random_state=random_state).fit_predict(Z)


def silhouette_k(Z, k_min=2, k_max=30, avg=3, random_state=0, max_eval=5000):
    """k de maior silhueta média (3 k-means por k), como no notebook do PBN.

    Para bases grandes a silhueta é calculada numa amostra de max_eval pontos
    (o notebook usa todos); a escolha de k é a mesma na prática.
    """
    from sklearn.metrics import silhouette_score
    rng = np.random.default_rng(random_state)
    ks = list(range(k_min, min(k_max, len(Z) - 1) + 1))
    best, best_s = ks[0], -np.inf
    for k in ks:
        sc = []
        for r in range(avg):
            lab = kmeans_labels(Z, k, random_state + r)
            if len(Z) > max_eval:
                i = rng.choice(len(Z), max_eval, replace=False)
                sc.append(silhouette_score(Z[i], lab[i]))
            else:
                sc.append(silhouette_score(Z, lab))
        if np.mean(sc) > best_s:
            best, best_s = k, float(np.mean(sc))
    return best


def tune(X, y_known, labeled, n_novel, n_trials=20, n_folds=3, n_hidden=None,
         epochs=200, random_state=0, device="cpu", log=print):
    """Busca aleatória do PBN (seção 4 do artigo): esconde classes conhecidas,
    agrupa D_U ∪ D_hid com k = n_hid + n_novel e mede o ARI só em D_hid.

    Faixas do artigo: lr log-uniforme em [1e-4, 1e-1], w em (0, 1), dropout
    em [0, 0,6], latent_dim inteiro em [5, d]. O artigo não informa quantas
    tentativas nem dobras usou; aqui são n_trials e n_folds.
    """
    from sklearn.metrics import adjusted_rand_score
    rng = np.random.default_rng(random_state)
    X = np.asarray(X, np.float32)
    labeled = np.asarray(labeled, bool)
    yk = np.asarray(y_known)
    classes = np.unique(yk[labeled])
    if n_hidden is None:
        n_hidden = max(1, len(classes) // 2)
    folds = [np.sort(rng.choice(classes, n_hidden, replace=False)) for _ in range(n_folds)]
    d = X.shape[1]
    best, best_score, history = None, -np.inf, []
    for t in range(n_trials):
        hp = {"lr": float(10 ** rng.uniform(-4, -1)), "w": float(rng.uniform(0.01, 0.99)),
              "p_dropout": float(rng.uniform(0, 0.6)), "latent_dim": int(rng.integers(5, d + 1))}
        aris = []
        for f, hid in enumerate(folds):
            is_hid = labeled & np.isin(yk, hid)
            lab_f = labeled & ~is_hid
            remap = {c: i for i, c in enumerate(np.unique(yk[lab_f]))}
            y_f = np.array([remap.get(c, -1) for c in yk])
            m = PBN(**hp, epochs=epochs, random_state=random_state + f, device=device)
            m.fit(X, y_f, lab_f)
            U = ~labeled | is_hid
            pred = kmeans_labels(m.embed(X[U]), n_hidden + n_novel, random_state)
            aris.append(adjusted_rand_score(yk[is_hid], pred[is_hid[U]]))
        score = float(np.mean(aris))
        history.append({**hp, "ari": score})
        log(f"  tentativa {t + 1}/{n_trials}: ARI {score:.3f} {hp}")
        if score > best_score:
            best, best_score = hp, score
    return best, best_score, history
