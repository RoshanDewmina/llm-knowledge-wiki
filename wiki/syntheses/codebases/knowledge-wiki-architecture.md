---
title: Knowledge Wiki Architecture
type: synthesis
created: 2026-04-10T12:31:26Z
updated: 2026-04-10T12:31:26Z
status: reviewed
confidence: 0.86
related:
  - projects/knowledge-wiki-project-memory
  - syntheses/context/knowledge-wiki-context-pack
source_pages:
  - sources/example-transformer-tooling-notes
  - sources/example-com-residual-stream-notes
compiled_at: 2026-04-10T12:31:26Z
---

# Knowledge Wiki Architecture

## Scope

- This synthesis explains the repo as a codebase-memory system rather than a generic note folder.

## Thesis

- The system works because it keeps one file-based source of truth, compiles higher-signal wiki pages on top of it, and then points agents at the condensed pages before they touch the full corpus.

## Evidence

- [[sources/example-transformer-tooling-notes]] states that the repo keeps `raw/` immutable, uses a manifest-backed frontend, and relies on project memory to avoid reloading the full vault every session.
- [[sources/example-com-residual-stream-notes]] contributes the repo's favored pattern for explaining systems: describe mechanism first, then flag interpretation separately.

## Citations

- [[sources/example-transformer-tooling-notes#ex-raw-immutable]]
- [[sources/example-transformer-tooling-notes#ex-manifest-no-db]]
- [[sources/example-transformer-tooling-notes#ex-project-memory]]
- [[sources/example-com-residual-stream-notes#ex-mechanism-vs-interpretation]]

## Contradictions

- No contradiction is recorded about the file-based architecture itself.
- There is an active tradeoff between keeping the web frontend lightweight and adding more interactive affordances for browsing large vaults.

## Implications

- Codebase-memory pages should crystallize completed work into `wiki/projects/` and `wiki/syntheses/codebases/`, not leave it buried in chat or raw notes.
- Agents should read the context pack and project memory first to reduce token cost and repeated rediscovery.

## Follow-Up

- Add more repo-oriented raw notes as the codebase evolves so this synthesis stays grounded.
