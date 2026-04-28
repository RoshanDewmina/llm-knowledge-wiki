---
name: quiz-me
description: Quiz and grade active paper studies
paths:
  - "wiki/studies/papers/**/*"
metadata:
  short-description: Quiz and grade active paper studies
---

# quiz-me

Use when the user says "Quiz me" or wants active recall from a study.

Steps:
1. Run `./bin/llm-wiki quiz [slug] --n 5` unless the user asked for another count/kind.
2. Ask one batch of questions, then grade against the study note and concept pages.
3. Update the mastery tracker only for rows directly tested.
4. Append a dated `## Quiz Log` entry with score, misses, and next prompts.
5. Mark confusions resolved only after a correct answer, not after exposure.
