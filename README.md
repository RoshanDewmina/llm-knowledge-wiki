# LLM Knowledge Wiki

This repo is a local-first knowledge system built from plain markdown files.

It is designed to work well with:

- Obsidian for browsing, clipping, backlinks, and graph view
- Claude Code for query, synthesis, and durable write-back
- Codex for multi-file maintenance work
- a local Next.js site for read-only browsing in the browser

## What This Repo Is

The repo has one job:

1. collect source material in `raw/`
2. compile it into linked pages in `wiki/`
3. answer questions and produce durable outputs from the compiled wiki

The core rule is:

- `raw/` is the original material
- `wiki/` is the maintained knowledge layer

Do not mix them up.

## Best Way To Share This

The best default is:

- publish this as a **GitHub template repo**
- have people **clone it and run it natively**
- keep Docker **optional** for the web frontend and CI-like validation only

Why:

- Obsidian is a desktop app and should run on the host
- Claude Code and Codex work best directly against the local filesystem
- Docker does not solve the main workflow of clipping, editing, and using desktop agents

If you publish this on GitHub:

1. enable `Template repository` in the repo settings
2. tell users to click `Use this template`
3. or use GitHub CLI:

```bash
gh repo create your-new-vault --template YOUR-ORG/llm-knowledge-wiki --clone
```

## Quick Clone Setup

Use this as the default public onboarding flow:

```bash
git clone <your-template-repo-url> llm-knowledge-wiki
cd llm-knowledge-wiki
./bin/llm-wiki onboard
open -a Obsidian .
```

If you are just sharing this quickly with one person, a `.zip` also works, but Git clone is better for future updates.

If you share a zip, tell them to start with:

- [START-HERE-STUDYING.md](START-HERE-STUDYING.md)
- `START-HERE.command`

Then optionally:

```bash
make site-dev
```

