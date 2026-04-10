---
title: Knowledge Wiki Project Memory
type: project
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.88
related:
  - sources/example-transformer-tooling-notes
  - sources/example-com-residual-stream-notes
  - syntheses/context/knowledge-wiki-context-pack
  - syntheses/codebases/knowledge-wiki-architecture
source_pages:
  - sources/example-transformer-tooling-notes
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Knowledge Wiki Project Memory

## Current State

- The repo is a local-first markdown knowledge system with `raw/` as immutable source material and `wiki/` as the maintained, linked layer.
- The browser frontend is read-only and uses a generated site manifest rather than a separate content store.
- The most important compaction pages for agents are this project memory page, the context pack, and the reviewed source pages.

## Stable Rules

- Treat `raw/` as evidence, not as a writable workspace.
- Prefer extending existing concept, synthesis, and output pages over creating duplicates.
- When a coding agent finishes a useful task, crystallize the result into `wiki/projects/`, `wiki/syntheses/`, or `wiki/outputs/`.

## Open Threads

- Which repo-specific workflows should be promoted from journal/question notes into more permanent syntheses?
- How much setup should remain native-first before optional Docker support becomes worthwhile?
- Which pages should agents read first to minimize context cost without losing important caveats?

## Citations

- [[sources/example-transformer-tooling-notes#ex-raw-immutable]]
- [[sources/example-transformer-tooling-notes#ex-manifest-no-db]]
- [[sources/example-transformer-tooling-notes#ex-project-memory]]
- [[sources/example-com-residual-stream-notes#ex-mechanism-vs-interpretation]]

## Contradictions

- No contradiction is recorded about the core repo boundary between `raw/` and `wiki/`.
- A working tension remains between keeping project memory concise and preserving enough nuance that agents do not over-compress the vault.

## Next Actions

- Refresh [[syntheses/context/knowledge-wiki-context-pack]] whenever the project surface changes materially.
- Promote stable patterns from [[journal/2026-04-10-daily-note]] and [[questions/when-should-a-note-be-promoted]] into reusable wiki pages.
