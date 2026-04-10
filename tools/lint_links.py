"""Check broken wikilinks and markdown links in the vault."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urldefrag

from wiki_utils import (
    WIKI_DIR,
    expand_markdown_targets,
    extract_markdown_links,
    extract_wikilinks,
    frontmatter_refs,
    has_valid_remote_url_syntax,
    is_absolute_local_markdown_link,
    is_remote_url,
    is_special_wiki_page,
    load_optional_markdown_page,
    path_to_wiki_ref,
    repo_relative,
    wiki_ref_to_path,
)


def validate_page(path: Path) -> List[Dict[str, Any]]:
    """Validate one markdown page."""

    errors: List[Dict[str, Any]] = []
    in_wiki = path.is_relative_to(WIKI_DIR)
    ref = path_to_wiki_ref(path) if in_wiki else repo_relative(path)
    frontmatter, body = load_optional_markdown_page(path)
    if in_wiki and is_special_wiki_page(ref):
        frontmatter = {}

    if in_wiki:
        for target in extract_wikilinks(body):
            try:
                resolved = wiki_ref_to_path(target)
            except ValueError:
                errors.append({"path": repo_relative(path), "type": "wikilink", "target": target, "message": "empty wikilink"})
                continue
            if not resolved.exists():
                errors.append(
                    {
                        "path": repo_relative(path),
                        "type": "wikilink",
                        "target": target,
                        "message": "missing wiki target: {0}".format(target),
                    }
                )

        for target in frontmatter_refs(frontmatter):
            if not wiki_ref_to_path(target).exists():
                errors.append(
                    {
                        "path": repo_relative(path),
                        "type": "frontmatter",
                        "target": target,
                        "message": "missing frontmatter wiki target: {0}".format(target),
                    }
                )

    for target in extract_markdown_links(body):
        if target.startswith("#"):
            continue
        if is_absolute_local_markdown_link(target):
            errors.append(
                {
                    "path": repo_relative(path),
                    "type": "markdown",
                    "target": target,
                    "message": "non-portable absolute local link: {0}".format(target),
                }
            )
            continue
        clean_target, _ = urldefrag(target)
        if is_remote_url(clean_target):
            if not has_valid_remote_url_syntax(clean_target):
                errors.append(
                    {
                        "path": repo_relative(path),
                        "type": "markdown",
                        "target": target,
                        "message": "invalid remote URL syntax: {0}".format(target),
                    }
                )
            continue
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(
                {
                    "path": repo_relative(path),
                    "type": "markdown",
                    "target": target,
                    "message": "missing local link target: {0}".format(target),
                }
            )
    return errors


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional markdown files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    try:
        files = expand_markdown_targets(args.paths)
    except (FileNotFoundError, ValueError) as exc:
        print("error: {0}".format(exc))
        return 2

    errors: List[Dict[str, Any]] = []
    for path in files:
        errors.extend(validate_page(path))

    if args.json:
        print(json.dumps(errors, indent=2))
    elif errors:
        for error in errors:
            print("{0}: {1}".format(error["path"], error["message"]))
    else:
        print("ok: checked {0} markdown files".format(len(files)))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
