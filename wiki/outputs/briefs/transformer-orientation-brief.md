---
title: Transformer Orientation Brief
type: output
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.88
related:
  - syntheses/transformer-orientation
  - syntheses/research/transformer-research-starter-map
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Transformer Orientation Brief

## Audience

- A newcomer who needs a short, grounded explanation of the current seed corpus.

## Key Takeaways

- Transformers are described here as residual-stream updates performed by self-attention and feed-forward blocks.
- Positional information is necessary because attention alone is permutation-invariant.
- Observed head specialization belongs on the interpretation side of the ledger, not as an architectural guarantee.

## Supporting Evidence

- [[sources/attention-is-all-you-need-excerpt]] provides the baseline architecture.
- [[sources/example-com-residual-stream-notes]] explains the residual stream as a running state with additive updates.
- [[sources/example-com-attention-as-interface]] warns against turning observed specialization into fixed meaning.

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/attention-is-all-you-need-excerpt#ex-positional-information]]
- [[sources/example-com-residual-stream-notes#ex-running-state]]
- [[sources/example-com-residual-stream-notes#ex-additive-updates]]
- [[sources/example-com-attention-as-interface#ex-specialization-not-guaranteed]]

## Contradictions

- The corpus does not contradict the baseline architectural summary.
- The corpus does preserve a tension between mechanism-level description and stronger interpretive claims about component meaning.

## Next Step

- Use this brief as the short public-facing handoff before opening [[syntheses/transformer-orientation]] or the slide export.