Open [http://localhost:3000/](http://localhost:3000/).

## One-Command Install

Once this repo is on GitHub, a new Mac user can install it with:

```bash
curl -fsSL https://raw.githubusercontent.com/RoshanDewmina/llm-knowledge-wiki/main/install.sh | bash
```

That installer:

- installs Homebrew if needed
- clones the repo into `~/llm-knowledge-wiki`
- runs `./bin/llm-wiki onboard`
- opens the repo in Obsidian

## Native-First Install Surface

The first-class macOS setup is:

- [bin/llm-wiki](bin/llm-wiki)
- [Brewfile](Brewfile)
- [scripts/bootstrap-macos.sh](scripts/bootstrap-macos.sh)
- `./bin/llm-wiki onboard`
- `./bin/llm-wiki doctor`
- `./bin/llm-wiki health`

### Homebrew Commands

The bootstrap script installs:

```bash
brew install python@3.12 git gh ripgrep
brew tap oven-sh/bun
brew install bun
brew install --cask obsidian
brew install --cask claude-code
brew install --cask codex
```

### Manual Fallbacks

- Obsidian: install from [obsidian.md](https://obsidian.md/) if you do not want the Homebrew cask
- Claude Code: the repo docs also point to Anthropic's official install path as an alternative
- Codex: use the Homebrew cask on macOS, or your preferred install path if you already manage it another way

## Start Here

If you are new, read these in order:

1. [docs/getting-started.md](docs/getting-started.md)
2. [docs/user-guide.md](docs/user-guide.md)
3. [docs/obsidian.md](docs/obsidian.md)
4. [docs/claude-code.md](docs/claude-code.md)
5. [docs/cli.md](docs/cli.md)

## Use Case Lanes

This repo now supports these main workflows:

- Academic research and literature review
  - [docs/use-cases/academic-research.md](docs/use-cases/academic-research.md)
- Studying for a test
  - [docs/use-cases/studying-for-a-test.md](docs/use-cases/studying-for-a-test.md)
- Context compaction for large note folders
  - [docs/use-cases/context-compaction.md](docs/use-cases/context-compaction.md)
- Obsidian as a thinking-partner workspace
  - [docs/use-cases/thinking-partner.md](docs/use-cases/thinking-partner.md)
- Codebase and agent memory
  - [docs/use-cases/codebase-memory.md](docs/use-cases/codebase-memory.md)
- Durable outputs from the same wiki
  - [docs/use-cases/durable-outputs.md](docs/use-cases/durable-outputs.md)
- MCP as optional phase 2
  - [docs/use-cases/mcp-optional.md](docs/use-cases/mcp-optional.md)

## Main Folders

```text
raw/articles/YYYY/              Clipped articles
raw/papers/                     Paper excerpts or markdown conversions
raw/repos/                      Repo notes, architecture notes, debugging notes
wiki/sources/                   Reviewed source pages linked to raw files
wiki/concepts/                  Reusable concept pages
wiki/projects/                  Project memory pages
wiki/syntheses/research/        Literature-review and topic syntheses
wiki/syntheses/context/         Compact state summaries for agents
wiki/syntheses/codebases/       Repo and architecture syntheses
wiki/journal/                   Daily notes and working notes
wiki/questions/                 Durable open questions
wiki/outputs/briefs/            Saved answers and briefs
wiki/outputs/tables/            Comparison tables
wiki/outputs/timelines/         Timelines
wiki/outputs/slides/            Slide-ready markdown
wiki/reviews/                   Generated maintenance pages
templates/                      Reusable note templates
tools/                          Local CLI tools
apps/site/                      Bun + Next.js frontend
```

## The Most Common Commands

```bash
./bin/llm-wiki onboard
./bin/llm-wiki doctor
./bin/llm-wiki health
./bin/llm-wiki status
./bin/llm-wiki query "your topic"
./bin/llm-wiki ingest raw/articles/YYYY/your-file.md
./bin/llm-wiki daily
./bin/llm-wiki question "your question"
make help
make setup
make doctor
make check
make review
make review-daily
make ingest SOURCE=raw/articles/YYYY/your-file.md
make query QUERY="your topic"
make daily
make question QUESTION="your question"
make research-demo
make project-demo
make export SYNTHESIS=wiki/syntheses/your-note.md
make site-dev
make test
```

## Daily Workflow

1. Add or clip a source into `raw/`.
2. Ingest it into `wiki/sources/`.
3. Add exact evidence anchors under `## Evidence Extracts`.
4. Update the relevant concept, project, synthesis, or output page.
5. Use `wiki/journal/` and `wiki/questions/` for thinking-partner work before promoting stable ideas.
6. Run `make check`.
7. Browse the result in Obsidian or the local site.

## Claude Code Quick Start

From the repo root:

1. Start Claude Code in this folder
2. Run `/memory`
3. Optionally run `/output-style "Local Wiki Operator"`
4. Use the shared project skills directly:
   - `/wiki-ingest raw/articles/YYYY/your-file.md`
   - `/research-assistant your task`
   - `/thinking-partner your task`
   - `/codebase-memory your task`
   - `/durable-output your task`
   - `/daily-review`

See [docs/claude-code.md](docs/claude-code.md) for the full Claude-specific workflow.

## Docker

Docker is **not** the primary installation path.

Use Docker only later if you want:

- a containerized frontend workflow
- CI-like validation in a reproducible environment
- an optional frontend-only contributor path

The core workflow stays:

- clone the repo
- install host tools
- open the repo as an Obsidian vault
- run Claude Code or Codex directly against the same files

## Validation

The repo is validated locally with:

```bash
./bin/llm-wiki onboard --skip-site-build
./bin/llm-wiki status
./bin/llm-wiki health
make doctor
make check
make test
```

That covers:

- host tool and repo verification
- Python tooling
- generated review pages and site manifest
- frontend lint and build
- Playwright browser tests

## Reference Docs

- [docs/architecture.md](docs/architecture.md)
- [docs/agent-contract.md](docs/agent-contract.md)
- [docs/mcp-plan.md](docs/mcp-plan.md)
