# Paper Mastery

Use this workflow when a paper is not just a source to summarize, but something Roshan wants to master.

## Folder Model

- Raw paper stubs: `raw/papers/YYYY/YYYY-MM-DD-<slug>.md`
- Legacy migration records: `raw/legacy-obsidian/papers/`
- Source pages with evidence anchors: `wiki/sources/<slug>.md`
- Active study notes: `wiki/studies/papers/<slug>.md`
- Private Anki decks: `wiki/studies/anki/<slug>.md`
- Derivation drills: `wiki/studies/derivations/<concept>.md`
- Implementation specs: `wiki/studies/implementations/<task>.md`
- Toy code: `experiments/papers/<study-slug>/<task-slug>/`

## Start a Paper

```bash
./bin/llm-wiki paper start <url-or-arxiv-id> --slug <slug>
```

This creates deterministic scaffolding only. It does not fetch or summarize full text.

## Import a Legacy Paper Note

```bash
./bin/llm-wiki paper import-obsidian /path/to/old-note.md --slug <slug> --copy-raw
```

Use `--dry-run` to confirm idempotency.

## Study Loop

1. Add user-authored notes under `## Reading Log` and `## My Notes`.
2. Keep the mastery tracker concept-centric: each row should point at `[[concepts/...]]`.
3. Run `./bin/llm-wiki quiz <slug> --n 5`.
4. Generate cards with `./bin/llm-wiki anki <slug>`, then fill them from My Notes and concept definitions only.
5. Create tiny implementation drills with `./bin/llm-wiki impl <slug> "<task>"`.
6. Promote only after citations are exact and the study is useful beyond private learning.

## Anti-Fabrication Rules

- Do not write `### ex-...` source anchors unless exact source text was checked.
- Do not copy raw paper text into Anki cards.
- Do not create every linked concept page automatically. Run `./bin/llm-wiki concept candidates <slug>` and create only confirmed, reusable concepts.

## Transformer Circuits Migration Check

The first migrated paper is:

- `wiki/studies/papers/transformer-circuits-framework.md`
- `raw/legacy-obsidian/papers/2026-04-28-a-mathematical-framework-for-transformer-circuits.md`

Ten source-backed concept pages now exist for the Transformer Circuits pilot; new papers should use `concept candidates` and create only user-confirmed reusable concepts.
