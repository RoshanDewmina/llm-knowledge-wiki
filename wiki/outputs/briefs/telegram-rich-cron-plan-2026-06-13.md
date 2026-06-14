---
title: Telegram Rich Formatting and Hermes Cron Plan
type: journal
created: 2026-06-14T01:02:33Z
updated: 2026-06-14T01:02:33Z
status: draft
confidence: 0.9
related: []
source_pages: []
compiled_at: 2026-06-14T01:02:33Z
---

# Telegram Rich Formatting + Hermes Cron Plan

Date: 2026-06-13

## Current Hermes Telegram / cron audit

Hermes gateway is running and cron is active.

Active scheduled jobs:

| Job | Schedule | Deliver | Status | Notes |
|---|---|---|---|---|
| Daily morning plan | 07:00 daily | origin | OK last run | Likely Telegram-origin only if created from Telegram; current job has `origin: null`, so delivery depends on scheduler origin fallback. |
| Daily 5pm review | 17:00 daily | origin | Error last run | Failed due model/provider usage limit. |
| Carleton timeticket check | 2026-06-17 09:00 once | origin | scheduled | Explicit Telegram origin: Roshan Silva, chat 8728796966. |
| Carleton financial hold warning | 2026-06-24 09:00 once | origin | scheduled | Explicit Telegram origin. |
| Carleton registration opens | 2026-07-10 09:00 once | origin | scheduled | Explicit Telegram origin. |
| Carleton fall tuition warning | 2026-08-18 09:00 once | origin | scheduled | Explicit Telegram origin. |
| Carleton winter tuition warning | 2026-11-18 09:00 once | origin | scheduled | Explicit Telegram origin. |
| morning-dashboard | 08:00 daily | local | OK last run | Does not deliver to Telegram; prompt says Telegram optional but deliver is local. |
| evening-review | 20:30 daily | local | OK last run | Does not deliver to Telegram; prompt says Telegram optional but deliver is local. |

Paused jobs that used to deliver to Telegram:

| Job | Schedule | Deliver | Last status | Notes |
|---|---|---|---|---|
| Daily AI briefing | 09:00 daily | telegram | error | Telegram delivery had DNS/connect failure; paused. |
| weekly autoresearch | Sunday 17:00 | telegram | error | Model usage-limit error; paused. |
| Market brief | 08:30, 12:30, 16:30 weekdays | telegram | OK | Paused manually. |
| Gmail triage digest | every 3h | telegram | OK | Paused manually. |

Config observations:

- `platforms.telegram.enabled: true`
- Telegram env keys exist: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_ALLOWED_USERS`
- `platforms.telegram.extra` is not configured.
- Hermes Telegram adapter has opt-in support for Bot API 10.1 `sendRichMessage`, but it is currently disabled because `platforms.telegram.extra.rich_messages` is absent/false.
- Current Telegram channel prompt says: “No markdown, no bullets, no headers. Natural spoken sentences.” That is good for conversational voice personas, but bad for cron dashboards/briefings.

## Telegram official capabilities researched

Source: official Telegram Bot API docs, especially `sendMessage`, formatting options, `MessageEntity`, and bot features/keyboards.

Useful current capabilities:

1. Standard `sendMessage`
   - Text cap: 1–4096 chars after entity parsing.
   - Supports `parse_mode`: `HTML`, `MarkdownV2`, legacy `Markdown`, or explicit `entities`.
   - Supports `message_thread_id`, `direct_messages_topic_id`, `reply_parameters`, `reply_markup`, `link_preview_options`, `disable_notification`, `protect_content`.

2. HTML formatting
   - Stable and easier than MarkdownV2 for generated bot output.
   - Supports bold, italic, underline, strikethrough, spoilers, links, code/pre blocks, blockquotes, expandable blockquotes, custom emoji/time tags where supported.
   - Requires escaping `&`, `<`, `>` outside real tags.

3. MarkdownV2 formatting
   - Supports nested formatting, links, spoilers, blockquotes, code/pre, custom emoji/time.
   - Fragile: many characters must be escaped. Better for human-written markdown; risky for LLM-generated arbitrary text unless escaped carefully.

4. Rich Messages / `sendRichMessage`
   - Telegram Bot API 10.1 adds structured rich messages with markdown/html payloads.
   - Supports longer/structured output: headings, lists, task lists, tables, media blocks, quotes, collapsible blocks, formulas, footnotes, references, anchors.
   - Limits include 32,768 UTF-8 chars, 500 blocks, 16 nesting levels, 50 media attachments, 20 table columns.
   - Hermes source already has a rich-message fast path, currently opt-in.

5. Link previews
   - `link_preview_options` controls previews, including disabling previews or choosing a specific URL.
   - Useful for briefings: keep previews off by default unless the preview is the point.

6. Inline keyboards
   - Telegram supports inline buttons below messages.
   - Good for low-friction actions without sending visible chat noise.
   - Hermes already uses inline buttons for approvals/clarify; cron outputs could use them for “Open artifact”, “Mark done”, “Snooze”, “Skip”, “Run follow-up”.

7. Topics / threads
   - Hermes already supports Telegram `message_thread_id` and DM topic handling.
   - Current Carleton reminders target the main DM; future recurring categories could route to topics like Planning, Jobs, Research, Market, Email if topics are configured and working.

## Live tests performed

Sent three silent test messages to Telegram chat 8728796966 using the bot token already configured on hermes-box:

1. `sendMessage` with `parse_mode=HTML`
   - Result: OK, message_id 1004
   - Included bold, italic, underline, strikethrough, spoiler, normal blockquote, expandable blockquote, Python code block.

2. `sendMessage` with `parse_mode=MarkdownV2`
   - Result: OK, message_id 1005
   - Included bold, inline code, quote, spoiler, and link.

3. `sendRichMessage`
   - Result: OK, message_id 1006
   - Included heading, task checkboxes, table, and quote.

4. Hermes `send_message` tool to Telegram home channel
   - Result: OK, message_id 1007
   - Included heading, checklist, Markdown table, and blockquote through Hermes' Telegram delivery path.

Conclusion: the bot/account/API path supports both standard rich formatting and the new `sendRichMessage` endpoint. Hermes' current Telegram delivery path also successfully sends structured Markdown, but the adapter's native rich-message fast path should be enabled for cleaner tables/checklists in non-conversational cron outputs.

## Recommended plan

### Phase 1 — Fix routing and noise

1. Make all user-facing important crons explicitly deliver to Telegram, not vague `origin` or `local` unless intentional.
   - Keep one-shot Carleton jobs as `origin` because they already store explicit Telegram origin.
   - Change daily morning/evening jobs to explicit Telegram destination or ensure their `origin` is backfilled.
   - Keep local-only dashboard jobs local, or replace them with artifact-producing upstream jobs consumed by a Telegram summary job.

2. Decide which paused jobs to resume after model/provider issue is fixed:
   - Resume Gmail triage if email digest is still wanted.
   - Resume market brief only if useful; otherwise keep paused to reduce noise.
   - Resume AI briefing only after Telegram delivery and model/provider issues are stable.
   - Weekly autoresearch should stay paused unless the model/provider extra-usage problem is solved.

3. Add a notification policy:
   - Critical reminders: push notification.
   - Daily briefings/dashboards: silent unless they require immediate action.
   - Errors/failures: push notification.

### Phase 2 — Enable rich messages in Hermes Telegram config

Add:

```yaml
platforms:
  telegram:
    enabled: true
    extra:
      rich_messages: true
      disable_link_previews: true
