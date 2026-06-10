---
title: "Hermes Personal Analyst Patterns"
type: synthesis
created: 2026-05-06T23:10:39Z
updated: 2026-05-06T23:10:39Z
status: draft
confidence: 0.78
related:
  - "[[sources/0xjeff-hermes-as-ultimate-analyst]]"
source_pages:
  - "[[sources/0xjeff-hermes-as-ultimate-analyst]]"
compiled_at: 2026-05-06T23:10:39Z
tags:
  - hermes
  - ai-agents
  - personal-analyst
  - investment-research
  - workflow
---

# Hermes Personal Analyst Patterns

This page collects useful, non-fluffy workflow patterns for using Hermes as a personal analyst. It starts from 0xJeff’s Part IV Hermes article and should be extended with future X articles/posts if they add durable patterns.

## Core Pattern

A useful personal analyst is not just a stronger chat model. It is a loop:

1. **Source monitoring**: track high-signal feeds such as X accounts, bookmarks, macro sources, and dashboards.
2. **Triage/scoring**: rank new material by priority and relevance before spending attention.
3. **Personal context injection**: condition analysis on theses, risk appetite, current positions, preferences, and prior rationales.
4. **Recurring synthesis**: create daily and weekly summaries that explain “why this matters,” not just “what happened.”
5. **Temporal memory**: store insights so later runs can ask what changed across days/weeks/months.
6. **Alerting instead of execution**: use Hermes to notify and stress-test; do not let it trade autonomously.

## Topic Categories

### Interface / UI Layer

- Discord is acceptable for push summaries, but weak for visual work.
- OpenWebUI is useful when the agent needs a ChatGPT/Claude-like interface, visual artifacts, HTML previews, and build/design workflows.
- Hermes Workspace may become the command center if Skills, Tasks, Memory, Soul, and Swarm can be edited/operated from one place.

### Builder vs Operator

- Claude-as-builder + Hermes-as-operator is friendly for visual/low-code workflows.
- The tradeoff is cost. If Claude usage is too expensive, switch more building work to Codex or use Hermes alone as both builder and operator.
- Treat model/tool choice as a cost-performance routing problem, not an identity choice. Don’t worship the expensive button, Boss. Very dignified way to burn money.

### Daily Briefing System

The recurring analyst stack should separate report types:

- **Tech briefing**: high-signal semiconductor, AI infra, cloud, model, and startup accounts.
- **Macro briefing**: macro accounts, market structure, rates, inflation, employment, VIX, liquidity.
- **Bookmark briefing**: user-curated X bookmarks from last 24h; score and prioritize before summarizing.
- **Top-5 daily synthesis**: choose the five cross-report insights that matter most and explain portfolio/project relevance.
- **Prediction-market briefing**: surface unusual wallet flows, sharp clusters, model-market gaps, correlated market convergence, and watch-list triggers.

### Investment Research Memory

The context that matters:

- Core theses.
- Risk appetite.
- Current positions and position sizing logic.
- Rationale for each investment.
- Watchlist and exit targets.
- Prior stress tests and what would invalidate a thesis.

This is where a persistent Hermes setup can beat a stateless LLM: the private context changes the analysis target.

### Memory and Hindsight Loop

A durable analyst loop needs temporal synthesis:

- Cron jobs collect daily evidence.
- Ingestion stores raw/source-backed material.
- Hindsight or equivalent memory layer extracts patterns.
- Hermes can later answer: “what changed since last week?”, “which thesis is weakening?”, “which signals keep recurring?”, or “what did we keep ignoring?”

### Risk Control

Use Hermes for:

- Alerts.
- Exit reminders.
- Stress tests.
- Contradiction checks.
- Position-specific research.
- Watchlist monitoring.

Do not use Hermes for:

- Direct trade execution.
- Unverified factual claims.
- Blind conviction laundering from social media screenshots.
- Anything where a hallucination can move money without human review.

## Roshan-Relevant Takeaways

- The article’s best match for this KB is not the investing advice itself; it is the workflow architecture.
- Roshan’s existing daily AI briefing and weekly autoresearch setup can reuse the same pattern: source monitoring → scoring → top insights → “why it matters” → memory across time.
- The X/bookmark workflow is worth testing later once xurl auth is configured, but the first capture proved public X articles can be read from the browser fallback.
- For Roshan’s ML/NLP path, replace “portfolio” with “research agenda”: track papers/blogs/repos, score novelty/relevance, connect to current theses, and alert when a topic deserves deeper study.

## Open Questions

- Should Roshan’s KB have a recurring “bookmark briefing” lane, or should bookmarks only feed the daily AI briefing?
- Should Hermes Workspace be adopted for editable Skills/Tasks/Memory once Roshan’s current cron/Kanban setup stabilizes?
- What scoring rubric should be used for X posts: novelty, credibility, actionability, ML relevance, career relevance, implementation value?

## Contradictions

- No contradictions recorded yet. The source is a single user report, not independently validated evidence.

## Citations

- Interface/OpenWebUI: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-interface-openwebui]]
- Workspace command-center idea: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-workspace-command-center]]
- Builder/operator cost tradeoff: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-builder-operator-cost]]
- Daily briefing report structure: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-daily-briefing-workflow]]
- Private context moat: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-private-context-moat]]
- Memory/Hindsight loop: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-memory-hindsight-loop]]
- Model cost stack: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-model-cost-stack]]
- No autonomous trading: [[sources/0xjeff-hermes-as-ultimate-analyst#ex-no-autonomous-trading]]
