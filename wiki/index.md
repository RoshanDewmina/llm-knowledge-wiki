# Wiki Index

This is the vault landing page for the compiled knowledge graph. Keep human notes above the auto-managed registry so ingest can update source listings safely.

## Start Here

- [[inbox]]
- [[reviews/daily-review]]
- [[reviews/review-queue]]
- [[reviews/coverage-dashboard]]
- [[projects/knowledge-wiki-project-memory]]
- [[syntheses/context/knowledge-wiki-context-pack]]
- [[syntheses/context/roshan-profile-context]]
- [[syntheses/context/roshan-personal-reference]]
- [[syntheses/context/roshan-personal-fact-index]]
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

## Legacy Course Imports

- COMP1501A hard practice papers: [[studies/courses/comp1501a/01-hard-mcq-papers]]
- COMP1501A hard practice answer key: [[studies/courses/comp1501a/01-hard-mcq-answer-key]]
- COMP1501A final 50 hard questions: [[studies/courses/comp1501a/02-final-50-hard-questions]]
- COMP1501A final 50 hard answer key: [[studies/courses/comp1501a/02-final-50-hard-answer-key]]

## Autoresearch Loop

- Plan: [[journal/2026-05-06-plan]]
- Previous plan: [[journal/2026-05-01-plan]]
- Today's daily review: [[reviews/daily/2026-05-06-review]]
- Latest scored daily review: [[reviews/daily/2026-05-05-review]]
- Previous daily review: [[reviews/daily/2026-05-01-review]]
- Previous daily review: [[reviews/daily/2026-04-29-review]]
- Weekly report: [[benchmarks/autoresearch/2026-W18-work-quality]]
- Experiment packs: `experiments/autoresearch/`

## Transformer Circuits Pilot

- Source: [[sources/transformer-circuits-framework]]
- Study: [[studies/papers/transformer-circuits-framework]]
- Anki: [[studies/anki/transformer-circuits-framework]]
- Implementation: [[studies/implementations/implement-combined-qk-ov-attention]]
- Concepts: [[concepts/residual-stream]], [[concepts/virtual-weights]], [[concepts/attention-head-decomposition]], [[concepts/qk-circuit]], [[concepts/ov-circuit]], [[concepts/zero-layer-transformer]], [[concepts/one-layer-attention-only-skip-trigram-model]], [[concepts/path-expansion]], [[concepts/head-composition]], [[concepts/induction-head]]

## Active Outputs

- [[outputs/briefs/2026-06-11-market-brief-midday]]
- [[outputs/briefs/2026-06-11-market-brief-pre-open]]
- [[outputs/briefs/2026-06-10-market-brief-pre-open]]
- [[outputs/briefs/2026-06-09-market-brief-post-close]]

- [[outputs/briefs/2026-06-08-market-brief-midday]]
- [[outputs/briefs/2026-06-07-market-brief-midday]]
- [[outputs/briefs/2026-06-04-ai-briefing]]
- [[outputs/briefs/2026-05-23-ai-briefing]]
- [[outputs/briefs/2026-05-22-ai-briefing]]
- [[outputs/briefs/2026-05-19-ai-briefing]]
- [[outputs/briefs/2026-05-10-ai-briefing]]
- [[outputs/briefs/2026-05-09-ai-briefing]]
- [[outputs/briefs/2026-05-07-ai-briefing]]
- [[outputs/briefs/2026-05-01-ai-briefing]]
- [[outputs/briefs/2026-04-28-ai]]
- [[outputs/briefs/2026-04-29-ai-briefing]]
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
- Run `./bin/llm-wiki health` after meaningful wiki edits.

## Context Syntheses
- [[syntheses/context/roshan-personal-reference|Roshan Personal Reference]]
- [[syntheses/context/roshan-personal-fact-index|Roshan Personal Fact Index]]
- [[syntheses/context/roshan-personal-travel-document-reference|Roshan Personal Travel and Identity Document Reference]]
- [[syntheses/context/agent-workflow-x-clips-2026-05-06|Agent Workflow X Clips 2026-05-06]]
- [[syntheses/context/roshan-profile-context|Roshan Profile Context]]
- [[syntheses/context/hermes-personal-analyst-patterns|Hermes Personal Analyst Patterns]]

