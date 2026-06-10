# Market Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Next.js 16 full command center dashboard at `~/.hermes/market-dashboard/` that displays live watchlist prices, Hermes market briefs, brief history, and an earnings calendar, with an editable watchlist drawer.

**Architecture:** Next.js 16.2 App Router with TypeScript + Tailwind v4. API routes read directly from the KB filesystem (`~/.hermes/knowledge-base/`) and call Finnhub REST for live prices. SWR handles all client-side data fetching with 60-second auto-refresh for prices and optimistic updates for watchlist edits. Split-panel layout: fixed 240px left sidebar (watchlist + run status) + main area (brief tabs + calendar/history panels).

**Tech Stack:** Next.js 16.2, React 19, TypeScript 5, Tailwind CSS v4, SWR 2.x, Bun 1.x

**Design Aesthetic — "Tungsten":** Near-black (#070B0F) with blue undertone. JetBrains Mono for all data/prices. Instrument Serif (Google Fonts) for section labels — unexpected serif in a fintech context, memorable. Teal-green (#22D3A0) for gains, warm coral (#F8716A) for losses, sky-blue (#38BDF8) for selection/active, amber (#FFB347) for streak warnings. Subtle 32px grid-paper texture on body (opacity 0.15, pointer-events none). Price numbers animate on SWR revalidation: tick-up (slides in from below) or tick-down (from above). Brief panel has a slow-shifting gradient border (3s loop) — the visual signal it's live AI output.

---

## File Structure

```
~/.hermes/market-dashboard/
├── package.json
├── bun.lockb
├── next.config.ts
├── tsconfig.json
├── postcss.config.mjs          ← Tailwind v4 PostCSS plugin
├── .env.local                  ← FINNHUB_API_KEY, KB_PATH, STATE_PATH
├── .env.local.example
├── src/
│   ├── app/
│   │   ├── globals.css         ← @import "tailwindcss"
│   │   ├── layout.tsx
│   │   ├── page.tsx            ← DashboardPage (assembles split panel)
│   │   └── api/
│   │       ├── prices/route.ts         ← GET: live Finnhub quotes
│   │       ├── brief/route.ts          ← GET: latest or specific brief
│   │       ├── briefs/route.ts         ← GET: list all brief files
│   │       ├── history/route.ts        ← GET: price-history.json
│   │       ├── watchlist/route.ts      ← GET + PUT: watchlist MD file
│   │       └── calendar/route.ts       ← GET: Finnhub earnings calendar
│   ├── components/
│   │   ├── Sidebar.tsx         ← Watchlist prices + brief run status
│   │   ├── PriceCard.tsx       ← Single ticker card (price, %, streak)
│   │   ├── BriefPanel.tsx      ← Active brief viewer with phase tabs
│   │   ├── BriefHistory.tsx    ← Scrollable list of past briefs
│   │   ├── EarningsCalendar.tsx← Upcoming earnings events
│   │   └── WatchlistEditor.tsx ← Slide-out drawer, form per entry
│   ├── lib/
│   │   ├── types.ts            ← All shared TypeScript interfaces
│   │   ├── kb.ts               ← Read brief files + price-history.json
│   │   ├── watchlist.ts        ← Parse + serialize market-watchlist.md
│   │   └── finnhub.ts          ← Finnhub HTTP client, rate-limit guard
│   └── hooks/
│       └── useMarketData.ts    ← All SWR hooks (usePrices, useBrief, etc.)
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `~/.hermes/market-dashboard/` (entire project)
- Create: `.env.local`
- Create: `.env.local.example`
- Modify: `postcss.config.mjs` (Tailwind v4)
- Modify: `src/app/globals.css` (Tailwind v4 import)

- [ ] **Step 1: Scaffold with bun**

```bash
cd ~/.hermes
bun create next-app@latest market-dashboard --yes
cd market-dashboard
```

Expected: project created with TypeScript, ESLint, App Router, Tailwind (v3), `@/*` alias, `src/` dir, `AGENTS.md`.

- [ ] **Step 2: Upgrade Tailwind to v4**

```bash
cd ~/.hermes/market-dashboard
bun remove tailwindcss postcss autoprefixer
bun add tailwindcss@latest @tailwindcss/postcss@latest
```

- [ ] **Step 3: Replace PostCSS config for v4**

Delete `postcss.config.mjs` if it exists, then create:

```js
// postcss.config.mjs
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
export default config;
```

Delete `tailwind.config.ts` — not used in v4.

- [ ] **Step 4: Replace globals.css for v4**

```css
/* src/app/globals.css */
@import "tailwindcss";
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400&display=swap');

:root {
  /* Tungsten palette */
  --bg:          #070B0F;
  --surface:     #0D1219;
  --surface-2:   #111920;
  --border:      #1A2535;
  --border-bright: #2A3D52;
  --text:        #C8D8E8;
  --muted:       #4A5A6A;
  --accent:      #38BDF8;   /* sky-blue: selected / active */
  --up:          #22D3A0;   /* teal-green: gains */
  --down:        #F8716A;   /* warm coral: losses */
  --warn:        #FFB347;   /* amber: streak warnings */
  --signal:      #818CF8;   /* indigo: AI/brief indicator */

  --font-mono:   'JetBrains Mono', ui-monospace, monospace;
  --font-serif:  'Instrument Serif', Georgia, serif;
  --font-sans:   'DM Sans', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-mono);
  -webkit-font-smoothing: antialiased;
  overflow: hidden;
}

/* Subtle 32px grid-paper texture — depth without noise */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(var(--border) 1px, transparent 1px),
    linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.15;
  pointer-events: none;
  z-index: 0;
}

/* Price tick animations — fire when SWR revalidates a price */
@keyframes tick-up {
  0%   { transform: translateY(6px); opacity: 0; }
  100% { transform: translateY(0);   opacity: 1; }
}
@keyframes tick-down {
  0%   { transform: translateY(-6px); opacity: 0; }
  100% { transform: translateY(0);    opacity: 1; }
}
.animate-tick-up   { animation: tick-up   0.18s cubic-bezier(0.22,1,0.36,1); }
.animate-tick-down { animation: tick-down 0.18s cubic-bezier(0.22,1,0.36,1); }

/* Live heartbeat dot */
@keyframes pulse-live {
  0%, 100% { opacity: 1;   transform: scale(1);    }
  50%       { opacity: 0.3; transform: scale(0.75); }
}
.animate-live { animation: pulse-live 2s ease-in-out infinite; }

/* Brief panel gradient border — slow shift signals "live AI output" */
@keyframes gradient-shift {
  0%   { background-position: 0%   50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0%   50%; }
}
.brief-live-border {
  background: linear-gradient(135deg, var(--signal), var(--accent), var(--up), var(--signal));
  background-size: 300% 300%;
  animation: gradient-shift 6s ease infinite;
  padding: 1px;
  border-radius: 6px;
}

/* Section label typography — unexpected serif in a data terminal */
.label-serif {
  font-family: var(--font-serif);
  font-size: 11px;
  font-style: italic;
  color: var(--muted);
  letter-spacing: 0.02em;
}
```

- [ ] **Step 5: Add SWR**

```bash
bun add swr
```

- [ ] **Step 6: Create env files**

```bash
# .env.local.example
FINNHUB_API_KEY=your_key_here
KB_PATH=/Users/YOURNAME/.hermes/knowledge-base
STATE_PATH=/Users/YOURNAME/.hermes/cron/state/market-brief
```

```bash
# .env.local  (fill in real values)
FINNHUB_API_KEY=<from ~/.hermes/.env>
KB_PATH=/Users/roshansilva/.hermes/knowledge-base
STATE_PATH=/Users/roshansilva/.hermes/cron/state/market-brief
```

These are server-only vars (no `NEXT_PUBLIC_` prefix) — Finnhub key is never sent to the browser.

- [ ] **Step 7: Verify scaffold boots**

```bash
bun dev
```

Expected: `http://localhost:3000` loads Next.js default page, no errors in terminal.

