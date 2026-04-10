# Site Guide

Read [../../CLAUDE.md](../../CLAUDE.md) and [../../docs/agent-contract.md](../../docs/agent-contract.md) first.

## Scope

- This app is a read-only frontend over the repo-level `wiki/` and `raw/` files.
- Prefer the generated `wiki/.cache/site-manifest.json` when reading vault content.
- Do not introduce a separate database, CMS, or content source.

## Commands

- `bun run lint`
- `bun run build`
- `bun run test:e2e`

## Rules

- Preserve the wiki-style article layout and local-first architecture.
- Keep internal navigation aligned with the markdown structure and wikilinks.
- Treat the repo root docs and wiki contract as canonical over app-local assumptions.
