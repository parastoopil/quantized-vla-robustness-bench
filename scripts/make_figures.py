#!/usr/bin/env python3
"""Regenerate every figure in ../figures from the CSVs in ../data.

Usage:  python3 scripts/make_figures.py

The figures are descriptive: they show the success rate of each quantized copy
of pi0.5 side by side with the FP16 model. No effect size is being tested; the
point is simply to see how the curves sit relative to one another.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIGS = os.path.join(HERE, "..", "figures")
os.makedirs(FIGS, exist_ok=True)

# --- design tokens (validated categorical palette, light surface) -------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e6e5e2"
C_FP16 = "#2a78d6"   # blue   — reference model
C_Q1 = "#eb6834"     # orange — W4A4 (Omega-QVLA)
C_Q2 = "#1baf7a"     # aqua   — W4A8 (QuantVLA)

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": GRID,
    "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 1.0,
    "font.family": "DejaVu Sans",
})


def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=1.0, zorder=0)
    ax.set_axisbelow(True)


# --- Figure 1: LIBERO-plus, three arms per axis -------------------------------
def fig_libero_plus():
    df = pd.read_csv(os.path.join(DATA, "libero_plus.csv"), comment="#")
    df = df.sort_values("fp16_omega")            # ascending: camera hardest on left
    axes = df["axis"].str.replace("_", " ")
    x = np.arange(len(df))
    w = 0.26
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ax.bar(x - w, df["fp16_omega"], w, label="pi0.5 FP16", color=C_FP16, zorder=3)
    ax.bar(x, df["w4a4"], w, label="W4A4 (Omega-QVLA)", color=C_Q1, zorder=3)
    ax.bar(x + w, df["w4a8"], w, label="W4A8 (QuantVLA)", color=C_Q2, zorder=3)
    style(ax)
    ax.set_xticks(x)
    ax.set_xticklabels(axes, rotation=20, ha="right")
    ax.set_ylabel("task success rate (%)")
    ax.set_ylim(0, 105)
    ax.set_title("LIBERO-plus: quantized copies of pi0.5 track the FP16 model on every axis",
                 fontsize=12, color=INK, loc="left", pad=12)
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.32))
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig1_libero_plus.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# --- Figure 2: injected-noise dose-response -----------------------------------
def fig_noise():
    df = pd.read_csv(os.path.join(DATA, "noise_dose_response.csv"), comment="#")
    act = pd.concat([df[df.stressor == "none"], df[df.stressor == "action_noise"]])
    pix = pd.concat([df[df.stressor == "none"], df[df.stressor == "pixel_noise"]])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 4.2))
    for ax, sub, xlab, title in [
        (a1, act, "action-noise sigma", "Executed-action noise"),
        (a2, pix, "pixel-noise sigma (uint8)", "Camera-image noise"),
    ]:
        xs = sub["sigma"].astype(str).tolist()
        ax.plot(xs, sub["fp16"], "-o", color=C_FP16, lw=2, ms=7, label="pi0.5 FP16", zorder=3)
        ax.plot(xs, sub["w4a8"], "-s", color=C_Q2, lw=2, ms=7, label="W4A8 (QuantVLA)", zorder=3)
        style(ax)
        ax.set_xlabel(xlab)
        ax.set_ylim(60, 103)
        ax.set_title(title, fontsize=11, color=INK, loc="left")
    a1.set_ylabel("task success rate (%)")
    a1.legend(frameon=False, loc="lower left")
    fig.suptitle("Injected-noise dose-response: the two curves overlap through the full drop to ~70%",
                 fontsize=12, color=INK, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(os.path.join(FIGS, "fig2_noise_dose_response.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# --- Figure 3: parity plot across every matched cell --------------------------
def fig_parity():
    rows = []
    lp = pd.read_csv(os.path.join(DATA, "libero_plus.csv"), comment="#")
    for _, r in lp.iterrows():
        rows.append(("LIBERO-plus", r["fp16_omega"], r["w4a4"]))
        rows.append(("LIBERO-plus", r["fp16_quantvla"], r["w4a8"]))
    pro = pd.read_csv(os.path.join(DATA, "libero_pro.csv"), comment="#")
    for _, r in pro.iterrows():
        rows.append(("LIBERO-PRO", r["fp16"], r["w4a8"]))
        rows.append(("LIBERO-PRO", r["fp16"], r["w4a4"]))
    nz = pd.read_csv(os.path.join(DATA, "noise_dose_response.csv"), comment="#")
    for _, r in nz.iterrows():
        rows.append(("injected noise", r["fp16"], r["w4a8"]))
    d = pd.DataFrame(rows, columns=["bench", "fp16", "quant"])
    colors = {"LIBERO-plus": C_FP16, "LIBERO-PRO": C_Q1, "injected noise": C_Q2}
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    ax.plot([0, 100], [0, 100], "--", color=INK2, lw=1.2, zorder=1)
    for b in ["LIBERO-plus", "LIBERO-PRO", "injected noise"]:
        s = d[d.bench == b]
        ax.scatter(s["fp16"], s["quant"], s=70, color=colors[b], alpha=0.85,
                   edgecolor=SURFACE, linewidth=1.5, label=b, zorder=3)
    style(ax)
    ax.grid(axis="x", color=GRID, linewidth=1.0)
    ax.set_xlim(-3, 103)
    ax.set_ylim(-3, 103)
    ax.set_xlabel("FP16 success rate (%)")
    ax.set_ylabel("quantized success rate (%)")
    ax.set_aspect("equal")
    ax.set_title("Every matched cell sits on the parity line\n(quantized = FP16 within episode noise)",
                 fontsize=12, color=INK, loc="left", pad=10)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig3_parity.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# --- Figure 4: BitVLA robustness profile (secondary observation) --------------
def fig_bitvla():
    df = pd.read_csv(os.path.join(DATA, "bitvla_native_lowbit.csv"), comment="#")
    df = df[df["axis"] != "clean"]
    axes = df["axis"]
    x = np.arange(len(df))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.bar(x - w / 2, df["bitvla_drop"], w, label="BitVLA (native ternary)", color=C_Q1, zorder=3)
    ax.bar(x + w / 2, df["pi05_drop"], w, label="pi0.5 FP16", color=C_FP16, zorder=3)
    ax.axhline(0, color=INK2, lw=1.0)
    style(ax)
    ax.set_xticks(x)
    ax.set_xticklabels(axes)
    ax.set_ylabel("change vs. own clean anchor (pp)")
    ax.set_title("BitVLA has a different shape, not a uniformly worse one\n(more robust to camera, less to language / lighting)",
                 fontsize=11.5, color=INK, loc="left", pad=10)
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig4_bitvla_profile.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_libero_plus()
    fig_noise()
    fig_parity()
    fig_bitvla()
    print("wrote figures to", os.path.abspath(FIGS))
