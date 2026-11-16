"""Gera as tabelas do artigo (paper/tables/*.tex) e paper/numbers.json a
partir dos CSVs de resultados. Rodar da raiz do repositório:

    python3 paper/make_tables.py

Fontes (ver EXPERIMENTOS.md):
  C2: results_v7/a0.1 (OCCs, RF-MSP, LR-MSP; k-means e SS-k-means com K
      conhecido), results_kmfix (k-means e SS-k-means com K estimado,
      mínimo de K corrigido), results_pbn/*_c2_pbn.csv (PBN).
  C4: results_c4_v2 (auto, RF-MSP), results_kmfix_c4 (SS-k-means),
      results_pbn/*_c4_pbn.csv (PBN).
  Ablações: results_pc (seleção por classe), results_ksil15 (estimador
      de K alternativo), results_diag (teto supervisionado).
  Apêndice: results_pbn/*_c1_pbn.csv (reprodução do PBN).
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "tables")
os.makedirs(OUT, exist_ok=True)
R = lambda *p: os.path.join(ROOT, *p)

BASES = ["census", "cnae9", "covertype", "har", "helena", "isolet", "krvsk", "letter",
         "mfeat", "optdigits", "pendigits", "satimage", "segment", "volkert", "vowel"]
PBN7 = {"har", "letter", "pendigits", "census", "mfeat", "optdigits", "cnae9"}
NAME = {"census": "Census", "cnae9": "CNAE-9", "covertype": "Covertype", "har": "HAR",
        "helena": "Helena", "isolet": "Isolet", "krvsk": "KRvsK", "letter": "Letter",
        "mfeat": "Mfeat", "optdigits": "Optdigits", "pendigits": "Pendigits",
        "satimage": "Satimage", "segment": "Segment", "volkert": "Volkert", "vowel": "Vowel"}
NUM = {}


def holm(p):
    keys = sorted(p, key=p.get)
    out, run = {}, 0.0
    for i, k in enumerate(keys):
        run = max(run, min(1.0, (len(keys) - i) * p[k]))
        out[k] = run
    return out


def f3(x):
    return "--" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.3f}"


def fp(p):
    return "$<$0.001" if p < 0.001 else f"{p:.3f}"


def save(name, s):
    # \bottomrule vai no próprio arquivo: depois de um \input dentro de um
    # tabular, um \bottomrule no documento dá "Misplaced \noalign"
    if name != "chosen.tex":
        s = s.rstrip("\n") + "\n\\bottomrule\n"
    with open(os.path.join(OUT, name), "w") as f:
        f.write(s)


# ------------------------------------------------------------------ bases
def table_datasets():
    rows = []
    for b in BASES:
        y = np.load(R("data", b, "y_train.npy"))
        X = np.load(R("data", b, "X_train.npy"), mmap_mode="r")
        sp = json.load(open(R("data", b, "split.json")))
        d = X.shape[1]
        pp = R("data", b, "preproc.json")
        if os.path.exists(pp):
            d -= len(json.load(open(pp)).get("drop_cols", []))
        c2 = pd.read_csv(R("results_v7", "a0.1", f"{b}_c2_kest.csv"))
        maxauc = c2.groupby("family").auroc.mean().max()
        dg = json.load(open(R("results_diag", f"{b}.json")))
        rows.append(dict(b=b, src="PBN" if b in PBN7 else "OpenML", n=len(y), d=d,
                         known=len(sp["known"]), novel=len(sp["novel"]),
                         minc=int(np.bincount(np.unique(y, return_inverse=True)[1]).min()),
                         maxc=int(np.bincount(np.unique(y, return_inverse=True)[1]).max()),
                         auc=maxauc, rf=dg["rf_acc"], knn=dg["knn_acc"]))
    T = pd.DataFrame(rows).set_index("b")
    T["detect"] = T.auc > 0.75
    NUM["datasets"] = T.to_dict(orient="index")
    lines = []
    for b, r in T.sort_values(["detect", "auc"], ascending=[False, False]).iterrows():
        lines.append(f"{NAME[b]} & {r.src} & {r.n:,} & {r.d} & {r.known} & {r.novel} & "
                     f"{r.minc:,} & {r.maxc:,} & {r.auc:.3f} & {r.rf:.3f} & {r.knn:.3f} \\\\")
    i = int(T.detect.sum())
    body = "\n".join(lines[:i]) + "\n\\midrule\n" + "\n".join(lines[i:])
    save("datasets.tex", body.replace(",", "{,}") + "\n")
    return T


# ------------------------------------------------------------------ C2
C2_METHODS = [("auto", "OCC (auto)"), ("rf_msp", "RF-MSP"), ("pbn", "PBN"),
              ("lr_msp", "LR-MSP"), ("sskmeans", "SS-$k$-means"), ("kmeans", "$k$-means")]


def load_c2(mode):
    """mode: 'kest' ou 'kknown'. Devolve {base: DataFrame por método (médias)}."""
    out = {}
    for b in BASES:
        v7 = pd.read_csv(R("results_v7", "a0.1", f"{b}_c2_{mode}.csv"))
        g = v7.groupby("family")[["acc_all", "acc_old", "acc_new", "auroc", "k_new"]].mean()
        if mode == "kest":
            fx = pd.read_csv(R("results_kmfix", f"{b}_c2_kest.csv"))
            g2 = fx.groupby("family")[["acc_all", "acc_old", "acc_new", "k_new"]].mean()
            for f in ["kmeans", "sskmeans"]:
                g.loc[f, ["acc_all", "acc_old", "acc_new", "k_new"]] = g2.loc[f].values
        pb = pd.read_csv(R("results_pbn", f"{b}_c2_pbn.csv"))
        pb = pb[pb.k_mode == ("est" if mode == "kest" else "known")]
        g.loc["pbn", ["acc_all", "acc_old", "acc_new", "k_new"]] = \
            pb[["acc_all", "acc_old", "acc_new", "k_new"]].mean().values
        g.loc["pbn", "auroc"] = np.nan
        g["k_true"] = v7.k_true_new.iloc[0]
        out[b] = g
    return out


def stats_block(T, ref="auto"):
    fr = friedmanchisquare(*[T[c] for c in T])
    ranks = T.rank(axis=1, ascending=False).mean()
    p = {c: wilcoxon(T[ref], T[c]).pvalue for c in T if c != ref}
    ph = holm(p)
    wins = {c: (int((T[ref] > T[c] + 0.005).sum()), int((T[c] > T[ref] + 0.005).sum()))
            for c in p}
    return fr, ranks, p, ph, wins


def table_c2(mode):
    G = load_c2(mode)
    keys = [k for k, _ in C2_METHODS]
    T = pd.DataFrame({b: {k: G[b].loc[k, "acc_all"] for k in keys} for b in BASES}).T
    fr, ranks, p, ph, wins = stats_block(T)
    NUM[f"c2_{mode}"] = {"mean": T.mean().to_dict(), "rank": ranks.to_dict(),
                         "friedman_p": fr.pvalue, "friedman_chi2": fr.statistic,
                         "wilcoxon_p": p, "holm_p": ph, "wins": wins,
                         "per_base": T.to_dict(orient="index")}
    lines = []
    for b in BASES:
        r = T.loc[b]
        best = r.max()
        cells = [(r"\textbf{%s}" % f3(r[k])) if r[k] >= best - 1e-9 else f3(r[k]) for k in keys]
        lines.append(f"{NAME[b]} & " + " & ".join(cells) + r" \\")
    lines.append(r"\midrule")
    lines.append("Mean & " + " & ".join(f3(T[k].mean()) for k in keys) + r" \\")
    lines.append("Mean rank & " + " & ".join(f"{ranks[k]:.2f}" for k in keys) + r" \\")
    lines.append("W/L vs.\\ OCC & -- & " + " & ".join(f"{wins[k][0]}/{wins[k][1]}"
                                                     for k in keys[1:]) + r" \\")
    lines.append("$p$ (Holm) & -- & " + " & ".join(fp(ph[k]) for k in keys[1:]) + r" \\")
    save(f"c2_{mode}.tex", "\n".join(lines) + "\n")
    # resumo Old/New/AUROC/K
    lines = []
    for k, lab in C2_METHODS:
        old = np.mean([G[b].loc[k, "acc_old"] for b in BASES])
        new = np.mean([G[b].loc[k, "acc_new"] for b in BASES])
        auc = np.nanmean([G[b].loc[k, "auroc"] for b in BASES]) if k in ("auto", "rf_msp", "lr_msp") else np.nan
        kerr = np.mean([abs(G[b].loc[k, "k_new"] - G[b].loc[k, "k_true"]) for b in BASES])
        NUM.setdefault(f"c2_{mode}_summary", {})[k] = dict(old=old, new=new, auroc=auc, kerr=kerr)
        lines.append(f"{lab} & {f3(T[k].mean())} & {f3(old)} & {f3(new)} & {f3(auc)}"
                     + (f" & {kerr:.1f}" if mode == "kest" else "") + r" \\")
    save(f"c2_{mode}_summary.tex", "\n".join(lines) + "\n")
    return T, G


# ------------------------------------------------------------------ C4
def c4_stats(df):
    """Médias por semente (nas sessões) e depois entre sementes."""
    per = df.groupby("seed")
    acc = per[["acc_all", "acc_old", "acc_new"]].mean().mean()

    def forget(x):
        x = x.sort_values("session")
        return x.acc_s0.iloc[0] - x.acc_s0.iloc[-1]
    fg = per.apply(forget).mean()
    return dict(all=acc.acc_all, old=acc.acc_old, new=acc.acc_new, forget=fg,
                time=df.t_session_s.mean(), ncls=df.groupby("seed").n_model_classes.last().mean(),
                ntrue=df.groupby("seed").n_true_classes.last().mean())


C4_METHODS = [("auto", "OCC (auto)"), ("rf_msp", "RF-MSP"), ("pbn", "PBN"),
              ("sskmeans", "SS-$k$-means")]


def table_c4():
    S = {}
    for b in BASES:
        v2 = pd.read_csv(R("results_c4_v2", f"{b}_c4.csv"))
        S[b] = {"auto": c4_stats(v2[v2.family == "auto-auroc"]),
                "rf_msp": c4_stats(v2[v2.family == "rf_msp"]),
                "sskmeans": c4_stats(pd.read_csv(R("results_kmfix_c4", f"{b}_c4.csv"))),
                "pbn": c4_stats(pd.read_csv(R("results_pbn", f"{b}_c4_pbn.csv")))}
    keys = [k for k, _ in C4_METHODS]
    T = pd.DataFrame({b: {k: S[b][k]["all"] for k in keys} for b in BASES}).T
    fr, ranks, p, ph, wins = stats_block(T)
    NUM["c4"] = {"mean": T.mean().to_dict(), "rank": ranks.to_dict(),
                 "friedman_p": fr.pvalue, "friedman_chi2": fr.statistic,
                 "wilcoxon_p": p, "holm_p": ph, "wins": wins,
                 "per_base": T.to_dict(orient="index")}
    lines = []
    for b in BASES:
        r = T.loc[b]
        best = r.max()
        cells = [(r"\textbf{%s}" % f3(r[k])) if r[k] >= best - 1e-9 else f3(r[k]) for k in keys]
        lines.append(f"{NAME[b]} & " + " & ".join(cells) + r" \\")
    lines.append(r"\midrule")
    lines.append("Mean & " + " & ".join(f3(T[k].mean()) for k in keys) + r" \\")
    lines.append("Mean rank & " + " & ".join(f"{ranks[k]:.2f}" for k in keys) + r" \\")
    lines.append("W/L vs.\\ OCC & -- & " + " & ".join(f"{wins[k][0]}/{wins[k][1]}"
                                                     for k in keys[1:]) + r" \\")
    lines.append("$p$ (Holm) & -- & " + " & ".join(fp(ph[k]) for k in keys[1:]) + r" \\")
    save("c4.tex", "\n".join(lines) + "\n")
    lines = []
    stores = {"auto": "No", "rf_msp": "Yes", "pbn": "Yes", "sskmeans": "Yes"}
    retrain = {"auto": "No", "rf_msp": "Yes", "pbn": "Yes", "sskmeans": "Yes"}
    for k, lab in C4_METHODS:
        m = {q: np.mean([S[b][k][q] for b in BASES]) for q in ["all", "old", "new", "forget", "time"]}
        NUM.setdefault("c4_summary", {})[k] = m
        lines.append(f"{lab} & {f3(m['all'])} & {f3(m['old'])} & {f3(m['new'])} & "
                     f"{f3(m['forget'])} & " + ("--" if k == "sskmeans" else f"{m['time']:.2f}")
                     + f" & {stores[k]} & {retrain[k]}" + r" \\")
    save("c4_summary.tex", "\n".join(lines) + "\n")
    return T


# ------------------------------------------------------------------ ablações
FAMS = [("gauss", "Gaussian"), ("knn", "$k$NN"), ("mst", "MST"), ("dic", "Dichotomy"),
        ("svm", r"OC-SVM ($\gamma$ default)"), ("svm-cv", r"OC-SVM ($\gamma$ by LOCO)")]


def table_families():
    T = {}
    for b in BASES:
        g = pd.read_csv(R("results_v7", "a0.1", f"{b}_c2_kest.csv")).groupby("family").acc_all.mean()
        T[b] = {k: g[k] for k in ["auto"] + [f for f, _ in FAMS]}
    T = pd.DataFrame(T).T
    fixed = [f for f, _ in FAMS if f not in ("svm-cv",)]
    oracle = T[fixed].max(axis=1)
    ranks = T.rank(axis=1, ascending=False).mean()
    p = {f: wilcoxon(T.auto, T[f]).pvalue for f, _ in FAMS}
    ph = holm(p)
    chosen = {}
    for b in BASES:
        d = pd.read_csv(R("results_v7", "a0.1", f"{b}_c2_kest.csv"))
        chosen[b] = d[d.family == "auto"].chosen.value_counts().to_dict()
    NUM["families"] = {"mean": T.mean().to_dict(), "rank": ranks.to_dict(), "holm_p": ph,
                       "oracle_mean": oracle.mean(),
                       "loss_mean": {k: (oracle - T[k]).mean() for k in T},
                       "loss_max": {k: (oracle - T[k]).max() for k in T},
                       "within002": {k: int(((oracle - T[k]) <= 0.02).sum()) for k in T},
                       "chosen": chosen}
    lines = [f"OCC (auto) & {f3(T.auto.mean())} & {ranks['auto']:.2f} & "
             f"{(oracle - T.auto).mean():.3f} & {(oracle - T.auto).max():.3f} & "
             f"{int(((oracle - T.auto) <= 0.02).sum())} & -- \\\\", r"\midrule"]
    for f, lab in FAMS:
        lines.append(f"{lab} & {f3(T[f].mean())} & {ranks[f]:.2f} & {(oracle - T[f]).mean():.3f} & "
                     f"{(oracle - T[f]).max():.3f} & {int(((oracle - T[f]) <= 0.02).sum())} & "
                     f"{fp(ph[f])} \\\\")
    save("families.tex", "\n".join(lines) + "\n")
    # família escolhida por base (moda das 5 sementes)
    def lab(s):
        return {"gauss": "Gaussian", "knn": "$k$NN", "mst": "MST", "dic": "Dichotomy"}.get(
            s, s.replace("svm@", r"OC-SVM $\gamma{\times}$"))
    items = []
    for b in BASES:
        c = chosen[b]
        top = max(c, key=c.get)
        items.append(f"{NAME[b]}: {lab(top)} ({c[top]}/5)")
    save("chosen.tex", "; ".join(items) + ".\n")


def table_ablation_selection():
    rows = {}
    for b in BASES:
        a = pd.read_csv(R("results_v7", "a0.1", f"{b}_c2_kest.csv"))
        a = a[a.family == "auto"]
        pc = pd.read_csv(R("results_pc", f"{b}_c2_kest.csv"))
        ks = pd.read_csv(R("results_ksil15", f"{b}_c2_kest.csv"))
        ks = ks[ks.family == "auto"]
        rows[b] = dict(auto=a.acc_all.mean(), auto_auc=a.auroc.mean(), k_auto=a.k_new.mean(),
                       pc=pc.acc_all.mean(), pc_auc=pc.auroc.mean(),
                       sil=ks.acc_all.mean(), k_sil=ks.k_new.mean(), k_true=a.k_true_new.iloc[0])
    T = pd.DataFrame(rows).T
    NUM["ablation"] = {
        "auto": T.auto.mean(), "pc": T.pc.mean(), "sil": T.sil.mean(),
        "auto_auc": T.auto_auc.mean(), "pc_auc": T.pc_auc.mean(),
        "p_pc": wilcoxon(T.pc, T.auto).pvalue, "p_sil": wilcoxon(T.sil, T.auto).pvalue,
        "pc_wl": (int((T.pc > T.auto + 0.005).sum()), int((T.pc < T.auto - 0.005).sum())),
        "sil_wl": (int((T.sil > T.auto + 0.005).sum()), int((T.sil < T.auto - 0.005).sum())),
        "kerr_auto": (T.k_auto - T.k_true).abs().mean(), "kerr_sil": (T.k_sil - T.k_true).abs().mean(),
        "per_base": T.to_dict(orient="index")}
    lines = [
        f"Proposed (global family, fragment-aware HDBSCAN) & {f3(T.auto.mean())} & {f3(T.auto_auc.mean())} & "
        f"{(T.k_auto - T.k_true).abs().mean():.1f} & -- & -- \\\\",
        f"Per-class family selection & {f3(T.pc.mean())} & {f3(T.pc_auc.mean())} & -- & "
        f"{NUM['ablation']['pc_wl'][0]}/{NUM['ablation']['pc_wl'][1]} & {NUM['ablation']['p_pc']:.2f} \\\\",
        f"Silhouette $k$-means with fragment filter & {f3(T.sil.mean())} & {f3(T.auto_auc.mean())} & "
        f"{(T.k_sil - T.k_true).abs().mean():.1f} & "
        f"{NUM['ablation']['sil_wl'][0]}/{NUM['ablation']['sil_wl'][1]} & {NUM['ablation']['p_sil']:.2f} \\\\"]
    save("ablation.tex", "\n".join(lines) + "\n")


PUB = {"har": (76.7, 71.1), "letter": (62.4, 61.3), "pendigits": (82.8, 83.0),
       "census": (62.4, 49.8), "mfeat": (91.7, 90.6), "optdigits": (92.6, 90.5),
       "cnae9": (72.6, 50.8)}


def table_pbn_repro():
    lines, ours_k, ours_e = [], [], []
    for b in ["har", "letter", "pendigits", "census", "mfeat", "optdigits", "cnae9"]:
        d = pd.read_csv(R("results_pbn", f"{b}_c1_pbn.csv"))
        k = d[d.k_mode == "known"].acc_test
        e = d[d.k_mode == "est"].acc_test
        ours_k.append(k.mean()); ours_e.append(e.mean())
        lines.append(f"{NAME[b]} & {100 * k.mean():.1f} $\\pm$ {100 * k.std():.1f} & {PUB[b][0]:.1f} & "
                     f"{100 * e.mean():.1f} $\\pm$ {100 * e.std():.1f} & {PUB[b][1]:.1f} \\\\")
    lines.append(r"\midrule")
    lines.append(f"Mean & {100 * np.mean(ours_k):.1f} & {np.mean([v[0] for v in PUB.values()]):.1f} & "
                 f"{100 * np.mean(ours_e):.1f} & {np.mean([v[1] for v in PUB.values()]):.1f} \\\\")
    NUM["pbn_repro"] = {"known": np.mean(ours_k), "est": np.mean(ours_e),
                        "pub_known": np.mean([v[0] for v in PUB.values()]) / 100,
                        "pub_est": np.mean([v[1] for v in PUB.values()]) / 100}
    save("pbn_repro.tex", "\n".join(lines) + "\n")


def table_c1():
    lines = []
    for b in ["har", "letter", "pendigits", "census", "mfeat", "optdigits", "cnae9"]:
        d = pd.read_csv(R("results_c1", f"{b}_c1_kknown.csv")).groupby("family")["acc"].mean()
        p = pd.read_csv(R("results_pbn", f"{b}_c1_pbn.csv"))
        p = p[p.k_mode == "known"].acc_train.mean()
        best_occ = max(d["gauss"], d["mst"])
        lines.append(f"{NAME[b]} & {f3(d['kmeans'])} & {f3(best_occ)} & {f3(p)} \\\\")
        NUM.setdefault("c1", {})[b] = dict(kmeans=d["kmeans"], occ=best_occ, pbn=p)
    save("c1.tex", "\n".join(lines) + "\n")


if __name__ == "__main__":
    table_datasets()
    table_c2("kest")
    table_c2("kknown")
    table_c4()
    table_families()
    table_ablation_selection()
    table_pbn_repro()
    table_c1()

    def conv(o):
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o
    json.dump(conv(NUM), open(os.path.join(ROOT, "paper", "numbers.json"), "w"), indent=1)
    print("tabelas em", OUT)
