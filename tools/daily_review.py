"""Generate a daily review page for the vault."""

from __future__ import annotations

import argparse
from typing import Any, Dict, List, Set

from review_queue import collect_incomplete_sources, collect_low_confidence, collect_stale
from wiki_utils import (
    WIKI_DIR,
    load_markdown_page,
    load_wiki_pages,
    now_utc,
    parse_timestamp,
    render_markdown_page,
    repo_relative,
    write_text_if_changed,
)


OUTPUT_PATH = WIKI_DIR / "reviews" / "daily-review.md"


def build_section(title: str, lines: List[str], empty_line: str) -> str:
    """Render one markdown section."""

    if not lines:
        lines = [empty_line]
    return "## {0}\n\n{1}\n".format(title, "\n".join(lines))


def newest_pages(page_type: str, limit: int = 5) -> List[Any]:
    """Return the newest pages of a given type."""

    pages = [page for page in load_wiki_pages(include_special=False) if str(page.frontmatter.get("type", "")) == page_type]
    pages.sort(
        key=lambda page: parse_timestamp(str(page.frontmatter.get("updated") or page.frontmatter.get("created") or now_utc())),
        reverse=True,
    )
    return pages[:limit]


def build_frontmatter(existing_frontmatter: Dict[str, Any], source_pages: List[str], now: str, changed: bool) -> Dict[str, Any]:
    """Build frontmatter for the generated daily review page."""

    created = str(existing_frontmatter.get("created") or now)
    updated = now if changed else str(existing_frontmatter.get("updated") or now)
    compiled_at = now if changed else str(existing_frontmatter.get("compiled_at") or updated)
    return {
        "title": "Daily Review",
        "type": "review",
        "created": created,
        "updated": updated,
        "status": "reviewed",
        "confidence": 0.85,
        "related": ["index", "inbox", "reviews/review-queue", "reviews/coverage-dashboard"],
        "source_pages": source_pages,
        "compiled_at": compiled_at,
    }


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print the generated markdown instead of writing it")
    args = parser.parse_args()

    recent_sources = newest_pages("source", limit=6)
    recent_journal = newest_pages("journal", limit=5)
    open_questions = [
        page
        for page in newest_pages("question", limit=12)
        if str(page.frontmatter.get("status", "")) not in {"archived", "published"}
    ]
    stale_items = collect_stale()
    incomplete_source_items = collect_incomplete_sources()
    low_confidence_items = collect_low_confidence()

    recent_source_lines = [
        "- {0} | [[{1}]] | `{2}`".format(
            page.frontmatter.get("updated") or page.frontmatter.get("created"),
            page.ref,
            page.frontmatter.get("source_path", ""),
        )
        for page in recent_sources
    ]
    journal_lines = [
        "- {0} | [[{1}]]".format(page.frontmatter.get("updated") or page.frontmatter.get("created"), page.ref)
        for page in recent_journal
    ]
    question_lines = [
        "- [[{0}]] -> status `{1}`".format(page.ref, page.frontmatter.get("status", "draft"))
        for page in open_questions
    ]
    queue_snapshot_lines = [
        f"- stale pages: `{len(stale_items)}`",
        f"- source pages still in stub/draft: `{len(incomplete_source_items)}`",
        f"- low-confidence pages: `{len(low_confidence_items)}`",
    ]

    next_actions: List[str] = []
    if incomplete_source_items:
        next_actions.append(f"- Review [[{incomplete_source_items[0]['ref']}]] and clear its extraction queue.")
    if open_questions:
        next_actions.append(f"- Decide whether [[{open_questions[0].ref}]] should become a synthesis or an output.")
    if stale_items:
        next_actions.append(f"- Refresh [[{stale_items[0]['ref']}]] because one of its raw sources changed.")
    if not next_actions:
        next_actions = [
            "- Open [[inbox]] and choose the newest source page to review.",
            "- Promote one useful journal note or question into a durable synthesis, project page, or output.",
            "- Run `python3 tools/check_wiki.py` after the next meaningful edit.",
        ]

    source_refs: Set[str] = {page.ref for page in recent_sources}
    if not source_refs:
        source_refs = {
            page.ref for page in load_wiki_pages(include_special=False) if str(page.frontmatter.get("type", "")) == "source"
        }

    existing_frontmatter: Dict[str, Any] = {}
    existing_body = ""
    if OUTPUT_PATH.exists():
        existing_frontmatter, existing_body = load_markdown_page(OUTPUT_PATH)

    body = (
        "# Daily Review\n\n"
        + build_section(
            "Today",
            [
                "- Use this page to decide what to read, review, and promote today.",
                "- Start in [[inbox]], then use this review to choose the smallest high-value next step.",
            ],
            "- No daily review summary generated yet.",
        )
        + "\n"
        + build_section("Recent Source Activity", recent_source_lines, "- No recent source pages detected.")
        + "\n"
        + build_section("Recent Journal Notes", journal_lines, "- No journal notes recorded yet.")
        + "\n"
        + build_section("Open Questions", question_lines, "- No open question notes recorded yet.")
        + "\n"
        + build_section("Review Queue Snapshot", queue_snapshot_lines, "- No review queue data recorded yet.")
        + "\n"
        + build_section("Next Best Actions", next_actions, "- No next actions generated yet.")
    )

    now = now_utc()
    changed = body.strip() != existing_body.strip()
    frontmatter = build_frontmatter(existing_frontmatter, sorted(source_refs), now, changed)
    content = render_markdown_page(frontmatter, body)

    if args.stdout:
        print(content)
        return 0

    changed = write_text_if_changed(OUTPUT_PATH, content)
    print("updated: {0}".format(repo_relative(OUTPUT_PATH)) if changed else "no changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
