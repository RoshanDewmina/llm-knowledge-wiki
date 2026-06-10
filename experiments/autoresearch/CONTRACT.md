# AutoResearch Contract

This contract defines what Hermes may edit during an AutoResearch run.

## Allowed Editable Targets

- `ai-briefing`: `experiments/autoresearch/ai-briefing/{prompts,filters}/`
- `paper-mastery`: `experiments/autoresearch/paper-mastery/{prompts,rubrics}/`
- `prompt-handoff`: `experiments/autoresearch/prompt-handoff/templates/`
- `retrieval`: `tools/query_index.py`, only the retrieval scoring/weighting section
- `work-quality`: `experiments/autoresearch/work-quality/{rubrics,prompts}/`

## Forbidden During A Run

- `/Users/roshansilva/.hermes/config.yaml`, `.env`, `SOUL.md`, and `memories/`
- Wiki pages outside the selected pack's own folder
- Anything under `wiki/concepts/`, `wiki/sources/`, or `wiki/syntheses/`
- `~/.hermes/cron/jobs.json`
- Shell config, dotfiles, and LaunchAgents
- Claude `bypassPermissions`, Codex sandbox settings, and anything under `~/.gemini/`

## Evaluation

Each pack defines a frozen `evaluator.md` and fixed `evalset.jsonl`.

Every run appends to that pack's `results.tsv` with this header:

```tsv
run_id	created_at	target	evaluator_version	score	status	decision	description	evidence_path
```

The score must improve, or the tradeoff must be explicit in the row's
`description`.

## Decision Rules

- Score improves and no regression: `status=kept`
- Score is the same or worse: `status=reverted`, then restore the previous file from git
- Mixed result: `status=notes-only`, leave for human review

## Rollback

Git is the rollback mechanism. Each candidate run should use one branch:

```text
autoresearch/<pack>/<run_id>
```

Reverted means the candidate branch can be deleted. Kept means the candidate can
be merged to main after approval with a one-line message.

## Human Approval

Human approval is required before:

- Merging any `kept` candidate to main
- Keeping a run that touched more than five files
- Editing forbidden targets

Weekly summaries are posted through the `weekly-autoresearch` cron after the row
has been appended.
