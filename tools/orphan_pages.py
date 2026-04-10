"""Find wiki pages with no inbound and no outbound internal links."""

from __future__ import annotations

import argparse
import json

from wiki_utils import extract_wikilinks, frontmatter_refs, is_special_wiki_page, load_wiki_pages, repo_relative


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-special", action="store_true", help="Include wiki/index.md and wiki/log.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    pages = load_wiki_pages(include_special=args.include_special)
    outbound: dict[str, set[str]] = {}
    inbound: dict[str, set[str]] = {page.ref: set() for page in pages}

    for page in pages:
        refs = set(extract_wikilinks(page.body))
        refs.update(frontmatter_refs(page.frontmatter))
        refs.discard(page.ref)
        outbound[page.ref] = refs
        for target in refs:
            if target in inbound:
                inbound[target].add(page.ref)

    orphans = []
    for page in pages:
        if not args.include_special and is_special_wiki_page(page.ref):
            continue
        if not outbound.get(page.ref) and not inbound.get(page.ref):
            orphans.append({"path": repo_relative(page.path), "ref": page.ref})

    if args.json:
        print(json.dumps(orphans, indent=2))
    elif orphans:
        for orphan in orphans:
            print(orphan["path"])
    else:
        print(f"ok: no orphan pages in {len(pages)} scanned pages")
    return 1 if orphans else 0


if __name__ == "__main__":
    raise SystemExit(main())

