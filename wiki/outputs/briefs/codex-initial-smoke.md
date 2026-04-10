---
title: Transformer Mechanism vs Interpretation
type: output
created: 2026-04-08T14:19:32Z
updated: 2026-04-08T21:18:05Z
status: draft
confidence: 0.9
related:
  - concepts/transformer-architecture
  - syntheses/transformer-orientation
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-08T21:18:05Z
---

# Transformer Mechanism vs Interpretation

## Answer

- This wiki treats transformer mechanism as the architecture-level structure and dataflow supported by [[concepts/transformer-architecture]]: a residual stream carried across layers, with self-attention and feed-forward blocks writing updates into it alongside positional information and multi-head attention.
- It treats interpretation as a stronger human reading of observed behavior, especially claims that particular attention heads have fixed semantic roles.
- In the wiki's framing, mechanism is what the architecture is described as doing, while interpretation is how people explain or label observed specialization or component meaning.

## Support

- [[sources/attention-is-all-you-need-excerpt]] is used for the mechanism-side claims about replacing recurrence with self-attention and feed-forward layers, injecting positional information, and using multi-head attention to model relationships in parallel.
- [[sources/example-com-residual-stream-notes]] is used for the mechanism-side claim that the residual stream is the running state across layers and that transformer sublayers write into it rather than replacing it wholesale.
- [[sources/example-com-attention-as-interface]] is used for the interpretation-side caution that head specialization is often observed but not guaranteed.
- [[syntheses/transformer-orientation]] makes the distinction explicit by saying durable answers should separate mechanism from interpretation.

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/attention-is-all-you-need-excerpt#ex-multi-head-parallelism]]
- [[sources/example-com-residual-stream-notes#ex-running-state]]
- [[sources/example-com-residual-stream-notes#ex-additive-updates]]
- [[sources/example-com-attention-as-interface#ex-specialization-not-guaranteed]]

## Implications

- The wiki does not treat head specialization or component meaning as an architectural guarantee.
- It prefers describing residual-stream dataflow separately from interpretability stories about what individual heads or blocks appear to do.

## Contradictions

- No direct contradiction is recorded about the base transformer mechanism or the existence of a residual stream.
- The wiki does record a tension between architecture-level descriptions of how components update the residual stream and stronger interpretability claims that those components have fixed semantic meanings.
