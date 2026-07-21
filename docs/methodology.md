# Methodology

The comparisons in this repository are only as trustworthy as the controls behind
them. This document records the design decisions that make a FP16-vs-quantized
comparison fair, and four evaluation pitfalls that were caught and corrected along
the way. Each decision was adopted in response to a concrete failure.

## Design decisions

**Released quantization packs only; no homemade quantization.** Clean parity is a
precondition. If a quantized model had already lost accuracy on clean data, any
shifted-condition drop would be ordinary quantization failure rather than a
property of behavior under shift. Both packs used (Omega-QVLA W4A4, QuantVLA
W4A8) are near-lossless on clean LIBERO-spatial (≈98% vs. 99% FP16).

**Seeded stochastic sampling.** pi0.5 is a flow-matching policy that *samples*
actions; unseeded, the same model queried twice on the same observation returns
different actions. The flow noise is derived from a hash of the observation,
which (a) makes runs bit-reproducible and (b) *pairs* the FP16 and quantized arms
on common random numbers — wherever they see the same observation they draw the
same noise. Verified: D(FP16, FP16) = 0.0 exactly, cross-process.

**Full-axis pooling on LIBERO-plus.** Its per-task `difficulty_level` is **not** a
perturbation magnitude — it records how many of four reference VLAs solved that
task, and one of those four is pi0, the direct ancestor of pi0.5. Conditioning on
it would select on our own model family's success. We pool all variants of an
axis instead. (Concretely: camera-axis FP16 success reads 55% conditioned on one
stratum versus 73% pooled — a large selection effect.)

**Pre-registered reporting rules.** Report all axes, including null and
near-ceiling ones; treat cells where both arms score ≈0 as uninformative (no
signal can exist there); treat any single-seed effect as a hypothesis until it is
replicated.

**Integrity gates on every quantized run.** Each run is rejected unless the
expected number of layers was actually replaced by quantized modules — 252 for
Omega-QVLA W4A4, 180 for QuantVLA W4A8 — guarding against a silently-inactive
quantizer that would look identical to the FP16 model for the wrong reason.

## Four evaluation pitfalls that were caught

Each of these produced an apparent effect that vanished under a proper control.
They are recorded because the affected practices are common in VLA robustness
evaluation.

1. **Unseeded stochastic policies manufacture apparent divergence.** An open-loop
   probe showed quantized action divergence growing 1.86× under camera shift. A
   null control comparing FP16 *against itself* — differing only in its own
   unseeded sampling noise — amplified 1.87×. The excess attributable to
   quantization was 1.00, i.e. zero. *Before measuring divergence between two
   models, measure a model against itself.*

2. **Benchmark "difficulty" can encode reference-model success.** As above,
   LIBERO-plus difficulty levels record how many reference VLAs (including pi0)
   solved a task; conditioning on them selects on the model family's own success.

3. **Fixed "severity" is not calibrated across axes.** At the same nominal
   difficulty, camera shift halves success while every other axis leaves the
   model at ceiling. Comparing axes at a fixed severity compares incomparable
   difficulties.

4. **Single-seed effects decay under replication.** The one LIBERO-plus cell
   whose CI excluded zero (sensor noise) shrank +5.7 → +2.6 → +1.1pp across three
   seeds — despite having been a principled a-priori prediction. With seven axes
   at a 5% threshold, ~1 false positive is expected.

## Harness integrity

A mundane but data-destroying class of failure deserves mention: over the course
of these runs, results were lost to a websocket keepalive that selectively killed
the slower (quantized) arm, to intermittent network-filesystem denials mid-sweep,
to log formatting that made completed runs unparseable, and to concurrent runs
colliding on identically-named log files. Every quantized number in this
repository is gated on an explicit layer-replacement check and an episode-count
check.

## Statistical scale

- Binomial standard error ≈5pp at n=100 episodes (mid-range success), ≈2pp at
  n=376.
- LIBERO-plus episodes cluster by base task (~10 base tasks per axis), so
  episode-level confidence intervals are **anti-conservative**; the true,
  cluster-adjusted intervals are wider than the episode-level ones tabulated in
  [`../data/libero_plus_per_seed.csv`](../data/libero_plus_per_seed.csv).
- Arms added most recently are seed-0 only. The Omega-QVLA LIBERO-plus sweep
  predates that decision and carries three seeds.