```

Then restart gateway and verify logs. This should let final agent replies use Hermes' existing `sendRichMessage` fast path. If anything breaks, the adapter already falls back to legacy MarkdownV2.

### Phase 3 — Split conversational persona from cron formatting

Current Telegram channel prompt says “No markdown, no bullets, no headers.” Keep that for normal voice/persona chat, but cron jobs need a different instruction.

Cron prompts should explicitly say:

- Use Telegram Rich Message markdown if available.
- Use short headings.
- Use task lists and compact tables for structured dashboards.
- Keep under 32k for rich path; keep under 3800 chars for legacy fallback where possible.
- No TTS hidden blocks in cron outputs.
- Include one artifact path/link and 1–3 action buttons if supported.

### Phase 4 — Standard message templates

Create templates for recurring Telegram outputs:

1. Morning plan
   - Heading: `Morning plan — YYYY-MM-DD`
   - Three outcomes as checklist items.
   - First action highlighted.
   - Blockers/warnings as quote/callout.
   - Link/path to full plan.

2. Evening review
   - Heading: `Evening review — score X/10`
   - Evidence checked collapsed/expandable.
   - Keep/change/tomorrow sections.
   - Path to review artifact.

3. Gmail triage
   - Heading with unread/important counts.
   - Each important email as compact row: sender, subject, reason, action.
   - Buttons: `Archive`, `Mark handled`, `Draft reply` only if Hermes gets safe Gmail action gates later.

4. Job search copilot
   - Heading: `Top job matches — YYYY-MM-DD`
   - Table: company, role, score, why.
   - Buttons or links: `Open packet`, `Apply manually`, `Build gap project?`.

5. AI briefing
   - Rich message with sections: papers, launches, tools, one deeper read.
   - Links inline, previews disabled by default.
   - Expandable source notes.

### Phase 5 — Add inline action buttons

Extend Hermes cron delivery for Telegram metadata to support `reply_markup` for safe actions:

- `Open artifact` URL/path button if URL or dashboard exists.
- `Mark done` for streak/task completion only after confirmation.
- `Snooze 1h` for reminders.
- `Skip today` for daily planning/review nudges.
- `Run follow-up` for job/application packet generation.

Do not add destructive buttons without confirmation.

### Phase 6 — Optional topics

If Telegram DM topics work reliably on Roshan's client, route categories:

- Main: interactive chat
- Planning: morning/evening rhythm and Carleton reminders
- Jobs: job copilot results/application packets
- Research: AI briefing/autoresearch
- Market: market brief
- Email: Gmail triage

If DM topics remain flaky, do not fight Telegram; use a topic-enabled group or keep one DM and prefix messages with clear headings.

## Concrete next implementation tasks

1. Back up config and enable `platforms.telegram.extra.rich_messages: true` and `disable_link_previews: true`.
2. Restart gateway.
3. Trigger/send one Hermes-generated message containing a table/checklist and verify it uses rich rendering instead of MarkdownV2 table rewriting.
4. Update active cron prompts to ask for rich-message-friendly structures.
5. Convert daily morning/evening jobs to explicit Telegram delivery if desired.
6. Write a small `telegram_formatting` helper in Hermes if direct rich rendering needs HTML escaping or markdown sanitation.
7. Add tests around Telegram rich-message routing and fallback.
8. Add a `telegram_digest` skill/template for future cron jobs so every recurring message has consistent structure.

## Recommended immediate changes

- Enable Telegram rich messages.
- Keep link previews disabled by default.
- Update morning/evening prompt formatting.
- Decide which paused Telegram crons should resume.
- Add job-copilot daily digest once the Claude-built job-copilot is ready.
