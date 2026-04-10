---
name: codebase-memory
description: Use when turning repo notes, architecture docs, debugging notes, or implementation learnings into project memory and codebase syntheses that reduce repeated agent context loading.
metadata:
  short-description: Codebase and project memory
---

# codebase-memory

Use this skill when:

- a repo note is added under `raw/repos/`
- the user wants a project memory page or architecture synthesis
- the agent should condense the current codebase state before coding

Steps:

1. Ingest repo notes from `raw/repos/` into `wiki/sources/`.
2. Update the relevant page in `wiki/projects/`.
3. Refresh `wiki/syntheses/context/` or `wiki/syntheses/codebases/` if the codebase state changed materially.
4. Favor compact pages that agents can read first before opening more raw notes.
5. Run `make check` after meaningful changes.
