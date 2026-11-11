"""Monta as tabelas de resultados a partir dos CSVs do run_gcd.py.

Uso:
    python summarize.py results            # lê results/*_c2_*.csv

Saída: uma tabela por métrica e por configuração de K (média ± desvio
sobre as sementes, métodos nas linhas, bases nas colunas), mais o rank
médio e o teste de Wilcoxon pareado de cada método contra o melhor OCC.
Grava também results/summary.md.
"""
import glob
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

OCC = ["gauss", "knn", "svm", "svm-cv", "mst", "modes", "dic"]


def md(df, index=True):
    """Tabela markdown sem depender do pacote tabulate."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    rows = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    rows += ["| " + " | ".join(str(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join(rows)


def load(folder):
    dfs = []
    for f in sorted(glob.glob(os.path.join(folder, "*_c2_*.csv"))):
        base, _, k = os.path.basename(f)[:-4].rpartition("_c2_")
        df = pd.read_csv(f)
        df["base"], df["k"] = base, k
        dfs.append(df)
    if not dfs:
        sys.exit(f"nenhum CSV *_c2_*.csv em {folder}")
    return pd.concat(dfs, ignore_index=True)


def table(df, metric, higher=True):
    g = df.groupby(["family", "base"])[metric]
    m = g.mean().unstack()
    s = g.std().unstack()
    out = m.map(lambda v: f"{v:.3f}") + " ± " + s.fillna(0).map(lambda v: f"{v:.3f}")
    out["média"] = m.mean(axis=1).map(lambda v: f"{v:.3f}")
    out["rank médio"] = m.rank(ascending=not higher).mean(axis=1).round(2)
    return out.sort_values("rank médio")


def wilcoxon_vs(df, metric, ref):
    """Wilcoxon pareado por (base, semente) de cada método contra ref."""
    p = df.pivot_table(index=["base", "seed"], columns="family", values=metric)
    rows = []
    for fam in p.columns:
        if fam == ref:
            continue
        d = (p[fam] - p[ref]).dropna()
        stat = wilcoxon(d).pvalue if len(d) > 5 and (d != 0).any() else np.nan
        rows.append({"método": fam, f"Δ média vs {ref}": round(d.mean(), 3),
                     "p (Wilcoxon)": round(stat, 4) if stat == stat else "—",
                     "pares": len(d)})
    return pd.DataFrame(rows).sort_values(f"Δ média vs {ref}", ascending=False)


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "results"
    df = load(folder)
    lines = []
    for k in sorted(df["k"].unique()):
        dk = df[df["k"] == k]
        title = "K conhecido" if k == "kknown" else "K estimado"
        for metric in ["acc_all", "acc_old", "acc_new"]:
            lines.append(f"## {metric} — {title}\n")
            lines.append(md(table(dk, metric)))
            lines.append("")
        # rejeição: só métodos com escore de novidade
        rej = dk[dk["auroc"].notna()] if "auroc" in dk else dk.iloc[:0]
        for metric, note in [("auroc", "AUROC Old × New do escore de novidade"),
                             ("old_false_reject", "fração de Old de D_U rejeitada (alvo ≤ α)"),
                             ("new_reject", "fração de New de D_U rejeitada (o resto é absorvido)")]:
            if len(rej) and metric in rej:
                lines.append(f"## {metric} — {title}\n\n{note}\n")
                lines.append(md(table(rej, metric, higher=metric != "old_false_reject")))
                lines.append("")
        if k != "kknown" and "k_new" in dk:
            kt = dk.groupby("base")["k_true_new"].first()
            g = dk[dk.family != "kmeans"].groupby(["family", "base"])["k_new"].mean().unstack().round(1)
            g.loc["(verdadeiro)"] = kt
            lines.append(f"## K_new usado — {title}\n")
            lines.append(md(g))
            lines.append("")
        for fam_sel in ("svm-cv", "auto-auroc"):
            if "chosen" in dk and (dk.family == fam_sel).any():
                a = dk[dk.family == fam_sel]
                ch = a.groupby("base")["chosen"].agg(
                    lambda v: ", ".join(f"{f}×{n}" for f, n in v.value_counts().items()))
                lines.append(f"## Escolha do {fam_sel} — {title}\n")
                lines.append(md(ch.to_frame("escolhas nas sementes")))
                lines.append("")
        if "chosen" in dk and (dk.family == "auto").any():
            a = dk[dk.family == "auto"]
            ch = a.groupby("base")["chosen"].agg(
                lambda v: ", ".join(f"{f}×{n}" for f, n in v.value_counts().items()))
            lines.append(f"## Família escolhida pelo 'auto' (deixa-uma-classe-de-fora em D_L) — {title}\n")
            lines.append(md(ch.to_frame("escolhas nas sementes")))
            lines.append("")
            lines.append(f"## Wilcoxon pareado em acc_all contra o auto — {title}\n")
            lines.append(md(wilcoxon_vs(dk, "acc_all", "auto"), index=False))
            lines.append("")
        is_occ = dk.family.str.split("+").str[0].isin(OCC)
        occ_means = dk[is_occ].groupby("family")["acc_all"].mean()
        best = occ_means.idxmax()
        lines.append(f"## Wilcoxon pareado em acc_all contra o melhor OCC ({best}) — {title}\n")
        lines.append(md(wilcoxon_vs(dk, "acc_all", best), index=False))
        lines.append("")
    text = "\n".join(lines)
    print(text)
    with open(os.path.join(folder, "summary.md"), "w") as f:
        f.write(text)
    print(f"\nTabela salva em {os.path.join(folder, 'summary.md')}")


if __name__ == "__main__":
    main()
