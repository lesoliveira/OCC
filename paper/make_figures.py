"""Figuras do artigo (incremental).

  fig_stream.pdf : T = 10 sessões, média das 6 bases por sessão: ACC All e tempo
                   por sessão (results_c4_long_tau para o nosso, results_c4_long
                   para RF-MSP e PBN).
  fig_har.pdf, fig_pendigits.pdf : t-SNE (T = 3) com a classe atribuída a
                   cada amostra ao fim de cada sessão (results_fig/<base>_c4_seed<s>.pkl,
                   gerado por run_c4.py --dump). HAR semente 0, pendigits semente 4.

Uso: python3 paper/make_figures.py
"""
import os
import pickle
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
OUT = os.path.join(ROOT, "paper", "figures")
os.makedirs(OUT, exist_ok=True)

# paleta categórica de referência (ordem fixa), tinta neutra para texto
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    # Springer: letras em Helvetica ou Arial, 8 a 12 pt. Liberation Sans tem as
    # mesmas métricas da Arial e é usada quando a Arial não está instalada.
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "TeX Gyre Heros"],
    "mathtext.fontset": "custom", "mathtext.rm": "sans", "mathtext.it": "sans:italic",
    "pdf.fonttype": 42,
})

LONG = ["covertype", "helena", "isolet", "letter", "pendigits", "volkert"]
METHODS = [("auto", "OCC (auto)", C[0], "o"), ("rf_msp", "RF-MSP", C[1], "s"),
           ("pbn", "PBN", C[2], "^")]


