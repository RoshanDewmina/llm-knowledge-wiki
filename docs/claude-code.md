# Claude Code Guide

This guide explains how to use the repository well in Claude Code.

If you are brand new, read [getting-started.md](getting-started.md) first.

## What Claude Code Is For Here

Use Claude Code for:

- answering questions from the compiled wiki
- updating multiple wiki files coherently
- saving durable syntheses and outputs back into the repo
- running repo health checks after meaningful changes

Use Obsidian for browsing and clipping.

Use the web frontend for read-only browsing and search in the browser.

## Start Claude In The Repo Root

Open Claude Code in the repo root so the project memory, skills, rules, subagents, and output styles all load.

## First Claude Commands

Start with these:

1. `/memory`
2. optionally `/output-style "Local Wiki Operator"`
3. `/daily-review`

Then pick the right lane:

- research: `/research-assistant your task`
- thinking partner: `/thinking-partner your task`
- codebase memory: `/codebase-memory your task`
- durable output: `/durable-output your task`
- generic ingest/query/lint/output: `/wiki-ingest`, `/wiki-query`, `/wiki-lint`, `/wiki-output`

## Project Features Already Included

### Shared Project Memory

[../CLAUDE.md](../CLAUDE.md) is the project memory file for Claude Code.

It imports [../AGENTS.md](../AGENTS.md) so Claude and Codex stay aligned.

### Slash-Invocable Skills

The repo ships project skills under [../.claude/skills/](../.claude/skills/).

Main skills:

- `/wiki-ingest`
- `/wiki-query`
- `/wiki-lint`
- `/wiki-output`
- `/obsidian-workflow`
- `/research-assistant`
- `/thinking-partner`
- `/codebase-memory`
- `/durable-output`
- `/daily-review`

### Project Subagents

The repo also includes project subagents under [../.claude/agents/](../.claude/agents/):

- `wiki-researcher`
- `wiki-auditor`

Use them for read-only mapping and audit work before making edits.

### Optional Output Style

The repo includes [../.claude/output-styles/local-wiki-operator.md](../.claude/output-styles/local-wiki-operator.md).

Use it when you want:

- shorter responses
- file-first behavior
- stronger citation discipline

## Best Daily Claude Workflows

### Research

```text
/research-assistant ingest this paper, add exact evidence anchors, extend the research synthesis, and run make check
```

### Thinking Partner

```text
/thinking-partner help me think through this topic in the vault first, then promote any stable insight into a synthesis or output
```

### Codebase Memory

```text
/codebase-memory ingest this repo note, refresh the project memory page, update the codebase synthesis if needed, and run make check
```

### Durable Output

```text
/durable-output turn this into a brief or table in wiki/outputs/ with exact citations and run make check
```

### Generic Query

```text
/wiki-query what does this vault already say about transformer interpretation
```

## Personal Local Preferences

Keep per-machine settings in `.claude/settings.local.json`.

Use shared files for shared repo behavior:

- `CLAUDE.md`
- `.claude/rules/`
- `.claude/skills/`

Use local-only memory for:

- your personal habits
- repeated local reminders
- one-machine preferences that should not become team rules

## The Most Useful Claude Prompt

If you only remember one prompt, use this:

```text
Read CLAUDE.md and docs/agent-contract.md. Work only from the repo state. Keep raw/ immutable, extend existing wiki pages before creating duplicates, write durable answers back into wiki/, include exact citations where available, and run make check before finishing meaningful wiki edits.
```
