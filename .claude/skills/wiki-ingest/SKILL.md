---
name: wiki-ingest
description: Use when ingesting a raw source, especially a clipped article under raw/articles/YYYY, and when refreshing the matching wiki source page plus any affected concept or synthesis pages.
argument-hint: [raw-path]
paths:
  - "raw/**/*"
  - "wiki/sources/**/*"
  - "wiki/inbox.md"
  - "wiki/index.md"
  - "wiki/log.md"
metadata:
  short-description: Ingest and refresh source pages
---

# wiki-ingest

Use this skill when:

- a user asks to ingest a new raw source
- a clipped article has appeared in `raw/articles/YYYY/`
- source changes should refresh one or more wiki pages
- a source page needs to be created or refreshed

Steps:

1. Confirm the source already lives under `raw/`, usually `raw/articles/YYYY/`.
2. Run `python3 tools/ingest.py raw/...`.
3. Read the resulting `wiki/sources/` page, add exact `### ex-...` evidence anchors once the source is reviewed, and search for related existing pages before adding content.
4. Refresh affected concept or synthesis pages if the source changes the compiled wiki.
5. Cite exact source anchors from derived pages instead of relying on page-level traceability alone.
6. Never summarize beyond what the source supports, and never edit existing raw files.
