"""Create a daily journal note in the wiki."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from wiki_utils import WIKI_DIR, now_utc, render_markdown_page, write_text_if_changed


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Date slug in YYYY-MM-DD format; defaults to local today")
    parser.add_argument("--title", help="Optional title override")
    parser.add_argument("--stdout", action="store_true", help="Print the note instead of writing it")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    date_slug = args.date or datetime.now().astimezone().date().isoformat()
    timestamp = now_utc()
    title = args.title or f"{date_slug} Daily Note"
    path = WIKI_DIR / "journal" / f"{date_slug}-daily-note.md"

    frontmatter = {
        "title": title,
        "type": "journal",
        "created": timestamp,
        "updated": timestamp,
        "status": "draft",
        "confidence": 0.25,
        "related": ["inbox", "reviews/daily-review"],
        "source_pages": [],
        "compiled_at": timestamp,
    }
    body = (
        f"# {title}\n\n"
        "## Focus\n\n"
        "- What matters most today?\n\n"
        "## Today's Sources\n\n"
        "- Which raw sources or wiki pages should be reviewed today?\n\n"
        "## Questions\n\n"
        "- What is unclear or worth turning into a durable `wiki/questions/` page?\n\n"
        "## Notes\n\n"
        "- Keep short working notes here before promoting anything durable.\n\n"
        "## Promote To Durable Pages\n\n"
        "- Which insight should become a concept, synthesis, project memory update, or output?\n"
    )
    content = render_markdown_page(frontmatter, body)

    if args.stdout:
        print(content)
        return 0

    if path.exists():
        print(f"unchanged: {path.relative_to(WIKI_DIR.parent)}")
        return 0

    changed = write_text_if_changed(path, content)
    print(("created" if changed else "unchanged") + f": {path.relative_to(WIKI_DIR.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
