---
title: Head Composition
type: concept
created: 2026-04-28T22:14:32Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.82
related:
  - sources/transformer-circuits-framework
  - concepts/induction-head
  - concepts/path-expansion
  - concepts/virtual-weights
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
---

# Head Composition

## Definition

Head composition is when the output of one attention head changes what another head can read, route to, or write. The Transformer Circuits paper distinguishes richer two-layer behavior from one-layer behavior through these compositions.

## Why It Matters

- It is the main reason two-layer attention-only transformers can implement algorithms more complex than one-layer skip-trigrams.
- It gives a mechanistic route to induction-head behavior.
- It forces analysis to include paths across heads, not only isolated heads.

## How To Recognize It

- Ask what part of the computation this concept isolates.
- Check whether the claim is about routing positions, transforming residual-stream information, or composing paths through layers.
- Use the citations below as the source of truth when reconstructing the math.

## Connections

- [[sources/transformer-circuits-framework]]
- [[concepts/induction-head]]
- [[concepts/path-expansion]]
- [[concepts/virtual-weights]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Two-layer models use attention-head composition and can create induction heads: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]].
- Path terms can be reasoned about independently and additively combined: [[sources/transformer-circuits-framework#ex-path-expansion]].
