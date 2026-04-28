---
title: OV Circuit
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/qk-circuit
  - concepts/attention-head-decomposition
  - concepts/one-layer-attention-only-skip-trigram-model
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# OV Circuit

## Definition

The OV circuit is the value-output product that determines what residual-stream information is read from the attended source token and how it is written to the destination token.

## Why It Matters

- It separates content transformation from attention routing.
- It can be studied with linear algebra tools such as rank and singular vectors.
- It explains why some one-layer heads act like copying or token-continuation mechanisms.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/qk-circuit]]
- [[concepts/attention-head-decomposition]]
- [[concepts/one-layer-attention-only-skip-trigram-model]]

## Contradictions

- No contradictions recorded yet.

## Citations

- OV as the output-value part of an attention head: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]].
- OV read/write role and low-rank structure: [[sources/transformer-circuits-framework#ex-attention-information-movement]].
- Copying interpretation in one-layer models: [[sources/transformer-circuits-framework#ex-copying-ov-summary]].
