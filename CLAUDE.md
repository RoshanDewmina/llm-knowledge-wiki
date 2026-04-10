# Claude Code Guide

@AGENTS.md

## Claude-Specific Additions

- Repo CLI commands to prefer:
  - `./bin/llm-wiki onboard`
  - `./bin/llm-wiki doctor`
  - `./bin/llm-wiki health`
  - `./bin/llm-wiki status`
- Run `/memory` if you want to confirm which project instructions and imports are loaded.
- The project skills under `.claude/skills/` are directly invocable as slash skills:
  - `/wiki-ingest [raw-path]`
  - `/wiki-query [question]`
  - `/wiki-lint`
  - `/wiki-output [task]`
  - `/obsidian-workflow [task]`
  - `/research-assistant [task]`
  - `/thinking-partner [task]`
  - `/codebase-memory [task]`
  - `/durable-output [task]`
  - `/daily-review [task]`
- The project includes two custom subagents under `.claude/agents/`:
  - `wiki-researcher` for read-only query and page-mapping work
  - `wiki-auditor` for read-only vault audits, stale-page checks, and citation hygiene
- The project includes an optional output style in `.claude/output-styles/local-wiki-operator.md`.
  - Use `/output-style "Local Wiki Operator"` when you want shorter, file-first, citation-focused behavior while keeping Claude Code's coding instructions.
- For personal project-only preferences, keep local settings in `.claude/settings.local.json`.
- If you want personal instructions without committing them, prefer importing a file from your home directory instead of growing the shared project memory.

## Deeper Reference

- [docs/agent-contract.md](docs/agent-contract.md)
- [docs/claude-code.md](docs/claude-code.md)
