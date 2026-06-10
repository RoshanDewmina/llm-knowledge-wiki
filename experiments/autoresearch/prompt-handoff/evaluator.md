# Prompt Handoff Frozen Evaluator v1

Score one agent handoff prompt from 0 to 5.

## Criteria

- States the goal, source-of-truth files, and forbidden actions.
- Gives exact files/paths to inspect first.
- Requires implementation or artifacts, not only advice.
- Requires verification commands and a concise final report.
- Avoids ambiguous scope, stale paths, and hidden assumptions.

## Scoring

- 5: a fresh agent can execute correctly without extra questions.
- 4: one minor ambiguity remains.
- 3: usable but misses verification or source-of-truth guidance.
- 2: requires substantial user clarification.
- 1: mostly motivational or generic.
- 0: not executable.
