"""Scaffold an Obsidian Spaced Repetition deck for a study."""

from __future__ import annotations
import argparse
from scaffold_study import scaffold
from wiki_utils import humanize_slug, slugify


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--style", choices=("qa", "cloze", "mixed"), default="mixed")
    args = parser.parse_args()
    slug = slugify(args.slug)
    scaffold("anki", slug, f"{humanize_slug(slug)} Anki", [f"studies/papers/{slug}"], [f"studies/papers/{slug}"], False)
    print(f"hint: fill roughly {args.n} {args.style} cards from My Notes and concept definitions only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
