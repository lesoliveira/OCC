"""PBN (Troisemaine et al., DMKD 2024) como baseline, nos cenários C1 e C2.

C1 (protocolo do artigo do PBN, para validar a reimplementação):
  treina com X_train (classes conhecidas rotuladas + novas sem rótulo),
  agrupa as amostras de classes novas de X_test com k-means no espaço latente
  e mede a ACC com casamento húngaro (média de 5 agrupamentos por rodada,
  10 rodadas). Também mede a ACC transdutiva, nas novas de X_train.
  Precisa de X_test.npy (gerado por prepare_pbn_datasets.py; só as 7 bases
  do PBN têm). Números do artigo para comparar (tabelas 4 e 5, ACC de teste,
  K conhecido / estimado): har 76,7 / 71,1; letter 62,4 / 61,3;
  pendigits 82,8 / 83,0; census 62,4 / 49,8; mfeat 91,7 / 90,6;
  optdigits 92,6 / 90,5; cnae9 72,6 / 50,8.

C2 (GCD transdutivo, como o run_gcd.py): mesma divisão por semente
  (gcd_split), mesma padronização (D_L ∪ D_U) e mesmo preproc.json. O PBN
  treina com D_L rotulado e D_U sem rótulo; o k-means no espaço latente agrupa
  D_U em n_old + K_new grupos; ACC All/Old/New com casamento húngaro.
  K estimado: silhueta no espaço latente com K total de n_old + 1 a n_old + 30
  (no GCD as classes conhecidas estão em D_U por construção; o intervalo de
  K_new, de 1 a 30, é o do notebook do PBN, que usa de 2 a 30).

Hiperparâmetros: os publicados pelo PBN nas 7 bases dele ("GT k" com K
conhecido, "Estimated k" com K estimado). Nas outras bases, rode antes
--tune, que aplica a busca aleatória do artigo e grava em
results_pbn/hparams/<base>.json.

Uso:
    pip install torch
    python3 run_pbn_baseline.py --data data/pendigits --scenario c1 --runs 1 --epochs 5   # teste rápido
    python3 run_pbn_baseline.py --data data/pendigits --scenario c1
    python3 run_pbn_baseline.py --data data/pendigits --scenario c2 --seeds 0 1 2 3 4
    python3 run_pbn_baseline.py --data data/vowel --tune
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from occ.metrics import cluster_acc, gcd_acc
from occ.pbn import PBN, PBN_HPARAMS, kmeans_labels, silhouette_k, tune
from splits import gcd_split


def load_base(path, with_test=False):
    X = np.load(os.path.join(path, "X_train.npy")).astype(float)
    y_raw = np.load(os.path.join(path, "y_train.npy"))
    Xt = yt_raw = None
    if with_test:
        Xt = np.load(os.path.join(path, "X_test.npy")).astype(float)
        yt_raw = np.load(os.path.join(path, "y_test.npy"))
    cfg = {}
    pp = os.path.join(path, "preproc.json")
    if os.path.exists(pp):
        cfg = json.load(open(pp))
    if cfg.get("drop_cols"):
        X = np.delete(X, cfg["drop_cols"], axis=1)
        if Xt is not None:
            Xt = np.delete(Xt, cfg["drop_cols"], axis=1)
    split = json.load(open(os.path.join(path, "split.json")))
    names, y = np.unique(y_raw, return_inverse=True)
    old = np.flatnonzero(np.isin(names.astype(str), [str(c) for c in split["known"]]))
    yt = None
    if yt_raw is not None:
        yt = np.searchsorted(names, yt_raw)
    return X, y, Xt, yt, old, bool(cfg.get("l2"))


def hparams_for(base, k_mode, out):
    key = "GT k" if k_mode == "known" else "Estimated k"
    if base in PBN_HPARAMS[key]:
        return PBN_HPARAMS[key][base], "publicado"
    f = os.path.join(out, "hparams", f"{base}.json")
    if os.path.exists(f):
        return json.load(open(f))["best"], "busca (--tune)"
    raise SystemExit(f"Sem hiperparâmetros para '{base}'. Rode antes: "
                     f"python3 run_pbn_baseline.py --data data/{base} --tune")


def to_codes(y, classes):
    m = {c: i for i, c in enumerate(classes)}
    return np.array([m.get(c, -1) for c in y])


def run_c1(args, base, X, y, Xt, yt, old, rows):
    sc = StandardScaler().fit(X)
    X, Xt = sc.transform(X), sc.transform(Xt)
    labeled = np.isin(y, old)
    y_codes = to_codes(y, old)
    novel_tr = ~labeled
    novel_te = ~np.isin(yt, old)
    for k_mode in args.k_modes:
        hp, src = hparams_for(base, k_mode, args.out)
        for r in range(args.runs):
            t0 = time.perf_counter()
            m = PBN(**hp, epochs=args.epochs, random_state=r, device=args.device)
            m.fit(X, y_codes, labeled)
            k_true = len(np.unique(y[novel_tr]))
            k = k_true if k_mode == "known" else \
                silhouette_k(m.embed(X[novel_tr], normalize=True), 2, 30, 3, r)
            Zte, Ztr = m.embed(Xt[novel_te]), m.embed(X[novel_tr])
            acc_te = np.mean([cluster_acc(yt[novel_te], kmeans_labels(Zte, k, 100 * r + j))
                              for j in range(5)])
            acc_tr = np.mean([cluster_acc(y[novel_tr], kmeans_labels(Ztr, k, 100 * r + j))
                              for j in range(5)])
            rows.append({"base": base, "scenario": "c1", "family": "pbn", "seed": r,
                         "k_mode": k_mode, "k_new": k, "k_true_new": k_true,
                         "acc_test": acc_te, "acc_train": acc_tr, "hparams": src,
                         "t_total_s": time.perf_counter() - t0})
            print(f"[{base}] C1 K {k_mode} rodada {r}: ACC teste {acc_te:.3f}, "
                  f"treino {acc_tr:.3f}, K {k} ({time.perf_counter() - t0:.0f} s)", flush=True)


def run_c2(args, base, X, y, old_fixed, l2, rows):
    for seed in args.seeds:
        il, iu, old = gcd_split(y, 0.5, 0.5, old_fixed, seed)
        X_l, X_u = X[il], X[iu]
        if l2:
            X_l = X_l / np.maximum(np.linalg.norm(X_l, axis=1, keepdims=True), 1e-12)
            X_u = X_u / np.maximum(np.linalg.norm(X_u, axis=1, keepdims=True), 1e-12)
        else:
            sc = StandardScaler().fit(np.vstack([X_l, X_u]))
            X_l, X_u = sc.transform(X_l), sc.transform(X_u)
        y_l, y_u = y[il], y[iu]
        Xa = np.vstack([X_l, X_u])
        labeled = np.r_[np.ones(len(X_l), bool), np.zeros(len(X_u), bool)]
        ya = np.r_[to_codes(y_l, np.asarray(old)), -np.ones(len(X_u), int)]
        k_true = len(np.unique(y_u[~np.isin(y_u, old)]))
        for k_mode in args.k_modes:
            hp, src = hparams_for(base, k_mode, args.out)
            t0 = time.perf_counter()
            m = PBN(**hp, epochs=args.epochs, random_state=seed, device=args.device)
            m.fit(Xa, ya, labeled)
            Zu = m.embed(X_u)
            n_old = len(old)
            k = n_old + k_true if k_mode == "known" else \
                silhouette_k(m.embed(X_u, normalize=True), n_old + 1, n_old + 30, 3, seed)
            pred = kmeans_labels(Zu, k, seed)
            a = gcd_acc(y_u, pred, old)
            rows.append({"base": base, "scenario": "c2", "family": "pbn", "seed": seed,
                         "k_mode": k_mode, "k_new": k - n_old, "k_true_new": k_true,
                         "acc_all": a["all"], "acc_old": a["old"], "acc_new": a["new"],
                         "hparams": src, "t_total_s": time.perf_counter() - t0})
            print(f"[{base}] C2 K {k_mode} semente {seed}: ACC all {a['all']:.3f} "
                  f"old {a['old']:.3f} new {a['new']:.3f}, K_new {k - n_old} "
                  f"({time.perf_counter() - t0:.0f} s)", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--scenario", choices=["c1", "c2"], default="c1")
    ap.add_argument("--tune", action="store_true",
                    help="busca aleatória de hiperparâmetros (protocolo do PBN, dados do C1)")
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--folds", type=int, default=3)
    ap.add_argument("--runs", type=int, default=10, help="rodadas no C1 (o artigo usa 10)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    ap.add_argument("--k-modes", nargs="+", choices=["known", "est"], default=["known", "est"])
    ap.add_argument("--epochs", type=int, default=200)
    ap.add_argument("--device", default="cpu", help="cpu ou mps")
    ap.add_argument("--out", default="results_pbn")
    args = ap.parse_args()
    base = os.path.basename(args.data.rstrip("/"))
    os.makedirs(args.out, exist_ok=True)
    try:
        import torch
        torch.set_num_threads(max(1, os.cpu_count() or 1))
        print(f"torch {torch.__version__}, dispositivo {args.device}")
    except ImportError:
        raise SystemExit("Instale o PyTorch: pip install torch")

    if args.tune:
        X, y, _, _, old, l2 = load_base(args.data)
        if not l2:
            X = StandardScaler().fit_transform(X)
        labeled = np.isin(y, old)
        n_novel = len(np.unique(y[~labeled]))
        print(f"[{base}] busca: {args.trials} tentativas x {args.folds} dobras, "
              f"{args.epochs} épocas")
        best, score, hist, n_hid = tune(X, y, labeled, n_novel, args.trials, args.folds,
                                 epochs=args.epochs, device=args.device)
        os.makedirs(os.path.join(args.out, "hparams"), exist_ok=True)
        with open(os.path.join(args.out, "hparams", f"{base}.json"), "w") as f:
            json.dump({"best": best, "ari_hidden": score, "n_hidden": n_hid,
                       "trials": args.trials,
                       "folds": args.folds, "history": hist}, f, indent=1)
        print(f"[{base}] melhor: {best} (ARI nas escondidas {score:.3f})")
        return

    rows = []
    if args.scenario == "c1":
        X, y, Xt, yt, old, _ = load_base(args.data, with_test=True)
        run_c1(args, base, X, y, Xt, yt, old, rows)
    else:
        X, y, _, _, old, l2 = load_base(args.data)
        run_c2(args, base, X, y, old, l2, rows)
    df = pd.DataFrame(rows)
    path = os.path.join(args.out, f"{base}_{args.scenario}_pbn.csv")
    df.to_csv(path, index=False)
    cols = ["acc_test", "acc_train", "k_new"] if args.scenario == "c1" else \
        ["acc_all", "acc_old", "acc_new", "k_new"]
    print(df.groupby("k_mode")[cols].agg(["mean", "std"]).round(3).to_string())
    print(f"Resultados salvos em {path}")


if __name__ == "__main__":
    main()
