"""Detect wiki pages whose source material or source pages changed after compilation."""

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
    sha256_file,
    wiki_ref_to_path,
)


def raw_source_for_source_page(frontmatter: dict[str, Any]) -> Path:
    """Resolve the raw source file for a source page."""

    source_path = frontmatter.get("source_path")
    if not isinstance(source_path, str):
        raise ValueError("source_path must be a string")
    return ensure_under_root(resolve_repo_path(source_path), RAW_DIR)


def source_page_status(source_ref: str) -> dict[str, Any]:
    """Resolve the current status for one source page."""

    source_page_path = wiki_ref_to_path(str(source_ref))
    source_frontmatter, _ = load_markdown_page(source_page_path)
    raw_path = raw_source_for_source_page(source_frontmatter)
    current_hash = sha256_file(raw_path)
    expected_hash = source_frontmatter.get("source_hash")
    if not isinstance(expected_hash, str) or not expected_hash:
        raise ValueError(f"source page missing source_hash: {source_ref}")
    compiled_at = parse_timestamp(str(source_frontmatter["compiled_at"]))
    return {
        "ref": str(source_ref),
        "path": source_page_path,
        "frontmatter": source_frontmatter,
        "raw_path": raw_path,
        "current_hash": current_hash,
        "expected_hash": expected_hash,
        "compiled_at": compiled_at,
    }


def collect_stale_entries() -> list[dict[str, str]]:
    """Collect stale wiki entries using stable hash and source-page timestamps."""

    stale: list[dict[str, str]] = []
    for page in load_wiki_pages(include_special=False):
        page_type = str(page.frontmatter.get("type", ""))
        if page_type == "source":
            try:
                raw_path = raw_source_for_source_page(page.frontmatter)
                current_hash = sha256_file(raw_path)
                expected_hash = page.frontmatter.get("source_hash")
                if not isinstance(expected_hash, str) or not expected_hash:
                    raise ValueError("source_hash missing or invalid")
            except (KeyError, FileNotFoundError, ValueError) as exc:
                stale.append({"path": repo_relative(page.path), "reason": str(exc)})
                continue
            if current_hash != expected_hash:
                stale.append(
                    {
                        "path": repo_relative(page.path),
                        "reason": f"source hash mismatch: {repo_relative(raw_path)}",
                    }
                )
            continue

        if page_type not in DERIVED_TYPES:
            continue

        try:
            compiled_at = parse_timestamp(str(page.frontmatter["compiled_at"]))
            source_pages = page.frontmatter.get("source_pages", [])
            if not isinstance(source_pages, list):
                raise ValueError("source_pages must be a list")
            if not source_pages:
                raise ValueError("source_pages must not be empty")
        except (KeyError, ValueError) as exc:
            stale.append({"path": repo_relative(page.path), "reason": str(exc)})
            continue

        page_reason = ""
        for source_ref in source_pages:
            try:
                status = source_page_status(str(source_ref))
            except (KeyError, FileNotFoundError, ValueError) as exc:
                page_reason = str(exc)
                break
            if status["current_hash"] != status["expected_hash"]:
                page_reason = f"source page stale: {status['ref']}"
                break
            if status["compiled_at"] > compiled_at:
                page_reason = f"source page newer than compiled_at: {status['ref']}"
                break

        if page_reason:
            stale.append({"path": repo_relative(page.path), "reason": page_reason})

    return stale


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    stale = collect_stale_entries()

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
