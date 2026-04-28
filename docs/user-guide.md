# User Guide

This guide explains how to use the repo day to day.

## The Simple Mental Model

The repo turns raw material into useful linked notes.

The lifecycle is:

1. collect something in `raw/`
2. register it in `wiki/sources/`
3. build durable knowledge in `wiki/concepts/`, `wiki/projects/`, `wiki/syntheses/`, and `wiki/outputs/`
4. keep the vault healthy with the review and lint tools

If you want one obvious terminal entry point, start with:

```bash
./bin/llm-wiki onboard
```

Then use [cli.md](cli.md) for the rest of the terminal workflow.

## Daily Workflows

### 1. Academic Research

Use this when adding papers or research articles.

```bash
./bin/llm-wiki ingest raw/papers/your-paper.md
./bin/llm-wiki query "your topic"
./bin/llm-wiki health
```

Maintain:

- `wiki/sources/`
- `wiki/concepts/`
- `wiki/syntheses/research/`

Read [use-cases/academic-research.md](use-cases/academic-research.md).

### 2. Context Compaction

Use this when the vault is getting large and an agent needs a compact starting point.

Maintain:

- `wiki/projects/`
- `wiki/syntheses/context/`

Typical loop:

```bash
./bin/llm-wiki review-daily
./bin/llm-wiki query "project memory"
./bin/llm-wiki health
```

Read [use-cases/context-compaction.md](use-cases/context-compaction.md).

### Study For A Test

Use this when you want to turn class notes, lecture transcripts, readings, and review sheets into a study wiki.

Start here:

```bash
./bin/llm-wiki onboard
./bin/llm-wiki ingest raw/articles/2026/your-class-notes.md
./bin/llm-wiki query "your test topic"
./bin/llm-wiki health
```

Read [use-cases/studying-for-a-test.md](use-cases/studying-for-a-test.md).

### 3. Thinking Partner Workflow

Use this when you are thinking inside the vault before deciding what should become durable.

```bash
./bin/llm-wiki daily
./bin/llm-wiki question "your question"
./bin/llm-wiki review-daily
```

Maintain:

- `wiki/journal/`
- `wiki/questions/`

Promote stable ideas into:

- `wiki/syntheses/`
- `wiki/projects/`
- `wiki/outputs/`

Read [use-cases/thinking-partner.md](use-cases/thinking-partner.md).

### 4. Codebase Memory

Use this when the repo itself is part of the knowledge you want agents to retain.

```bash
./bin/llm-wiki ingest raw/repos/your-repo-note.md
make project-demo
./bin/llm-wiki health
```

Maintain:

- `wiki/projects/`
- `wiki/syntheses/codebases/`

Read [use-cases/codebase-memory.md](use-cases/codebase-memory.md).

### 5. Durable Outputs

Use this when a useful answer should become a reusable artifact.

Output homes:

- `wiki/outputs/briefs/`
- `wiki/outputs/tables/`
- `wiki/outputs/timelines/`
- `wiki/outputs/slides/`

Typical loop:

```bash
./bin/llm-wiki export wiki/syntheses/your-note.md
./bin/llm-wiki health
```

Read [use-cases/durable-outputs.md](use-cases/durable-outputs.md).

## What To Put In Each Folder

### `raw/`

Use `raw/` for:

- clipped articles
- paper excerpts
- repo notes
- datasets
- images

Do:

- add new source files here
- keep useful source metadata in frontmatter when available

Do not:

- ask the model to rewrite existing raw files
- store final syntheses or outputs here

### `wiki/`

Use `wiki/` for the maintained knowledge base.

Important subfolders:

- `wiki/sources/`
- `wiki/concepts/`
- `wiki/projects/`
- `wiki/syntheses/research/`
- `wiki/syntheses/context/`
- `wiki/syntheses/codebases/`
- `wiki/journal/`
- `wiki/questions/`
- `wiki/outputs/`
- `wiki/reviews/`

## Best Prompts

### For Codex

```text
Read AGENTS.md and docs/agent-contract.md. Ingest this source, review the related pages, add exact evidence anchors where needed, update the relevant existing wiki pages, avoid duplicates, and run ./bin/llm-wiki health.
```

### For Claude Code

```text
Read CLAUDE.md and docs/agent-contract.md. Answer this from the compiled wiki only. If the answer is durable, save it into wiki/outputs/ or wiki/syntheses/, include exact citations, and run ./bin/llm-wiki health.
```

### For Thinking Partner Work

```text
Read CLAUDE.md and docs/agent-contract.md. Use the vault as a thinking workspace first. Create or update a daily note or question page, then promote any stable insight into a synthesis, project page, or output if warranted, and run ./bin/llm-wiki health.
```

## Common Commands

```bash
./bin/llm-wiki setup
./bin/llm-wiki doctor
./bin/llm-wiki health
./bin/llm-wiki review
./bin/llm-wiki review-daily
./bin/llm-wiki ingest raw/.../your-file.md
./bin/llm-wiki query "your topic"
./bin/llm-wiki daily
./bin/llm-wiki question "your question"
make research-demo
make project-demo
make site-dev
make test
```

`make` still works for shortcuts, but prefer `./bin/llm-wiki` as the main command surface.

## Common Files To Open

- [../wiki/inbox.md](../wiki/inbox.md)
- [../wiki/index.md](../wiki/index.md)
- [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
- [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)
- [../wiki/projects/knowledge-wiki-project-memory.md](../wiki/projects/knowledge-wiki-project-memory.md)

## What Not To Do

- do not let the model rewrite existing files in `raw/`
- do not create a new concept or synthesis page when an existing one should be extended
- do not keep durable knowledge only in chat
- do not skip `./bin/llm-wiki health` after meaningful changes
- do not rely on page-level traceability alone when exact source anchors are available

## Troubleshooting

### `./bin/llm-wiki health` fails

Read the named file, fix the issue, and run `./bin/llm-wiki health` again.

### I do not know what to work on next

Open:

- [../wiki/inbox.md](../wiki/inbox.md)
- [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
- [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)
