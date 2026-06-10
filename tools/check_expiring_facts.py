"""Surface facts whose validity is about to expire.

Reads the personal-facts JSONL and prints rows whose `valid_to` falls within
N days of today (default 60). Designed to feed the Monday AI briefing — the
output is plain markdown bullets that can be appended to the briefing page.

Each row prints id, predicate, valid_to, days remaining (negative = already
expired). Sensitive values are NOT printed (would defeat the privacy posture);
only metadata is shown so the briefing surface stays low-sensitivity.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from wiki_utils import RAW_DIR


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"


def parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        # Accept YYYY-MM-DD or full ISO timestamps.
        return datetime.fromisoformat(value.split("T")[0]).date()
    except ValueError:
        return None


def load_records(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--facts", type=Path, default=DEFAULT_FACTS)
    parser.add_argument(
        "--within",
        default="60d",
        help="Time window, e.g. 30d, 60d, 180d (default: %(default)s)",
    )
    parser.add_argument(
        "--include-expired",
        action="store_true",
        help="Also include rows whose valid_to is already in the past",
    )
    parser.add_argument(
        "--today",
        help="Override 'today' (YYYY-MM-DD) — useful for tests",
    )
    args = parser.parse_args(argv)

    if not args.within.endswith("d"):
        print("error: --within must end with 'd' (e.g., 60d)", file=sys.stderr)
        return 2
    try:
        window_days = int(args.within[:-1])
    except ValueError:
        print("error: invalid --within value: {0}".format(args.within), file=sys.stderr)
        return 2

    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        print("error: invalid --today value", file=sys.stderr)
        return 2
    horizon = today + timedelta(days=window_days)

    records = load_records(args.facts)
    rows: List[Dict[str, Any]] = []
    for record in records:
        valid_to = parse_date(record.get("valid_to"))
        if valid_to is None:
            continue
        if valid_to > horizon:
            continue
        if not args.include_expired and valid_to < today:
            continue
        rows.append({
            "id": record.get("id"),
            "category": record.get("category"),
            "predicate": record.get("predicate"),
            "valid_to": record.get("valid_to"),
            "days": (valid_to - today).days,
            "tags": record.get("tags") or [],
        })

    rows.sort(key=lambda r: r["days"])

    print("# Expiring facts (within {0}d, as of {1})".format(window_days, today.isoformat()))
    print()
    if not rows:
        print("- No expiring facts in the window.")
        return 0
    for row in rows:
        marker = "expired" if row["days"] < 0 else "in {0}d".format(row["days"])
        tags = ", ".join(row["tags"]) if row["tags"] else "—"
        print("- `{id}` ({category}/{predicate}) — valid_to {valid_to} ({marker}); tags: {tags}".format(
            id=row["id"],
            category=row["category"],
            predicate=row["predicate"],
            valid_to=row["valid_to"],
            marker=marker,
            tags=tags,
        ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
