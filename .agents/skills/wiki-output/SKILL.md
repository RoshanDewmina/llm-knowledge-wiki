---
name: wiki-output
description: Use when a chat answer should become a durable wiki artifact, when saving a synthesis or deliverable into wiki/, or when exporting a synthesis/output page to Marp slides.
metadata:
  short-description: Save durable outputs
---

# wiki-output

Use this skill when:

- a chat answer should become a durable wiki artifact
- you need to produce a brief, memo, or slide-ready output
- a synthesis or output page should be exported to Marp

Steps:

1. Prefer extending an existing synthesis or output page.
2. Write durable content under `wiki/syntheses/` or the right output folder:
   - `wiki/outputs/briefs/`
   - `wiki/outputs/tables/`
   - `wiki/outputs/timelines/`
   - `wiki/outputs/slides/`
3. Set `created`, `updated`, and `compiled_at` from `date -u +%Y-%m-%dT%H:%M:%SZ` when creating a page; update `updated` and `compiled_at` when refreshing one.
4. Include exact source anchors under `## Citations`, not just page-level traceability, and keep an explicit `## Contradictions` section.
5. Update `wiki/index.md` and `wiki/log.md`.
6. Run `python3 tools/export_marp.py wiki/...` when slides are needed.
7. Run `python3 tools/check_wiki.py` after meaningful edits.
