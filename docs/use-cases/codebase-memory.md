# Codebase Memory

Use this lane when the repo itself is part of what you are studying, building, or maintaining, and you want agents to stop rediscovering the same architectural state every session.

## Put In `raw/`

- `raw/repos/` for architecture notes, debugging transcripts, implementation notes, and repo snapshots

## Maintain In `wiki/`

- `wiki/sources/` for reviewed repo notes
- `wiki/projects/` for the durable current-state page
- `wiki/syntheses/codebases/` for architecture or design syntheses

## Best Prompt

```text
Read AGENTS.md or CLAUDE.md and docs/agent-contract.md. Ingest this repo note, refresh the project memory page, update the codebase synthesis if needed, and run make check.
```

## Checks

```bash
make ingest SOURCE=raw/repos/your-repo-note.md
make project-demo
make check
```

## Done Looks Like

- the raw repo note is preserved in `raw/repos/`
- the source page is reviewed and anchored
- the project memory page captures the current state
- the architecture synthesis explains the codebase without making the agent reread everything
