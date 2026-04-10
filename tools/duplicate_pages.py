"""Flag obvious duplicate concept-like pages in the wiki."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, List

from wiki_utils import load_wiki_pages, repo_relative, slugify

DUPLICATE_TYPES = {"concept", "entity", "benchmark", "project", "synthesis", "review"}


def collect_duplicates() -> List[Dict[str, Any]]:
    """Collect duplicate groups by normalized title."""

    groups: Dict[str, List[Dict[str, str]]] = {}
    for page in load_wiki_pages(include_special=False):
        page_type = str(page.frontmatter.get("type", ""))
        if page_type not in DUPLICATE_TYPES:
            continue
        title = str(page.frontmatter.get("title", "")).strip() or page.path.stem
        key = slugify(title)
        groups.setdefault(key, []).append(
            {
                "path": repo_relative(page.path),
                "title": title,
                "type": page_type,
                "ref": page.ref,
            }
        )

    duplicates: List[Dict[str, Any]] = []
    for key, pages in sorted(groups.items()):
        if len(pages) > 1:
            duplicates.append({"normalized_title": key, "pages": pages})
    return duplicates


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    duplicates = collect_duplicates()
    if args.json:
        print(json.dumps(duplicates, indent=2))
    elif duplicates:
        for item in duplicates:
            print("duplicate title group: {0}".format(item["normalized_title"]))
            for page in item["pages"]:
                print("  - {0} [{1}]".format(page["path"], page["type"]))
    else:
        print("ok: no obvious duplicate concept-like pages")
    return 1 if duplicates else 0


if __name__ == "__main__":
    raise SystemExit(main())

