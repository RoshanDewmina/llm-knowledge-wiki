# CLI Guide

The easiest terminal entry point for this repo is:

```bash
./bin/llm-wiki
```

Use it when you want one obvious command surface for setup, onboarding, health checks, and the most common day-to-day actions.

## Best First Command

```bash
./bin/llm-wiki onboard
```

This is the recommended first-run path.

It follows the same general pattern used by onboarding-oriented CLIs like OpenClaw:

- detect whether the machine already satisfies the requirements
- run setup only when needed
- run a full doctor pass
- leave you with the next commands to use

## Core Commands

```bash
./bin/llm-wiki onboard
./bin/llm-wiki setup
./bin/llm-wiki doctor
./bin/llm-wiki health
./bin/llm-wiki status
./bin/llm-wiki review
./bin/llm-wiki paper start <url-or-id>
./bin/llm-wiki paper import-obsidian <old-path> --copy-raw
./bin/llm-wiki quiz [slug] --n 5
./bin/llm-wiki anki <slug>
./bin/llm-wiki impl <slug> "Implement a tiny check"
./bin/llm-wiki concept candidates [slug]
./bin/llm-wiki query "transformer"
./bin/llm-wiki ingest raw/articles/2026/your-file.md
./bin/llm-wiki daily
./bin/llm-wiki question "What should this vault explain next?"
./bin/llm-wiki review-daily
./bin/llm-wiki manifest
./bin/llm-wiki export wiki/syntheses/transformer-orientation.md
```

## What Each Command Does

- `onboard`
  - best first-run command
  - runs setup only if the machine still needs it
  - runs doctor afterward
- `setup`
  - native macOS bootstrap using the repo's package manifest
- `doctor`
  - verifies host tools, repo structure, vault checks, and optionally the frontend build
- `health`
  - runs the standard vault health checks
- `status`
  - shows a compact readiness and content summary
- `review`
  - regenerates `wiki/reviews/coverage-dashboard.md`, `wiki/reviews/review-queue.md`, and `wiki/reviews/daily-review.md`
- `query`
  - searches the compiled wiki
- `ingest`
  - scaffolds or refreshes a source page from `raw/`
- `daily`
  - creates today's journal note if missing
- `question`
  - creates a durable question note
- `review-daily`
  - regenerates `wiki/reviews/daily-review.md`
- `manifest`
  - regenerates the frontend site manifest
- `export`
  - writes a Marp-friendly slide file from a synthesis or output page

## Shell Completion

Install shell completion:

```bash
./bin/llm-wiki completion zsh --install
./bin/llm-wiki completion bash --install
./bin/llm-wiki completion fish --install
```

If you only want to inspect the script:

```bash
./bin/llm-wiki completion zsh
```

## Makefile Relationship

`make` still works and is still useful.

Use:

- `./bin/llm-wiki ...` for onboarding and the most common direct actions
- `make ...` only when you want shorter aliases for the same actions or frontend tasks

If you are new, start with the repo CLI first.

## Paper Mastery Commands

- `paper start <url-or-id> [--slug <slug>] [--no-open]`
  - creates a raw paper stub, source page, paper study note, and up to six concept stubs.
- `paper import-obsidian <old-path> [--slug <slug>] [--copy-raw] [--dry-run]`
  - preserves a legacy Obsidian note under `raw/legacy-obsidian/` and scaffolds an equivalent study page.
- `paper status [slug] [--all]`
  - lists paper studies with read status and mastery average.
- `quiz [slug] [--n 5] [--kind recall|confusion|derivation|mixed]`
  - emits active-recall prompts from a paper study.
- `anki <slug> [--n 10] [--style qa|cloze|mixed]`
  - scaffolds `wiki/studies/anki/<slug>.md`; agents fill cards from My Notes and concept definitions.
- `impl <slug> "<task>" [--lang numpy|pytorch]`
  - scaffolds an implementation study plus `experiments/papers/<slug>/<task-slug>/`.
- `promote <slug> [--target brief|table|timeline|slides]`
  - scaffolds a durable output from the study.
- `concept <name> [--source-page sources/<slug>]`
  - scaffolds a user-confirmed concept page.
- `concept candidates [slug]`
  - lists study concept links whose pages do not exist yet.