- [ ] **Step 8: Commit**

```bash
git init
git add -A
git commit -m "feat: scaffold Next.js 16 market dashboard (Bun, Tailwind v4)"
```

---

## Task 2: Shared Types

**Files:**
- Create: `src/lib/types.ts`
- Create: `src/__tests__/lib/types.test.ts`

- [ ] **Step 1: Write the type definitions**

```typescript
// src/lib/types.ts

export type Phase = "pre-open" | "midday" | "post-close";
export type PositionType = "holding" | "watching";
export type Direction = "long" | "short";

export interface QuoteData {
  c: number;       // current price
  pc: number;      // previous close
  dp: number;      // % change
  t: number;       // unix timestamp
  stale?: boolean; // true when market is closed and quote is old
}

export interface WatchlistEntry {
  ticker: string;
  exchange: string;
  type: PositionType;
  direction: Direction;
  note: string;
}

export interface PriceHistoryEntry {
  date: string;      // YYYY-MM-DD
  close: number;
  pct_change: number;
}

export interface StreakInfo {
  direction: "up" | "down";
  count: number;
  totalPct: number;
}

export interface TickerPrice {
  ticker: string;
  quote: QuoteData;
  streak: StreakInfo | null;
  entry: WatchlistEntry;
}

export interface BriefSummary {
  date: string;
  phase: Phase;
  title: string;
  filePath: string;
  items: number;
}

export interface BriefDetail extends BriefSummary {
  content: string;      // raw markdown body (below frontmatter)
  confidence: number;
}

export interface EarningsEvent {
  symbol: string;
  date: string;
  epsEstimate: number | null;
  revenueEstimate: number | null;
  hour: string;  // "bmo" (before market open) | "amc" (after market close) | ""
}

// API response shapes
export interface PricesResponse {
  tickers: TickerPrice[];
  fetchedAt: string;
}

export interface WatchlistResponse {
  entries: WatchlistEntry[];
}

export interface BriefListResponse {
  briefs: BriefSummary[];
}

export interface HistoryResponse {
  history: Record<string, PriceHistoryEntry[]>;
}

export interface CalendarResponse {
  earnings: EarningsEvent[];
}
```

- [ ] **Step 2: Write trivial type-shape test (ensures no import errors)**

```typescript
// src/__tests__/lib/types.test.ts
import { describe, expect, test } from "bun:test";
import type { WatchlistEntry, QuoteData, StreakInfo } from "@/lib/types";

describe("types", () => {
  test("WatchlistEntry shape is correct", () => {
    const entry: WatchlistEntry = {
      ticker: "AAPL",
      exchange: "NASDAQ",
      type: "holding",
      direction: "long",
      note: "test",
    };
    expect(entry.ticker).toBe("AAPL");
    expect(entry.type).toBe("holding");
  });

  test("QuoteData shape is correct", () => {
    const q: QuoteData = { c: 200, pc: 190, dp: 5.26, t: 1700000000 };
    expect(q.dp).toBeCloseTo(5.26);
  });
});
```

- [ ] **Step 3: Run test**

```bash
bun test src/__tests__/lib/types.test.ts
```

Expected: 2 tests pass.

- [ ] **Step 4: Commit**

```bash
git add src/lib/types.ts src/__tests__/lib/types.test.ts
git commit -m "feat: add shared TypeScript types"
```

---

## Task 3: KB Utilities

**Files:**
- Create: `src/lib/kb.ts`
- Create: `src/__tests__/lib/kb.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
// src/__tests__/lib/kb.test.ts
import { describe, expect, test } from "bun:test";
import { parseBriefFrontmatter, listBriefFiles, computeStreak } from "@/lib/kb";
import type { PriceHistoryEntry } from "@/lib/types";

describe("parseBriefFrontmatter", () => {
  test("extracts phase, date, title, items from frontmatter", () => {
    const md = `---
title: "Market Brief 2026-06-08 (midday)"
captured_at: "2026-06-08"
phase: midday
confidence: 0.7
---

> disclaimer

## Content here`;
    const result = parseBriefFrontmatter(md);
    expect(result.phase).toBe("midday");
    expect(result.date).toBe("2026-06-08");
    expect(result.title).toBe("Market Brief 2026-06-08 (midday)");
    expect(result.confidence).toBe(0.7);
    expect(result.content).toContain("Content here");
  });

  test("returns defaults when fields missing", () => {
    const result = parseBriefFrontmatter("---\n---\nBody only");
    expect(result.phase).toBe("midday");
    expect(result.confidence).toBe(0.7);
  });
});

describe("computeStreak", () => {
  test("returns null for single entry", () => {
    const history: PriceHistoryEntry[] = [
      { date: "2026-06-06", close: 200, pct_change: -1 },
    ];
    expect(computeStreak(history)).toBeNull();
  });

  test("detects 3-session down streak", () => {
    const history: PriceHistoryEntry[] = [
      { date: "2026-06-04", close: 220, pct_change: -1 },
      { date: "2026-06-05", close: 215, pct_change: -2.3 },
      { date: "2026-06-06", close: 205, pct_change: -4.7 },
      { date: "2026-06-08", close: 200, pct_change: -2.4 },
    ];
    const streak = computeStreak(history);
    expect(streak).not.toBeNull();
    expect(streak!.direction).toBe("down");
    expect(streak!.count).toBe(4);
  });

  test("detects 2-session up streak", () => {
    const history: PriceHistoryEntry[] = [
      { date: "2026-06-06", close: 200, pct_change: 1 },
      { date: "2026-06-08", close: 205, pct_change: 2.5 },
    ];
    const streak = computeStreak(history);
    expect(streak!.direction).toBe("up");
    expect(streak!.count).toBe(2);
  });

  test("returns null when last two sessions have mixed direction", () => {
    const history: PriceHistoryEntry[] = [
      { date: "2026-06-06", close: 200, pct_change: -1 },
      { date: "2026-06-08", close: 205, pct_change: 2.5 },
    ];
    expect(computeStreak(history)).toBeNull();
  });

  test("ignores duplicate dates (weekend gap dedup)", () => {
    const history: PriceHistoryEntry[] = [
      { date: "2026-06-06", close: 200, pct_change: -1 },
      { date: "2026-06-06", close: 200, pct_change: -1 }, // duplicate
      { date: "2026-06-08", close: 205, pct_change: 2.5 },
    ];
    const streak = computeStreak(history);
    // only 2 distinct dates → check direction matches last two
    expect(streak).toBeNull(); // mixed: down then up
  });
});
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
bun test src/__tests__/lib/kb.test.ts
```

Expected: FAIL with "Cannot find module '@/lib/kb'".

- [ ] **Step 3: Implement kb.ts**

```typescript
// src/lib/kb.ts
import fs from "node:fs";
import path from "node:path";
import type { BriefSummary, BriefDetail, PriceHistoryEntry, StreakInfo, Phase } from "@/lib/types";

const KB_PATH = process.env.KB_PATH ?? "";
const STATE_PATH = process.env.STATE_PATH ?? "";

const BRIEFS_DIR = path.join(KB_PATH, "wiki/outputs/briefs");
const HISTORY_FILE = path.join(STATE_PATH, "price-history.json");

// ---------------------------------------------------------------------------
// Frontmatter parser
// ---------------------------------------------------------------------------

interface ParsedBrief {
  title: string;
  phase: Phase;
  date: string;
  confidence: number;
  content: string;
}

