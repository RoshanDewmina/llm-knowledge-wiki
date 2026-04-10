---
title: Knowledge Wiki Context Pack
type: synthesis
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.86
related:
  - projects/knowledge-wiki-project-memory
  - syntheses/codebases/knowledge-wiki-architecture
  - journal/2026-04-10-daily-note
source_pages:
  - sources/example-transformer-tooling-notes
  - sources/example-com-attention-as-interface
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Knowledge Wiki Context Pack

## Scope

- This page is the compact state summary an agent should read before diving into the rest of the vault.

## Current State

- The repo separates evidence from compiled knowledge: `raw/` is immutable and `wiki/` is the maintained layer.
- The frontend is a file-backed reader over the generated site manifest, not a parallel content system.
- The current corpus emphasizes the same discipline the repo uses operationally: separate stable mechanism from stronger interpretive claims.

## Read First

- [[projects/knowledge-wiki-project-memory]]
- [[concepts/transformer-architecture]]
- [[syntheses/transformer-orientation]]

## Evidence

- [[sources/example-transformer-tooling-notes]] captures the repo's architecture and the reason project memory exists.
- [[sources/example-com-residual-stream-notes]] provides the mechanism-versus-interpretation distinction used as a model for broader wiki behavior.
- [[sources/example-com-attention-as-interface]] reinforces the caution against turning observed behavior into fixed guarantees.

## Citations

- [[sources/example-transformer-tooling-notes#ex-raw-immutable]]
- [[sources/example-transformer-tooling-notes#ex-manifest-no-db]]
- [[sources/example-transformer-tooling-notes#ex-project-memory]]
- [[sources/example-com-residual-stream-notes#ex-mechanism-vs-interpretation]]
- [[sources/example-com-attention-as-interface#ex-capability-vs-interpretation]]

## Contradictions

- The repo wants compressed context for agents, but over-compression can erase nuance and source caveats.
- The context pack should stay short, but it must still preserve the explicit distinction between grounded mechanism and stronger interpretive stories.

## Next Actions

- Refresh this page whenever the repo structure or core workflows change.
- Link any new stable operational rule back into [[projects/knowledge-wiki-project-memory]].
