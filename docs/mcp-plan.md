# MCP Phase 2 Plan

MCP is optional in this repository.

## Why It Is Not Required

- The primary workflow is direct filesystem access over markdown files.
- Obsidian is the human frontend, not the agent runtime.
- Codex and Claude Code can already read, write, query, and lint the vault directly.

## When MCP Would Actually Help

MCP becomes useful when direct file access is not enough, for example:

- reading the active note or current selection from Obsidian
- accessing richer vault-aware context than plain files provide
- triggering Obsidian-specific commands without manual interaction
- exposing structured search or metadata views beyond simple local CLIs

## Useful Future MCP Cases

- active-note context for “update the note I am looking at”
- vault-aware backlink or graph queries
- Obsidian-specific automation helpers
- richer integration with saved searches, bookmarks, or workspace state

## How To Avoid Over-Coupling

- Keep markdown files as the source of truth.
- Keep the local CLIs useful even if no MCP server exists.
- Treat any future MCP integration as an adapter, not the core architecture.
- Avoid storing essential knowledge only in a tool-specific database or runtime.

## Risk To Avoid

The main failure mode is building around one Obsidian integration so tightly that the repo stops being portable to plain Git, Codex, Claude Code, or another markdown tool. This project should stay useful even if Obsidian or MCP is unavailable.

## Optional Future Example

If MCP is added later, document it as an optional enhancement with clear setup steps and clear fallbacks. Do not make it mandatory for ingest, query, synthesis, or lint workflows.
