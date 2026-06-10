# AI Briefing Autoresearch Pack

## Editable Target

- Primary: `~/.hermes/skills/personal/ai-briefing/SKILL.md`
- Scheduler: `~/.hermes/cron/jobs.json`
- Output directory: `wiki/outputs/briefs/`

## Frozen Evaluator

Use `evaluator.md` before changing the target. The evaluator scores one run from
0 to 5 on relevance, freshness, provenance, concision, and correct filing.

## Baseline

The baseline captures the existing daily briefing behavior before changing the
skill path from the legacy Obsidian vault to `llm-knowledge-wiki`.

## Procedure

1. Run the existing briefing once or inspect the latest cron output.
2. Score it with `evaluator.md`.
3. Append the row to `results.tsv`.
4. Patch only the briefing skill or cron metadata.
5. Re-run the evaluator and keep the change only if the score improves.
