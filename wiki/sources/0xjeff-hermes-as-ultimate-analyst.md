---
title: "Hermes as the Ultimate Analyst - I've found the gist for my ultimate analyst"
type: source
created: 2026-05-06T23:10:29Z
updated: 2026-05-06T23:10:39Z
status: reviewed
confidence: 0.82
related:
  - "[[syntheses/context/hermes-personal-analyst-patterns]]"
source_path: raw/articles/2026/2026-05-04-0xjeff-hermes-as-ultimate-analyst.md
source_kind: articles
compiled_at: 2026-05-06T23:10:39Z
source_hash: 7d72c3e8f6d59807600ed31c651dea651489526218f1a3ed8e445f62cda25a97
author: "0xJeff (@0xJeff)"
captured_at: 2026-05-06T23:09:33Z
tags:
  - hermes
  - ai-agents
  - investment-research
  - x-article
  - workflow/personal-analyst
---

# Hermes as the Ultimate Analyst - I've found the gist for my ultimate analyst

## Source Snapshot

- Raw file: `raw/articles/2026/2026-05-04-0xjeff-hermes-as-ultimate-analyst.md`
- Source: https://x.com/0xJeff/status/2051214993719427258
- Author: `0xJeff (@0xJeff)`
- Published: `2026-05-04T04:18:00Z`
- Captured: `2026-05-06T23:09:33Z`
- Capture method: public X article page; `xurl read` was unavailable because local xurl had no registered apps/auth.

## Topic Map

- **Hermes interface layer**: move beyond Discord when visual artifacts, HTML previews, or ChatGPT/Claude-style UI matter.
- **Builder/operator setup**: Claude can be used as a visual builder while Hermes operates workflows, but cost pushes users toward Codex or Hermes-only setups.
- **Daily investment briefings**: X API, tracked accounts, bookmarks, macro/tech sources, synthesis reports, and Polymarket dashboard alerts.
- **Personalized investment research**: Hermes becomes useful when it remembers theses, preferences, risk appetite, positions, and rationale.
- **Memory/reflection loop**: cron jobs feed Hindsight; Hindsight ingests insights; Hermes later recalls and synthesizes across time windows.
- **Model/inference cost stack**: Claude dashboard maintenance plus DeepSeek API for Hermes; Opencode Go mentioned as a cheap first-time setup.
- **Risk controls**: author does not allow Hermes to trade directly; uses it for alerts and timely exits because hallucinations remain a risk.

## Useful Notes, Not Fluff

### 1. Interface choice changes what Hermes is good for

Discord is enough for text summaries, but poor for visual artifacts, HTML, and design/build workflows. OpenWebUI is framed as the missing UI layer: it gives Hermes a ChatGPT/Claude-like surface where it can generate and display HTML/visual explainers inside the same conversation.

Hermes Workspace is treated as a command-center candidate, with editable Skills, Tasks, Memory, Soul, and Swarm/multi-agent capabilities, but the author had not yet integrated it into daily workflow.

### 2. Claude-as-builder + Hermes-as-operator is beginner-friendly but expensive

Claude Desktop/Artifacts/site previews/design features lower the barrier for non-technical users. The author’s objection is cost: Claude Pro is framed as insufficient for sustained building, while Claude Max is expensive. Suggested alternatives: Codex for more generous usage, or Hermes alone as both builder and operator.

### 3. Daily briefings are the highest-value workflow

The author’s daily analyst system is built around recurring reports:

- Tech report from accounts such as `@SemiAnalysis_`.
- Macro report from accounts such as `@KobeissiLetter` and other news sources.
- X Bookmark Briefing from the last 24 hours, scored for priority.
- Top 5 Daily Synthesis that reflects across same-day briefings and explains why the top insights matter.
- Polybond Morning Brief that inspects a personal Polymarket dashboard for insiders, sharp signals, trends, and alerts.

Core pattern: ingest high-signal sources automatically, score/triage them, then synthesize only what matters to the portfolio.

### 4. The moat is private context, not the generic model

The author says the advantage comes from Hermes remembering three key theses, preferences, risk appetite, current positions across crypto/equities/prediction markets, and investment rationales. That context lets Hermes tailor research and stress tests in a way a stateless LLM cannot.

### 5. Memory loop: cron jobs + Hindsight + temporal synthesis

The useful memory loop described is:

1. Daily cron jobs gather insights.
2. Hindsight ingests them.
3. Hermes pulls patterns and synthesizes insights across arbitrary time periods.
4. Hermes recalls past discussions and draws relationships/conclusions from them.

This is directly relevant to building Roshan’s KB/briefing stack: raw ingestion is less valuable than later time-window synthesis and pattern extraction.

### 6. Model stack is cost-optimized, not prestige-optimized

The author’s current setup at capture time:

- Claude subscription at roughly $20/month to maintain dashboards.
- DeepSeek API at roughly $60/month for Hermes experimentation, about $2/day.
- DeepSeek v4 Pro discount noted as 75% until end of May; DeepSeek v4 Flash for simple tasks.
- Opencode Go as suggested cheap first-time Hermes setup at $5 for first month.

These are time-sensitive pricing/model claims from the article date, not durable recommendations.

### 7. Do not let Hermes directly trade

The author explicitly does not permit Hermes to execute trades because hallucinations remain possible. The safer use is alerting: track key positions and notify when targets or exit conditions are hit. This prevents behavioral failure modes such as bag-holding or turning short-term trades into identity/community positions.

## Image-Derived Context

The article included screenshots. Vision extraction was used only for low-resolution support notes, not as exact evidence anchors.

