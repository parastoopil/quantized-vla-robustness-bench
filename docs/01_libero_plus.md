# LIBERO-plus — appearance & physical nuisance shift

**Model:** pi0.5, LIBERO-spatial suite. **Data:** [`../data/libero_plus.csv`](../data/libero_plus.csv),
per-seed detail in [`../data/libero_plus_per_seed.csv`](../data/libero_plus_per_seed.csv).

LIBERO-plus perturbs the *appearance and physics* of a scene along seven axes. We
pool **all** perturbation variants of each axis (full-axis), rather than
conditioning on the benchmark's `difficulty_level` — see
[methodology](methodology.md) for why that field is not a perturbation magnitude.

Omega-QVLA W4A4 was run on seeds 0–2 (means below); QuantVLA W4A8 on seed 0.

| axis | FP16 | W4A4 | Δ (W4A4) | FP16 | W4A8 | Δ (W4A8) |
|---|---:|---:|---:|---:|---:|---:|
| camera (viewpoint) | 73.5 | 73.9 | −0.4 | 74.2 | 71.3 | +2.9 |
| sensor noise | 91.5 | 88.3 | +3.1 | 92.6 | 89.2 | +3.4 |
| robot initial state | 85.0 | 84.8 | +0.3 | 87.4 | 86.3 | +1.1 |
| object layout | 98.5 | 97.8 | +0.7 | 98.2 | 97.1 | +1.0 |
| language (paraphrase) | 95.6 | 96.2 | −0.6 | 95.4 | 96.7 | −1.3 |
| lighting | 98.6 | 99.3 | −0.7 | 99.3 | 99.3 | 0.0 |
| background texture | 99.6 | 99.1 | +0.5 | 99.6 | 99.2 | +0.4 |
| **mean Δ** | | | **+0.41** | | | **+0.9** |

![LIBERO-plus](../figures/fig1_libero_plus.png)

## Reading the table

- **Camera is the informative axis.** It is the only one where the FP16 model is
  well below ceiling (~74%), so it is the only axis with real room for the two
  copies to separate. Across three seeds the W4A4 − FP16 difference there reads
  +0.5 / −1.9 / +0.0 — scatter around zero.
- **The other six axes are near-ceiling for FP16 (85–99.6%).** These are
  informative in one direction: a quantized *collapse* would still be visible,
  and none appears. A separate, small graded difference could hide under the
  ceiling; success rate is binary and saturates.
- **Across all 21 Omega axis-seed cells:** mean +0.41pp, sd 1.62pp, range
  [−1.9, +5.7]. Six of seven axes flip sign across seeds.
- **Sensor noise is the one cell that looked non-zero on seed 0** (+5.7pp, its
  CI the only one to exclude zero). On the two independent replications it moved
  +5.7 → +2.6 → +1.1 — a monotone decay back toward zero. With seven axes at a
  5% threshold, ~1 cell excluding zero by chance is expected; this was that cell.

## A note on the near-ceiling axes

That five of seven axes leave pi0.5 at 95–99.6% is itself a fact about the
benchmark: **LIBERO-plus nuisance perturbations barely move pi0.5**, camera
viewpoint (and mildly robot-initial / sensor-noise) aside. So the comparison has
the most to say on the camera axis and least on the saturated ones.

## Confidence intervals

The per-seed CSV carries episode-level 95% Wilson intervals on each difference. These
are **anti-conservative**: LIBERO-plus episodes cluster by ~10 base tasks per
axis, so the effective sample size is nearer 10 than ~376. Cluster-adjusted
intervals are wider than the ones tabulated — do not quote the raw intervals
without that caveat.
