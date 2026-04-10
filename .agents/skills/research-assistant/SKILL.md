---
name: research-assistant
description: Use when collecting papers or articles for academic research, refreshing reviewed source pages, or extending research syntheses instead of rereading the raw corpus from scratch.
metadata:
  short-description: Research and literature review
---

# research-assistant

Use this skill when:

- a paper or article is added under `raw/papers/` or `raw/articles/`
- a literature-review style synthesis should be updated
- the user wants a research-oriented answer grounded in reviewed source pages

Steps:

1. Ingest the raw source into `wiki/sources/`.
2. Add exact `### ex-...` evidence anchors on the reviewed source page.
3. Extend existing concept pages before creating new ones.
4. Save literature-review style notes in `wiki/syntheses/research/`.
5. Run `make check` after meaningful changes.
