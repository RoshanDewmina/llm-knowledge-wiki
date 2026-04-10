---
name: thinking-partner
description: Use when working in the vault as a personal thinking workspace, especially through daily notes, durable question pages, and review-driven promotion into longer-lived wiki pages.
argument-hint: [task]
paths:
  - "wiki/journal/**/*"
  - "wiki/questions/**/*"
  - "wiki/reviews/daily-review.md"
  - "templates/daily_note.md"
  - "templates/question.md"
metadata:
  short-description: Journal, question, and promotion workflow
---

# thinking-partner

Use this skill when:

- the user wants to think through a topic inside the vault
- a daily note should be created or continued
- a question should become a durable `wiki/questions/` page
- a journal note should be promoted into a synthesis, project page, or output

Steps:

1. Create or open a note in `wiki/journal/` or `wiki/questions/`.
2. Keep exploratory notes there until a stable rule or answer emerges.
3. Promote reusable outcomes into `wiki/syntheses/`, `wiki/projects/`, or `wiki/outputs/`.
4. Regenerate `wiki/reviews/daily-review.md` when deciding what to do next.
5. Run `make check` after meaningful durable edits.
