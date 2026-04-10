"""Create a durable question note in the wiki."""

from __future__ import annotations

import argparse

from wiki_utils import WIKI_DIR, now_utc, render_markdown_page, slugify, write_text_if_changed


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Question title to scaffold")
    parser.add_argument("--slug", help="Optional slug override")
    parser.add_argument("--stdout", action="store_true", help="Print the note instead of writing it")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    timestamp = now_utc()
    title = args.question.strip()
    slug = slugify(args.slug or title)
    path = WIKI_DIR / "questions" / f"{slug}.md"

    frontmatter = {
        "title": title,
        "type": "question",
        "created": timestamp,
        "updated": timestamp,
        "status": "draft",
        "confidence": 0.3,
        "related": ["inbox", "reviews/daily-review"],
        "source_pages": [],
        "compiled_at": timestamp,
    }
    body = (
        f"# {title}\n\n"
        "## Why This Matters\n\n"
        "- Explain why this question is worth keeping in the vault.\n\n"
        "## Working Notes\n\n"
        "- Capture provisional answers or competing hypotheses here.\n\n"
        "## Pages To Inspect\n\n"
        "- List the existing wiki pages that should be read before creating a new synthesis.\n\n"
        "## Candidate Sources\n\n"
        "- Add reviewed source-page refs here, for example `sources/attention-is-all-you-need-excerpt`.\n\n"
        "## Contradictions\n\n"
        "- Record disagreements explicitly or say none are recorded yet.\n\n"
        "## Promotion Target\n\n"
        "- If answered well, should this become a concept, synthesis, project memory update, or output?\n"
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
