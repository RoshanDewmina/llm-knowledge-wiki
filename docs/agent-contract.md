# Agent Contract

This is the canonical operating contract for agents working in this repository.

[AGENTS.md](../AGENTS.md) and [CLAUDE.md](../CLAUDE.md) are concise wrappers over the same rules.

## System Boundaries

- The repo root is the Obsidian vault.
- `raw/` is immutable after a source file is captured or added.
- `wiki/` is the writable compiled knowledge graph.
- Durable work belongs in files, not chat alone.
- Direct filesystem + markdown workflows are the default.
- MCP is optional phase 2.

## Folder Contract

- `raw/articles/` and `raw/papers/` are for research inputs.
- `raw/repos/` is for codebase-memory inputs.
- `wiki/sources/` is the bridge between raw files and the rest of the wiki.
- `wiki/projects/` holds current-state project memory pages.
- `wiki/syntheses/research/` holds literature-review and topic syntheses.
- `wiki/syntheses/context/` holds compact context packs for agents.
- `wiki/syntheses/codebases/` holds architecture and codebase syntheses.
- `wiki/journal/` and `wiki/questions/` hold thinking-partner notes.
- `wiki/outputs/briefs/`, `wiki/outputs/tables/`, `wiki/outputs/timelines/`, and `wiki/outputs/slides/` hold durable outputs.

## Frontmatter Contract

Every durable wiki content page must include:

- `title`
- `type`
- `created`
- `updated`
- `status`
- `confidence`
- `related`

Source pages must also include:

- `source_path`
- `source_kind`
- `compiled_at`
- `source_hash`

Derived pages with `type` in `concept`, `entity`, `benchmark`, `project`, `synthesis`, `output`, or `review` must also include:

- `source_pages`
- `compiled_at`

Lightweight thinking-partner pages with `type` in `journal` or `question` must include:

- `source_pages`
- `compiled_at`

For `journal` and `question`, `source_pages` may be empty while the note is still exploratory.

## Linking Rules

- Prefer wikilinks for internal wiki references.
- Reviewed source pages should add exact evidence anchors under `## Evidence Extracts` using `### ex-...` headings.
- Derived concept, synthesis, and output pages should include `## Citations` with exact source anchors such as `[[sources/example-source#ex-claim]]`.
- Extend an existing page before creating a near-duplicate.
- If a new durable page is created, update `wiki/index.md` and append an entry to `wiki/log.md`.

## Contradictions

- Source, concept, project, synthesis, review, and output pages should include `## Contradictions` where relevant.
- If sources disagree, record the disagreement explicitly.
- If no contradiction is currently recorded, say so directly instead of omitting the section entirely.

## Workflow Contract

### Ingest

1. Confirm the raw file already exists under `raw/`.
2. Run `python3 tools/ingest.py raw/...`.
3. Review the created or refreshed source page.
4. Add `## Evidence Extracts` anchors once exact source support has been verified.
5. Read related wiki pages before updating concepts, projects, or syntheses.
6. Never let ingest fabricate a summary.

### Query

1. Run `python3 tools/query_index.py "..."` or `make query QUERY="..."`.
2. Read the highest-signal hits in `wiki/`.
3. Answer from compiled wiki pages.
4. If the answer is durable, save it into `wiki/syntheses/` or `wiki/outputs/` with exact `## Citations`.

### Thinking Partner

1. Use `wiki/journal/` for daily notes and short working notes.
2. Use `wiki/questions/` for durable open questions.
3. Promote stable rules, repeated answers, or compact context into stronger pages under `wiki/projects/`, `wiki/syntheses/`, or `wiki/outputs/`.

### Maintenance

Run `python3 tools/check_wiki.py` before concluding a meaningful wiki edit.

`check_wiki.py` regenerates:

- `wiki/reviews/coverage-dashboard.md`
- `wiki/reviews/review-queue.md`
- `wiki/reviews/daily-review.md`
- `wiki/.cache/site-manifest.json`

## Configuration Notes

- [../Brewfile](../Brewfile) and [../scripts/bootstrap-macos.sh](../scripts/bootstrap-macos.sh) are the public native-first setup path.
- [.codex/config.toml](../.codex/config.toml) is a safe project reference for Codex.
- [.claude/settings.json](../.claude/settings.json), [../CLAUDE.md](../CLAUDE.md), [../.claude/skills/](../.claude/skills/), and [../.claude/agents/](../.claude/agents/) define the Claude Code project experience.
- [.obsidian/](../.obsidian/) is intentionally minimal and avoids personal workspace state.
