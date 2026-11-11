"""Tabelas do cenário C4 a partir dos CSVs do run_c4.py.

Uso: python summarize_c4.py results_c4      # lê results_c4/*_c4.csv

Por base e método (média ± desvio nas sementes):
- ACC All na última sessão e média nas sessões;
- ACC New média (descoberta) e ACC Old média (reconhecimento do que já
  foi visto, incluindo classes descobertas antes);
- esquecimento: acc_s0 na sessão 1 menos acc_s0 na última;
- classes no modelo ao fim / classes verdadeiras;
- tempo por sessão (média) e razão última/primeira sessão.
Wilcoxon pareado (base × semente) da ACC All média contra a referência.
Grava <pasta>/summary_c4.md.
"""
import glob
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from summarize import md


def load(folder):
    dfs = []
    for f in sorted(glob.glob(os.path.join(folder, "*_c4.csv"))):
        d = pd.read_csv(f)
        d["base"] = os.path.basename(f)[:-7]
        dfs.append(d)
    if not dfs:
        sys.exit(f"nenhum *_c4.csv em {folder}")
    return pd.concat(dfs, ignore_index=True)


def per_run(df):
    T = df.groupby(["base"])["session"].transform("max")
    last = df[df.session == T]
    first = df[df.session == 1]
    key = ["base", "family", "seed"]
    g = df.groupby(key)
    out = pd.DataFrame({
        "acc_all_mean": g.acc_all.mean(),
        "acc_new_mean": g.acc_new.mean(),
        "acc_old_mean": g.acc_old.mean(),
        "t_mean": g.t_session_s.mean(),
    })
    L = last.set_index(key)
    F = first.set_index(key)
    out["acc_all_last"] = L.acc_all
    out["forgetting"] = F.acc_s0 - L.acc_s0
    out["classes"] = L.n_model_classes.astype(str) + "/" + L.n_true_classes.astype(str)
    out["t_ratio"] = L.t_session_s / F.t_session_s.clip(lower=1e-3)
    return out.reset_index()


def table(r, col, fmt="{:.3f}"):
    g = r.groupby(["family", "base"])[col]
    m, s = g.mean().unstack(), g.std().unstack().fillna(0)
    out = m.map(fmt.format) + " ± " + s.map(fmt.format)
    out["média"] = m.mean(axis=1).map(fmt.format)
    return out.sort_values("média", ascending=col == "forgetting")


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "results_c4"
    ref = sys.argv[2] if len(sys.argv) > 2 else "auto-auroc"
    r = per_run(load(folder))
    L = []
    for col, title in [("acc_all_mean", "ACC All média nas sessões"),
                       ("acc_all_last", "ACC All na última sessão"),
                       ("acc_new_mean", "ACC New média (classes que estreiam na sessão)"),
                       ("acc_old_mean", "ACC Old média (classes já vistas, incl. descobertas)"),
                       ("forgetting", "Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor"),
                       ("t_mean", "Tempo médio por sessão (s)")]:
        L += [f"## {title}\n", md(table(r, col)), ""]
    df = load(folder)
    if "spur_from_s0" in df:
        sp = df.groupby(["family", "base"])[["spur_from_s0", "spur_from_prev", "spur_from_new"]].sum()
        sp = sp.div(df.groupby(["family", "base"]).seed.nunique(), axis=0).round(1)
        sp.columns = ["de classe da sessão 0", "de classe já descoberta", "de classe nova"]
        sp["tamanho médio"] = df.groupby(["family", "base"]).spur_size_mean.mean().round(0)
        L += ["## Clusters espúrios por semente (somados nas sessões), pela classe majoritária\n",
              md(sp), ""]
    cl = r.groupby(["family", "base"]).classes.agg(lambda v: ", ".join(v)).unstack()
    L += ["## Classes no modelo ao fim / classes verdadeiras (por semente)\n", md(cl), ""]
    if ref in set(r.family):
        p = r.pivot_table(index=["base", "seed"], columns="family", values="acc_all_mean")
        rows = []
        for f in p.columns:
            if f == ref:
                continue
            d = (p[f] - p[ref]).dropna()
            pv = wilcoxon(d).pvalue if len(d) > 5 and (d != 0).any() else np.nan
            rows.append({"método": f, f"Δ vs {ref}": round(d.mean(), 3),
                         "p (Wilcoxon)": round(pv, 4) if pv == pv else "—", "pares": len(d)})
        L += [f"## Wilcoxon pareado na ACC All média contra {ref}\n",
              md(pd.DataFrame(rows).sort_values(f"Δ vs {ref}", ascending=False), index=False), ""]
    text = "\n".join(L)
    print(text)
    with open(os.path.join(folder, "summary_c4.md"), "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