def fig_stream():
    per = {k: [] for k, *_ in METHODS}
    for b in LONG:
        o = pd.read_csv(os.path.join(ROOT, "results_c4_long", f"{b}_c4.csv"))
        n = pd.read_csv(os.path.join(ROOT, "results_c4_long_tau", f"{b}_c4.csv"))
        D = {"auto": n[n.family == "auto-auroc"], "rf_msp": o[o.family == "rf_msp"],
             "pbn": o[o.family == "pbn"]}
        for k in per:
            per[k].append(D[k].groupby("session")[["acc_all", "t_session_s"]].mean())
    fig, ax = plt.subplots(1, 2, figsize=(5.15, 2.1))
    for k, lab, col, mk in METHODS:
        m = pd.concat(per[k]).groupby(level=0).mean()
        s = m.index.values
        for a, col_name in zip(ax, ["acc_all", "t_session_s"]):
            a.plot(s, m[col_name], color=col, lw=1.6, marker=mk, ms=4,
                   markeredgecolor="white", markeredgewidth=0.6, label=lab)
        # rótulo direto na última sessão
        # no painel de acurácia, RF-MSP e OCC terminam próximos: afasta os rótulos
        dy0 = {"rf_msp": 4, "auto": -4}.get(k, 0)
        for a, col_name, dy in zip(ax, ["acc_all", "t_session_s"], [dy0, 0]):
            a.annotate(lab, (s[-1], m[col_name].iloc[-1]), xytext=(5, dy),
                       textcoords="offset points", va="center", fontsize=8, color=INK)
    ax[0].set_ylabel("ACC All")
    ax[0].set_ylim(0, 0.6)
    ax[1].set_ylabel("Seconds (log scale)")
    ax[1].set_yscale("log")
    ax[1].set_yticks([0.3, 1, 3, 10, 30])
    ax[1].set_yticklabels(["0.3", "1", "3", "10", "30"])
    ax[1].minorticks_off()
    ax[1].set_ylim(0.25, 30)
    for a, t in zip(ax, ["(a) Accuracy", "(b) Time per session"]):
        a.set_xlabel("Session")
        a.set_xticks(range(1, 11))
        a.set_xlim(0.6, 12.2)
        a.grid(axis="y", color=GRID, lw=0.6)
        a.set_axisbelow(True)
        a.set_title(t, loc="left", color=INK)
    fig.legend(*ax[0].get_legend_handles_labels(), loc="lower center", ncol=3,
               frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(w_pad=2.0)
    fig.savefig(os.path.join(OUT, "fig_stream.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(OUT, "fig_stream.png"), dpi=200, bbox_inches="tight")


# uma cor por classe (conhecidas primeiro, novas na ordem de estreia): as 8
# cores da paleta de referência e mais duas para bases com 10 classes
CLASS_COLS = C + ["#008300", "#e34948", "#8c564b", "#7f7f7f"]
SPUR = INK
UNSEEN = "#ecebe7"


def fig_tsne(base, seed, name):
    """t-SNE com a classe atribuída a cada amostra ao fim de cada sessão.

    Uma cor por classe (conhecidas primeiro, novas na ordem de estreia),
    classes espúrias em preto, amostras ainda não vistas em cinza claro. O t-SNE é calculado uma vez, nos dados padronizados com S0.
    """
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    from run_c4 import load, scaler_s0
    X, y, known, _ = load(os.path.join(ROOT, "data", base))
    with open(os.path.join(ROOT, "results_fig", f"{base}_c4_seed{seed}.pkl"), "rb") as f:
        D = pickle.load(f)[("auto-auroc", seed)]
    idx_l, sess, pred, debut = D["idx_l"], D["sess"], D["pred"], D["debut"]
    mu, sd = scaler_s0(X[idx_l])
    Xs = (X - mu) / sd
    cache = os.path.join(ROOT, "results_fig", f"{base}_tsne_seed{seed}.npy")
    if os.path.exists(cache):
        Z = np.load(cache)
    else:
        Xp = PCA(50, random_state=0).fit_transform(Xs) if Xs.shape[1] > 50 else Xs
        Z = TSNE(2, random_state=0, init="pca", perplexity=40).fit_transform(Xp)
        np.save(cache, Z)
    kn = sorted(int(c) for c in np.unique(y) if debut[int(c)] == 0)
    nv = sorted((int(c) for c in np.unique(y) if debut[int(c)] > 0),
                key=lambda c: (debut[c], c))
    order = kn + nv
    col = {c: CLASS_COLS[i] for i, c in enumerate(order)}
    T = len(sess)
    fig, ax = plt.subplots(1, T + 1, figsize=(5.15, 1.75))
    kw = dict(s=0.9, linewidths=0, rasterized=True)
    for c in order:
        m = y == c
        ax[0].scatter(Z[m, 0], Z[m, 1], color=col[c], **kw)
    ax[0].set_title("(a) Ground truth", loc="left")
    assigned = np.full(len(y), -1)      # -1 = ainda não chegou
    assigned[idx_l] = y[idx_l]          # S0: rotulado
    for t in range(T):
        assigned[sess[t]] = pred[t]     # não muda depois (sem reetiquetar)
        a = ax[t + 1]
        m = assigned == -1
        a.scatter(Z[m, 0], Z[m, 1], color=UNSEEN, **kw)
        for c in order:
            m = assigned == c
            a.scatter(Z[m, 0], Z[m, 1], color=col[c], **kw)
        m = assigned == -999
        a.scatter(Z[m, 0], Z[m, 1], color=SPUR, s=1.2, linewidths=0, rasterized=True)
        a.set_title(f"({chr(98 + t)}) After $U_{t + 1}$", loc="left")
    for a in ax:
        a.set_xticks([]), a.set_yticks([])
        for sp in a.spines.values():
            sp.set_visible(False)
    dot = lambda c, l: plt.Line2D([], [], ls="", marker="o", ms=3.5, color=c, label=l)
    h = [dot(col[c], f"Class {c} (known)") for c in kn]
    h += [dot(col[c], f"Class {c} ($U_{debut[c]}$)") for c in nv]
    h += [dot(SPUR, "Spurious class"), dot("#d6d5d0", "Not yet seen")]
    nc = 4
    rows = -(-len(h) // nc)
    fig.legend(handles=h, loc="upper center", ncol=nc, frameon=False,
               bbox_to_anchor=(0.5, 0.02), columnspacing=1.2, handletextpad=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f"{name}.pdf"), bbox_inches="tight", dpi=300)
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    fig_stream()
    fig_tsne("har", 0, "fig_har")
    fig_tsne("pendigits", 4, "fig_pendigits")
