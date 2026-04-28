---
name: anki-generate
description: Generate in-vault spaced-repetition cards
paths:
  - "wiki/studies/anki/**/*"
  - "wiki/studies/papers/**/*"
  - "wiki/concepts/**/*"
metadata:
  short-description: Generate in-vault spaced-repetition cards
---

# anki-generate

Use when the user says "Make Anki cards" for a study.

Rules:
- Write only under `wiki/studies/anki/`.
- Cards must be derived from the study note `## My Notes` and concept `## Definition` sections, never copied from raw paper text.
- Every card must include `<!-- src: [[concepts/...]] -->` or `<!-- src: [[sources/...#ex-...]] -->`.
- Default to Q/A; use cloze for definitions or formulas.
- Cap around one card per 100 words of source notes.
- Run `./bin/llm-wiki health`; fix `lint_study.py` failures.
