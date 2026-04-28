---
title: Induction Head
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/head-composition
  - concepts/qk-circuit
  - concepts/ov-circuit
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Induction Head

## Definition

An induction head is an attention head involved in a general in-context continuation algorithm: after seeing a repeated prefix or matching context, it helps copy or predict the token that followed the previous occurrence.

## Why It Matters

- It is the headline two-layer phenomenon in the paper.
- It links mechanistic interpretability to in-context learning.
- It is a later study target after mastering QK/OV, skip-trigrams, and head composition.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/head-composition]]
- [[concepts/qk-circuit]]
- [[concepts/ov-circuit]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Two-layer attention-only transformers can use head composition to create induction heads: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]].
