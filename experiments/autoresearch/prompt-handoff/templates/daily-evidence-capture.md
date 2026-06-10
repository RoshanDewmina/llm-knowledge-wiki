# Daily Evidence Capture Handoff Template

Use this when handing a daily plan/review or study-work session to a fresh agent. The goal is to leave enough evidence that the weekly work-quality evaluator can score the day from artifacts, not memory.

## Goal

Create or finish the day's durable evidence loop:

1. morning plan in `wiki/journal/YYYY-MM-DD-plan.md`
2. concrete habit evidence in `streak`
3. evening review in `wiki/reviews/daily/YYYY-MM-DD-review.md`
4. if a score is produced, one ledger row in `experiments/autoresearch/work-quality/results.tsv`

## Source Of Truth Files To Inspect First

- `AGENTS.md`
- `docs/agent-contract.md`
- `wiki/journal/YYYY-MM-DD-plan.md` if it exists
- `wiki/reviews/daily/YYYY-MM-DD-review.md` if it exists
- `experiments/autoresearch/work-quality/evaluator.md`
- `experiments/autoresearch/work-quality/results.tsv`

## Required Live State Checks

Run these before claiming what happened today:

```bash
export HOME=/Users/roshansilva
/Users/roshansilva/bin/streak
/Users/roshansilva/bin/streak week
/Users/roshansilva/bin/streak goals
/Users/roshansilva/bin/streak topic
```

Also inspect the relevant artifacts directly:

```bash
cd /Users/roshansilva/.hermes/knowledge-base
git status --short
find wiki/journal wiki/reviews/daily -type f -mtime -8 | sort
```

## Evidence Standard

For each work-quality dimension, require at least one artifact-backed observation:

- Depth: focused block note, study section, code run, or command output.
- Output: file path, diff, brief, study note, implementation, or visible deliverable.
- Retention: Anki, derivation, quiz, teach-back, worked example, or recall questions.
- Shipping: email/application draft, PR, runnable code, published note, or project artifact.
- Focus: plan-vs-actual comparison from the plan and review.
- Goal alignment: active `streak topic` or `streak goals` moved forward.

If an observation is missing, write `missing evidence` instead of inferring from intention.

## Forbidden Actions

- Do not edit `raw/` files.
- Do not create a second habit database or productivity dashboard.
- Do not mark `streak` habits complete unless the user supplied concrete evidence or an artifact proves it.
- Do not merge AutoResearch branches; human approval is required.
- Do not edit `experiments/autoresearch/*/evaluator.md` during the same candidate run.

## Expected Artifacts

- Updated daily plan or review path.
- A six-dimension score only if evidence exists.
- `## Contradictions` in the review, even when empty.
- A concise final report with changed files, score, pending evidence, and verification command output.

## Verification

Before final response, run:

```bash
cd /Users/roshansilva/.hermes/knowledge-base
./bin/llm-wiki health
```

If health fails, report the failing check and the file path that likely caused it.