- OpenWebUI screenshot: self-hosted LLM chat interface; connects to Ollama/OpenAI/Anthropic/local/custom endpoints; handles files, tools, workflows, routing, users, roles, and knowledge/context.
- AI infrastructure daily briefing screenshot: tracks electrical equipment orders, ABB/Vertiv/Eaton/Schneider, datacenter electrical bottlenecks, and AI agents in finance as inference-demand signals.
- Bookmark briefing screenshot: scores X bookmarks by priority, highlighting xAI/Grok agent mode, xAI voice cloning API, crypto market structure, AI stack value accrual, coding agents for PMs, and AI-generated micro-drama workflows.
- Top 5 daily insights screenshot: AI infrastructure capex, layoffs-to-compute reallocation, defensive macro signals, energy as an AI-stack input, and consumer AI platform consolidation.
- Polymarket morning brief screenshot: ranks markets using fresh-wallet activity, sharp clusters, correlated markets, model-vs-market discrepancies, and watch-list triggers.
- Stock watch screenshot: bear-case/conviction framework for NVDA, TSLA, and RGTI.

## Verified Claims

- The article argues that Hermes is becoming useful as a personal investment analyst by combining automated ingestion, private context, memory, and recurring synthesis.
- The author’s highest-value current workflow is daily briefings from X/API/bookmarks/macroeconomic sources and a Polymarket dashboard.
- The author treats context and memory as the durable moat: theses, preferences, risk appetite, positions, and rationales are what differentiate Hermes from a normal LLM.
- The author prefers using Hermes for alerts and research support, not autonomous trading, because hallucinations remain an unacceptable execution risk.
- The article’s model/tooling recommendations are cost-sensitive and time-sensitive, not stable technical claims.

## Evidence Extracts

### ex-interface-openwebui

> The real unlock with Hermes happens when I started exploring using Hermes with other medium beyond Discord.
>
> Sure, Discord is great BUT you can’t really see visuals, html, or get that Claude artifacts experience.
>
> This is where OpenWebUI comes in
>
> OpenWebUI transforms the experience of talking with your agent to using a ChatGPT or a Claude. Seamless experience, great for building/designing something.

### ex-workspace-command-center

> As for Hermes Workspace,
>
> I’m still not there yet. There are features like Swarm where you can run multiple agents to compete a mission. Apparently great for developer use cases.
>
> You can also see key items/files like Skills, Tasks, Memory, Soul and edit them directly. It feels like Hermes command center that has everything together in one interface.

### ex-builder-operator-cost

> In last week’s Hermes article (Part III), we’ve talked about Claude as the builder and Hermes as the operator mindset.
>
> The downside to this is that Claude is quite expensive — $20 Pro plan is just a teaser, you need to buy $100 Max plan to be able to build stuff.
>
> Like me, if you don’t have unlimited money, it’s better to either switch to Codex (because they’re much more generous) or just stick with Hermes alone and use Hermes as both the builder and the operator.

### ex-daily-briefing-workflow

> The most useful tool here is X API. It’s not free but it’s pretty reliable.
>
> For every single report, Hermes tracks certain accounts, synthesizes, summarizes and explains why it matters for me and my portfolio.
>
> Report on Tech: Hermes tracks @SemiAnalysis_ and other accounts
>
> Report on Macro: Hermes tracks @KobeissiLetter and other news sources
>
> X Bookmark Briefing: Hermes queries my X bookmark in the last 24hr and go through them with scoring to let me know which one to prioritize first. I can then ask it to summarize the ones that I like.
>
> Top 5 Daily Synthesis: Hermes reflects on other briefing that’s happening on the day, picks the top 5 insights and explains why it matters
>
> Polybond Morning Brief: Hermes looks at Polybond (my personal Polymarket dashboard) to surface potential insiders, sharp signals, trends and drop them daily.

### ex-private-context-moat

> I love doing research with Hermes because it remembers by 3 key theses + my preferences + my risk appetite + my current positions (across crypto, equities, prediction markets) and my rationale for those investments.
>
> It then uses all these things as context to find the right kinds of investment/research tailored to me.
>
> Normal LLM can’t compete with that.
>
> The moat is in the data/context.

### ex-memory-hindsight-loop

> Hermes is fascinating because it remembers, it recalls, and it reflects on past information.
>
> The loop that I enjoy is:
>
> Daily cron jobs ➝ Hindsight ingests insights ➝ pull patterns & synthesizes insights across any time period
>
> Recalls things we discussed in past sessions and draw conclusions/relationships from it.

### ex-model-cost-stack

> DeepSeek API is so cheap, 75% discount on DeepSeek v4 Pro extended till end of May. DeepSeek v4 Flash is cheap and efficient for simple tasks.
>
> My latest set up is now
>
> $20/month subscription on Claude to maintain the dashboards
>
> ~\$60/month on DeepSeek API for Hermes (been experimenting with Hermes a lot, paying roughly $2 per day)
>
> Opencode Go is still the #1 choice if you’re setting up Hermes for the first time. It’s only $5 for the first month.

### ex-no-autonomous-trading

> I still don't allow Hermes to directly trade (due to hallucinations), what I find very useful are alerts tracking my key positions so that I can gradually exit in a timely manner when they hit my targets.
>
> I do this because I usually bag hold far too long.

## Contradictions

- No contradictions recorded yet. The article is a single first-person workflow report; its pricing/model claims are time-sensitive and should be rechecked before action.

## Related Pages

- [[syntheses/context/hermes-personal-analyst-patterns]]

## Compilation Notes

- Raw article text was captured from X’s public article rendering.
- `xurl` exists locally, but `xurl read 2051214993719427258` returned HTTP 401 because no apps were registered in local xurl auth.
- Browser extraction succeeded and exposed the full article body.
