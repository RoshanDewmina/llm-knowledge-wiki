"""Rebuild roshan-personal-fact-index.md deterministically from the JSONL.

Reads raw/transcripts/2026/2026-05-09-roshan-personal-facts.jsonl, groups facts
by category, and rewrites the per-category bullet blocks between the
`<!-- FACTS:START -->` and `<!-- FACTS:END -->` markers in
wiki/syntheses/context/roshan-personal-fact-index.md.

Hand-maintained sections (Gaps / TODO, Citations) are left untouched. The
frontmatter `updated` field is bumped to the current UTC timestamp. The output
file is forced to chmod 0600.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Dict, List

from wiki_utils import (
    REPO_ROOT,
    RAW_DIR,
    WIKI_DIR,
    now_utc,
    read_text,
    update_marker_file,
)


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"
DEFAULT_INDEX = WIKI_DIR / "syntheses" / "context" / "roshan-personal-fact-index.md"
MARKER = "FACTS"

# Order in which category sections render. Categories not listed are appended
# alphabetically at the end.
CATEGORY_ORDER = [
    "banking",
    "contact",
    "education",
    "employment",
    "housing",
    "identity",
    "immigration",
    "passport",
    "travel",
]

CATEGORY_HEADINGS = {
    "banking": "Banking",
    "contact": "Contact",
    "education": "Education",
    "employment": "Employment",
    "housing": "Housing",
    "identity": "Identity",
    "immigration": "Immigration",
    "passport": "Passport",
    "travel": "Travel",
    "medical": "Medical",
    "family": "Family / Emergency",
    "tax": "Tax / CRA",
    "legal": "Legal Status / Expiries",
    "ids": "Government IDs",
    "preferences": "Preferences",
    "locale": "Locale / Languages",
    "career": "Career History",
}


def load_facts(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise SystemExit("invalid JSONL at line {0}: {1}".format(line_number, exc))
    return records


def render_value(value: Any) -> str:
    """Render a fact's value in a stable, search-friendly form."""

    if value is None:
        return "(none)"
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def render_metadata_line(record: Dict[str, Any]) -> str:
    parts = [
        "observed: {0}".format(record.get("observed_at", "?")),
        "confidence: {0}".format(record.get("confidence", "?")),
    ]
    tags = record.get("tags") or []
    if tags:
        parts.append("tags: {0}".format(", ".join(str(tag) for tag in tags)))
    if record.get("event_date"):
        parts.append("event {0}".format(record["event_date"]))
    valid_from = record.get("valid_from")
    valid_to = record.get("valid_to")
    if valid_from or valid_to:
        parts.append("valid {0} to {1}".format(valid_from or "?", valid_to or "?"))
    return "  - " + "; ".join(parts)


def render_record(record: Dict[str, Any]) -> List[str]:
    """Render one fact as bullet lines."""

    lines = [
        "- `{id}` `{predicate}`: {value}".format(
            id=record.get("id", "?"),
            predicate=record.get("predicate", "?"),
            value=render_value(record.get("value")),
        ),
        render_metadata_line(record),
    ]
    notes = record.get("notes")
    if notes:
        lines.append("  - note: {0}".format(notes))
    sources = record.get("source") or []
    for src in sources:
        if isinstance(src, dict):
            path = src.get("path", "")
        else:
            path = str(src)
        if path:
            lines.append("  - source: `{0}`".format(path))
    return lines


def render_category(category: str, records: List[Dict[str, Any]]) -> List[str]:
    heading = CATEGORY_HEADINGS.get(category, category.title())
    out = ["", "## {0}".format(heading), ""]
    for index, record in enumerate(records):
        out.extend(render_record(record))
        if index != len(records) - 1:
            out.append("")
    out.append("")
    return out


def build_marker_lines(records: List[Dict[str, Any]]) -> List[str]:
    """Build the full body that lives between FACTS:START and FACTS:END."""

    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for record in records:
        by_category.setdefault(record.get("category", "uncategorized"), []).append(record)

    ordered: List[str] = []
    for category in CATEGORY_ORDER:
        if category in by_category:
            ordered.append(category)
    for category in sorted(by_category):
        if category not in ordered:
            ordered.append(category)

    lines: List[str] = []
    for category in ordered:
        # Stable ordering inside a category: by id.
        records_sorted = sorted(by_category[category], key=lambda r: r.get("id", ""))
        lines.extend(render_category(category, records_sorted))
    return lines


def bump_updated_frontmatter(path: Path, timestamp: str) -> None:
    """Update the `updated:` field in the frontmatter without touching anything else."""

    text = read_text(path)
    if not text.startswith("---\n"):
        return
    end = text.find("\n---\n", 4)
    if end == -1:
        return
    head = text[: end + 5]
    body = text[end + 5 :]
    new_head_lines = []
    replaced = False
    for line in head.splitlines(keepends=True):
        if line.startswith("updated:") and not replaced:
            new_head_lines.append("updated: {0}\n".format(timestamp))
            replaced = True
        else:
            new_head_lines.append(line)
    new_text = "".join(new_head_lines) + body
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--facts", type=Path, default=DEFAULT_FACTS)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the index would change (no write)",
    )
    args = parser.parse_args(argv)

    if not args.facts.exists():
        print("error: facts file not found: {0}".format(args.facts), file=sys.stderr)
        return 2
    if not args.index.exists():
        print("error: index file not found: {0}".format(args.index), file=sys.stderr)
        return 2

    records = load_facts(args.facts)
    lines = build_marker_lines(records)

    if args.check:
        from wiki_utils import replace_marker_block

        current = read_text(args.index)
        candidate = replace_marker_block(current, MARKER, lines)
        if candidate != current:
            print("rebuild_fact_index: index is stale, rerun without --check", file=sys.stderr)
            return 1
        print("rebuild_fact_index: index up to date ({0} records)".format(len(records)))
        return 0

    changed = update_marker_file(args.index, MARKER, lines)
    if changed:
        bump_updated_frontmatter(args.index, now_utc())
        os.chmod(args.index, stat.S_IRUSR | stat.S_IWUSR)
        print("rebuild_fact_index: regenerated {0} ({1} records)".format(
            args.index.relative_to(REPO_ROOT), len(records),
        ))
    else:
        print("rebuild_fact_index: no change ({0} records)".format(len(records)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
