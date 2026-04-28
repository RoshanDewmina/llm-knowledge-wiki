"""List concept wikilinks in studies that do not have pages yet."""

from __future__ import annotations
import argparse
from pathlib import Path
from wiki_utils import WIKI_DIR, extract_wikilinks, load_markdown_page, normalize_wiki_ref, repo_relative, slugify


def iter_studies(slug: str | None) -> list[Path]:
    if slug:
        return [WIKI_DIR / "studies" / "papers" / f"{slugify(slug)}.md"]
    return sorted((WIKI_DIR / "studies").rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", nargs="?")
    args = parser.parse_args()
    missing: list[tuple[str, str]] = []
    for path in iter_studies(args.slug):
        if not path.exists():
            continue
        _, body = load_markdown_page(path)
        for ref in sorted(set(extract_wikilinks(body))):
            norm = normalize_wiki_ref(ref)
            if not norm.startswith("concepts/"):
                continue
            if not (WIKI_DIR / f"{norm}.md").exists():
                missing.append((repo_relative(path), norm))
    if not missing:
        print("ok: no missing concept pages referenced by studies")
        return 0
    print("Concept candidates:")
    for study, ref in missing:
        print(f"- [ ] {ref} (referenced by {study})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