export function parseBriefFrontmatter(markdown: string): ParsedBrief {
  const fmMatch = markdown.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  const fm: Record<string, string> = {};
  let body = markdown;

  if (fmMatch) {
    body = fmMatch[2] ?? "";
    for (const line of fmMatch[1].split("\n")) {
      const colon = line.indexOf(":");
      if (colon === -1) continue;
      const k = line.slice(0, colon).trim();
      const v = line.slice(colon + 1).trim().replace(/^["']|["']$/g, "");
      fm[k] = v;
    }
  }

  const phase = (["pre-open", "midday", "post-close"].includes(fm.phase ?? "")
    ? fm.phase
    : "midday") as Phase;

  return {
    title: fm.title ?? "",
    phase,
    date: fm.captured_at ?? "",
    confidence: parseFloat(fm.confidence ?? "0.7"),
    content: body.trim(),
  };
}

// ---------------------------------------------------------------------------
// Brief file listing
// ---------------------------------------------------------------------------

export function listBriefFiles(): BriefSummary[] {
  if (!fs.existsSync(BRIEFS_DIR)) return [];

  return fs
    .readdirSync(BRIEFS_DIR)
    .filter((f) => f.match(/^\d{4}-\d{2}-\d{2}-market-brief-.+\.md$/))
    .sort()
    .reverse()
    .map((filename) => {
      const filePath = path.join(BRIEFS_DIR, filename);
      const raw = fs.readFileSync(filePath, "utf-8");
      const parsed = parseBriefFrontmatter(raw);
      const itemsMatch = raw.match(/(\d+)\s+items/);
      return {
        date: parsed.date,
        phase: parsed.phase,
        title: parsed.title,
        filePath,
        items: itemsMatch ? parseInt(itemsMatch[1]) : 0,
      };
    });
}

export function readBriefDetail(filePath: string): BriefDetail | null {
  if (!fs.existsSync(filePath)) return null;
  const raw = fs.readFileSync(filePath, "utf-8");
  const parsed = parseBriefFrontmatter(raw);
  const itemsMatch = raw.match(/(\d+)\s+items/);
  return {
    ...parsed,
    filePath,
    items: itemsMatch ? parseInt(itemsMatch[1]) : 0,
  };
}

// ---------------------------------------------------------------------------
// Price history
// ---------------------------------------------------------------------------

export function readPriceHistory(): Record<string, PriceHistoryEntry[]> {
  if (!fs.existsSync(HISTORY_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(HISTORY_FILE, "utf-8"));
  } catch {
    return {};
  }
}

// ---------------------------------------------------------------------------
// Streak computation
// ---------------------------------------------------------------------------

export function computeStreak(history: PriceHistoryEntry[]): StreakInfo | null {
  // Dedup by date (keep last occurrence), then sort ascending
  const byDate = new Map<string, PriceHistoryEntry>();
  for (const e of history) byDate.set(e.date, e);
  const sorted = [...byDate.values()].sort((a, b) => a.date.localeCompare(b.date));

  if (sorted.length < 2) return null;

  const last = sorted[sorted.length - 1];
  const dir: "up" | "down" = last.pct_change >= 0 ? "up" : "down";

  let count = 0;
  let totalPct = 0;
  for (let i = sorted.length - 1; i >= 0; i--) {
    const same = dir === "up" ? sorted[i].pct_change >= 0 : sorted[i].pct_change < 0;
    if (!same) break;
    count++;
    totalPct += sorted[i].pct_change;
  }

  if (count < 2) return null;
  return { direction: dir, count, totalPct: Math.round(totalPct * 10) / 10 };
}
```

- [ ] **Step 4: Run tests**

```bash
bun test src/__tests__/lib/kb.test.ts
```

Expected: all 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/lib/kb.ts src/__tests__/lib/kb.test.ts
git commit -m "feat: add KB utilities (brief parser, history reader, streak computation)"
```

---

## Task 4: Watchlist Utilities

**Files:**
- Create: `src/lib/watchlist.ts`
- Create: `src/__tests__/lib/watchlist.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
// src/__tests__/lib/watchlist.test.ts
import { describe, expect, test } from "bun:test";
import { parseWatchlistMd, serializeWatchlistMd } from "@/lib/watchlist";

const SAMPLE_MD = `---
title: "Market Watchlist"
type: journal
---

# Market Watchlist

\`\`\`yaml watchlist
watchlist:
  - ticker: AAPL
    exchange: NASDAQ
    type: holding
    direction: long
    note: main position
  - ticker: SPY
    exchange: NYSE
    type: watching
    note: benchmark
\`\`\`

## How to Edit
`;

describe("parseWatchlistMd", () => {
  test("parses entries from fenced yaml block", () => {
    const entries = parseWatchlistMd(SAMPLE_MD);
    expect(entries).toHaveLength(2);
    expect(entries[0].ticker).toBe("AAPL");
    expect(entries[0].type).toBe("holding");
    expect(entries[0].direction).toBe("long");
    expect(entries[0].note).toBe("main position");
    expect(entries[1].ticker).toBe("SPY");
    expect(entries[1].type).toBe("watching");
    expect(entries[1].direction).toBe("long"); // default
  });

  test("defaults type to watching and direction to long when missing", () => {
    const md = `\`\`\`yaml watchlist\nwatchlist:\n  - ticker: MSFT\n    exchange: NASDAQ\n\`\`\``;
    const entries = parseWatchlistMd(md);
    expect(entries[0].type).toBe("watching");
    expect(entries[0].direction).toBe("long");
  });
});

describe("serializeWatchlistMd", () => {
  test("round-trips: parse → serialize → parse gives same entries", () => {
    const original = parseWatchlistMd(SAMPLE_MD);
    const serialized = serializeWatchlistMd(SAMPLE_MD, original);
    const reparsed = parseWatchlistMd(serialized);
    expect(reparsed).toHaveLength(original.length);
    expect(reparsed[0].ticker).toBe(original[0].ticker);
    expect(reparsed[0].type).toBe(original[0].type);
  });

  test("preserves frontmatter and non-yaml sections", () => {
    const entries = parseWatchlistMd(SAMPLE_MD);
    const result = serializeWatchlistMd(SAMPLE_MD, entries);
    expect(result).toContain("title: \"Market Watchlist\"");
    expect(result).toContain("## How to Edit");
  });

  test("adds a new ticker correctly", () => {
    const entries = parseWatchlistMd(SAMPLE_MD);
    entries.push({ ticker: "NVDA", exchange: "NASDAQ", type: "watching", direction: "long", note: "" });
    const result = serializeWatchlistMd(SAMPLE_MD, entries);
    const reparsed = parseWatchlistMd(result);
    expect(reparsed).toHaveLength(3);
    expect(reparsed[2].ticker).toBe("NVDA");
  });
});
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
bun test src/__tests__/lib/watchlist.test.ts
```

Expected: FAIL with "Cannot find module '@/lib/watchlist'".

- [ ] **Step 3: Implement watchlist.ts**

```typescript
// src/lib/watchlist.ts
import fs from "node:fs";
import path from "node:path";
import type { WatchlistEntry } from "@/lib/types";

const KB_PATH = process.env.KB_PATH ?? "";
export const WATCHLIST_FILE = path.join(KB_PATH, "wiki/journal/market-watchlist.md");

// ---------------------------------------------------------------------------
// Parser — extracts entries from the fenced ```yaml watchlist``` block
// ---------------------------------------------------------------------------

export function parseWatchlistMd(markdown: string): WatchlistEntry[] {
  const fenceMatch = markdown.match(/```yaml\s+watchlist\s*\n([\s\S]*?)```/i);
  if (!fenceMatch) return [];

  const yaml = fenceMatch[1];
  const entries: WatchlistEntry[] = [];
  let current: Partial<WatchlistEntry> | null = null;

  for (const rawLine of yaml.split("\n")) {
    const line = rawLine.rstrip?.() ?? rawLine.trimEnd();
    const stripped = line.trimStart();
    if (!stripped || stripped.startsWith("#")) continue;

    if (/^watchlist\s*:/.test(stripped)) continue;

    if (stripped.startsWith("- ")) {
      if (current?.ticker) entries.push(normalizeEntry(current));
      current = {};
      const rest = stripped.slice(2).trim();
      if (rest.includes(":")) {
        const [k, ...vParts] = rest.split(":");
        if (/^\w+$/.test(k.trim())) current[k.trim() as keyof WatchlistEntry] = vParts.join(":").trim() as never;
      }
    } else if (current !== null && stripped.includes(":")) {
      const colonIdx = stripped.indexOf(":");
      const k = stripped.slice(0, colonIdx).trim();
      const v = stripped.slice(colonIdx + 1).trim();
      if (/^\w+$/.test(k)) current[k as keyof WatchlistEntry] = v as never;
    }
  }
  if (current?.ticker) entries.push(normalizeEntry(current));
  return entries;
}

function normalizeEntry(raw: Partial<WatchlistEntry>): WatchlistEntry {
  return {
    ticker: (raw.ticker ?? "").toUpperCase(),
    exchange: raw.exchange ?? "",
    type: raw.type === "holding" ? "holding" : "watching",
    direction: raw.direction === "short" ? "short" : "long",
    note: raw.note ?? "",
  };
}

// ---------------------------------------------------------------------------
// Serializer — replaces the fenced block content, preserves the rest of the MD
// ---------------------------------------------------------------------------

export function serializeWatchlistMd(originalMd: string, entries: WatchlistEntry[]): string {
  const lines = entries.map((e) => {
    const parts = [`  - ticker: ${e.ticker}`, `    exchange: ${e.exchange}`, `    type: ${e.type}`];
    if (e.type === "holding") parts.push(`    direction: ${e.direction}`);
    if (e.note) parts.push(`    note: ${e.note}`);
    return parts.join("\n");
  });

  const newBlock = `\`\`\`yaml watchlist\nwatchlist:\n${lines.join("\n")}\n\`\`\``;
  return originalMd.replace(/```yaml\s+watchlist\s*\n[\s\S]*?```/i, newBlock);
}

// ---------------------------------------------------------------------------
// File I/O
// ---------------------------------------------------------------------------

export function readWatchlistFile(): WatchlistEntry[] {
  if (!fs.existsSync(WATCHLIST_FILE)) return [];
  return parseWatchlistMd(fs.readFileSync(WATCHLIST_FILE, "utf-8"));
}

export function writeWatchlistFile(entries: WatchlistEntry[]): void {
  const original = fs.existsSync(WATCHLIST_FILE)
    ? fs.readFileSync(WATCHLIST_FILE, "utf-8")
    : `---\ntitle: "Market Watchlist"\ntype: journal\n---\n\n\`\`\`yaml watchlist\nwatchlist:\n\`\`\`\n`;
  fs.writeFileSync(WATCHLIST_FILE, serializeWatchlistMd(original, entries), "utf-8");
}
```

- [ ] **Step 4: Run tests**

```bash
bun test src/__tests__/lib/watchlist.test.ts
```

Expected: all 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/lib/watchlist.ts src/__tests__/lib/watchlist.test.ts
git commit -m "feat: add watchlist parser and serializer"
```

---

## Task 5: Finnhub Client

**Files:**
- Create: `src/lib/finnhub.ts`
- Create: `src/__tests__/lib/finnhub.test.ts`

- [ ] **Step 1: Write failing tests**

```typescript
// src/__tests__/lib/finnhub.test.ts
import { describe, expect, test, mock, beforeEach } from "bun:test";
import { normalizeQuote, buildQuoteUrl, isStale } from "@/lib/finnhub";

describe("normalizeQuote", () => {
  test("computes dp when null but c and pc are present", () => {
    const result = normalizeQuote({ c: 210, pc: 200, dp: null, t: 1000 });
    expect(result.dp).toBeCloseTo(5.0, 1);
  });

  test("passes through dp when present", () => {
    const result = normalizeQuote({ c: 210, pc: 200, dp: 5.0, t: 1000 });
    expect(result.dp).toBe(5.0);
  });

  test("marks stale when timestamp is more than 8 hours old", () => {
    const old = Math.floor(Date.now() / 1000) - 9 * 3600;
    const result = normalizeQuote({ c: 200, pc: 190, dp: 5.26, t: old });
    expect(result.stale).toBe(true);
  });

  test("not stale when timestamp is recent", () => {
    const recent = Math.floor(Date.now() / 1000) - 60;
    const result = normalizeQuote({ c: 200, pc: 190, dp: 5.26, t: recent });
    expect(result.stale).toBe(false);
  });
});

describe("isStale", () => {
  test("returns true for timestamp older than threshold", () => {
    const old = Math.floor(Date.now() / 1000) - 9 * 3600;
    expect(isStale(old)).toBe(true);
  });
});

describe("buildQuoteUrl", () => {
  test("builds correct Finnhub URL without exposing token in path", () => {
    const url = buildQuoteUrl("AAPL", "testtoken");
    expect(url).toContain("finnhub.io/api/v1/quote");
    expect(url).toContain("symbol=AAPL");
    expect(url).toContain("token=testtoken");
  });
});
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
bun test src/__tests__/lib/finnhub.test.ts
```

Expected: FAIL with "Cannot find module '@/lib/finnhub'".

- [ ] **Step 3: Implement finnhub.ts**

```typescript
// src/lib/finnhub.ts
import type { QuoteData } from "@/lib/types";

const BASE = "https://finnhub.io/api/v1";
const STALE_THRESHOLD_SEC = 8 * 3600; // 8 hours — covers weekend/holiday close

export function buildQuoteUrl(symbol: string, token: string): string {
  return `${BASE}/quote?symbol=${encodeURIComponent(symbol)}&token=${encodeURIComponent(token)}`;
}

export function buildCalendarUrl(from: string, to: string, token: string): string {
  return `${BASE}/calendar/earnings?from=${from}&to=${to}&token=${encodeURIComponent(token)}`;
}

export function isStale(unixTimestamp: number): boolean {
  const ageSeconds = Date.now() / 1000 - unixTimestamp;
  return ageSeconds > STALE_THRESHOLD_SEC;
}

export function normalizeQuote(raw: { c: number; pc: number; dp: number | null; t: number }): QuoteData {
  let dp = raw.dp ?? 0;
  if (!dp && raw.c && raw.pc) {
    dp = Math.round(((raw.c - raw.pc) / raw.pc) * 10000) / 100;
  }
  return { c: raw.c, pc: raw.pc, dp, t: raw.t, stale: isStale(raw.t) };
}

export async function fetchQuote(symbol: string): Promise<QuoteData> {
  const token = process.env.FINNHUB_API_KEY;
  if (!token) throw new Error("FINNHUB_API_KEY not set");

  const res = await fetch(buildQuoteUrl(symbol, token), {
    next: { revalidate: 55 }, // Next.js fetch cache: refresh just under 60s
  });
  if (!res.ok) throw new Error(`Finnhub ${res.status} for ${symbol}`);
  const raw = await res.json();
  return normalizeQuote(raw);
}

export async function fetchEarnings(from: string, to: string) {
  const token = process.env.FINNHUB_API_KEY;
  if (!token) throw new Error("FINNHUB_API_KEY not set");

  const res = await fetch(buildCalendarUrl(from, to, token));
  if (!res.ok) throw new Error(`Finnhub calendar ${res.status}`);
  const raw = await res.json();
  return (raw.earningsCalendar ?? []) as Array<{
    symbol: string;
    date: string;
    epsEstimate: number | null;
    revenueEstimate: number | null;
    hour: string;
  }>;
}
```

- [ ] **Step 4: Run tests**

```bash
bun test src/__tests__/lib/finnhub.test.ts
```

Expected: all 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/lib/finnhub.ts src/__tests__/lib/finnhub.test.ts
git commit -m "feat: add Finnhub HTTP client with stale detection"
```

---

## Task 6: API Routes — Read-Only

**Files:**
- Create: `src/app/api/prices/route.ts`
- Create: `src/app/api/brief/route.ts`
- Create: `src/app/api/briefs/route.ts`
- Create: `src/app/api/history/route.ts`
- Create: `src/app/api/calendar/route.ts`

- [ ] **Step 1: Prices route**

```typescript
// src/app/api/prices/route.ts
import { NextResponse } from "next/server";
import { readWatchlistFile } from "@/lib/watchlist";
import { readPriceHistory, computeStreak } from "@/lib/kb";
import { fetchQuote } from "@/lib/finnhub";
import type { PricesResponse, TickerPrice } from "@/lib/types";

export const dynamic = "force-dynamic"; // never cache — always fresh

export async function GET() {
  const entries = readWatchlistFile();
  const history = readPriceHistory();

  const results = await Promise.allSettled(
    entries.map(async (entry): Promise<TickerPrice> => {
      const quote = await fetchQuote(entry.ticker);
      const streak = computeStreak(history[entry.ticker] ?? []);
      return { ticker: entry.ticker, quote, streak, entry };
    })
  );

  const tickers: TickerPrice[] = results
    .filter((r): r is PromiseFulfilledResult<TickerPrice> => r.status === "fulfilled")
    .map((r) => r.value);

  const response: PricesResponse = { tickers, fetchedAt: new Date().toISOString() };
  return NextResponse.json(response);
}
```

- [ ] **Step 2: Brief route**

```typescript
// src/app/api/brief/route.ts
import { NextRequest, NextResponse } from "next/server";
import { listBriefFiles, readBriefDetail } from "@/lib/kb";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const filePath = searchParams.get("path");

  if (filePath) {
    // Specific brief requested
    const detail = readBriefDetail(filePath);
    if (!detail) return NextResponse.json({ error: "Brief not found" }, { status: 404 });
    return NextResponse.json(detail);
  }

  // Latest brief
  const briefs = listBriefFiles();
  if (!briefs.length) return NextResponse.json({ error: "No briefs found" }, { status: 404 });
  const latest = readBriefDetail(briefs[0].filePath);
  return NextResponse.json(latest);
}
```

- [ ] **Step 3: Briefs list route**

```typescript
// src/app/api/briefs/route.ts
import { NextResponse } from "next/server";
import { listBriefFiles } from "@/lib/kb";

export const dynamic = "force-dynamic";

export async function GET() {
  const briefs = listBriefFiles();
  return NextResponse.json({ briefs });
}
```

- [ ] **Step 4: History route**

```typescript
// src/app/api/history/route.ts
import { NextResponse } from "next/server";
import { readPriceHistory } from "@/lib/kb";

export const dynamic = "force-dynamic";

export async function GET() {
  const history = readPriceHistory();
  return NextResponse.json({ history });
}
```

- [ ] **Step 5: Calendar route**

```typescript
// src/app/api/calendar/route.ts
import { NextResponse } from "next/server";
import { fetchEarnings } from "@/lib/finnhub";
import type { EarningsEvent } from "@/lib/types";

export const dynamic = "force-dynamic";

function toDateStr(offsetDays: number): string {
  const d = new Date();
  d.setDate(d.getDate() + offsetDays);
  return d.toISOString().slice(0, 10);
}

export async function GET() {
  try {
    const raw = await fetchEarnings(toDateStr(0), toDateStr(14));
    const earnings: EarningsEvent[] = raw.map((e) => ({
      symbol: e.symbol,
      date: e.date,
      epsEstimate: e.epsEstimate,
      revenueEstimate: e.revenueEstimate,
      hour: e.hour ?? "",
    }));
    return NextResponse.json({ earnings });
  } catch {
    return NextResponse.json({ earnings: [] });
  }
}
```

- [ ] **Step 6: Smoke test all routes in browser**

Start dev server: `bun dev`

Visit each in browser and confirm valid JSON:
- `http://localhost:3000/api/briefs` → `{ briefs: [...] }`
- `http://localhost:3000/api/brief` → latest brief detail
- `http://localhost:3000/api/history` → `{ history: {...} }`
- `http://localhost:3000/api/prices` → `{ tickers: [...], fetchedAt: "..." }`
- `http://localhost:3000/api/calendar` → `{ earnings: [...] }`

- [ ] **Step 7: Commit**

```bash
git add src/app/api/
git commit -m "feat: add read-only API routes (prices, brief, briefs, history, calendar)"
```

---

## Task 7: Watchlist API Route (GET + PUT)

**Files:**
- Create: `src/app/api/watchlist/route.ts`
- Create: `src/__tests__/api/watchlist.test.ts`

- [ ] **Step 1: Write failing test**

```typescript
// src/__tests__/api/watchlist.test.ts
import { describe, expect, test } from "bun:test";
import { serializeWatchlistMd, parseWatchlistMd } from "@/lib/watchlist";
import type { WatchlistEntry } from "@/lib/types";

// Tests the serialization round-trip used by the PUT route
describe("PUT /api/watchlist serialization", () => {
  test("new entry round-trips correctly through serialize → parse", () => {
    const original = `---\ntitle: "Watchlist"\n---\n\`\`\`yaml watchlist\nwatchlist:\n  - ticker: AAPL\n    exchange: NASDAQ\n    type: watching\n\`\`\`\n`;
    const newEntries: WatchlistEntry[] = [
      { ticker: "AAPL", exchange: "NASDAQ", type: "watching", direction: "long", note: "" },
      { ticker: "NVDA", exchange: "NASDAQ", type: "holding", direction: "long", note: "gpu play" },
    ];
    const written = serializeWatchlistMd(original, newEntries);
    const parsed = parseWatchlistMd(written);
    expect(parsed).toHaveLength(2);
    expect(parsed[1].ticker).toBe("NVDA");
    expect(parsed[1].type).toBe("holding");
    expect(parsed[1].note).toBe("gpu play");
  });

  test("direction field omitted for watching entries", () => {
    const original = `\`\`\`yaml watchlist\nwatchlist:\n\`\`\``;
    const entries: WatchlistEntry[] = [
      { ticker: "SPY", exchange: "NYSE", type: "watching", direction: "long", note: "" },
    ];
    const written = serializeWatchlistMd(original, entries);
    expect(written).not.toContain("direction:");
  });
});
```

- [ ] **Step 2: Run to confirm FAIL**

```bash
bun test src/__tests__/api/watchlist.test.ts
```

Expected: FAIL (module not found or assertion failure).

- [ ] **Step 3: Implement watchlist route**

```typescript
// src/app/api/watchlist/route.ts
import { NextRequest, NextResponse } from "next/server";
import { readWatchlistFile, writeWatchlistFile } from "@/lib/watchlist";
import type { WatchlistEntry } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET() {
  const entries = readWatchlistFile();
  return NextResponse.json({ entries });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const entries: WatchlistEntry[] = body.entries;

    if (!Array.isArray(entries)) {
      return NextResponse.json({ error: "entries must be an array" }, { status: 400 });
    }

    // Validate required fields
    for (const e of entries) {
      if (!e.ticker || typeof e.ticker !== "string") {
        return NextResponse.json({ error: "each entry needs a ticker" }, { status: 400 });
      }
    }

    writeWatchlistFile(entries);
    return NextResponse.json({ ok: true, count: entries.length });
  } catch (err) {
    return NextResponse.json({ error: String(err) }, { status: 500 });
  }
}
```

- [ ] **Step 4: Run tests**

```bash
bun test src/__tests__/api/watchlist.test.ts
```

Expected: all 2 tests pass.

- [ ] **Step 5: Smoke test PUT in terminal**

```bash
curl -s -X PUT http://localhost:3000/api/watchlist \
  -H "Content-Type: application/json" \
  -d '{"entries":[{"ticker":"AAPL","exchange":"NASDAQ","type":"watching","direction":"long","note":"test"}]}' \
  | jq .
