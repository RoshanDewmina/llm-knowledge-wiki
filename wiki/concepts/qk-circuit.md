---
title: QK Circuit
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/ov-circuit
  - concepts/attention-head-decomposition
  - concepts/one-layer-attention-only-skip-trigram-model
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# QK Circuit

## Definition

The QK circuit is the query-key product that determines the attention pattern: which source positions a destination position attends to.

## Why It Matters

- It separates routing from content movement.
- It lets you inspect a head by asking where information comes from, before asking what is moved.
- It combines with the OV circuit to explain skip-trigram and copying behavior.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/ov-circuit]]
- [[concepts/attention-head-decomposition]]
- [[concepts/one-layer-attention-only-skip-trigram-model]]

## Contradictions

- No contradictions recorded yet.

## Citations

- QK as the attention-pattern circuit: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]].
- Routing role in copying behavior: [[sources/transformer-circuits-framework#ex-copying-ov-summary]].
