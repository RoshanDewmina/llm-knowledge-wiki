---
name: wiki-query
description: Use when answering a question from the compiled wiki, locating relevant concept or synthesis pages, or deciding whether a durable answer should be written back into wiki/syntheses or wiki/outputs.
argument-hint: [question]
paths:
  - "wiki/**/*"
  - "wiki/.cache/site-manifest.json"
metadata:
  short-description: Query the compiled wiki
---

# wiki-query

Use this skill when:

- a user asks a question that should be answered from the compiled wiki
- you need to locate relevant pages before writing a synthesis or output

Steps:

1. Run `make query QUERY="..."` or `python3 tools/query_index.py "..."`, adding `--type`, `--section`, `--status`, or `--min-confidence` when useful.
2. Read the top wiki hits directly.
3. Answer from compiled pages, not from raw files alone.
4. If the answer is durable, write it back into `wiki/syntheses/` or `wiki/outputs/` with exact `## Citations`.
5. Update `wiki/index.md` and `wiki/log.md` if you create a new durable page.
6. Prefer syntheses and concepts over slide exports unless the user explicitly wants the presentation output.