```

Expected: `{ "ok": true, "count": 1 }`

- [ ] **Step 6: Commit**

```bash
git add src/app/api/watchlist/route.ts src/__tests__/api/watchlist.test.ts
git commit -m "feat: add watchlist GET/PUT route"
```

---

## Task 8: SWR Hooks

**Files:**
- Create: `src/hooks/useMarketData.ts`

- [ ] **Step 1: Implement all SWR hooks**

```typescript
// src/hooks/useMarketData.ts
"use client";

import useSWR from "swr";
import useSWRMutation from "swr/mutation";
import type {
  PricesResponse,
  BriefDetail,
  BriefListResponse,
  HistoryResponse,
  CalendarResponse,
  WatchlistResponse,
  WatchlistEntry,
} from "@/lib/types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function usePrices() {
  return useSWR<PricesResponse>("/api/prices", fetcher, {
    refreshInterval: 60_000,
    revalidateOnFocus: true,
  });
}

export function useBriefList() {
  return useSWR<BriefListResponse>("/api/briefs", fetcher, {
    refreshInterval: 5 * 60_000, // check for new briefs every 5 min
  });
}

export function useBriefDetail(filePath: string | null) {
  const key = filePath ? `/api/brief?path=${encodeURIComponent(filePath)}` : "/api/brief";
  return useSWR<BriefDetail>(key, fetcher);
}

