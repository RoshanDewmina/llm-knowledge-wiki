"""Generate a JSON manifest for the local wiki frontend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any, Dict, List

from wiki_utils import (
    RAW_DIR,
    WIKI_DIR,
    extract_first_heading,
    extract_wikilinks,
    frontmatter_refs,
    is_special_wiki_page,
    iter_markdown_files,
    load_markdown_page,
    load_optional_markdown_page,
    normalize_wiki_ref,
    now_utc,
    path_to_wiki_ref,
    repo_relative,
    slugify_heading,
    write_text_if_changed,
)

OUTPUT_PATH = WIKI_DIR / ".cache" / "site-manifest.json"
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+)$", re.MULTILINE)


def strip_markdown_syntax(markdown: str) -> str:
    """Remove the most visible markdown syntax for excerpt generation."""

    return (
        markdown.replace("[[", "")
        .replace("]]", "")
        .replace("`", " ")
        .replace("*", " ")
        .replace("_", " ")
        .replace(">", " ")
        .replace("#", " ")
    )


def remove_leading_title(body: str, title: str) -> str:
    """Remove a duplicate H1 when it matches the frontmatter title."""

    lines = body.splitlines()
    if not lines:
        return body.strip()
    first = lines[0].strip()
    if first.startswith("# ") and first[2:].strip().lower() == title.strip().lower():
        return "\n".join(lines[1:]).strip()
    return body.strip()


def excerpt_from_markdown(markdown: str, fallback: str = "") -> str:
    """Build a short excerpt from markdown content."""

    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        return strip_markdown_syntax(stripped).strip()
    return fallback.strip()


def section_for_target(target: str) -> str:
    """Return the top-level wiki section for a target."""

    return "index" if target in {"index", "log", "inbox"} else target.split("/", 1)[0]


def serialize_headings(markdown: str) -> List[Dict[str, Any]]:
    """Serialize headings into a simple JSON shape."""

    headings: List[Dict[str, Any]] = []
    for match in HEADING_RE.finditer(markdown):
        text = match.group(2).strip()
        headings.append({"depth": len(match.group(1)), "text": text, "id": slugify_heading(text)})
    return headings


def serialize_wiki_page(path: Path) -> Dict[str, Any]:
    """Serialize one wiki markdown page for the frontend."""

    ref = path_to_wiki_ref(path)
    if is_special_wiki_page(ref):
        frontmatter: Dict[str, Any] = {}
        body = path.read_text(encoding="utf-8")
    else:
        frontmatter, body = load_markdown_page(path)

    title = str(frontmatter.get("title") or extract_first_heading(body) or path.stem.replace("-", " ").title())
    markdown = remove_leading_title(body, title)
    outbound_targets = sorted(set(extract_wikilinks(body) + frontmatter_refs(frontmatter)))
    relative_path = path.resolve().relative_to(WIKI_DIR.resolve()).as_posix()

    return {
        "title": title,
        "type": str(frontmatter.get("type") or ("operational" if is_special_wiki_page(ref) else section_for_target(ref)[:-1])),
        "target": ref,
        "relative_path": relative_path,
        "section": section_for_target(ref),
        "frontmatter": frontmatter,
        "markdown": markdown,
        "headings": serialize_headings(markdown),
        "excerpt": str(frontmatter.get("description") or excerpt_from_markdown(markdown)),
        "outbound_targets": outbound_targets,
        "source_path": str(frontmatter.get("source_path", "")).strip() or None,
        "source_url": str(frontmatter.get("source_url", "")).strip() or None,
    }


def serialize_raw_document(path: Path) -> Dict[str, Any]:
    """Serialize one raw markdown file for the frontend."""

    frontmatter, body = load_optional_markdown_page(path)
    title = str(frontmatter.get("title") or extract_first_heading(body) or path.stem.replace("-", " ").title())
    markdown = remove_leading_title(body, title)
    return {
        "title": title,
        "relative_path": repo_relative(path),
        "frontmatter": frontmatter,
        "markdown": markdown,
        "headings": serialize_headings(markdown),
        "excerpt": str(frontmatter.get("description") or excerpt_from_markdown(markdown)),
        "source_url": str(frontmatter.get("source_url", "")).strip() or None,
        "source_domain": str(frontmatter.get("source_domain", "")).strip() or None,
    }


def build_manifest() -> Dict[str, Any]:
    """Build the site manifest payload."""

    wiki_pages = [serialize_wiki_page(path) for path in iter_markdown_files(WIKI_DIR)]
    raw_documents = [serialize_raw_document(path) for path in iter_markdown_files(RAW_DIR)]
    generated_at = now_utc()
    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        if existing.get("pages") == wiki_pages and existing.get("raw_documents") == raw_documents:
            generated_at = str(existing.get("generated_at") or generated_at)
    return {
        "generated_at": generated_at,
        "pages": wiki_pages,
        "raw_documents": raw_documents,
    }


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print the manifest instead of writing it")
    args = parser.parse_args()

    manifest = build_manifest()
    payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.stdout:
        print(payload, end="")
        return 0

    changed = write_text_if_changed(OUTPUT_PATH, payload)
    print("updated: {0}".format(repo_relative(OUTPUT_PATH)) if changed else "no changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
