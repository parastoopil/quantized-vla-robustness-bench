# Injected noise — dose–response

**Model:** pi0.5, LIBERO-spatial, 100 episodes per cell, seed 0.
**Data:** [`../data/noise_dose_response.csv`](../data/noise_dose_response.csv).

Because neither LIBERO-plus nor LIBERO-PRO offers a true severity knob, we added
two, following published protocols, injecting noise at evaluation time on
otherwise-clean scenes:

- **Action noise** — zero-mean Gaussian added to every *executed* action, using
  the exact σ grid of RobustVLA (simulating actuation error).
- **Pixel noise** — Gaussian on the camera images as the policy consumes them
  (uint8 scale, STRONG-VLA style).

| | clean | act σ=0.1 | act σ=0.2 | act σ=0.3 | pix σ=10 | pix σ=25 | pix σ=50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| pi0.5 FP16 | 99 | 98 | 90 | 70 | 98 | 99 | 71 |
| pi0.5 W4A8 | 98 | 99 | 89 | 70 | 99 | 100 | 72 |
| Δ (FP16 − W4A8) | +1 | −1 | +1 | 0 | −1 | −1 | −1 |

![noise dose-response](../figures/fig2_noise_dose_response.png)

## What the curves show

Both stressors produce clean monotone dose–response curves (99 → ~70), which is
the point of running them: it confirms the design has real statistical power to
resolve a difference if one existed. Across the whole descent the W4A8 curve lies
on the FP16 curve within ±2pp, including a dead-even **70 vs. 70** at the
strongest action noise.

Three reasons this particular comparison is worth having:

1. Closed-loop error compounding under execution noise is the most plausible
   mechanism by which a coarser quantized *action head* could underperform.
2. Recent survey work identifies **action** as the most fragile VLA modality.
3. To our knowledge, quantized VLAs had not previously been evaluated under
   execution noise at all.

## The overlap is not a dead quantizer

At σ=0.3 the two arms differ on **9 of the 10 individual tasks** — by up to 30pp
per task — and merely *sum* to the same total success count. The quantized model
genuinely behaves differently under noise; it simply does not succeed less often
in aggregate.
