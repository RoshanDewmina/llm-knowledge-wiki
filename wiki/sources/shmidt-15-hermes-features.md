---
title: "99% of Hermes Agent Users Have Never Touched These 15 Features"
type: source
created: 2026-05-06T23:35:03Z
updated: 2026-05-06T23:35:03Z
status: reviewed
confidence: 0.74
related:
  - "[[syntheses/context/agent-workflow-x-clips-2026-05-06]]"
  - "[[syntheses/context/hermes-personal-analyst-patterns]]"
source_path: raw/articles/2026/2026-05-04-shmidt-15-hermes-features.md
source_kind: articles
compiled_at: 2026-05-06T23:35:03Z
source_hash: d27328e2ba70f207a4b44202b2badbc407617a3a18d5c4ce78c32559e0d08998
author: "shmidt (@shmidtqq)"
captured_at: 2026-05-06T23:35:03Z
tags: [hermes, slash-commands, ai-agents, workflow]
---

# 99% of Hermes Agent Users Have Never Touched These 15 Features

## Topic Map

- Persistent persona and memory setup.
- Session branching, rollback, steering, queueing.
- Provider/model routing and auxiliary models.
- Multi-platform gateway and voice.
- Cron/webhooks.
- Skills as reusable slash-command workflows.

## Useful Notes

- Strong workflow claim: Hermes is underused if treated as a Telegram chatbot; value comes from persisted identity/memory, recovery controls, scheduled/evented runs, and custom skills.
- Immediate Roshan relevance: skills, cron, memory, rollback, model routing, and gateway are all already part of his Hermes setup or near it.
- Treat command names as version-sensitive. The current loaded Hermes skill documents `/branch`, `/queue`, `/rollback`, `/fast`, `/reasoning`, `/voice`, `/model`, and cron/webhook commands, but not every named command in the article (`/snapshot`, `/btw`, `/steer`) appears in the loaded docs.

## Verified Claims

- The article lists 15 Hermes features and argues most users ignore them.
- The article emphasizes custom skills/slash commands as the difference between tourists and real users.
- The article frames multi-provider routing and auxiliary model routing as cost controls.

## Evidence Extracts

### ex-using-eight-percent

> You hooked up Telegram. You picked a model. You type prompts, get answers, close the tab. You're using 8% of Hermes.

### ex-memory-files

> Two persistent files, read every session. MEMORY.md = project notebook. USER.md = what it knows about you. Indexed with FTS5 + LLM summarizer, so a memory from 8 weeks ago surfaces in today's session.

### ex-midflight-controls

> Branch the session like a git commit. Try a riskier path without burning your good context. Doesn't pan out? Come back.

### ex-gateway-cron-webhooks

> Built-in scheduler. Plain language schedules... Pair with /webhook-subscriptions for the inverse: GitHub, Vercel, Stripe, uptime checks push payloads straight to your DMs.

### ex-skills-are-slash-commands

> Skills Are Slash Commands... You can write your own. I built /sage. It spots outliers in my niche, scouts trends, drafts QTs and threads in my voice. Built once. Type /sage in any session, any platform, runs forever.

## Contradictions

- Some command names may not match Roshan's active Hermes build/docs. Verify with live `/help` before use.

## Related Pages

- [[syntheses/context/agent-workflow-x-clips-2026-05-06]]
- [[syntheses/context/hermes-personal-analyst-patterns]]
