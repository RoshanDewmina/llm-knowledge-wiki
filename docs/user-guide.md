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
python3 tools/ingest.py raw/papers/your-paper.md
make query QUERY="your topic"
make check
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
make review-daily
make query QUERY="project memory"
make check
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
make daily
make question QUESTION="your question"
make review-daily
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
python3 tools/ingest.py raw/repos/your-repo-note.md
make project-demo
make check
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
make export SYNTHESIS=wiki/syntheses/your-note.md
make check
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
Read AGENTS.md and docs/agent-contract.md. Ingest this source, review the related pages, add exact evidence anchors where needed, update the relevant existing wiki pages, avoid duplicates, and run make check.
```

### For Claude Code

```text
Read CLAUDE.md and docs/agent-contract.md. Answer this from the compiled wiki only. If the answer is durable, save it into wiki/outputs/ or wiki/syntheses/, include exact citations, and run make check.
```

### For Thinking Partner Work

```text
Read CLAUDE.md and docs/agent-contract.md. Use the vault as a thinking workspace first. Create or update a daily note or question page, then promote any stable insight into a synthesis, project page, or output if warranted, and run make check.
```

## Common Commands

```bash
make setup
make doctor
make check
make review
make review-daily
make ingest SOURCE=raw/.../your-file.md
make query QUERY="your topic"
make daily
make question QUESTION="your question"
make research-demo
make project-demo
make site-dev
make test
```

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
- do not skip `make check` after meaningful changes
- do not rely on page-level traceability alone when exact source anchors are available

## Troubleshooting

### `make check` fails

Read the named file, fix the issue, and run `make check` again.

### I do not know what to work on next

Open:

- [../wiki/inbox.md](../wiki/inbox.md)
- [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
- [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)
