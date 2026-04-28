# Wiki Index

This is the vault landing page for the compiled knowledge graph. Keep human notes above the auto-managed registry so ingest can update source listings safely.

## Start Here

- [[inbox]]
- [[reviews/daily-review]]
- [[reviews/review-queue]]
- [[reviews/coverage-dashboard]]
- [[projects/knowledge-wiki-project-memory]]
- [[syntheses/context/knowledge-wiki-context-pack]]
- [[syntheses/research/transformer-research-starter-map]]
- [[syntheses/transformer-orientation]]
- [[concepts/transformer-architecture]]
- [[studies/papers/transformer-circuits-framework]]

## Active Studies

```dataview
TABLE read_status, mastery_avg, updated
FROM "wiki/studies"
WHERE type = "study" AND read_status != "done"
SORT mastery_avg ASC
```

## Transformer Circuits Pilot

- Source: [[sources/transformer-circuits-framework]]
- Study: [[studies/papers/transformer-circuits-framework]]
- Anki: [[studies/anki/transformer-circuits-framework]]
- Implementation: [[studies/implementations/implement-combined-qk-ov-attention]]
- Concepts: [[concepts/residual-stream]], [[concepts/virtual-weights]], [[concepts/attention-head-decomposition]], [[concepts/qk-circuit]], [[concepts/ov-circuit]], [[concepts/zero-layer-transformer]], [[concepts/one-layer-attention-only-skip-trigram-model]], [[concepts/path-expansion]], [[concepts/head-composition]], [[concepts/induction-head]]

## Active Outputs

- [[outputs/briefs/transformer-orientation-brief]]
- [[outputs/briefs/codex-initial-smoke]]
- [[outputs/briefs/claude-sonnet-smoke]]
- [[outputs/tables/source-use-case-comparison]]
- [[outputs/timelines/knowledge-wiki-evolution]]
- [[outputs/slides/transformer-orientation.slides]]

## Use Case Lanes

- Academic research: [[syntheses/research/transformer-research-starter-map]]
- Context compaction: [[syntheses/context/knowledge-wiki-context-pack]]
- Codebase memory: [[projects/knowledge-wiki-project-memory]]
- Thinking partner: [[journal/2026-04-10-daily-note]] and [[questions/when-should-a-note-be-promoted]]
- Durable outputs: [[outputs/briefs/transformer-orientation-brief]], [[outputs/tables/source-use-case-comparison]], [[outputs/timelines/knowledge-wiki-evolution]]

## Working Rules

- Add or clip new source material under `raw/`.
- Treat `wiki/` as the maintained, linked, agent-written layer.
- Write durable answers back into `wiki/syntheses/` or `wiki/outputs/`.
- Run `python3 tools/check_wiki.py` after meaningful wiki edits.

## Auto-Managed Source Registry

<!-- AUTO-SOURCES:START -->
- [[sources/attention-is-all-you-need-excerpt]] -> `raw/papers/attention-is-all-you-need-excerpt.md`
- [[sources/example-com-attention-as-interface]] -> `raw/articles/2026/2026-04-07-example-com-attention-as-interface.md`
- [[sources/example-com-residual-stream-notes]] -> `raw/articles/2026/2026-04-08-example-com-residual-stream-notes.md`
- [[sources/example-transformer-tooling-notes]] -> `raw/repos/example-transformer-tooling-notes.md`
- [[sources/transformer-circuits-framework]] -> `raw/papers/2021/2021-12-22-transformer-circuits-framework-evidence.md`
<!-- AUTO-SOURCES:END -->
