# Durable Outputs

Use this lane when a useful answer should become a reusable artifact like a brief, table, timeline, or slide-ready page.

## Put In `raw/`

- only if the output depends on new source material that is not already in the vault

## Maintain In `wiki/`

- `wiki/outputs/briefs/`
- `wiki/outputs/tables/`
- `wiki/outputs/timelines/`
- `wiki/outputs/slides/`

## Best Prompt

```text
Read AGENTS.md or CLAUDE.md and docs/agent-contract.md. Turn this into a durable output in the right folder under wiki/outputs/, include exact citations, update wiki/index.md and wiki/log.md if needed, and run make check.
```

## Checks

```bash
make export SYNTHESIS=wiki/syntheses/your-note.md
make check
```

## Done Looks Like

- the output lives in the right output subfolder
- the page has exact citations and contradictions where relevant
- the result is easy to browse in Obsidian and the web frontend