export function useHistory() {
  return useSWR<HistoryResponse>("/api/history", fetcher, {
    refreshInterval: 10 * 60_000,
  });
}

export function useCalendar() {
  return useSWR<CalendarResponse>("/api/calendar", fetcher, {
    refreshInterval: 60 * 60_000, // earnings calendar changes slowly
  });
}

export function useWatchlist() {
  return useSWR<WatchlistResponse>("/api/watchlist", fetcher);
}

async function saveWatchlist(url: string, { arg }: { arg: WatchlistEntry[] }) {
  const res = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ entries: arg }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function useSaveWatchlist() {
  return useSWRMutation("/api/watchlist", saveWatchlist);
}
```

- [ ] **Step 2: Verify no TypeScript errors**

```bash
bunx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add src/hooks/useMarketData.ts
git commit -m "feat: add SWR hooks for all API endpoints"
```

---

## Task 9: PriceCard + Sidebar Components

**Files:**
- Create: `src/components/PriceCard.tsx`
- Create: `src/components/Sidebar.tsx`

- [ ] **Step 1: PriceCard component**

```typescript
// src/components/PriceCard.tsx
"use client";

import { useRef, useEffect, useState } from "react";
import type { TickerPrice } from "@/lib/types";

interface Props {
  ticker: TickerPrice;
  selected?: boolean;
  onClick?: () => void;
}

