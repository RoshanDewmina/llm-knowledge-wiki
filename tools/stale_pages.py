"""Detect wiki pages whose source material changed after compilation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from wiki_utils import (
    DERIVED_TYPES,
    RAW_DIR,
    ensure_under_root,
    load_markdown_page,
    load_wiki_pages,
    parse_timestamp,
    repo_relative,
    resolve_repo_path,
    wiki_ref_to_path,
)


def raw_sources_for_page(page_type: str, frontmatter: dict[str, Any]) -> list[Path]:
    """Resolve raw source files for a wiki page."""

    if page_type == "source":
        source_path = frontmatter.get("source_path")
        if not isinstance(source_path, str):
            raise ValueError("source_path must be a string")
        return [ensure_under_root(resolve_repo_path(source_path), RAW_DIR)]

    if page_type in DERIVED_TYPES:
        source_paths: list[Path] = []
        source_pages = frontmatter.get("source_pages", [])
        if not isinstance(source_pages, list):
            raise ValueError("source_pages must be a list")
        for item in source_pages:
            source_page_path = wiki_ref_to_path(str(item))
            source_frontmatter, _ = load_markdown_page(source_page_path)
            source_path = source_frontmatter.get("source_path")
            if not isinstance(source_path, str):
                raise ValueError(f"source page missing source_path: {item}")
            source_paths.append(ensure_under_root(resolve_repo_path(source_path), RAW_DIR))
        return source_paths

    return []


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    stale: list[dict[str, str]] = []

    for page in load_wiki_pages(include_special=False):
        page_type = str(page.frontmatter.get("type", ""))
        if page_type not in {"source"} | DERIVED_TYPES:
            continue
        try:
            compiled_at = parse_timestamp(str(page.frontmatter["compiled_at"]))
            raw_paths = raw_sources_for_page(page_type, page.frontmatter)
        except (KeyError, FileNotFoundError, ValueError) as exc:
            stale.append({"path": repo_relative(page.path), "reason": str(exc)})
            continue
        newest_source = max(raw_paths, key=lambda raw_path: raw_path.stat().st_mtime)
        newest_source_mtime = newest_source.stat().st_mtime
        if newest_source_mtime > compiled_at.timestamp():
            stale.append(
                {
                    "path": repo_relative(page.path),
                    "reason": f"source newer than compiled_at: {repo_relative(newest_source)}",
                }
            )

    if args.json:
        print(json.dumps(stale, indent=2))
    elif stale:
        for item in stale:
            print(f"{item['path']}: {item['reason']}")
    else:
        print("ok: no stale pages detected")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())

