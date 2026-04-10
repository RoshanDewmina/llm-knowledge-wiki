---
name: obsidian-workflow
description: Use when operating on this repo as an Obsidian vault, especially after clipping a new source into raw/articles/YYYY, refreshing the wiki from vault changes, or running a full vault maintenance pass.
argument-hint: [task]
paths:
  - "raw/**/*"
  - "wiki/**/*"
  - "docs/obsidian.md"
  - "docs/obsidian-web-clipper-template.md"
metadata:
  short-description: Work in the Obsidian vault
---

# obsidian-workflow

Use this skill when:

- a new source was clipped into `raw/articles/YYYY/`
- the vault needs to be refreshed from newly added source material
- a synthesis or output should be written back into the vault
- the vault should be checked for stale pages, missing links, or duplicates

Steps:

1. Treat the repo root as the Obsidian vault.
2. Keep `raw/` immutable except for adding new source files.
3. Ingest new clips with `python3 tools/ingest.py raw/articles/YYYY/...`.
4. Open `wiki/inbox.md` to review recent source activity and next actions.
5. Add exact evidence anchors under `## Evidence Extracts` on reviewed source pages, and cite them from derived pages under `## Citations`.
6. Save durable notes into `wiki/syntheses/` or `wiki/outputs/` with current UTC `created`/`updated`/`compiled_at` values from `date -u +%Y-%m-%dT%H:%M:%SZ`.
7. Run `make check` or `python3 tools/check_wiki.py` before concluding meaningful vault edits, then inspect `wiki/reviews/`.