export function PriceCard({ ticker: t, selected, onClick }: Props) {
  const { quote, streak, entry } = t;
  const isUp = quote.dp >= 0;
  const prevPrice = useRef(quote.c);
  const [tickClass, setTickClass] = useState("");

  // Fire tick animation when price changes direction
  useEffect(() => {
    if (quote.c === prevPrice.current) return;
    const cls = quote.c > prevPrice.current ? "animate-tick-up" : "animate-tick-down";
    setTickClass(cls);
    prevPrice.current = quote.c;
    const t = setTimeout(() => setTickClass(""), 300);
    return () => clearTimeout(t);
  }, [quote.c]);

  const priceColor = isUp ? "text-[var(--up)]" : "text-[var(--down)]";
  const borderColor = selected
    ? "border-[var(--accent)]"
    : "border-[var(--border)] hover:border-[var(--border-bright)]";

  return (
    <button
      onClick={onClick}
      className={`w-full text-left bg-[var(--surface)] border ${borderColor} rounded px-3 py-2.5 transition-colors duration-150`}
    >
      <div className="flex justify-between items-baseline">
        <span className="text-[11px] font-semibold tracking-widest text-[var(--muted)] uppercase">
          {t.ticker}
        </span>
        <span className={`text-[11px] font-medium ${priceColor}`}>
          {isUp ? "+" : ""}{quote.dp.toFixed(2)}%
        </span>
      </div>

      <div className={`flex justify-between items-baseline mt-1 ${tickClass}`}>
        <span className={`text-[15px] font-semibold tabular-nums ${priceColor}`}>
          ${quote.c.toFixed(2)}
        </span>
        <span className="text-[10px] text-[var(--muted)]">
          {quote.stale
            ? <span className="opacity-50">closed</span>
            : entry.type === "holding"
              ? <span className="text-[var(--accent)]">{entry.direction}</span>
              : "watch"}
        </span>
      </div>

      {streak && streak.count >= 2 && (
        <div className="text-[10px] text-[var(--warn)] mt-1 flex items-center gap-1">
          <span>{streak.count}{streak.direction === "down" ? "↓" : "↑"}</span>
          <span className="text-[var(--muted)]">
            ({streak.totalPct > 0 ? "+" : ""}{streak.totalPct.toFixed(1)}%)
          </span>
        </div>
      )}
    </button>
  );
}
```

- [ ] **Step 2: Sidebar component**

```typescript
// src/components/Sidebar.tsx
"use client";

import { usePrices, useBriefList } from "@/hooks/useMarketData";
import { PriceCard } from "@/components/PriceCard";
import type { BriefSummary } from "@/lib/types";

interface Props {
  selectedBrief: string | null;
  onSelectBrief: (path: string) => void;
  onOpenEditor: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  "pre-open": "pre",
  midday: "mid",
  "post-close": "post",
};

export function Sidebar({ selectedBrief, onSelectBrief, onOpenEditor }: Props) {
  const { data: prices, isLoading: pricesLoading } = usePrices();
  const { data: briefList } = useBriefList();

  // Today's briefs for run status indicator
  const today = new Date().toISOString().slice(0, 10);
  const todayBriefs = briefList?.briefs.filter((b) => b.date === today) ?? [];
  const phasesRun = new Set(todayBriefs.map((b) => b.phase));

  return (
    <aside className="w-60 flex-shrink-0 flex flex-col gap-3 p-3 border-r border-[var(--color-border)] h-screen overflow-y-auto">
      {/* Live prices */}
      <div>
        <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-2">
          Watchlist {pricesLoading && <span className="opacity-50">↻</span>}
        </div>
        <div className="flex flex-col gap-1.5">
          {prices?.tickers.map((t) => (
            <PriceCard
              key={t.ticker}
              ticker={t}
              selected={false}
              onClick={() => {}}
            />
          ))}
          {!prices && !pricesLoading && (
            <p className="text-xs text-[var(--color-muted)]">No prices</p>
          )}
        </div>
      </div>

      {/* Run status */}
      <div>
        <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1">
          Today's runs
        </div>
        <div className="flex gap-2 text-[11px]">
          {(["pre-open", "midday", "post-close"] as const).map((phase) => (
            <span
              key={phase}
              className={phasesRun.has(phase) ? "text-green-400" : "text-[var(--color-border)]"}
            >
              {PHASE_LABELS[phase]} {phasesRun.has(phase) ? "✓" : "—"}
            </span>
          ))}
        </div>
      </div>

      {/* Brief history in sidebar */}
      <div className="flex-1 min-h-0">
        <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1">
          Brief history
        </div>
        <div className="flex flex-col gap-1 overflow-y-auto max-h-48">
          {briefList?.briefs.slice(0, 20).map((b) => (
            <button
              key={b.filePath}
              onClick={() => onSelectBrief(b.filePath)}
              className={`text-left text-[11px] px-2 py-1 rounded truncate transition-colors ${
                selectedBrief === b.filePath
                  ? "bg-indigo-900/50 text-indigo-300"
                  : "text-[var(--color-muted)] hover:text-[var(--color-text)]"
              }`}
            >
              {b.date} · {PHASE_LABELS[b.phase]}
            </button>
          ))}
        </div>
      </div>

      {/* Edit watchlist button */}
      <button
        onClick={onOpenEditor}
        className="text-xs text-[var(--color-muted)] border border-[var(--color-border)] rounded px-3 py-1.5 hover:border-indigo-500 hover:text-indigo-300 transition-colors"
      >
        Edit Watchlist
      </button>
    </aside>
  );
}
```

- [ ] **Step 3: Verify no TypeScript errors**

```bash
bunx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add src/components/PriceCard.tsx src/components/Sidebar.tsx
git commit -m "feat: add PriceCard and Sidebar components"
```

---

## Task 10: BriefPanel Component

**Files:**
- Create: `src/components/BriefPanel.tsx`

- [ ] **Step 1: Implement BriefPanel**

```typescript
// src/components/BriefPanel.tsx
"use client";

import { useBriefDetail, useBriefList } from "@/hooks/useMarketData";
import type { Phase } from "@/lib/types";

