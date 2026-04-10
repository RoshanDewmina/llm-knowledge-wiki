---
title: Source Use Case Comparison
type: output
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.85
related:
  - syntheses/research/transformer-research-starter-map
  - syntheses/codebases/knowledge-wiki-architecture
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-transformer-tooling-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Source Use Case Comparison

## Purpose

- This table compares how different source types feed the shared wiki.

## Table

| Source page | Best use case | Main contribution | Caveat |
| --- | --- | --- | --- |
| [[sources/attention-is-all-you-need-excerpt]] | Academic research | Grounds baseline transformer architecture claims. | It is only a small excerpt, not a full literature review. |
| [[sources/example-com-attention-as-interface]] | Interpretability caution | Distinguishes architectural capability from interpretation. | It is a synthetic clipped article, not a benchmark study. |
| [[sources/example-transformer-tooling-notes]] | Codebase memory | Explains why project-memory pages and manifest-backed browsing reduce repeated agent context loading. | It is a repo note, not a runtime benchmark. |

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/example-com-attention-as-interface#ex-capability-vs-interpretation]]
- [[sources/example-transformer-tooling-notes#ex-project-memory]]

## Contradictions

- Different source types serve different layers of the vault, so direct contradiction is limited.
- The main caveat is scope mismatch: a repo note can justify workflow choices, but it cannot replace research evidence.
