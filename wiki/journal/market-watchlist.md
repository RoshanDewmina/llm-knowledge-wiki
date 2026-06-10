---
title: "Market Watchlist"
type: journal
tags: ["market/watchlist", "ibkr", "trading"]
created: "2026-06-07T00:00:00Z"
updated: "2026-06-07T00:00:00Z"
status: draft
confidence: 0.8
related: []
compiled_at: "2026-06-07T13:20:00Z"
source_pages: []
---

# Market Watchlist

This file is the user-editable watchlist for the market-brief skill. Tickers listed here get quote data, news, and SEC filings pulled at each briefing run.

```yaml watchlist
watchlist:
  - ticker: AAPL
    exchange: NASDAQ
    type: watching
    note: example — replace with your actual holdings
  - ticker: MSFT
    exchange: NASDAQ
    type: watching
    note: example — replace with your actual holdings
  - ticker: NVDA
    exchange: NASDAQ
    type: watching
    note: example — replace with your actual holdings
  - ticker: SPY
    exchange: NYSE
    type: watching
    note: broad market ETF benchmark
  - ticker: QQQ
    exchange: NASDAQ
    type: watching
    note: tech ETF benchmark
```

## How to Edit This File

- To add a stock: add a new `- ticker: SYMBOL` block under `watchlist:` and set `exchange: NYSE` or `exchange: NASDAQ`
- `type:` — `holding` if you own it, `watching` if you're monitoring it (default: `watching`). Holdings get position-aware framing in the brief ("paper loss on your long").
- `direction:` — `long` or `short` (default: `long`). Only meaningful when `type: holding`. Flips the framing for short positions.
- `note:` is optional context for your reference only — not used in analysis
- `cost_basis:` is an optional informational field; never used in any advice or analysis
- Tickers must be US-listed (NYSE or NASDAQ) — non-US tickers will have limited or no Finnhub coverage
- Save the file and the next briefing run will automatically pick up the changes

## Related

- [[index]]
- [[outputs/briefs/2026-05-07-ai-briefing]]
