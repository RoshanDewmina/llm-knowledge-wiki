---
title: Zero Layer Transformer
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/path-expansion
  - concepts/one-layer-attention-only-skip-trigram-model
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Zero Layer Transformer

## Definition

A zero-layer transformer has embeddings and unembedding but no attention or MLP blocks, so its next-token logits can be interpreted as a learned bigram table.

## Why It Matters

- It is the baseline case for path expansion.
- It shows what the model can do without moving information between positions.
- It gives the contrast class for one-layer skip-trigram behavior.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/path-expansion]]
- [[concepts/one-layer-attention-only-skip-trigram-model]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Zero-layer transformers model bigram statistics: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]].
