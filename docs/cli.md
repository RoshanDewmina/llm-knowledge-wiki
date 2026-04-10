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
- `make ...` for task-runner style shortcuts

If you are new, start with the repo CLI first.
