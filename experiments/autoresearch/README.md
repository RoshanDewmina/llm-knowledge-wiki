# Autoresearch Experiment Packs

This folder holds small personal workflow experiments using the same loop:

1. Read `CONTRACT.md` and stay within the allowed editable targets.
2. Pick one bounded editable target.
3. Freeze an evaluator before changing the target.
4. Run or inspect the fixed `evalset.jsonl`.
5. Record the current baseline in `results.tsv`.
6. Make one small change.
7. Run the evaluator and append a row.
8. Keep the change only when the score improves or the tradeoff is explicit.

Each pack uses plain Markdown plus an append-only TSV ledger. Do not add a database,
dashboard, or new app surface here.

## Packs

- `ai-briefing/` - daily AI/ML briefing relevance and filing.
- `paper-mastery/` - research-paper study depth and retained mastery.
- `prompt-handoff/` - prompts handed to Codex, Claude Code, or Hermes.
- `retrieval/` - wiki query and top-5 hit-rate behavior.
- `work-quality/` - daily planning, evidence review, and shipping quality.

Each pack must include `README.md`, `evaluator.md`, `evalset.jsonl`, `results.tsv`,
an editable target directory (`prompts/`, `filters/`, `rubrics/`, or
`templates/` where applicable), and `runs/` for per-run notes or diff snapshots.

## Ledger Contract

Every `results.tsv` uses this header:

```tsv
run_id	created_at	target	evaluator_version	score	status	decision	description	evidence_path
```

Allowed `status` values are `baseline`, `candidate`, `kept`, `reverted`, and
`notes-only`. Keep rows append-only unless correcting a typo immediately after
creation.
