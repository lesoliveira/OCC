"""Frequência do fallback (k-means + silhueta) quando o HDBSCAN não acha
cluster nos rejeitados. Transdutivo, K estimado, família escolhida pelo auto
em results_v7 para cada semente. Uso: python3 check_fallback.py <base>
"""
import json, sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
import occ.fragments as F
from sklearn.preprocessing import StandardScaler
from splits import gcd_split
from occ.gcd import OCCDiscovery
from run_gcd import parse_spec

EV = []
_orig = F.corrected_discovery
def wrapped(Xr, best_old, base, tau, method="sil-size", *a, **k):
    out, kn = _orig(Xr, best_old, base, tau, method, *a, **k)
    if method in ("hdbscan", "hdbscan-leaf"):
        if len(Xr) < 2 * tau:
            ev = "too_few"
        else:
            from sklearn.cluster import HDBSCAN
            lab = HDBSCAN(min_cluster_size=int(round(tau)),
                          cluster_selection_method="leaf" if method == "hdbscan-leaf" else "eom").fit_predict(Xr)
            ev = "fallback" if (lab >= 0).sum() == 0 else "hdbscan"
        EV.append(dict(ev=ev, n_rej=len(Xr), tau=float(tau), k=kn))
    return out, kn
F.corrected_discovery = wrapped
import occ.gcd as G
if hasattr(G, "corrected_discovery"):
    G.corrected_discovery = wrapped

b = sys.argv[1]
X = np.load(f"data/{b}/X_train.npy"); yr = np.load(f"data/{b}/y_train.npy")
names, y = np.unique(yr, return_inverse=True)
known = [str(c) for c in json.load(open(f"data/{b}/split.json"))["known"]]
of = np.flatnonzero(np.isin(names.astype(str), known))
r = pd.read_csv(f"results_v7/a0.1/{b}_c2_kest.csv")
for seed in range(5):
    il, iu, old = gcd_split(y, 0.5, 0.5, of, seed)
    sc = StandardScaler().fit(np.vstack([X[il], X[iu]]))
    Xl, Xu = sc.transform(X[il]), sc.transform(X[iu])
    fam, kws = parse_spec(r[(r.family == "auto") & (r.seed == seed)].chosen.iloc[0])
    m = OCCDiscovery(fam, kws, alpha=0.1, random_state=seed, cal_mode="nested",
                     k_est="hdbscan-leaf").fit(Xl, y[il])
    m.discover(Xu)
    e = EV[-1] if EV else {"ev": "none"}
    print(json.dumps(dict(base=b, seed=seed, **e)), flush=True)
