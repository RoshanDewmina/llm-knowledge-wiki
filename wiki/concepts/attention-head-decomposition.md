---
title: Attention Head Decomposition
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/residual-stream
  - concepts/qk-circuit
  - concepts/ov-circuit
  - concepts/path-expansion
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Attention Head Decomposition

## Definition

Attention head decomposition rewrites multi-head attention from efficient concatenate-and-project implementation form into a sum of per-head outputs added to the residual stream.

## Why It Matters

- It justifies analyzing heads independently as additive contributors.
- It clarifies why a head can be treated as an operation that writes into the residual stream.
- It is the algebraic entry point for QK/OV factorization and path expansion.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/residual-stream]]
- [[concepts/qk-circuit]]
- [[concepts/ov-circuit]]
- [[concepts/path-expansion]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Independent additive head formulation: [[sources/transformer-circuits-framework#ex-independent-additive-heads]].
