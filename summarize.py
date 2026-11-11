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


def friedman_block(M, ref=None, title=""):
    """Friedman nas bases (Demšar, JMLR 2006) e Wilcoxon com correção de Holm
    contra a referência, usando a média de cada base (uma observação por
    base, sem pseudorreplicação das sementes). M: DataFrame base × método."""
    from scipy.stats import friedmanchisquare
    M = M.dropna(axis=1)  # só métodos presentes em todas as bases
    L = [f"## Friedman nas bases (média das sementes por base) — {title}\n"]
    if M.shape[0] < 3 or M.shape[1] < 3:
        return L + ["(precisa de ao menos 3 bases e 3 métodos)", ""]
    stat, p = friedmanchisquare(*[M[c].to_numpy() for c in M.columns])
    ranks = M.rank(axis=1, ascending=False).mean().sort_values()
    L.append(f"{M.shape[0]} bases, {M.shape[1]} métodos: χ² = {stat:.2f}, p = {p:.2g}\n")
    ref = ref if ref in M.columns else ranks.index[0]
    rows = []
    for c in M.columns:
        if c == ref:
            continue
        d = M[c] - M[ref]
        pv = wilcoxon(d).pvalue if (d != 0).any() else 1.0
        rows.append([c, d.mean(), pv])
    # Holm separado por grupo de hipóteses, definido de antemão:
    # baselines (a pergunta principal) e variantes de OCC (ablação)
    BASE = {"kmeans", "sskmeans", "rf_msp", "lr_msp"}
    L.append(f"Rank médio de {ref}: {ranks[ref]:.2f}\n")
    for gname, grp in [("baselines", [r for r in rows if r[0] in BASE]),
                       ("variantes de OCC (ablação)", [r for r in rows if r[0] not in BASE])]:
        if not grp:
            continue
        grp.sort(key=lambda r: r[2])
        m = len(grp)
        adj, run = [], 0.0
        for i, r in enumerate(grp):  # Holm dentro do grupo
            run = max(run, min(1.0, (m - i) * r[2]))
            adj.append(run)
        T = pd.DataFrame({"método": [r[0] for r in grp],
                          f"Δ média vs {ref}": [round(r[1], 3) for r in grp],
                          "p (Wilcoxon nas bases)": [round(r[2], 4) for r in grp],
                          f"p ajustado (Holm, {m} comparações)": [round(a, 4) for a in adj],
                          "rank médio": [round(ranks[r[0]], 2) for r in grp]})
        L.append(f"**{ref} contra {gname}**\n")
        L.append(md(T, index=False))
        L.append("")
    return L


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
        M = dk.groupby(["base", "family"])["acc_all"].mean().unstack()
        lines += friedman_block(M, "auto-auroc" if "auto-auroc" in M else "auto", title)
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
