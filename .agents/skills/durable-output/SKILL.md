---
name: durable-output
description: Use when an answer, brief, table, timeline, or slide export should become a durable artifact in the vault rather than staying in chat.
metadata:
  short-description: Durable briefs, tables, timelines, and slides
---

# durable-output

Use this skill when:

- a useful chat answer should be saved back into the vault
- the user wants a brief, comparison table, timeline, or slide-ready page
- an existing synthesis should be transformed into a deliverable

Steps:

1. Choose the right output home:
   - `wiki/outputs/briefs/`
   - `wiki/outputs/tables/`
   - `wiki/outputs/timelines/`
   - `wiki/outputs/slides/`
2. Use exact `## Citations` with `[[sources/...#ex-...]]` links.
3. Keep an explicit `## Contradictions` section when relevant.
4. Update `wiki/index.md` and `wiki/log.md` when adding a new durable page.
5. Run `make check`, then `python3 tools/export_marp.py wiki/...` when slides are needed.
