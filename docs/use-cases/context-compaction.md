# Context Compaction

Use this lane when your vault is getting large and you want agents to read a compact state summary before touching the full note set.

## Put In `raw/`

- repo notes under `raw/repos/`
- clipped notes or source material that change the current state of a project

## Maintain In `wiki/`

- `wiki/projects/` for durable project memory pages
- `wiki/syntheses/context/` for compact context packs that agents should read first

## Best Prompt

```text
Read AGENTS.md or CLAUDE.md and docs/agent-contract.md. Refresh the project memory page and the context pack so an agent can understand the current state of this vault without rereading the whole repo, then run make check.
```

## Checks

```bash
make project-demo
make review-daily
make check
```

## Done Looks Like

- there is a current project memory page in `wiki/projects/`
- there is a compact context page in `wiki/syntheses/context/`
- an agent can read those pages first and avoid loading the full vault blindly
