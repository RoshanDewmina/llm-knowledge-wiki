---
title: Residual Stream
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/virtual-weights
  - concepts/attention-head-decomposition
  - concepts/qk-circuit
  - concepts/ov-circuit
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Residual Stream

## Definition

The residual stream is the additive state channel in a transformer. Embeddings and earlier layers write vectors into it; later attention heads, MLPs, and the unembedding read from it. The useful interpretability framing is communication, not a single contextual word embedding.

## Why It Matters

- It explains why many components can communicate through linear subspaces.
- It makes path and virtual-weight analysis possible.
- It prevents the common mistake of treating every residual vector dimension as a directly meaningful neuron.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/virtual-weights]]
- [[concepts/attention-head-decomposition]]
- [[concepts/qk-circuit]]
- [[concepts/ov-circuit]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Residual-stream communication-channel framing: [[sources/transformer-circuits-framework#ex-residual-stream-communication]].
- Residual subspaces and path decomposition: [[sources/transformer-circuits-framework#ex-residual-stream-subspaces]].
