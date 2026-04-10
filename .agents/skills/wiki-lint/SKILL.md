---
name: wiki-lint
description: Use when wiki pages changed or when the vault should be checked for broken links, stale pages, duplicate pages, missing frontmatter, or other graph-health issues.
metadata:
  short-description: Run vault health checks
---

# wiki-lint

Use this skill when:

- you have changed wiki pages
- you want to audit graph health
- you need to check for stale, duplicate, or malformed pages

Run:

- `make check`
- `python3 tools/check_wiki.py`

`check_wiki.py` also regenerates `wiki/reviews/review-queue.md`, `wiki/reviews/coverage-dashboard.md`, refreshes `wiki/.cache/site-manifest.json`, and runs exact citation linting.

If it reports failures, drill into the individual tools to fix them.
