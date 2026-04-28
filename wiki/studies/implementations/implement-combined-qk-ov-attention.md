---
title: Implement Combined QK/OV Attention
type: study
created: 2026-04-28T22:15:53Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.8
related:
  - studies/papers/transformer-circuits-framework
  - sources/transformer-circuits-framework
  - concepts/qk-circuit
  - concepts/ov-circuit
  - concepts/attention-head-decomposition
source_pages:
  - studies/papers/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
study_kind: implementation
read_status: done
rating: null
mastery_avg: 3.0
tags:
  - study
  - implementation
lang: numpy
---

# Implement Combined QK/OV Attention

## Task

Build a minimal NumPy equivalence check showing that the standard single-head attention computation equals the Transformer Circuits rewrite using combined QK and OV matrices.

## Three-Step Plan

1. Build deterministic toy residual-stream inputs and random-but-seeded matrices.
2. Implement the reference path in `numpy`: `Q = X W_Q`, `K = X W_K`, `V = X W_V`, `A = softmax(Q K^T / sqrt(d_head))`, `Y = A V W_O`.
3. Implement the equivalent rewritten path: `W_QK = W_Q W_K^T`, `W_OV = W_V W_O`, `A = softmax(X W_QK X^T / sqrt(d_head))`, `Y = A X W_OV`, then compare outputs.

## Equivalence-Check Checklist

- [x] Shapes match at each intermediate step.
- [x] Outputs match within a stated tolerance.
- [x] A failure case is included by perturbing the combined OV matrix and asserting that outputs diverge.
- [x] Script exits non-zero on failed assertions.

## Experiment Directory

- `experiments/papers/transformer-circuits-framework/implement-combined-qk-ov-attention/`

Run:

```bash
python3 experiments/papers/transformer-circuits-framework/implement-combined-qk-ov-attention/main.py
```

Expected result:

```text
ok: standard attention equals combined QK/OV rewrite
```

## What This Tests

This does not prove interpretability. It verifies the algebraic equivalence behind the useful interpretability rewrite: keys/queries/values are not the only valid conceptual objects; the effective QK and OV products can reproduce the same attention output under the same attention pattern.

## Citations

- QK/OV circuit split and mathematical equivalence: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]].
- Attention as information movement through `A` and `W_O W_V`: [[sources/transformer-circuits-framework#ex-attention-information-movement]].
