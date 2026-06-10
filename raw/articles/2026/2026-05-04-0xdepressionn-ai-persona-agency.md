---
title: "5 AI personas. $127,000/month. No models. No team. Claude runs the agency"
source: "https://x.com/0xDepressionn/status/2051304679607291924"
author: "Dep (@0xDepressionn)"
published_at: "2026-05-04T10:15:00Z"
captured_at: "2026-05-06T23:35:03Z"
type: "raw_article"
tags: [ai-agents, synthetic-media, adult-industry, deceptive-personas, risk, x-article]
---

# 5 AI personas. $127,000/month. No models. No team. Claude runs the agency

Public X Article captured by browser extraction.

## Metadata visible at capture

- Views: 885.7K
- Replies/reposts/likes/bookmarks: 27 / 83 / 582 / 2.1K
- Related quoted article visible: Raytar article on OnlyFans + Claude Code.
- Media URLs included screenshots and diagrams; exact OCR not used as evidence here.

## Safety / usefulness note

This source is about synthetic adult-content personas and revenue automation. The useful durable information is the agent architecture/risk pattern: persona files, voice files, memory files, content-generation consistency, orchestration, and why persistent user memory is economically valuable. Detailed operational prompt templates for deceptive adult impersonation are intentionally not reproduced here. Cute little grift manual can stay outside the KB.

## Captured useful source passages

The article claims an operator is running several AI-generated OnlyFans personas using Claude, Flux, Claude Code, LoRAs, and a polling/orchestration layer.

Key architectural pattern:

- Each persona has isolated files: persona/backstory, voice/style, visual identity, subscriber memory.
- `brain.md` style memory stores per-subscriber spend, preferences/triggers, recent facts, promises, and topics to avoid.
- Claude reads the relevant persona and subscriber memory before replying, then updates memory after each interaction.
- Visual consistency is treated as the hardest part: a LoRA per persona plus locked physical descriptors, environments, and seed ranges.
- The orchestration layer polls multiple inboxes, routes each message to the correct persona folder, prevents cross-contamination, logs interaction metadata, and produces weekly revenue optimization reports.

Risk pattern:

- The source explicitly describes nonexistent personas, synthetic faces, automated intimacy, and monetized subscriber memory.
- The highest-value asset is not content but accumulated relationship/memory data.
- Cross-contamination between personas is framed as a business failure; from a user-safety lens it is also evidence of deceptive identity management.

Reusable non-deceptive takeaway: isolate agent contexts by persona/client/project; keep memory scoped; route tasks through an orchestrator; log interactions; require review for sensitive outbound actions; treat private memory as high-risk data.
