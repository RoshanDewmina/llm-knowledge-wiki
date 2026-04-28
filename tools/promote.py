"""Promote a study into a durable output scaffold."""

from __future__ import annotations
import argparse
from pathlib import Path
from wiki_utils import WIKI_DIR, humanize_slug, load_markdown_page, now_utc, render_markdown_page, slugify, write_text_if_changed

TARGET_DIRS = {"brief": "briefs", "table": "tables", "timeline": "timelines", "slides": "slides"}


def extract_section(body: str, heading: str) -> str:
    capture = False; lines = []
    for line in body.splitlines():
        if line.startswith("## "):
            if capture: break
            capture = line[3:].strip().lower() == heading.lower()
            continue
        if capture: lines.append(line)
    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--target", choices=sorted(TARGET_DIRS), default="brief")
    args = parser.parse_args()
    slug = slugify(args.slug)
    study_path = WIKI_DIR / "studies" / "papers" / f"{slug}.md"
    if not study_path.exists():
        print(f"error: missing study page: {study_path.relative_to(WIKI_DIR.parent)}")
        return 2
    sfm, sbody = load_markdown_page(study_path)
    timestamp = now_utc()
    title = f"{sfm.get('title', humanize_slug(slug))} {args.target.title()}"
    out_path = WIKI_DIR / "outputs" / TARGET_DIRS[args.target] / f"{slug}.md"
    notes = extract_section(sbody, "My Notes") or "- Add synthesized notes here before publishing."
    citations = extract_section(sbody, "Citations") or "- Citation pass pending. Do not publish until exact source anchors are added."
    fm = {
        "title": title,
        "type": "output",
        "created": timestamp,
        "updated": timestamp,
        "status": "draft",
        "confidence": 0.3,
        "related": [f"studies/papers/{slug}"],
        "source_pages": [f"studies/papers/{slug}"],
        "compiled_at": timestamp,
    }
    body = f"""# {title}

## Summary

{notes}

## Citations

{citations}

## Contradictions

- No contradictions recorded yet.
"""
    if out_path.exists():
        print(f"unchanged: {out_path.relative_to(WIKI_DIR.parent)}")
    else:
        write_text_if_changed(out_path, render_markdown_page(fm, body))
        print(f"created: {out_path.relative_to(WIKI_DIR.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
