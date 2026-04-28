"""Scaffold study pages for papers, derivations, implementations, and Anki decks."""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any

from wiki_utils import WIKI_DIR, humanize_slug, now_utc, render_markdown_page, slugify, write_text_if_changed

STUDY_DIRS = {
    "paper": WIKI_DIR / "studies" / "papers",
    "anki": WIKI_DIR / "studies" / "anki",
    "derivation": WIKI_DIR / "studies" / "derivations",
    "implementation": WIKI_DIR / "studies" / "implementations",
}


def build_frontmatter(kind: str, slug: str, title: str, source_pages: list[str], related: list[str], timestamp: str, **extra: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "title": title,
        "type": "study",
        "created": timestamp,
        "updated": timestamp,
        "status": "draft",
        "confidence": 0.3,
        "related": related or source_pages,
        "source_pages": source_pages,
        "compiled_at": timestamp,
        "study_kind": kind,
        "read_status": "todo",
        "rating": None,
        "mastery_avg": 0.0,
        "tags": ["study", kind],
    }
    data.update({key: value for key, value in extra.items() if value is not None})
    return data


def paper_body(title: str) -> str:
    return f"""# {title}

## Why This Paper Matters

## Core Claim

## Scope For First Pass

## Concept Map

## Mastery Tracker

| Topic | Concept Page | Intuition | Equation | Visual | Trace | Comparison | Practice | Mastery |
|---|---|---|---|---|---|---|---|---|

## Reading Log

## Key Claims To Verify

## Equations / Derivations To Reconstruct

## Confusions To Resolve

## Active Recall Questions

## Tiny Examples To Build

## Connections

## My Notes

## Quiz Log

## Citations

## Output Artifact Target
"""


def anki_body(title: str, slug: str, study_ref: str) -> str:
    return f"""# {title}

#flashcards/{slug}

## Cards

<!-- Add cards below. Every card must include an HTML source comment: `<!-- src: [[...]] -->`. -->

## Source Notes

- Study: [[{study_ref}]]
"""


def derivation_body(title: str, concept_ref: str) -> str:
    return f"""# {title}

## Goal

Reconstruct [[{concept_ref}]] from definitions without looking.

## Prerequisites

## Step-By-Step Reconstruction

1. State the object being derived.
2. Expand the definitions.
3. Check dimensions and invariants.

## Checkpoints

- [ ] I can explain each symbol.
- [ ] I can reconstruct the derivation without looking.

## Citations
"""


def implementation_body(title: str, study_ref: str, task_slug: str, lang: str) -> str:
    return f"""# {title}

## Task

## Three-Step Plan

1. Build the smallest input tensors that expose the idea.
2. Implement the reference path in `{lang}`.
3. Implement the equivalent rewritten path and compare outputs.

## Equivalence-Check Checklist

- [ ] Shapes match at each intermediate step.
- [ ] Outputs match within a stated tolerance.
- [ ] A failure case is included.

## Experiment Directory

- `experiments/papers/{study_ref.split('/')[-1]}/{task_slug}/`

## Citations
"""


def scaffold(kind: str, slug_text: str, title: str | None, source_pages: list[str], related: list[str], stdout: bool = False, lang: str = "numpy") -> Path:
    slug = slugify(slug_text)
    timestamp = now_utc()
    title = title or humanize_slug(slug)
    path = STUDY_DIRS[kind] / f"{slug}.md"
    if kind == "paper":
        fm = build_frontmatter(kind, slug, title, source_pages or [f"sources/{slug}"], related or [f"sources/{slug}"], timestamp)
        body = paper_body(title)
    elif kind == "anki":
        study_ref = (source_pages or [f"studies/papers/{slug}"])[0]
        fm = build_frontmatter(kind, slug, title, [study_ref], related or [study_ref], timestamp)
        body = anki_body(title, slug, study_ref)
    elif kind == "derivation":
        concept_ref = (source_pages or [f"concepts/{slug}"])[0]
        fm = build_frontmatter(kind, slug, title, [concept_ref], related or [concept_ref], timestamp)
        body = derivation_body(title, concept_ref)
    else:
        study_ref = (source_pages or [f"studies/papers/{slug}"])[0]
        fm = build_frontmatter(kind, slug, title, [study_ref], related or [study_ref], timestamp, lang=lang)
        body = implementation_body(title, study_ref, slug, lang)
    content = render_markdown_page(fm, body)
    if stdout:
        print(content)
        return path
    if path.exists():
        print(f"unchanged: {path.relative_to(WIKI_DIR.parent)}")
        return path
    changed = write_text_if_changed(path, content)
    print(("created" if changed else "unchanged") + f": {path.relative_to(WIKI_DIR.parent)}")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(STUDY_DIRS))
    parser.add_argument("slug")
    parser.add_argument("--title")
    parser.add_argument("--source-page", action="append", default=[])
    parser.add_argument("--related", action="append", default=[])
    parser.add_argument("--lang", choices=("numpy", "pytorch"), default="numpy")
    parser.add_argument("--stdout", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    scaffold(args.kind, args.slug, args.title, args.source_page, args.related, args.stdout, args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
