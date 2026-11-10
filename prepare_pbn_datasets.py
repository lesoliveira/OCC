"""Baixa e prepara as 7 bases tabulares do PBN (Troisemaine et al., DMKD 2024).

Reproduz o pré-processamento do repositório oficial
(github.com/Orange-OpenSource/PracticalNCD, src/dataset_utils.py) e a
divisão de classes conhecidas/novas usada no artigo. Para cada base, salva
em data/<base>/:

    X_train.npy, y_train.npy   conjunto de treino (onde o GCD é rodado)
    X_test.npy,  y_test.npy    conjunto de teste (para o cenário indutivo C3)
    split.json                 classes conhecidas e novas do PBN

Os atributos são salvos SEM padronização; o run_gcd.py padroniza.

Uso:
    python prepare_pbn_datasets.py                  # as 6 bases menores
    python prepare_pbn_datasets.py --with-census    # inclui o Census (~360 MB)
    python prepare_pbn_datasets.py --only pendigits optdigits

Diferenças conhecidas em relação ao artigo:
  - Letter, Census e mfeat têm divisão treino/teste aleatória no código do
    PBN; aqui a semente é fixa (0), então os números podem variar um pouco.
  - mfeat: o código do PBN usa só o arquivo mfeat-fac (216 atributos),
    embora a tabela 2 do artigo indique 515. Seguimos o código.
  - Letter: o código do PBN lê o arquivo com a primeira linha como
    cabeçalho e perde uma amostra; aqui ela é mantida.
"""
import argparse
import io
import json
import os
import urllib.request
import zipfile

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

UCI = "https://archive.ics.uci.edu/static/public"
URLS = {
    "har": f"{UCI}/240/human+activity+recognition+using+smartphones.zip",
    "letter": f"{UCI}/59/letter+recognition.zip",
    "pendigits": f"{UCI}/81/pen+based+recognition+of+handwritten+digits.zip",
    "census": f"{UCI}/116/us+census+data+1990.zip",
    "mfeat": f"{UCI}/72/multiple+features.zip",
    "optdigits": f"{UCI}/80/optical+recognition+of+handwritten+digits.zip",
    "cnae9": f"{UCI}/233/cnae+9.zip",
}

# Divisão conhecidas / novas do PBN (import_dataset_with_name)
SPLITS = {
    "har": ([1, 2, 5], [0, 3, 4]),
    "letter": ([1, 2, 4, 5, 6, 8, 9, 10, 11, 13, 14, 16, 17, 18, 19, 20, 22, 24, 25],
               [0, 3, 7, 12, 15, 21, 23]),
    "pendigits": ([1, 2, 4, 8, 9], [0, 3, 5, 6, 7]),
    "census": ([1, 2, 4, 6, 7, 8, 9, 10, 13, 14, 16, 17], [0, 3, 5, 11, 12, 15]),
    "mfeat": ([0, 2, 5, 4, 8], [7, 3, 1, 9, 6]),
    "optdigits": ([2, 1, 9, 8, 7], [3, 6, 0, 5, 4]),
    "cnae9": ([5, 0, 7, 8, 4], [2, 9, 6, 3, 1]),
}


def fetch_zip(url):
    print(f"  baixando {url}")
    with urllib.request.urlopen(url, timeout=600) as r:
        return zipfile.ZipFile(io.BytesIO(r.read()))


def find(z, suffix):
    names = [n for n in z.namelist() if n.endswith(suffix) and "__MACOSX" not in n]
    if not names:
        raise FileNotFoundError(f"{suffix} não encontrado no zip: {z.namelist()[:20]}")
    return names[0]


def read_txt(z, suffix, **kw):
    return pd.read_csv(io.BytesIO(z.read(find(z, suffix))), **kw)


def prep_har(z):
    # o zip da UCI contém outro zip, "UCI HAR Dataset.zip"
    inner = [n for n in z.namelist() if n.endswith("UCI HAR Dataset.zip")]
    if inner:
        z = zipfile.ZipFile(io.BytesIO(z.read(inner[0])))
    out = []
    for part in ("train", "test"):
        X = read_txt(z, f"{part}/X_{part}.txt", header=None, sep=r"\s+").to_numpy(float)
        subj = read_txt(z, f"{part}/subject_{part}.txt", header=None, sep=r"\s+")[0].to_numpy(float)
        X = np.column_stack([X, subj])  # 561 atributos + sujeito, como no PBN
        y = read_txt(z, f"{part}/y_{part}.txt", header=None)[0].to_numpy()
        # o PBN ordena as classes pelo nome da atividade
        names = {1: "WALKING", 2: "WALKING_UPSTAIRS", 3: "WALKING_DOWNSTAIRS",
                 4: "SITTING", 5: "STANDING", 6: "LAYING"}
        order = {n: i for i, n in enumerate(sorted(names.values()))}
        out += [X, np.array([order[names[v]] for v in y])]
    return out


