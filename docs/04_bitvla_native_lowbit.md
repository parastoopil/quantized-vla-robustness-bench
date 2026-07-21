# BitVLA — a natively-trained 1-bit model (secondary observation)

**Model:** BitVLA 3B, LIBERO-spatial, seed 0 (**provisional** — four axes still
pending). **Data:** [`../data/bitvla_native_lowbit.csv`](../data/bitvla_native_lowbit.csv).

This section sits apart from the rest of the repository. BitVLA is **not**
post-training quantized: every LLM weight is trained ternary {−1,0,1} and the
vision encoder is 1.58-bit quantization-aware distilled. It has **no FP16 twin**,
so it cannot be put into a matched comparison the way the PTQ packs can. It is
shown here only to contrast native low-bit training against the post-training
quantization measured elsewhere in this repo.

At ~1.4 GB it is roughly 11× smaller than OpenVLA-OFT.

Because the two models start from different clean scores, the fair cross-model
view is each model's **drop relative to its own clean anchor**:

| axis | BitVLA SR | BitVLA drop | pi0.5-FP16 SR | pi0.5 drop | relative |
|---|---:|---:|---:|---:|---:|
| clean | 95.0 | — | 99.0 | — | — |
| camera (viewpoint) | 83.5 | −11.5 | 74.2 | −24.8 | **+13.3** |
| lighting | 80.5 | −14.5 | 99.3 | +0.3 | **−14.8** |
| language (paraphrase) | 66.2 | −28.8 | 95.4 | −3.6 | **−25.2** |

`relative` = BitVLA drop − pi0.5 drop; positive means BitVLA is *more* robust on
that axis.

![BitVLA profile](../figures/fig4_bitvla_profile.png)

## What it shows

The observation is not "BitVLA is worse" but "**BitVLA has a different
robustness shape**":

- **More** robust to camera viewpoint — it loses 11.5pp where pi0.5 loses 24.8pp.
- **Less** robust to instruction paraphrase (−28.8pp vs. −3.6pp) and to lighting
  (−14.5pp vs. ≈0).

Set against the PTQ results in this repo — where the quantized copies of pi0.5
track the FP16 model across every benchmark — the contrast is the point:
post-training quantization of pi0.5 preserves the base model's robustness shape,
while a natively-trained 1-bit model of a different architecture class has its
own, different shape.

## Caveats

Provisional: seed 0 only, four LIBERO-plus axes (sensor noise, layout, robot
initial, background) and the noise dose–response arms still pending. The three
axes above are the completed ones. Attribution is open — how much of the language
deficit is ternary *training* versus BitVLA being a smaller, OFT-style backbone
that may rely on language differently — and cannot be settled from these numbers
alone.
