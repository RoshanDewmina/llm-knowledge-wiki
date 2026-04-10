---
title: Transformer Research Starter Map
type: synthesis
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.87
related:
  - concepts/transformer-architecture
  - syntheses/transformer-orientation
  - outputs/briefs/transformer-orientation-brief
source_pages:
  - sources/attention-is-all-you-need-excerpt
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Transformer Research Starter Map

## Scope

- This synthesis maps the current seed corpus into a beginner-friendly literature-review starting point.

## Research Questions

- What architectural claims about transformers are stable across the current source set?
- Where does the corpus shift from architecture into interpretation?
- Which open questions deserve deeper paper collection next?

## Evidence

- [[sources/attention-is-all-you-need-excerpt]] supports the core architectural claims about replacing recurrence, adding positional information, and using multi-head attention.
- [[sources/example-com-attention-as-interface]] adds a caution that observed head specialization should not be treated as a fixed architectural guarantee.
- [[sources/example-com-residual-stream-notes]] grounds the residual stream as the running state across layers and warns against collapsing mechanism into interpretation.

## Citations

- [[sources/attention-is-all-you-need-excerpt#ex-replaces-recurrence]]
- [[sources/attention-is-all-you-need-excerpt#ex-positional-information]]
- [[sources/attention-is-all-you-need-excerpt#ex-multi-head-parallelism]]
- [[sources/example-com-attention-as-interface#ex-capability-vs-interpretation]]
- [[sources/example-com-residual-stream-notes#ex-running-state]]
- [[sources/example-com-residual-stream-notes#ex-mechanism-vs-interpretation]]

## Contradictions

- The current corpus does not contradict the baseline architectural description of transformers.
- The main tension is interpretive: the corpus supports studying specialization and component meaning, but it does not support turning those observations into fixed architectural claims.

## Implications

- A good research workflow should compile papers into exact source anchors first, then update concept and synthesis pages rather than restarting from PDFs every session.
- New research sources should deepen [[concepts/transformer-architecture]] and related syntheses instead of creating duplicate top-level summaries.

## Follow-Up

- Add a second real paper source to compare claims about interpretability versus architecture.
- Expand this map into a literature review once the corpus includes more than one paper excerpt.
