# AI Briefing Frozen Evaluator v1

Score one completed briefing run from 0 to 5.

## Criteria

- Relevance: top items are genuinely AI/ML signal, not generic tech noise.
- Freshness: every item has an explicit date within the requested window.
- Provenance: every item has a source name and working link or local evidence.
- Concision: final Telegram output stays under roughly 4096 characters.
- Filing: the full Markdown artifact lands in `wiki/outputs/briefs/`.

## Scoring

- 5: all criteria pass, no manual cleanup needed.
- 4: one minor issue, artifact still usable.
- 3: useful but missing either freshness evidence or correct filing.
- 2: major mismatch in output location, delivery, or source quality.
- 1: mostly unusable but contains at least one valid item.
- 0: no usable briefing was produced.

Do not change this evaluator while testing prompt or workflow changes. Create
`evaluator-v2.md` if the evaluator itself needs to change.
