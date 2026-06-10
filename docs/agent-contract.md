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


## Memory Hierarchy

Agents must not save every useful fact into every memory layer. Use the smallest durable surface that fits the job:

1. **Always-on Hermes memory** is for compact behavioral defaults that should affect nearly every session: identity/status, response preferences, machine setup, confirmation policy, and current default persona/addressing. Keep entries short and deduplicated.
2. **Holographic fact store** is for stable structured facts and relationships that may need reasoning later, such as academic status, coursework, career goals, setup relationships, and explicit exclusions. Prefer one atomic fact per relationship with consistent tags.
3. **Obsidian / llm-wiki KB** is for source-backed, browseable, study-worthy, or synthesis-heavy material: papers, concepts, research syntheses, durable profile/context pages, AI briefings worth reviewing, Anki/derivation/implementation artifacts, and exact citations.
4. **Do not persist transient material**: casual Q&A, raw session dumps, one-off debugging chatter, terminal/tool comparisons, and temporary project progress unless Roshan explicitly asks for a durable record.

Promotion rule: if it changes behavior every turn, use always-on memory; if it is a stable relationship, use fact store; if it needs evidence/browsing/synthesis, use the KB; if it is temporary, leave it in chat/session history.

## Durable Write Thresholds

Write to the KB only when at least one condition holds:

- Roshan explicitly asks to save, ingest, or update the KB.
- A source-backed paper/article/research item is being compiled.
- A study artifact is produced: paper notes, Anki, derivation, toy implementation, or writeup.
- A repeated answer/workflow would be painful to rederive.
- A stable profile, career, learning, or research-context fact needs browseable citations.

Do not create KB pages for casual answers, raw previous-session imports, tooling-choice history, or automation noise. Prefer extending an existing context/synthesis page over creating a near-duplicate.

## Lean Vault Policy

- Generated build/test/cache artifacts are not KB content. Keep `apps/**/.build/`, `apps/**/test-results/`, `**/node_modules/`, virtualenvs, and similar caches ignored or excluded from Obsidian.
- Daily journals/reviews are optional workflow outputs, not mandatory memory. If Roshan is not actively using the daily rhythm, freeze or archive old outputs instead of expanding them.
- Context/profile syntheses may be single-source when Roshan himself is the authoritative source; do not treat them like weak literature reviews merely because they cite one source.
- Do not import all session transcripts into the KB. Repair session search/indexing instead, and use raw JSON sessions only as a fallback for targeted recall.

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
- `wiki/studies/` holds private learning scaffolds: paper notes, Anki decks, derivations, and toy implementation specs.

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

Derived pages with `type` in `concept`, `entity`, `benchmark`, `project`, `synthesis`, `output`, `review`, or `study` must also include:

- `source_pages`
- `compiled_at`

Lightweight thinking-partner pages with `type` in `journal` or `question` must include:

- `source_pages`
- `compiled_at`

For `journal` and `question`, `source_pages` may be empty while the note is still exploratory.

Study pages must also include `study_kind`. Valid values are `paper`, `derivation`, `implementation`, and `anki`. Paper studies may link to missing `concepts/...` candidates; run `./bin/llm-wiki concept candidates [slug]` to review them before creating pages.

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
2. Run `./bin/llm-wiki ingest raw/...`.
3. Review the created or refreshed source page.
4. Add `## Evidence Extracts` anchors once exact source support has been verified.
5. Read related wiki pages before updating concepts, projects, or syntheses.
6. Never let ingest fabricate a summary.

### Query

1. Run `./bin/llm-wiki query "..."`.
2. Read the highest-signal hits in `wiki/`.
3. Answer from compiled wiki pages.
4. If the answer is durable, save it into `wiki/syntheses/` or `wiki/outputs/` with exact `## Citations`.

### Thinking Partner

1. Use `wiki/journal/` for daily notes and short working notes.
2. Use `wiki/questions/` for durable open questions.
3. Promote stable rules, repeated answers, or compact context into stronger pages under `wiki/projects/`, `wiki/syntheses/`, or `wiki/outputs/`.

### Maintenance

Run `./bin/llm-wiki health` before concluding a meaningful wiki edit.

That health command regenerates:

- `wiki/reviews/coverage-dashboard.md`
- `wiki/reviews/review-queue.md`
- `wiki/reviews/daily-review.md`
- `wiki/.cache/site-manifest.json`

## Configuration Notes

- [../Brewfile](../Brewfile) and [../scripts/bootstrap-macos.sh](../scripts/bootstrap-macos.sh) are the public native-first setup path.
- [.codex/config.toml](../.codex/config.toml) is a safe project reference for Codex.
- [.claude/settings.json](../.claude/settings.json), [../CLAUDE.md](../CLAUDE.md), [../.claude/skills/](../.claude/skills/), and [../.claude/agents/](../.claude/agents/) define the Claude Code project experience.
- [.obsidian/](../.obsidian/) is intentionally minimal and avoids personal workspace state.

### Study Workflow

1. `./bin/llm-wiki paper start <url-or-id>` creates raw/source/study scaffolds.
2. `./bin/llm-wiki quiz [slug]` emits active-recall prompts from the study.
3. `./bin/llm-wiki anki <slug>` creates an in-vault Spaced Repetition deck under `wiki/studies/anki/`.
4. `./bin/llm-wiki impl <slug> "task"` creates a study spec plus code under `experiments/papers/<slug>/`.
5. `./bin/llm-wiki promote <slug>` scaffolds a durable output; do not mark reviewed/done until citations are exact.