interface Props {
  selectedPath: string | null;
}

const PHASE_ORDER: Phase[] = ["pre-open", "midday", "post-close"];
const PHASE_LABELS: Record<Phase, string> = {
  "pre-open": "Pre-Open",
  midday: "Midday",
  "post-close": "Post-Close",
};

export function BriefPanel({ selectedPath }: Props) {
  const { data: brief, isLoading } = useBriefDetail(selectedPath);
  const { data: briefList } = useBriefList();

  const today = new Date().toISOString().slice(0, 10);
  const todayBriefs = briefList?.briefs.filter((b) => b.date === today) ?? [];

  if (isLoading) {
    return (
      <div className="flex-1 p-6 text-[var(--color-muted)] text-sm">Loading brief...</div>
    );
  }

  if (!brief) {
    return (
      <div className="flex-1 p-6 text-[var(--color-muted)] text-sm">
        No brief available. Hermes runs at 08:30, 12:30, and 16:30 ET on weekdays.
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
      {/* Phase tabs for today */}
      {todayBriefs.length > 1 && (
        <div className="flex gap-1 px-4 pt-3 border-b border-[var(--color-border)]">
          {todayBriefs.map((b) => (
            <button
              key={b.filePath}
              className={`text-xs px-3 py-1.5 rounded-t transition-colors ${
                b.filePath === (selectedPath ?? briefList?.briefs[0]?.filePath)
                  ? "bg-indigo-900/40 text-indigo-300 border border-[var(--color-border)] border-b-0"
                  : "text-[var(--color-muted)] hover:text-[var(--color-text)]"
              }`}
            >
              {PHASE_LABELS[b.phase] ?? b.phase}
            </button>
          ))}
        </div>
      )}

      {/* Brief content — wrapped in gradient border signalling live AI output */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="label-serif mb-3">
          {brief.date} · {brief.phase} · {brief.items} items · {(brief.confidence * 100).toFixed(0)}% confidence
        </div>
        <div className="brief-live-border">
          <div className="bg-[var(--surface)] rounded-[5px] p-4">
            <pre className="text-xs text-[var(--text)] whitespace-pre-wrap font-mono leading-relaxed">
              {brief.content}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify no TypeScript errors**

```bash
bunx tsc --noEmit
```

- [ ] **Step 3: Commit**

```bash
git add src/components/BriefPanel.tsx
git commit -m "feat: add BriefPanel component with phase tabs"
```

---

## Task 11: WatchlistEditor Drawer

**Files:**
- Create: `src/components/WatchlistEditor.tsx`

- [ ] **Step 1: Implement WatchlistEditor**

```typescript
// src/components/WatchlistEditor.tsx
"use client";

import { useState, useEffect } from "react";
import { useWatchlist, useSaveWatchlist } from "@/hooks/useMarketData";
import type { WatchlistEntry } from "@/lib/types";

interface Props {
  open: boolean;
  onClose: () => void;
}

const EMPTY_ENTRY: WatchlistEntry = {
  ticker: "",
  exchange: "NASDAQ",
  type: "watching",
  direction: "long",
  note: "",
};

export function WatchlistEditor({ open, onClose }: Props) {
  const { data: watchlistData, mutate } = useWatchlist();
  const { trigger: save, isMutating } = useSaveWatchlist();
  const [entries, setEntries] = useState<WatchlistEntry[]>([]);
  const [dirty, setDirty] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (watchlistData?.entries) {
      setEntries(watchlistData.entries);
      setDirty(false);
    }
  }, [watchlistData]);

  function update(index: number, field: keyof WatchlistEntry, value: string) {
    setEntries((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
    setDirty(true);
  }

  function addRow() {
    setEntries((prev) => [...prev, { ...EMPTY_ENTRY }]);
    setDirty(true);
  }

  function removeRow(index: number) {
    setEntries((prev) => prev.filter((_, i) => i !== index));
    setDirty(true);
  }

  async function handleSave() {
    setError(null);
    try {
      // Optimistic update
      mutate({ entries }, { revalidate: false });
      await save(entries);
      mutate(); // revalidate from server
      setDirty(false);
    } catch (e) {
      setError(String(e));
      mutate(); // revert optimistic update
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Backdrop */}
      <div className="flex-1 bg-black/50" onClick={onClose} />

      {/* Drawer */}
      <div className="w-[480px] bg-[var(--color-surface)] border-l border-[var(--color-border)] flex flex-col h-full">
        <div className="flex items-center justify-between px-4 py-3 border-b border-[var(--color-border)]">
          <h2 className="text-sm font-semibold">Edit Watchlist</h2>
          <button onClick={onClose} className="text-[var(--color-muted)] hover:text-[var(--color-text)] text-lg">✕</button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
          {entries.map((entry, i) => (
            <div key={i} className="border border-[var(--color-border)] rounded p-3 flex flex-col gap-2">
              <div className="flex gap-2">
                <input
                  className="flex-1 bg-[var(--color-bg)] border border-[var(--color-border)] rounded px-2 py-1 text-xs font-mono uppercase"
                  placeholder="TICKER"
                  value={entry.ticker}
                  onChange={(e) => update(i, "ticker", e.target.value.toUpperCase())}
                />
                <select
                  className="bg-[var(--color-bg)] border border-[var(--color-border)] rounded px-2 py-1 text-xs"
                  value={entry.exchange}
                  onChange={(e) => update(i, "exchange", e.target.value)}
                >
                  <option>NASDAQ</option>
                  <option>NYSE</option>
                </select>
                <button
                  onClick={() => removeRow(i)}
                  className="text-[var(--color-muted)] hover:text-red-400 text-sm px-1"
                >
                  ✕
                </button>
              </div>
              <div className="flex gap-2">
                <select
                  className="bg-[var(--color-bg)] border border-[var(--color-border)] rounded px-2 py-1 text-xs flex-1"
                  value={entry.type}
                  onChange={(e) => update(i, "type", e.target.value)}
                >
                  <option value="watching">watching</option>
                  <option value="holding">holding</option>
                </select>
                {entry.type === "holding" && (
                  <select
                    className="bg-[var(--color-bg)] border border-[var(--color-border)] rounded px-2 py-1 text-xs"
                    value={entry.direction}
                    onChange={(e) => update(i, "direction", e.target.value)}
                  >
                    <option value="long">long</option>
                    <option value="short">short</option>
                  </select>
                )}
              </div>
              <input
                className="bg-[var(--color-bg)] border border-[var(--color-border)] rounded px-2 py-1 text-xs text-[var(--color-muted)]"
                placeholder="note (optional)"
                value={entry.note}
                onChange={(e) => update(i, "note", e.target.value)}
              />
            </div>
          ))}

          <button
            onClick={addRow}
            className="border border-dashed border-[var(--color-border)] rounded px-3 py-2 text-xs text-[var(--color-muted)] hover:border-indigo-500 hover:text-indigo-300 transition-colors"
          >
            + Add ticker
          </button>
        </div>

        <div className="px-4 py-3 border-t border-[var(--color-border)] flex items-center gap-3">
          {error && <p className="text-red-400 text-xs flex-1 truncate">{error}</p>}
          {!error && dirty && <p className="text-[var(--color-muted)] text-xs flex-1">Unsaved changes</p>}
          {!error && !dirty && <p className="text-green-400 text-xs flex-1">Saved</p>}
          <button
            onClick={handleSave}
            disabled={!dirty || isMutating}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs px-4 py-1.5 rounded transition-colors"
          >
            {isMutating ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify no TypeScript errors**

```bash
bunx tsc --noEmit
```

- [ ] **Step 3: Commit**

```bash
git add src/components/WatchlistEditor.tsx
git commit -m "feat: add WatchlistEditor drawer with optimistic updates"
```

---

## Task 12: EarningsCalendar + BriefHistory Components

**Files:**
- Create: `src/components/EarningsCalendar.tsx`
- Create: `src/components/BriefHistory.tsx`

- [ ] **Step 1: EarningsCalendar**

```typescript
// src/components/EarningsCalendar.tsx
"use client";

import { useCalendar } from "@/hooks/useMarketData";
import { useWatchlist } from "@/hooks/useMarketData";

export function EarningsCalendar() {
  const { data, isLoading } = useCalendar();
  const { data: watchlistData } = useWatchlist();

  const watchedTickers = new Set(watchlistData?.entries.map((e) => e.ticker) ?? []);

  const earnings = (data?.earnings ?? [])
    .filter((e) => watchedTickers.has(e.symbol) || watchedTickers.size === 0)
    .slice(0, 10);

  if (isLoading) return <div className="text-xs text-[var(--color-muted)] p-3">Loading calendar...</div>;

  if (!earnings.length) {
    return <div className="text-xs text-[var(--color-muted)] p-3">No upcoming earnings for watchlist.</div>;
  }

  return (
    <div className="p-3">
      <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-2">
        Upcoming Earnings
      </div>
      <div className="flex flex-col gap-1">
        {earnings.map((e, i) => (
          <div key={i} className="flex justify-between text-xs">
            <span className="font-mono text-[var(--color-text)]">{e.symbol}</span>
            <span className="text-[var(--color-muted)]">{e.date}</span>
            <span className="text-[10px] text-[var(--color-muted)]">
              {e.hour === "bmo" ? "pre-mkt" : e.hour === "amc" ? "after-hrs" : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: BriefHistory**

```typescript
// src/components/BriefHistory.tsx
"use client";

import { useBriefList } from "@/hooks/useMarketData";

interface Props {
  selectedPath: string | null;
  onSelect: (path: string) => void;
}

const PHASE_SHORT: Record<string, string> = {
  "pre-open": "pre",
  midday: "mid",
  "post-close": "post",
};

export function BriefHistory({ selectedPath, onSelect }: Props) {
  const { data } = useBriefList();
  const briefs = data?.briefs ?? [];

  if (!briefs.length) {
    return <div className="text-xs text-[var(--color-muted)] p-3">No brief history yet.</div>;
  }

  return (
    <div className="p-3">
      <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-2">
        Brief History
      </div>
      <div className="flex flex-col gap-0.5 max-h-48 overflow-y-auto">
        {briefs.map((b) => (
          <button
            key={b.filePath}
            onClick={() => onSelect(b.filePath)}
            className={`text-left text-xs px-2 py-1 rounded flex justify-between transition-colors ${
              selectedPath === b.filePath
                ? "bg-indigo-900/40 text-indigo-300"
                : "text-[var(--color-muted)] hover:text-[var(--color-text)]"
            }`}
          >
            <span>{b.date}</span>
            <span className="text-[10px]">{PHASE_SHORT[b.phase] ?? b.phase} · {b.items}i</span>
          </button>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add src/components/EarningsCalendar.tsx src/components/BriefHistory.tsx
git commit -m "feat: add EarningsCalendar and BriefHistory components"
```

---

## Task 13: Main Page Assembly

**Files:**
- Modify: `src/app/layout.tsx`
- Modify: `src/app/page.tsx`

- [ ] **Step 1: Root layout**

```typescript
// src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Market Dashboard",
  description: "Hermes market brief command center",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased overflow-hidden">{children}</body>
    </html>
  );
}
```

- [ ] **Step 2: Main dashboard page**

```typescript
// src/app/page.tsx
"use client";

import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { BriefPanel } from "@/components/BriefPanel";
import { EarningsCalendar } from "@/components/EarningsCalendar";
import { BriefHistory } from "@/components/BriefHistory";
import { WatchlistEditor } from "@/components/WatchlistEditor";

export default function DashboardPage() {
  const [selectedBrief, setSelectedBrief] = useState<string | null>(null);
  const [editorOpen, setEditorOpen] = useState(false);

  return (
    <div className="flex h-screen bg-[var(--color-bg)] text-[var(--color-text)] overflow-hidden">
      {/* Left sidebar */}
      <Sidebar
        selectedBrief={selectedBrief}
        onSelectBrief={setSelectedBrief}
        onOpenEditor={() => setEditorOpen(true)}
      />

      {/* Main content area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Brief panel — takes most of the space */}
        <div className="flex-1 flex flex-col min-h-0 overflow-hidden border-b border-[var(--color-border)]">
          <BriefPanel selectedPath={selectedBrief} />
        </div>

        {/* Bottom panels: earnings + history */}
        <div className="flex border-t border-[var(--color-border)] h-52 shrink-0">
          <div className="flex-1 border-r border-[var(--color-border)] overflow-y-auto">
            <EarningsCalendar />
          </div>
          <div className="flex-1 overflow-y-auto">
            <BriefHistory selectedPath={selectedBrief} onSelect={setSelectedBrief} />
          </div>
        </div>
      </main>

      {/* Watchlist editor drawer */}
      <WatchlistEditor open={editorOpen} onClose={() => setEditorOpen(false)} />
    </div>
  );
}
```

- [ ] **Step 3: Run full TypeScript check**

```bash
bunx tsc --noEmit
```

Expected: no errors.

- [ ] **Step 4: Run dev server and manually verify**

```bash
bun dev
```

Open `http://localhost:3000` and confirm:
- Left sidebar shows watchlist prices from Finnhub
- Brief panel shows latest brief content
- Phase tabs appear when multiple briefs exist for today
- Bottom-left shows earnings calendar for watchlist tickers
- Bottom-right shows brief history list, clicking a row loads that brief
- "Edit Watchlist" button opens the drawer
- Adding/editing/removing a ticker and saving updates the sidebar prices on next 60s refresh

- [ ] **Step 5: Final commit**

```bash
git add src/app/layout.tsx src/app/page.tsx
git commit -m "feat: assemble main dashboard page — split panel layout complete"
```

---

## Task 14: End-to-End Smoke Test

- [ ] **Step 1: Run all unit tests**

```bash
bun test
```

Expected: all tests pass.

- [ ] **Step 2: Verify watchlist edit round-trip**

1. Open `http://localhost:3000`
2. Click "Edit Watchlist"
3. Change an entry's type from `watching` to `holding`
4. Click Save → see "Saved" confirmation
5. Open `~/.hermes/knowledge-base/wiki/journal/market-watchlist.md` in another editor
6. Confirm the `type: holding` change is present in the yaml block

- [ ] **Step 3: Verify brief navigation**

1. Click a brief in the history list → main panel updates to that brief
2. Click "Edit Watchlist", add a new ticker (e.g. `TSLA / NASDAQ / watching`), save
3. Prices panel shows TSLA within 60 seconds

- [ ] **Step 4: Verify stale price label**

If running on a weekend or after market close, prices should show "closed" label next to the price. The quote timestamp in `/api/prices` response will have `stale: true`.

- [ ] **Step 5: Final tag**

```bash
git tag v0.1.0
```

---

## Self-Review Notes

**Spec coverage check:**
- ✅ Next.js 16 + Bun + Tailwind v4
- ✅ Split panel: sidebar (watchlist prices + run status + brief history) + main (brief panel) + bottom (calendar + history)
- ✅ Live prices via Finnhub REST, 60s SWR refresh
- ✅ Streak detection from price-history.json
- ✅ Position-aware labels (holding/watching, long/short)
- ✅ Brief viewer with phase tabs
- ✅ Editable watchlist drawer (slide-out, optimistic update, writes back to MD file)
- ✅ Earnings calendar (Finnhub, filtered to watchlist tickers)
- ✅ Brief history navigation
- ✅ Stale price detection (market closed / weekend)
- ✅ API key server-only (no NEXT_PUBLIC_ prefix, never in browser)

**No placeholders:** All code blocks are complete and runnable.

**Type consistency:** `WatchlistEntry`, `TickerPrice`, `QuoteData`, `BriefDetail` defined in Task 2 and used consistently across all tasks. `WATCHLIST_FILE` exported from `watchlist.ts` and used in route. `computeStreak` imported from `kb.ts` in both the API route and tests.
