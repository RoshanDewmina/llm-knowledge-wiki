# MCP Is Optional

This repo is designed to work well without MCP.

The default workflow is:

- add sources as files under `raw/`
- maintain durable knowledge in `wiki/`
- use Obsidian, Claude Code, Codex, and the web frontend directly against the filesystem

## Use Direct File Access First

Direct file access is enough for:

- ingesting sources
- updating source, concept, project, synthesis, and output pages
- answering questions from the compiled wiki
- running lint and review tools
- browsing the vault in Obsidian or the local website

## When MCP Helps Later

MCP becomes interesting when you need:

- active-note awareness inside Obsidian
- richer vault-specific commands
- deeper editor state integration
- a future workflow that cannot be expressed cleanly through plain files

## Do Not Make MCP Mandatory

Keep these as the defaults:

- the repo is the source of truth
- markdown files stay portable
- agents should work with plain file access first

Read [../mcp-plan.md](../mcp-plan.md) for the longer phase-2 note.
