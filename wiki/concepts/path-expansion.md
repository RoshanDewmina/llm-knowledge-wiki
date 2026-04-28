---
title: Path Expansion
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/virtual-weights
  - concepts/attention-head-decomposition
  - concepts/head-composition
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Path Expansion

## Definition

Path expansion rewrites a product of layer-level transformations into a sum of end-to-end computational paths, so each path can be inspected as an additive contributor to logits or intermediate activations.

## Why It Matters

- It is the algebraic move that turns transformer computation into circuit-like terms.
- It helps localize which route through components caused an output effect.
- It makes downstream tasks like term importance and head-composition analysis more concrete.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/virtual-weights]]
- [[concepts/attention-head-decomposition]]
- [[concepts/head-composition]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Path expansion turns products into sums of end-to-end paths: [[sources/transformer-circuits-framework#ex-path-expansion]].
- Attention-only models as sums of interpretable paths: [[sources/transformer-circuits-framework#ex-independent-additive-heads]].
