---
paths:
  - "apps/site/**/*"
---

# Site Frontend Rules

- The site is a read-only frontend over repo files, not a separate content system.
- Prefer the generated `wiki/.cache/site-manifest.json` over repeated ad hoc vault crawls.
- Do not add a database, CMS, or remote dependency for core content.
- Preserve the wiki-like reading layout and local-first search flow.
- Validate meaningful site changes with `bun run lint`, `bun run build`, and `bun run test:e2e`.
