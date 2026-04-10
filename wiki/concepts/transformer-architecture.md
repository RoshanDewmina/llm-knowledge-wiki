---
title: Transformer Architecture
type: concept
created: 2026-04-07T21:26:24Z
updated: 2026-04-08T21:18:05Z
status: reviewed
confidence: 0.9
related:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
  - syntheses/transformer-orientation
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-08T21:18:05Z
---

# Transformer Architecture

## Definition

- A transformer replaces recurrence with layers organized around a residual stream, where self-attention and feed-forward blocks write updates and positional information supplies order.

## Evidence

- [[sources/attention-is-all-you-need-excerpt]] states that the architecture swaps recurrence for stacked self-attention and feed-forward blocks.
- [[sources/example-com-residual-stream-notes]] states that the residual stream is a running state that carries information across transformer layers.
- [[sources/example-com-residual-stream-notes]] states that attention and feed-forward blocks write into the residual stream rather than replacing it wholesale.
- [[sources/attention-is-all-you-need-excerpt]] states that positional information must be injected because attention is permutation-invariant.
- [[sources/example-com-attention-as-interface]] frames attention as a reusable interface for connecting distant tokens.

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/attention-is-all-you-need-excerpt#ex-positional-information]]
- [[sources/example-com-residual-stream-notes#ex-running-state]]
- [[sources/example-com-residual-stream-notes#ex-additive-updates]]
- [[sources/example-com-attention-as-interface#ex-distant-tokens]]

## Contradictions

- No source in the current corpus contradicts the basic architectural description.
- [[sources/example-com-attention-as-interface]] and [[sources/example-com-residual-stream-notes]] both caution that interpretive stories about what components mean should not be collapsed into architectural facts.

## Related Pages

- [[syntheses/transformer-orientation]]
- [[sources/attention-is-all-you-need-excerpt]]
- [[sources/example-com-attention-as-interface]]
- [[sources/example-com-residual-stream-notes]]

## Open Questions

- Which properties of multi-head attention are architecture-level guarantees versus empirical tendencies?
- How should introductory transformer explanations describe the residual stream without smuggling in interpretive claims?
