# Codex Guide

Read [docs/agent-contract.md](docs/agent-contract.md) before making durable changes.

## Core Rules

- The repo root is the Obsidian vault.
- `raw/` is immutable source material. Add new files there, but do not rewrite existing raw files.
- `wiki/` is the agent-maintained compiled knowledge graph.
- Save durable work into files, not chat alone.
- Use direct file access first. MCP is optional later when plain files are insufficient.

## Main Commands

- `./bin/llm-wiki onboard`
- `./bin/llm-wiki doctor`
- `./bin/llm-wiki health`
- `./bin/llm-wiki status`
- `make setup`
- `make doctor`
- `make check`
- `make review`
- `make review-daily`
- `make query QUERY="question terms"`
- `make daily`
- `make question QUESTION="..."`
- `make research-demo`
- `make project-demo`

## Main Folders

- `raw/papers/` and `raw/articles/` for academic research inputs
- `raw/repos/` for codebase-memory inputs
- `wiki/projects/` for project memory
- `wiki/syntheses/research/` for literature-review style syntheses
- `wiki/syntheses/context/` for compact agent-first context packs
- `wiki/syntheses/codebases/` for repo or architecture syntheses
- `wiki/journal/` and `wiki/questions/` for thinking-partner notes
- `wiki/outputs/briefs/`, `wiki/outputs/tables/`, `wiki/outputs/timelines/`, and `wiki/outputs/slides/` for durable outputs

## Workflow

1. New source in `raw/`: ingest it, review the matching `wiki/sources/` page, add `## Evidence Extracts`, then update the relevant concept, project, synthesis, or output pages.
2. User question: query `wiki/`, read the top hits, answer from compiled notes, then save anything durable back into `wiki/`.
3. Daily triage: open `wiki/inbox.md`, `wiki/reviews/daily-review.md`, and `wiki/reviews/review-queue.md` before choosing the next edit.
4. Significant wiki edit: run `make check` before concluding.

## Required Invariants

- Never let tooling summarize raw material in Python.
- Record contradictions explicitly in `## Contradictions`.
- Reviewed source pages should include exact evidence anchors under `## Evidence Extracts` using `### ex-...` headings.
- Concept, synthesis, and output pages should include exact `## Citations` with `[[sources/...#ex-...]]` links.
- Prefer extending existing pages over creating duplicates.
- Set `created`, `updated`, and `compiled_at` from `date -u +%Y-%m-%dT%H:%M:%SZ` when creating or refreshing durable pages.
- When adding durable pages, update `wiki/index.md` and `wiki/log.md`.
