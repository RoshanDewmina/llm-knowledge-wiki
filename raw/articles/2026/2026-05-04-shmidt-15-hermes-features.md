---
title: "99% of Hermes Agent Users Have Never Touched These 15 Features"
source: "https://x.com/shmidtqq/status/2051307460208578864"
author: "shmidt (@shmidtqq)"
published_at: "2026-05-04T10:26:00Z"
captured_at: "2026-05-06T23:35:03Z"
type: "raw_article"
tags: [hermes, ai-agents, slash-commands, workflow, x-article]
---

# 99% of Hermes Agent Users Have Never Touched These 15 Features

Public X Article captured by browser extraction. Duplicate user URLs to this status were deduplicated.

## Metadata visible at capture

- Views: 128.3K
- Replies/reposts/likes/bookmarks: 40 / 83 / 805 / 1.9K
- Media cover and screenshots included:
  - https://pbs.twimg.com/media/HHduwNiXwAA6Nlf?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdv0tTXoAAMBfu?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdv-EBWwAAjMUw?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdrr0GWwAAGfwS?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdrjyRXIAAR5oG?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdru4EXgAEIJFV?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdryBmWwAAd6LS?format=jpg&name=small
  - https://pbs.twimg.com/media/HHdr-DFWIAEaRpU?format=jpg&name=small

## Captured useful source passages

The article argues most Hermes users only use chat + model selection and ignore deeper features: persistent memory, session branching, file rollbacks, voice mode, multi-platform gateway, custom slash commands, cron, webhooks, and model routing.

Ranked feature list from source:

1. `/personality` + `SOUL.md`: persistent agent voice/persona.
2. `MEMORY.md` + `USER.md`: persistent project/user memory, indexed with FTS5 and summarized.
3. `/insights [days]`: cross-session usage analytics.
4. `/snapshot`: save/restore full Hermes state before risky work. Version-sensitive; verify against active Hermes commands.
5. `/branch` / `/fork`: branch session context to try risky paths.
6. `/rollback`: filesystem checkpoints for touched files.
7. `/btw`: ephemeral side question; version-sensitive, verify availability.
8. `/steer` and `/queue`: mid-run steering and queued next turn; version-sensitive, verify availability.
9. `/yolo`, `/fast`, `/reasoning`: approval, priority, and reasoning effort toggles.
10. `/model [--provider] [--global]`: model/provider switching without restart.
11. Auxiliary models: route compression/session summaries/titles/vision to cheaper or task-specific models.
12. 17-platform gateway: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Feishu, WeCom, DingTalk, BlueBubbles, Home Assistant, QQBot, CLI, voice.
13. `/voice`: voice on CLI, Telegram DMs, Discord channels, Discord voice rooms.
14. Cron + `/webhook-subscriptions`: scheduled jobs and event-driven payloads to DMs.
15. Skills as slash commands: built-in and custom skills become workflow commands; author cites custom `/sage` for trend scouting and drafting.

Caveat: some command names in this article may be version-specific or promotional; verify against `hermes-agent` docs and live `/help` before assuming availability.
