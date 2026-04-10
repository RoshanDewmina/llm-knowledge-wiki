# Architecture

This repo is a local-first markdown knowledge system.

## Core Model

- `raw/` is the source-of-truth input layer and should not be rewritten by agents after capture.
- `wiki/` is the writable compiled layer.
- The web frontend reads repo files and a generated site manifest; it is not a separate content system.
- Obsidian is the human-facing frontend for browsing, backlinks, graph view, clipping, and templates.
- Claude Code and Codex are operators over the same repo files.

## Durable Knowledge Rules

- Every durable claim should trace back to at least one source page.
- Where possible, durable claims should cite exact source anchors from `## Evidence Extracts`.
- Backlinks and cross-links are required where appropriate.
- Contradictions should be recorded explicitly rather than silently flattened.
- Good answers should be written back into the wiki as syntheses, project pages, or outputs.

## Main Layers

### Raw Layer

- `raw/articles/`
- `raw/papers/`
- `raw/repos/`
- `raw/datasets/`
- `raw/images/`

The raw layer is for evidence and inputs.

### Compiled Wiki Layer

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

The compiled layer is for durable, linked knowledge and operational pages.

## Why This Structure Exists

It supports the main real-world use cases people are using this pattern for:

- academic research and literature review
- context reduction for large note folders
- Obsidian as a thinking-partner workspace
- codebase and agent memory
- durable outputs such as briefs, tables, timelines, and slides

## Sharing And Setup

The recommended public packaging is:

- GitHub template repository
- native macOS-first bootstrap with Homebrew
- Docker optional only for frontend or CI-like use

This keeps the system easy to clone, portable, and aligned with how Obsidian and local coding agents actually work.
