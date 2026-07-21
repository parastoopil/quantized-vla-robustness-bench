# LIBERO-PRO — semantic & compositional shift

**Model:** pi0.5, spatial and goal suites, 100 episodes per cell, seed 0.
**Data:** [`../data/libero_pro.csv`](../data/libero_pro.csv).

LIBERO-PRO perturbs task *semantics* rather than appearance. All three arms
(FP16, W4A8, W4A4) were run on identical variants.

| axis (what changes) | suite | FP16 | W4A8 | Δ | W4A4 | Δ |
|---|---|---:|---:|---:|---:|---:|
| swap — object positions exchanged | spatial | 47 | 44 | +3 | 45 | +2 |
| | goal | 32 | 34 | −2 | 32 | 0 |
| env — table/scene asset replaced | spatial | 46 | 45 | +1 | 36 | +10 |
| | goal | 36 | 42 | −6 | 40 | −4 |
| lan — instruction paraphrased | spatial | 95 | 96 | −1 | 96 | −1 |
| | goal | 99 | 97 | +2 | 99 | 0 |
| object — appearance/category swapped | spatial | 95 | 100 | −5 | 98 | −3 |
| | goal | 91 | 85 | +6 | 85 | +6 |
| task — goal rewritten, pixels fixed | spatial | 0 | 0 | 0 | 0 | 0 |
| | goal | 9 | 7 | +2 | 10 | −1 |
| **mean Δ** | | | | **0.0** | | **+0.9** |

## What stands out

The rows worth attention are **base-model behaviors**, and both quantized copies
inherit them unchanged:

- **Object swaps** (`swap`) knock pi0.5 down to ~32–47%. W4A4 and W4A8 land on
  the same range.
- **Goal rewrites with fixed pixels** (`task`) put *all three* arms on the floor
  (0–10%). This reproduces the LIBERO-PRO paper's headline finding — VLAs rely on
  the scene more than on the instruction. It is a property of the base policy;
  quantization neither causes nor removes it. Because both arms sit at the floor,
  the cell carries no comparative information (no signal can exist there).

The Δ values scatter symmetrically around zero with no consistent sign, and ±6pp
is roughly one standard error at n=100. The largest single cell, W4A4 on
spatial-env (+10), is contradicted by W4A8 on the very same cell (+1) — two
quantizers disagreeing on one cell is the shape of noise, and it would need seed
replication before meaning anything.

## Harness validation

Two external checks that the harness is measuring the right thing:

1. **FP16 spatial-env = 46%** reproduces the LIBERO-PRO paper's reported 46 exactly.
2. **The task-axis floor (0–10% for all three arms)** reproduces their headline
   scene-memorization claim.

## Caveat

The clean anchor was measured on the spatial suite only, so goal-suite Δ values
are raw shifted-condition differences without a same-suite clean baseline.
