---
title: Virtual Weights
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/residual-stream
  - concepts/path-expansion
  - concepts/head-composition
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Virtual Weights

## Definition

Virtual weights are implicit effective connections between model components obtained by multiplying the output weights of an earlier component with the input weights of a later component through the residual stream.

## Why It Matters

- They turn indirect communication through the residual stream into concrete matrices you can inspect.
- They let you ask whether a downstream component reads the information an upstream component wrote.
- They are a bridge between circuit diagrams and actual parameter products.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/residual-stream]]
- [[concepts/path-expansion]]
- [[concepts/head-composition]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Virtual-weight definition and motivation: [[sources/transformer-circuits-framework#ex-virtual-weights]].
