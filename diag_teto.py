"""Diagnóstico: teto supervisionado de cada base.

Com TODAS as classes rotuladas, mede por validação cruzada estratificada a
acurácia de um RF (não depende da métrica do espaço) e de um kNN no espaço
padronizado (o mesmo espaço que os OCCs usam). Serve para separar dois casos
nas bases em que nenhum método detecta as classes novas:
  RF alto e kNN baixo  -> as classes existem, a distância não as enxerga
                          (problema de representação);
  RF baixo e kNN baixo -> as classes se sobrepõem nos atributos (limite dos dados).

Uso: python diag_teto.py --data data/krvsk --out results_diag
"""
import argparse, json, os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.metrics import accuracy_score, balanced_accuracy_score

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--out", default="results_diag")
ap.add_argument("--folds", type=int, default=3)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
name = os.path.basename(a.data.rstrip("/"))
X = np.load(os.path.join(a.data, "X_train.npy")).astype(float)
y = np.load(os.path.join(a.data, "y_train.npy"))
split = json.load(open(os.path.join(a.data, "split.json")))
pre = {}
pp = os.path.join(a.data, "preproc.json")
if os.path.exists(pp):
    pre = json.load(open(pp))
if pre.get("drop_cols"):
    X = np.delete(X, pre["drop_cols"], axis=1)
novel = np.isin(y, split["novel"])
cv = StratifiedKFold(a.folds, shuffle=True, random_state=a.seed)
models = {"rf": RandomForestClassifier(300, n_jobs=-1, random_state=a.seed)}
if pre.get("l2"):
    Xk = normalize(X); models["knn"] = KNeighborsClassifier(5, n_jobs=-1)
else:
    Xk = X; models["knn"] = make_pipeline(StandardScaler(), KNeighborsClassifier(5, n_jobs=-1))
C = len(np.unique(y))
res = {"base": name, "n": len(y), "d": X.shape[1], "classes": C,
       "acaso": round(float(np.bincount(y).max() / len(y)), 4)}
for m, clf in models.items():
    p = cross_val_predict(clf, Xk if m == "knn" else X, y, cv=cv)
    res[f"{m}_acc"] = round(accuracy_score(y, p), 4)
    res[f"{m}_bal"] = round(balanced_accuracy_score(y, p), 4)
    res[f"{m}_acc_novas"] = round(accuracy_score(y[novel], p[novel]), 4)
    res[f"{m}_acc_conhecidas"] = round(accuracy_score(y[~novel], p[~novel]), 4)
os.makedirs(a.out, exist_ok=True)
json.dump(res, open(os.path.join(a.out, f"{name}.json"), "w"), indent=1)
print(res)
