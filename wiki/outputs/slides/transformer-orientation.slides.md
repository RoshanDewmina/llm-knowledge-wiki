---
title: Transformer Orientation
type: output
created: 2026-04-07T21:26:24Z
status: draft
confidence: 0.84
related:
  - concepts/transformer-architecture
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
marp: true
theme: default
paginate: true
updated: 2026-04-10T15:32:29Z
compiled_at: 2026-04-10T15:32:29Z
---

# Transformer Orientation

---

## Scope

- This synthesis orients a new reader to the small seed corpus in this repo.

---

## Thesis

- The current source set supports an architectural summary of transformers as residual-stream updates performed by attention and feed-forward blocks, while also warning against over-reading component behavior as fixed meaning.

---

## Evidence

- [[concepts/transformer-architecture]] summarizes the base architecture.
- [[sources/attention-is-all-you-need-excerpt]] provides the architectural claims about self-attention, feed-forward blocks, positional information, and multi-head attention.
- [[sources/example-com-residual-stream-notes]] adds that the residual stream is the running state carried across layers and that transformer sublayers write into it.
- [[sources/example-com-attention-as-interface]] adds the caution that specialization observations should remain interpretations rather than guarantees.

---

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/attention-is-all-you-need-excerpt#ex-multi-head-parallelism]]
- [[sources/example-com-residual-stream-notes#ex-running-state]]
- [[sources/example-com-residual-stream-notes#ex-mechanism-vs-interpretation]]
- [[sources/example-com-attention-as-interface#ex-specialization-not-guaranteed]]

---

## Contradictions

- The corpus does not contain a direct contradiction on the architecture itself.
- The corpus does contain a tension between architecture-level descriptions of how components update the residual stream and stronger interpretability claims that individual heads or components have fixed semantic roles.

---

## Implications

- Durable answers about transformers should separate residual-stream mechanism from interpretation.
- Future sources should be linked into [[concepts/transformer-architecture]] rather than creating duplicate concept pages.

---

## Follow-Up

- Export this synthesis to slides when a quick presentation artifact is useful.
