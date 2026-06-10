# Prompt Handoff Autoresearch Pack

## Editable Target

- Prompt templates stored in this pack or in repo docs under `docs/`.
- Handoff outputs saved into `wiki/outputs/briefs/` when durable.

## Frozen Evaluator

Use `evaluator.md` to score whether another agent can execute the prompt without
needing hidden context.

## Procedure

1. Pick one real handoff prompt.
2. Run it with a fresh agent or review the response as if it were fresh.
3. Score whether it produced the requested files, verification, and report.
4. Change one instruction in the prompt template.
5. Re-test and append the result.
