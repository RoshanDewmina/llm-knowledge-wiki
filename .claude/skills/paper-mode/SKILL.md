---
name: paper-mode
description: Update active paper study notes from user reading prose
paths:
  - "wiki/studies/papers/**/*"
  - "wiki/concepts/**/*"
metadata:
  short-description: Update active paper study notes from user reading prose
---

# paper-mode

Use when the user says "Paper mode", shares notes from a paper section, or wants the active study updated.

Steps:
1. Identify the active study under `wiki/studies/papers/` (ask only if ambiguous).
2. Append the user's prose as a dated entry under `## Reading Log` and distill only user-authored explanations into `## My Notes`.
3. Update mastery tracker cells conservatively; never mark a row done from vague prose.
4. Resolve checked confusions only when the user's note directly answers them.
5. You may propose new `### ex-...` source anchors in chat, but do not write them without explicit user confirmation and exact source text.
6. Extend existing concept pages before proposing new ones; do not auto-create concept pages.
7. Run `./bin/llm-wiki health` after durable edits.
