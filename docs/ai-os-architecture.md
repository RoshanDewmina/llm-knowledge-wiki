# AI-First Personal Operating System — Architecture Map

> Canonical system map for all AI agents (Claude Code / Cowork, Hermes, Codex, Gemini, others).
> This file is the **one place** that describes where data lives, what tools exist, and how to
> retrieve personal context safely. Each agent's native config is a thin pointer to this file —
> do not duplicate this content elsewhere; update it here.

Last reviewed: 2026-06-07

---

## 1. Source-of-truth strategy

| Concern | Single source of truth | How agents access it |
|---|---|---|
| Notes & knowledge | `~/.hermes/knowledge-base/wiki/` | Direct file read, or `./bin/llm-wiki query` |
| Personal facts / PII | `~/.hermes/knowledge-base/secure/` | **Only** via `personal-kb` MCP (`query_facts`); writes via `propose_fact` → human approval |
| Raw/source material | `~/.hermes/knowledge-base/raw/` | Read-only; never rewrite existing raw files |
| Habits / goals / todos | `~/.streak/streak.db` | `~/bin/streak` CLI (via the `streak` Hermes skill) |
| Secrets / API keys | macOS Keychain + `~/.hermes/.env` (0600) | Never printed; pulled at call time |
| Agent contract | `~/.hermes/knowledge-base/AGENTS.md` (+ `docs/agent-contract.md`) | Read before durable changes |
| This system map | `~/.hermes/knowledge-base/docs/ai-os-architecture.md` (this file) | Linked from each agent's home config |

**Retired:** `~/Documents/Obsidian/files` (empty decoy vault). Never read or write it. Remove it from
Obsidian via Settings → About → Manage vaults (handles registry + Sync cleanly).

**Rule:** one fact, one home. If something belongs in the KB, it goes in the KB — not duplicated into
an agent's memory file. Agent memory holds only pointers and always-on preferences.

---

## 2. Data sources & where they live

- **Knowledge base / vault:** `~/.hermes/knowledge-base` (git repo + Obsidian vault). See `AGENTS.md` for the folder taxonomy (`wiki/`, `raw/`, `secure/`, `experiments/`, `tools/`).
- **Habit tracker:** `~/.streak/streak.db` (SQLite). CLI at `~/bin/streak`.
- **Hermes agent home:** `~/.hermes` (personas, routines/cron, gateway, skills, memory store).
- **Dotfiles:** `~/.dotfiles` (zsh, tmux, ghostty, theme scripts).

## 3. Tools / APIs available to agents (MCP)

Read-only and low-risk first; write/financial tools flagged.

- **`personal-kb`** (project-scoped to the KB) — safe reads of the knowledge base + `propose_fact` gate. The correct way to reach personal context.
- **`context7`, `apple-docs`** — read-only docs lookup.
- **iOS dev stack** (`XcodeBuildMCP`, `xcode`, `ios-simulator`) — for Conduit/iOS work.
- **Remote OAuth connectors (claude.ai):** Gmail, Google Calendar, Google Drive (have write/create/delete), Gamma, Figma, HuggingFace, Vercel.
- **Interactive Brokers (`feb1e819…`)** — ⚠️ FINANCIAL. Read tools: `get_account_*`, `get_price_*`, `search_contracts`. **Write/trade tools** (`create_order_instruction`, `delete_order_instruction`) must NEVER be called by an automated/scheduled job. Trades require an explicit, human-driven, typed-confirmation session. See `docs/portfolio-brief.md` (when created).

## 4. Per-agent roles (separate systems, shared substrate)

All agents point at the SAME source of truth (§1) and read this map.

- **Claude Code / Cowork** — coding + repo work. Reads the KB via `personal-kb` when run inside it. Home config: `~/.claude/CLAUDE.md` → points here.
- **Hermes** — always-on personal agent: routines/cron, habit tracking (`streak`), briefings, study (`research-paper-mastery`), personas. Contract: `~/.hermes/knowledge-base/AGENTS.md`.
- **Codex** — execution lanes (sandboxed). Home config: `~/.codex/AGENTS.md` → points to KB AGENTS.md.
- **Gemini / others** — point `GEMINI.md` (etc.) at this map.

## 5. Conventions

- **Filenames:** lowercase kebab-case. Date-prefix daily/dated artifacts (`YYYY-MM-DD-...`).
- **Frontmatter:** `title, type, source, captured_at, tags, status, confidence` as applicable. Set `created/updated/compiled_at` from `date -u +%Y-%m-%dT%H:%M:%SZ`.
- **Tags:** hierarchical (`ml/llm`, `ml/inference`, `infra/gpu`, `cs/systems`).
- **Config:** each agent's home file is a thin pointer to this map + always-on rules only. No duplicated workflow docs.
- **Safety:** advisory docs (this file, AGENTS.md, memory) guide behavior; hard constraints belong in hooks/permissions. Financial writes are never automated.

## 6. Workflows worth automating (status)

- **Daily AI/ML briefing** (`ai-briefing` skill, Hermes cron) — *paused* (was failing on offline/Telegram DNS). Re-enable once delivery is reliable.
- **Daily rhythm** (`daily-rhythm`: morning plan / reschedule / evening review) — on demand; can be cron'd.
- **Habit check-ins** (`streak` Scheduled Routines: 2pm nudge / 9pm check-in) — available.
- **Weekly autoresearch** — *paused*; revisit only when KB evidence + experiment packs are rich enough to be worth the tokens.
- **Morning portfolio brief (IBKR)** — designed, read-only, not yet built. See §3 safety rules.
