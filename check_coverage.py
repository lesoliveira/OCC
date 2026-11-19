"""Cobertura empírica dos p-valores conformes: fração das amostras conhecidas de
D_U com p-valor da própria classe abaixo de alpha (semente 0, família do auto
em results_v7). Uso: for b in ...; do python3 check_coverage.py $b; done > results_coverage/coverage.jsonl
"""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, '/home/claude/occ')
from sklearn.preprocessing import StandardScaler
from splits import gcd_split
from occ.gcd import OCCDiscovery
from run_gcd import parse_spec
b = sys.argv[1]; seed = 0
X = np.load(f'data/{b}/X_train.npy'); yr = np.load(f'data/{b}/y_train.npy')
names, y = np.unique(yr, return_inverse=True)
known = [str(c) for c in json.load(open(f'data/{b}/split.json'))['known']]
of = np.flatnonzero(np.isin(names.astype(str), known))
il, iu, old = gcd_split(y, 0.5, 0.5, of, seed)
sc = StandardScaler().fit(np.vstack([X[il], X[iu]]))
Xl, Xu = sc.transform(X[il]), sc.transform(X[iu]); yl, yu = y[il], y[iu]
r = pd.read_csv(f'results_v7/a0.1/{b}_c2_kest.csv')
spec = r[(r.family == 'auto') & (r.seed == seed)].chosen.iloc[0]
fam, kws = parse_spec(spec)
m = OCCDiscovery(fam, kws, alpha=0.1, random_state=seed, cal_mode='nested').fit(Xl, yl).model_
P = m.pvalues(Xu); cls = list(m.classes_)
kn = np.isin(yu, old)
own = P[kn, [cls.index(c) for c in yu[kn]]]
out = {'base': b, 'family': spec}
for a in (0.05, 0.1, 0.2):
    out[f'miss@{a}'] = float((own < a).mean())
# pior classe em alpha 0,1
pc = pd.Series(own < 0.1).groupby(yu[kn]).mean()
out['miss_worst'] = float(pc.max()); out['ncal_min'] = int(min(len(v) for v in m.cal_.values()))
print(json.dumps(out))
