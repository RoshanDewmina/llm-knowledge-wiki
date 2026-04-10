# Site Frontend

This subproject is the Bun + Next.js reader for the local-first wiki.

- It renders the same `wiki/` and `raw/` files used by Obsidian, Codex, and Claude Code.
- It prefers the generated `wiki/.cache/site-manifest.json` for fast local reads.
- It remains read-only: the repo markdown stays the source of truth.

## Commands

```bash
bun run lint
bun run build
bun run test:e2e
bun run dev
```

Use the repo-root README and agent docs for the full workflow.
