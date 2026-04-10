"""Convert a synthesis or output page into a Marp-friendly slide file."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Any

from wiki_utils import WIKI_DIR, load_markdown_page, now_utc, render_markdown_page, resolve_repo_path, write_text_if_changed

H2_SPLIT_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def body_has_slide_separators(body: str) -> bool:
    """Return True when the body already contains explicit slide separators."""

    return "\n---\n" in body or body.startswith("---\n") or body.endswith("\n---")


def split_into_section_slides(body: str, title: str) -> str:
    """Split a markdown body into Marp slides using H2 headings."""

    stripped = body.strip()
    if body_has_slide_separators(stripped):
        return stripped

    lines = stripped.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    stripped = "\n".join(lines).strip()
    matches = list(H2_SPLIT_RE.finditer(stripped))
    slides: list[str] = [f"# {title}"]
    if not matches:
        if stripped:
            slides.append(stripped)
        return "\n\n---\n\n".join(slides)

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(stripped)
        heading = match.group(1).strip()
        content = stripped[start:end].strip()
        slide_parts = [f"## {heading}"]
        if content:
            slide_parts.append(content)
        slides.append("\n\n".join(slide_parts))
    return "\n\n---\n\n".join(slides)


def default_output_path(input_path: Path) -> Path:
    """Choose the default output path for exported slides."""

    slides_dir = WIKI_DIR / "outputs" / "slides"
    if input_path.parent == slides_dir:
        return input_path
    return slides_dir / f"{input_path.stem}.slides.md"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="Synthesis or output markdown file")
    parser.add_argument("--output", help="Optional output markdown path")
    parser.add_argument("--title", help="Optional slide-deck title override")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    input_path = resolve_repo_path(args.input_path)
    if not input_path.exists() or input_path.suffix != ".md":
        print(f"error: missing markdown input: {args.input_path}")
        return 2

    frontmatter, body = load_markdown_page(input_path)
    input_type = str(frontmatter.get("type", ""))
    if input_type not in {"synthesis", "output"}:
        print(f"error: expected a synthesis or output page, found: {input_type or 'unknown'}")
        return 2

    title = args.title or str(frontmatter.get("title") or input_path.stem)
    output_path = resolve_repo_path(args.output) if args.output else default_output_path(input_path)
    timestamp = now_utc()
    slide_body = split_into_section_slides(body, title)
    existing_frontmatter: dict[str, Any] = {}
    existing_body = ""
    if output_path.exists():
        try:
            existing_frontmatter, existing_body = load_markdown_page(output_path)
        except Exception:
            existing_frontmatter = {}
            existing_body = ""

    base_frontmatter = {
        "title": title,
        "type": "output",
        "created": str(existing_frontmatter.get("created") or frontmatter.get("created") or timestamp),
        "status": str(frontmatter.get("status") or "draft"),
        "confidence": frontmatter.get("confidence", 0.5),
        "related": frontmatter.get("related", []),
        "source_pages": frontmatter.get("source_pages", []),
        "marp": True,
        "theme": "default",
        "paginate": True,
    }
    unchanged = existing_frontmatter and existing_body == slide_body and all(
        existing_frontmatter.get(key) == value for key, value in base_frontmatter.items()
    )
    if unchanged:
        print("unchanged: {0}".format(output_path.relative_to(WIKI_DIR.parent).as_posix()))
        return 0

    output_frontmatter = dict(base_frontmatter)
    output_frontmatter["updated"] = timestamp
    output_frontmatter["compiled_at"] = timestamp
    changed = write_text_if_changed(output_path, render_markdown_page(output_frontmatter, slide_body))
    print(f"{'updated' if changed else 'unchanged'}: {output_path.relative_to(WIKI_DIR.parent).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
