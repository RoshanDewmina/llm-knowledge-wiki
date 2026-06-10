# Work Quality Frozen Evaluator v1

Score one day from 0 to 30, then divide by 6 for the ledger score.

## Dimensions

Each dimension is 0 to 5.

- Depth: uninterrupted hard work or deep study.
- Output: durable artifact produced or meaningfully improved.
- Retention: Anki, derivation, quiz, or teach-back completed.
- Shipping: code/docs/project moved toward a visible deliverable.
- Focus: plan matched actual work; low context switching.
- Goal alignment: work moved an active weekly topic or goal.

## Evidence Rules

Use files, git diffs, `streak` notes, wiki pages, or command output. Do not score
based only on memory.

## Ledger Score

`score = round((depth + output + retention + shipping + focus + goal_alignment) / 6, 2)`