## Auto-Managed Source Registry

<!-- AUTO-SOURCES:START -->
- [[sources/roshan-personal-travel-documents-2026-05-09]] -> `raw/transcripts/2026/2026-05-09-roshan-immigration-documents.md`
- [[sources/0xdepressionn-ai-persona-agency]] -> `raw/articles/2026/2026-05-04-0xdepressionn-ai-persona-agency.md`
- [[sources/0xjeff-hermes-as-ultimate-analyst]] -> `raw/articles/2026/2026-05-04-0xjeff-hermes-as-ultimate-analyst.md`
- [[sources/2026-04-28-a-mathematical-framework-for-transformer-circuits]] -> `raw/legacy-obsidian/papers/2026-04-28-a-mathematical-framework-for-transformer-circuits.md`
- [[sources/arxiv-1706-03762]] -> `raw/papers/2026/2026-05-01-arxiv-1706-03762.md`
- [[sources/attention-is-all-you-need-excerpt]] -> `raw/papers/attention-is-all-you-need-excerpt.md`
- [[sources/comp1501a-legacy-study-artifacts]] -> `raw/legacy-obsidian/courses/comp1501a-legacy-study-artifacts.md`
- [[sources/example-com-attention-as-interface]] -> `raw/articles/2026/2026-04-07-example-com-attention-as-interface.md`
- [[sources/example-com-residual-stream-notes]] -> `raw/articles/2026/2026-04-08-example-com-residual-stream-notes.md`
- [[sources/example-transformer-tooling-notes]] -> `raw/repos/example-transformer-tooling-notes.md`
- [[sources/rasmic-openclaw-agent-harness-video]] -> `raw/articles/2026/2026-05-04-rasmic-openclaw-agent-harness-video.md`
- [[sources/rohit-solo-founder-stack-2026]] -> `raw/articles/2026/2026-04-24-rohit-solo-founder-stack-2026.md`
- [[sources/roshan-profile-2026-05-06]] -> `raw/transcripts/2026/2026-05-06-roshan-profile.md`
- [[sources/shmidt-15-hermes-features]] -> `raw/articles/2026/2026-05-04-shmidt-15-hermes-features.md`
- [[sources/transformer-circuits-framework]] -> `raw/papers/2021/2021-12-22-transformer-circuits-framework-evidence.md`
- [[sources/vmiss-what-i-use-hermes-agent-for]] -> `raw/articles/2026/2026-05-03-vmiss-what-i-use-hermes-agent-for.md`
- [[sources/x-com-launching-a-real-shopify-store-used-to-cost-3-000-claude-just-made-that-0]] -> `raw/articles/2026/2026-05-06-0xdepressionn-shopify-mcp-claude-store.md`
<!-- AUTO-SOURCES:END -->


## Outputs
- [[outputs/briefs/2026-06-08-market-brief-midday|Market Brief 2026-06-08 midday]]
- [[outputs/briefs/2026-06-07-market-brief-midday|Market Brief 2026-06-07 midday]]
- [[outputs/briefs/2026-06-04-ai-briefing|AI Briefing 2026-06-04]]
- [[outputs/briefs/2026-05-23-ai-briefing|AI Briefing 2026-05-23]]
- [[outputs/briefs/2026-05-22-ai-briefing|AI Briefing 2026-05-22]]
- [[outputs/briefs/2026-05-19-ai-briefing|AI Briefing 2026-05-19]]
- [[outputs/briefs/2026-05-10-ai-briefing|AI Briefing 2026-05-10]]
- [[outputs/briefs/2026-05-09-ai-briefing|AI Briefing 2026-05-09]]
- [[outputs/briefs/2026-05-07-ai-briefing|AI Briefing 2026-05-07]]
- [[outputs/briefs/2026-05-06-ai-briefing|AI Briefing 2026-05-06]]
- [[outputs/briefs/2026-06-09-market-brief-post-close|Market Brief 2026-06-09 post-close]]
- [[outputs/briefs/2026-06-10-market-brief-pre-open|Market Brief 2026-06-10 pre-open]]
- [[outputs/briefs/2026-06-11-market-brief-pre-open|Market Brief 2026-06-11 pre-open]]
- [[outputs/briefs/2026-06-11-market-brief-midday|Market Brief 2026-06-11 midday]]
