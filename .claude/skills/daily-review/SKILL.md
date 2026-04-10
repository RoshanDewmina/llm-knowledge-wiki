---
name: daily-review
description: Use when the user wants to know what to work on next, which pages are stale, or which journal/questions should be promoted into durable knowledge.
argument-hint: [task]
paths:
  - "wiki/inbox.md"
  - "wiki/reviews/daily-review.md"
  - "wiki/reviews/review-queue.md"
  - "wiki/journal/**/*"
  - "wiki/questions/**/*"
metadata:
  short-description: Daily triage and review
---

# daily-review

Use this skill when:

- the user asks what to work on next
- the vault should be triaged for the day
- stale pages, open questions, and recent journal notes should be summarized

Steps:

1. Run `make review-daily`.
2. Open `wiki/reviews/daily-review.md`, `wiki/reviews/review-queue.md`, and `wiki/inbox.md`.
3. Pick the smallest high-value next action: review a source, answer a durable question, or refresh a stale page.
4. Promote any stable result into `wiki/projects/`, `wiki/syntheses/`, or `wiki/outputs/`.
5. Run `make check` after meaningful edits.
