# Obsidian Guide

This repo is meant to be opened directly as an Obsidian vault.

Obsidian is the human-facing frontend for:

- browsing the vault
- backlinks
- graph view
- clipping web pages
- template insertion
- manual markdown editing

It is **not** the agent runtime.

Claude Code and Codex operate on the same files, but they do not need Obsidian to run.

## Open The Vault

1. Open Obsidian
2. Choose `Open folder as vault`
3. Select this repo folder
4. Open these files first:
   - [../wiki/inbox.md](../wiki/inbox.md)
   - [../wiki/index.md](../wiki/index.md)
   - [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
   - [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)

## The Most Important Idea

Do not mix up `raw/` and `wiki/`.

- `raw/` is the original source material
- `wiki/` is the maintained knowledge base

## Folder Guide

### `raw/`

Browse `raw/` when you want the original source material.

Common places:

- `raw/articles/YYYY/`
- `raw/papers/`
- `raw/repos/`
- `raw/datasets/`
- `raw/images/`

### `wiki/`

Browse `wiki/` when you want the maintained, linked notes.

Most important folders:

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

### `templates/`

Use `templates/` with Obsidian's Templates core plugin for:

- paper notes
- project memory
- daily notes
- durable question notes
- briefs, tables, and timelines

## The Basic Obsidian Workflow

### 1. Clip Or Add A Source

Put the new source in:

```text
raw/articles/YYYY/YYYY-MM-DD-domain-slug.md
raw/papers/your-paper.md
raw/repos/your-repo-note.md
```

### 2. Ingest It

Run:

```bash
python3 tools/ingest.py raw/.../your-file.md
```

### 3. Open The Source Page

Open the matching page in `wiki/sources/`.

Add:

- verified claims
- contradictions
- related pages
- exact evidence anchors under `## Evidence Extracts`

### 4. Update The Knowledge Pages

Update an existing concept, project, synthesis, or output page if possible.

### 5. Use Journal And Question Pages

For exploratory work:

- create a daily note in `wiki/journal/`
- create a durable question in `wiki/questions/`
- promote stable outcomes into `wiki/syntheses/`, `wiki/projects/`, or `wiki/outputs/`

### 6. Run Checks

Run:

```bash
make check
```

Then inspect:

- [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
- [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)
- [../wiki/reviews/coverage-dashboard.md](../wiki/reviews/coverage-dashboard.md)

## What You Can Edit Manually

Safe to edit manually:

- `wiki/` notes
- `templates/`
- `docs/`
- new raw files you are adding before ingest

Avoid editing manually:

- existing raw clips after capture, except for obvious metadata fixes
- the auto-managed marker blocks in [../wiki/index.md](../wiki/index.md), [../wiki/log.md](../wiki/log.md), and [../wiki/inbox.md](../wiki/inbox.md)

## Web Clipper

Use Obsidian Web Clipper to save articles into `raw/articles/YYYY/`.

Recommended naming format:

```text
YYYY-MM-DD-domain-slug.md
```

Recommended metadata:

- `title`
- `source_url`
- `source_domain`
- `captured_at`

Use the ready-made templates in [obsidian-web-clipper-template.md](obsidian-web-clipper-template.md).

## Keep The Vault Clean

Good habits:

- extend existing notes instead of making duplicates
- save durable answers back into `wiki/`
- run `make check` after meaningful changes
- use `wiki/reviews/daily-review.md` and `wiki/reviews/review-queue.md` to choose the next action

## Recommended Tabs To Keep Open

- [../wiki/inbox.md](../wiki/inbox.md)
- [../wiki/index.md](../wiki/index.md)
- [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
- [../wiki/reviews/review-queue.md](../wiki/reviews/review-queue.md)
- [../wiki/projects/knowledge-wiki-project-memory.md](../wiki/projects/knowledge-wiki-project-memory.md)

## If You Get Stuck

Read:

- [getting-started.md](getting-started.md)
- [user-guide.md](user-guide.md)
- [claude-code.md](claude-code.md)
- [agent-contract.md](agent-contract.md)
