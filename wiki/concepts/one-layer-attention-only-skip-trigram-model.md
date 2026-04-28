---
title: One Layer Attention Only Skip Trigram Model
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/zero-layer-transformer
  - concepts/qk-circuit
  - concepts/ov-circuit
  - concepts/path-expansion
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# One Layer Attention Only Skip Trigram Model

## Definition

A one-layer attention-only transformer can be viewed as combining direct bigram behavior with attention-mediated skip-trigram behavior of the form `A ... B -> C`.

## Why It Matters

- It is the first setting where attention moves information across positions.
- It explains why one-layer models can show primitive in-context learning while still being inspectable from weights.
- It gives concrete examples for testing QK/OV understanding.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/zero-layer-transformer]]
- [[concepts/qk-circuit]]
- [[concepts/ov-circuit]]
- [[concepts/path-expansion]]

## Contradictions

- No contradictions recorded yet.

## Citations

- One-layer attention-only models as bigram plus skip-trigram ensembles: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]].
- Concrete skip-trigram examples and tokenizer caveats: [[sources/transformer-circuits-framework#ex-skip-trigram-examples]].
- QK/OV copying behavior in one-layer models: [[sources/transformer-circuits-framework#ex-copying-ov-summary]].
