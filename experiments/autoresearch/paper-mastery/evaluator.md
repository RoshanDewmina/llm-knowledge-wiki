# Paper Mastery Frozen Evaluator v1

Score one paper-study session from 0 to 5.

## Criteria

- A source-backed study note exists in `wiki/studies/papers/`.
- The session identifies equations, assumptions, confusions, and prerequisites.
- The user gets active-recall prompts or Anki cards.
- There is at least one derivation, trace, implementation, or writeup task.
- The output is filed in the repo and passes `./bin/llm-wiki health`.

## Scoring

- 5: all criteria pass and the user could resume without context loss.
- 4: strong artifacts with one missing depth element.
- 3: useful notes but weak recall or implementation pressure.
- 2: mostly summary with little mastery scaffolding.
- 1: artifact exists but is not actionable.
- 0: no durable artifact.
