"""Scaffold a concept page without inventing evidence anchors."""

from __future__ import annotations
import argparse
from typing import Any

from wiki_utils import WIKI_DIR, humanize_slug, now_utc, render_markdown_page, slugify, write_text_if_changed


def scaffold(name: str, source_page: str, description: str, status: str = "stub") -> int:
    slug = slugify(name)
    title = humanize_slug(slug)
    path = WIKI_DIR / "concepts" / f"{slug}.md"
    timestamp = now_utc()
    fm: dict[str, Any] = {
        "title": title,
        "type": "concept",
        "created": timestamp,
        "updated": timestamp,
        "status": status,
        "confidence": 0.2,
        "related": [source_page] if source_page else [],
        "source_pages": [source_page] if source_page else [],
        "compiled_at": timestamp,
    }
    body = f"""# {title}

## Definition

{description or 'Stub concept seeded for paper mastery. Extend only after reading linked study/source notes.'}

## Why It Matters

- Used by active paper studies to keep mastery tracking concept-centric.

## Connections

- [[{source_page}]]

## Contradictions

- No contradictions recorded yet.

## Citations

- Exact citations pending source-page review.
"""
    content = render_markdown_page(fm, body)
    if path.exists():
        print(f"unchanged: {path.relative_to(WIKI_DIR.parent)}")
        return 0
    changed = write_text_if_changed(path, content)
    print(("created" if changed else "unchanged") + f": {path.relative_to(WIKI_DIR.parent)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--source-page", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--status", default="stub")
    args = parser.parse_args()
    return scaffold(args.name, args.source_page, args.description, args.status)


if __name__ == "__main__":
    raise SystemExit(main())
