"""Bases tabulares adicionais do OpenML, com critérios fixados de antemão.

Objetivo: fechar os vãos de cobertura das 7 bases do PBN (mais de 26
classes, atributos categóricos, classes desbalanceadas, bases grandes) e
chegar a 10 ou mais bases para o teste de Friedman sobre as bases.

Critérios de inclusão (fixados antes de rodar qualquer método):
  1. classificação multiclasse com pelo menos 6 classes;
  2. pelo menos 500 amostras;
  3. classes com menos de MIN_PER_CLASS (20) amostras são descartadas e,
     depois disso, continuam valendo os critérios 1 e 2;
  4. não é uma base de imagens brutas (pixels), que vão no estudo com
     representações de imagem.
Bases com mais de MAX_SAMPLES (20.000) amostras são subamostradas de forma
estratificada (a proporção entre classes é mantida, inclusive o
desbalanceamento).

Pré-processamento: atributos categóricos viram one-hot; valores ausentes
numéricos são preenchidos pela mediana; colunas constantes são removidas.
Os atributos são salvos sem padronização (o run_gcd.py padroniza).

Divisão conhecidas/novas: as classes são embaralhadas com semente fixa
(SPLIT_SEED = 0) e a primeira metade (arredondada para baixo) é a das
conhecidas, como em Vaze et al.

Saída, por base, em data/<nome>/: X_train.npy, y_train.npy, split.json e
meta.json (origem, id do OpenML, tamanho, classes descartadas).

Uso (precisa de internet; roda no seu computador):
    python prepare_openml_datasets.py                 # todas da lista
    python prepare_openml_datasets.py --only isolet vowel
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

MIN_CLASSES = 6
MIN_SAMPLES = 500
MIN_PER_CLASS = 20
MAX_SAMPLES = 20000
SPLIT_SEED = 0

# nome local -> (nome no OpenML, versão), com o vão que a base cobre
CANDIDATES = {
    "isolet":    ("isolet", 1),          # 26 classes, 617 atributos (fala)
    "satimage":  ("satimage", 1),        # 6 classes, sensoriamento remoto
    "segment":   ("segment", 1),         # 7 classes, segmentação de imagem (atributos)
    "vowel":     ("vowel", 1),           # 11 classes, poucas amostras, atributos mistos
    "krvsk":     ("kr-vs-k", 1),         # 18 classes, categórico, desbalanceado
    "covertype": ("covertype", 3),       # 7 classes, grande, desbalanceado
    "helena":    ("helena", 1),          # 100 classes, desbalanceado
    "volkert":   ("volkert", 1),         # 10 classes, 180 atributos, grande
    "shuttle":   ("shuttle", 1),         # 7 classes, muito desbalanceado
}


def to_numeric(X):
    """DataFrame -> matriz float: one-hot nos categóricos, mediana nos ausentes."""
    X = X.copy()
    cat = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
    num = [c for c in X.columns if c not in cat]
    for c in num:
        X[c] = X[c].astype(float).fillna(X[c].astype(float).median())
    if cat:
        X = pd.get_dummies(X, columns=cat, dummy_na=False, dtype=float)
    A = X.to_numpy(float)
    keep = A.std(axis=0) > 0
    return A[:, keep], int((~keep).sum()), len(cat)


def process(X_df, y_raw, rng):
    y_raw = pd.Series(np.asarray(y_raw)).astype(str).to_numpy()
    classes, counts = np.unique(y_raw, return_counts=True)
    dropped = [str(c) for c, n in zip(classes, counts) if n < MIN_PER_CLASS]
    ok = ~np.isin(y_raw, dropped)
    X_df, y_raw = X_df[ok].reset_index(drop=True), y_raw[ok]
    classes = np.unique(y_raw)
    if len(classes) < MIN_CLASSES or len(y_raw) < MIN_SAMPLES:
        return None, f"reprovada: {len(classes)} classes, {len(y_raw)} amostras"
    if len(y_raw) > MAX_SAMPLES:  # subamostragem estratificada
        idx = []
        for c in classes:
            ic = np.flatnonzero(y_raw == c)
            n = max(MIN_PER_CLASS, int(round(len(ic) * MAX_SAMPLES / len(y_raw))))
            idx.append(rng.choice(ic, min(n, len(ic)), replace=False))
        idx = np.sort(np.concatenate(idx))
        X_df, y_raw = X_df.iloc[idx].reset_index(drop=True), y_raw[idx]
    X, n_const, n_cat = to_numeric(X_df)
    y = np.unique(y_raw, return_inverse=True)[1]
    C = len(np.unique(y))
    perm = np.random.default_rng(SPLIT_SEED).permutation(C)
    known = sorted(perm[:C // 2].tolist())
    novel = sorted(perm[C // 2:].tolist())
    meta = {"n": int(len(y)), "d": int(X.shape[1]), "classes": int(C),
            "categorical_columns": n_cat, "constant_columns_removed": n_const,
            "dropped_classes_lt_min": dropped,
            "min_class_size": int(np.bincount(y).min()),
            "max_class_size": int(np.bincount(y).max()),
            "class_names": [str(c) for c in np.unique(y_raw)]}
    return (X, y, known, novel, meta), "aprovada"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data")
    ap.add_argument("--only", nargs="+", choices=list(CANDIDATES))
    args = ap.parse_args()
    from sklearn.datasets import fetch_openml
    rng = np.random.default_rng(0)
    report = []
    for name in args.only or list(CANDIDATES):
        oml, ver = CANDIDATES[name]
        print(f"[{name}] OpenML '{oml}' v{ver}")
        try:
            b = fetch_openml(name=oml, version=ver, as_frame=True, parser="auto")
        except Exception as e:  # noqa: BLE001
            print(f"  ERRO ao baixar: {e}")
            report.append((name, "erro ao baixar"))
            continue
        res, status = process(b.data, b.target, rng)
        print(f"  {status}")
        if res is None:
            report.append((name, status))
            continue
        X, y, known, novel, meta = res
        meta.update({"source": "OpenML", "openml_name": oml, "openml_version": ver,
                     "openml_id": int(b.details.get("id", -1)) if hasattr(b, "details") else -1})
        d = os.path.join(args.out, name)
        os.makedirs(d, exist_ok=True)
        np.save(os.path.join(d, "X_train.npy"), X)
        np.save(os.path.join(d, "y_train.npy"), y)
        with open(os.path.join(d, "split.json"), "w") as f:
            json.dump({"known": known, "novel": novel}, f)
        with open(os.path.join(d, "meta.json"), "w") as f:
            json.dump(meta, f, indent=1)
        print(f"  n={meta['n']} d={meta['d']} classes={meta['classes']} "
              f"(conhecidas {len(known)}, novas {len(novel)}) "
              f"menor classe={meta['min_class_size']} maior={meta['max_class_size']}"
              + (f" descartadas={meta['dropped_classes_lt_min']}" if meta['dropped_classes_lt_min'] else ""))
        report.append((name, f"ok: {meta['n']}×{meta['d']}, {meta['classes']} classes"))
    print("\nResumo:")
    for n, s in report:
        print(f"  {n:10s} {s}")


if __name__ == "__main__":
    main()
