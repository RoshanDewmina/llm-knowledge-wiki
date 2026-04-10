# Getting Started

This guide is for someone using the repo for the first time.

You do not need to understand the whole system before you start.

## Get The Repo First

Best option:

```bash
git clone <your-repo-url> llm-knowledge-wiki
cd llm-knowledge-wiki
```

If someone shared a zip instead:

1. unzip it
2. open Terminal
3. `cd` into the unzipped folder

Example:

```bash
cd ~/Downloads/llm-knowledge-wiki
```

## What You Need

- macOS and Homebrew for the first-class setup path
- Python `3.12+`
- Bun
- Obsidian
- optionally Claude Code
- optionally Codex

Linux can be added next. Windows is not the first-class path yet.

## First 10 Minutes

From the repo root:

```bash
./bin/llm-wiki onboard
./bin/llm-wiki health
make site-dev
```

Then:

1. Open Obsidian
2. Choose `Open folder as vault`
3. Select this repo folder
4. Open [../wiki/inbox.md](../wiki/inbox.md)
5. Open [../wiki/index.md](../wiki/index.md)
6. Open [../wiki/reviews/daily-review.md](../wiki/reviews/daily-review.md)
7. Open [http://localhost:3000/](http://localhost:3000/)

If all of that works, the repo is ready.

## The Most Important Idea

Do not mix up `raw/` and `wiki/`.

- `raw/` = the original material
- `wiki/` = the maintained knowledge layer

That one distinction prevents most mistakes.

## Your First Real Workflow

### Option 1: Try The Seeded Demos

Academic research:

```bash
make research-demo
```

Codebase memory:

```bash
make project-demo
```

Thinking partner:

```bash
make daily
make question QUESTION="What should this vault explain next?"
make review-daily
```

### Option 2: Add Your Own First Source

1. Put a markdown file into one of these:

```text
raw/articles/YYYY/YYYY-MM-DD-domain-slug.md
raw/papers/your-paper.md
raw/repos/your-repo-note.md
```

2. Ingest it:

```bash
python3 tools/ingest.py raw/.../your-file.md
```

3. Open the matching page in `wiki/sources/`
4. Add exact evidence anchors under `## Evidence Extracts`
5. Update the most relevant concept, project, synthesis, or output page
6. Run:

```bash
make check
```

## Which Folder To Use

- Academic research
  - `raw/papers/`
  - `wiki/syntheses/research/`
- Context compaction
  - `wiki/projects/`
  - `wiki/syntheses/context/`
- Codebase memory
  - `raw/repos/`
  - `wiki/projects/`
  - `wiki/syntheses/codebases/`
- Thinking partner
  - `wiki/journal/`
  - `wiki/questions/`
- Durable outputs
  - `wiki/outputs/briefs/`
  - `wiki/outputs/tables/`
  - `wiki/outputs/timelines/`
  - `wiki/outputs/slides/`

## How To Use Each Interface

### Obsidian

Use Obsidian for:

- browsing the vault
- backlinks
- graph view
- clipping web pages
- manually reading and editing markdown notes

Read [obsidian.md](obsidian.md) next.

### Claude Code

Use Claude Code for:

- answering questions from the compiled wiki
- producing clean syntheses and outputs
- saving durable work back into the vault

Good first Claude steps:

1. run `/memory`
2. optionally run `/output-style "Local Wiki Operator"`
3. try `/research-assistant`, `/thinking-partner`, or `/codebase-memory`
4. use `/agents` if you want the `wiki-researcher` or `wiki-auditor` subagent

### Codex

Use Codex for:

- ingest-driven multi-file updates
- refreshing concept, project, synthesis, and output pages
- running repo tools and checks

### Web Frontend

Use the website for:

- read-only browsing
- search
- section index pages
- raw-source viewing without editing

## The 5 Commands You Will Use Most

```bash
./bin/llm-wiki doctor
./bin/llm-wiki ingest raw/.../your-file.md
./bin/llm-wiki query "your question"
./bin/llm-wiki health
make site-dev
```

## What To Read Next

- [user-guide.md](user-guide.md)
- [claude-code.md](claude-code.md)
- [obsidian.md](obsidian.md)
- [cli.md](cli.md)
- [use-cases/academic-research.md](use-cases/academic-research.md)
- [agent-contract.md](agent-contract.md)