def prep_letter(z):
    df = read_txt(z, "letter-recognition.data", header=None)
    y = np.unique(df[0].to_numpy(), return_inverse=True)[1]
    X = df.drop(columns=[0]).to_numpy(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, random_state=0)
    return Xtr, ytr, Xte, yte


def prep_pendigits(z):
    tr = read_txt(z, "pendigits.tra", header=None)
    te = read_txt(z, "pendigits.tes", header=None)
    return (tr.iloc[:, :-1].to_numpy(float), tr.iloc[:, -1].to_numpy(),
            te.iloc[:, :-1].to_numpy(float), te.iloc[:, -1].to_numpy())


def prep_census(z):
    df = read_txt(z, "USCensus1990.data.txt", dtype=np.int16).drop(columns=["caseid"])
    y = df["iYearsch"].to_numpy()
    X = df.drop(columns=["iYearsch"]).to_numpy(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, random_state=0)

    def cap(X, y, n=1000):  # o PBN limita a 1000 amostras por classe
        rng = np.random.default_rng(0)
        idx = np.sort(np.concatenate([rng.permutation(np.flatnonzero(y == c))[:n]
                                      for c in np.unique(y)]))
        return X[idx], y[idx]
    return (*cap(Xtr, ytr), *cap(Xte, yte))


def prep_mfeat(z):
    df = read_txt(z, "mfeat-fac", header=None, sep=r"\s+")
    y = np.repeat(np.arange(10), 200)  # 200 padrões por classe, em ordem
    X = df.to_numpy(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=42)
    return Xtr, ytr, Xte, yte


def prep_optdigits(z):
    tr = read_txt(z, "optdigits.tra", header=None)
    te = read_txt(z, "optdigits.tes", header=None)
    out = []
    for df in (tr, te):
        y = df[64].to_numpy()
        X = df.drop(columns=[0, 39, 64]).to_numpy(float)  # colunas constantes
        out += [X, y]
    return out


def prep_cnae9(z):
    df = read_txt(z, "CNAE-9.data", header=None)
    y = df[0].to_numpy()
    X = df.drop(columns=[0]).to_numpy(float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.20, random_state=42)
    # Rótulos originais 1..9, como no PBN. A divisão do PBN lista a classe 0,
    # que não existe; por isso o artigo tem 4 conhecidas e 5 novas.
    return Xtr, ytr, Xte, yte


PREP = {"har": prep_har, "letter": prep_letter, "pendigits": prep_pendigits,
        "census": prep_census, "mfeat": prep_mfeat, "optdigits": prep_optdigits,
        "cnae9": prep_cnae9}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data")
    ap.add_argument("--only", nargs="+", choices=list(PREP))
    ap.add_argument("--with-census", action="store_true")
    args = ap.parse_args()
    names = args.only or [n for n in PREP if n != "census" or args.with_census]
    for name in names:
        print(f"[{name}]")
        Xtr, ytr, Xte, yte = PREP[name](fetch_zip(URLS[name]))
        present = set(np.unique(ytr).tolist())
        # mantém só as classes que existem (no CNAE-9, a classe 0 do PBN não existe)
        known = [c for c in SPLITS[name][0] if c in present]
        novel = [c for c in SPLITS[name][1] if c in present]
        dropped = [c for c in SPLITS[name][0] + SPLITS[name][1] if c not in present]
        if dropped:
            print(f"  nota: classes da divisão do PBN ausentes nos dados: {dropped}")
        extra = sorted(present - set(known) - set(novel))
        if extra:
            print(f"  AVISO: classes nos dados fora da divisão do PBN: {extra}")
        d = os.path.join(args.out, name)
        os.makedirs(d, exist_ok=True)
        for k, v in {"X_train": Xtr, "y_train": ytr, "X_test": Xte, "y_test": yte}.items():
            np.save(os.path.join(d, f"{k}.npy"), v)
        with open(os.path.join(d, "split.json"), "w") as f:
            json.dump({"known": known, "novel": novel}, f)
        print(f"  treino {Xtr.shape}, teste {Xte.shape}, classes {sorted(present)}")
        print(f"  conhecidas {known}  novas {novel}")


if __name__ == "__main__":
    main()
