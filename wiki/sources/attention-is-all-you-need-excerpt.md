---
title: Attention Is All You Need Excerpt
type: source
created: 2026-04-07T21:26:24Z
updated: 2026-04-07T21:33:52Z
status: reviewed
confidence: 0.95
related:
  - concepts/transformer-architecture
  - syntheses/transformer-orientation
source_path: raw/papers/attention-is-all-you-need-excerpt.md
source_kind: papers
compiled_at: 2026-04-07T21:33:52Z
source_hash: 3ffb8116161755cbf1cfbc1369267c177cce4f48ecc823b590ddec499a1e0538
---

# Attention Is All You Need Excerpt

## Source Snapshot

- Raw file: `raw/papers/attention-is-all-you-need-excerpt.md`
- Source kind: `papers`

## Extraction Queue

- [ ] Add exact section names if the raw paper excerpt becomes more detailed.
- [ ] Expand this page with architectural caveats if new raw notes are added.

## Verified Claims

- The source states that the architecture replaces recurrence with stacked self-attention and feed-forward blocks.
- The source states that positional information is needed because attention alone is permutation-invariant.
- The source states that multi-head attention allows different relationships to be modeled in parallel.

## Evidence Extracts

### ex-replaces-recurrence

- Evidence: The raw excerpt says the architecture replaces recurrence with stacked self-attention and feed-forward blocks.
- Trace: raw bullet 1 in `raw/papers/attention-is-all-you-need-excerpt.md`
- Use for: high-level transformer architecture descriptions.

### ex-positional-information

- Evidence: The raw excerpt says positional information is injected because attention alone is permutation-invariant.
- Trace: raw bullet 2 in `raw/papers/attention-is-all-you-need-excerpt.md`
- Use for: claims about why positional information is required.

### ex-multi-head-parallelism

- Evidence: The raw excerpt says multi-head attention allows the model to attend to different relationships at different positions.
- Trace: raw bullet 3 in `raw/papers/attention-is-all-you-need-excerpt.md`
- Use for: claims about parallel relation modeling in multi-head attention.

## Contradictions

- No direct contradictions are recorded in this source excerpt.

## Related Pages

- [[concepts/transformer-architecture]]
- [[syntheses/transformer-orientation]]

## Compilation Notes

- This page is a seed summary over a synthetic raw excerpt.
