"""Generate a durable coverage dashboard for the vault."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Any, Dict, List, Set

from stale_pages import raw_sources_for_page
from wiki_utils import (
    DERIVED_TYPES,
    WIKI_DIR,
    load_markdown_page,
    load_wiki_pages,
    normalize_wiki_ref,
    now_utc,
    parse_timestamp,
    render_markdown_page,
    repo_relative,
    write_text_if_changed,
)

OUTPUT_PATH = WIKI_DIR / "reviews" / "coverage-dashboard.md"


def collect_stale_refs() -> Set[str]:
    """Collect page refs that are stale relative to their raw sources."""

    refs: Set[str] = set()
    for page in load_wiki_pages(include_special=False):
        page_type = str(page.frontmatter.get("type", ""))
        if page_type not in {"source"} | DERIVED_TYPES:
            continue
        try:
            compiled_at = parse_timestamp(str(page.frontmatter["compiled_at"]))
            raw_paths = raw_sources_for_page(page_type, page.frontmatter)
        except (KeyError, FileNotFoundError, ValueError):
            refs.add(page.ref)
            continue
        newest_source = max(raw_paths, key=lambda raw_path: raw_path.stat().st_mtime)
        if newest_source.stat().st_mtime > compiled_at.timestamp():
            refs.add(page.ref)
    return refs


def build_frontmatter(
    existing_frontmatter: Dict[str, Any],
    source_pages: List[str],
    now: str,
    changed: bool,
) -> Dict[str, Any]:
    """Build frontmatter for the generated coverage page."""

    created = str(existing_frontmatter.get("created") or now)
    updated = now if changed else str(existing_frontmatter.get("updated") or now)
    compiled_at = now if changed else str(existing_frontmatter.get("compiled_at") or updated)
    return {
        "title": "Coverage Dashboard",
        "type": "review",
        "created": created,
        "updated": updated,
        "status": "reviewed",
        "confidence": 0.92,
        "related": ["index", "inbox", "reviews/review-queue"],
        "source_pages": source_pages,
        "compiled_at": compiled_at,
    }


def build_section(title: str, lines: List[str], empty_line: str) -> str:
    """Render one markdown section."""

    if not lines:
        lines = [empty_line]
    return "## {0}\n\n{1}\n".format(title, "\n".join(lines))


def main() -> int:
    """CLI entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print the generated markdown instead of writing it")
    args = parser.parse_args()

    pages = load_wiki_pages(include_special=False)
    source_pages = [page for page in pages if str(page.frontmatter.get("type", "")) == "source"]
    derived_pages = [page for page in pages if str(page.frontmatter.get("type", "")) in DERIVED_TYPES]
    stale_refs = collect_stale_refs()

    pages_by_type = Counter(str(page.frontmatter.get("type", "unknown")) for page in pages)
    pages_by_status = Counter(str(page.frontmatter.get("status", "unknown")) for page in pages)

    derived_by_source: Dict[str, Set[str]] = defaultdict(set)
    concepts_by_source: Dict[str, Set[str]] = defaultdict(set)
    for page in derived_pages:
        source_refs = page.frontmatter.get("source_pages", [])
        if not isinstance(source_refs, list):
            continue
        for raw_ref in source_refs:
            source_ref = normalize_wiki_ref(str(raw_ref))
            if not source_ref:
                continue
            derived_by_source[source_ref].add(page.ref)
            if str(page.frontmatter.get("type", "")) == "concept":
                concepts_by_source[source_ref].add(page.ref)

    source_without_concepts = [
        f"- [[{page.ref}]] -> no concept page cites this source yet"
        for page in source_pages
        if not concepts_by_source.get(page.ref)
    ]

    concepts_with_one_source = [
        f"- [[{page.ref}]] -> only `{len(page.frontmatter.get('source_pages', []))}` source page"
        for page in derived_pages
        if str(page.frontmatter.get("type", "")) == "concept"
        and isinstance(page.frontmatter.get("source_pages"), list)
        and len(page.frontmatter.get("source_pages", [])) == 1
    ]

    weak_syntheses = [
        f"- [[{page.ref}]] -> only `{len(page.frontmatter.get('source_pages', []))}` source page"
        for page in derived_pages
        if str(page.frontmatter.get("type", "")) == "synthesis"
        and isinstance(page.frontmatter.get("source_pages"), list)
        and len(page.frontmatter.get("source_pages", [])) < 2
    ]

    drifting_outputs = [
        f"- [[{page.ref}]] -> stale relative to at least one source page"
        for page in derived_pages
        if str(page.frontmatter.get("type", "")) == "output" and page.ref in stale_refs
    ]

    underlinked_sources = [
        f"- [[{page.ref}]] -> linked by `{len(derived_by_source.get(page.ref, set()))}` derived page(s)"
        for page in source_pages
        if len(derived_by_source.get(page.ref, set())) <= 1
    ]

    summary_lines = [
        f"- Total content pages: `{len(pages)}`",
        f"- Source pages: `{len(source_pages)}`",
        f"- Derived pages: `{len(derived_pages)}`",
    ]
    type_lines = [f"- `{page_type}` -> `{count}`" for page_type, count in sorted(pages_by_type.items())]
    status_lines = [f"- `{status}` -> `{count}`" for status, count in sorted(pages_by_status.items())]

    now = now_utc()
    existing_frontmatter: Dict[str, Any] = {}
    existing_body = ""
    if OUTPUT_PATH.exists():
        existing_frontmatter, existing_body = load_markdown_page(OUTPUT_PATH)

    body = (
        "# Coverage Dashboard\n\n"
        + build_section("Summary", summary_lines, "- No coverage data generated yet.")
        + "\n"
        + build_section("Pages By Type", type_lines, "- No pages loaded.")
        + "\n"
        + build_section("Pages By Status", status_lines, "- No page statuses recorded.")
        + "\n"
        + build_section("Sources Without Concepts", source_without_concepts, "- Every source is cited by at least one concept page.")
        + "\n"
        + build_section("Concepts With Only One Source", concepts_with_one_source, "- No concept page is supported by only one source.")
        + "\n"
        + build_section("Syntheses With Thin Support", weak_syntheses, "- Every synthesis currently cites at least two source pages.")
        + "\n"
        + build_section("Outputs Drifting From Sources", drifting_outputs, "- No output page is stale relative to its source pages.")
        + "\n"
        + build_section("Underlinked Sources", underlinked_sources, "- Every source feeds more than one derived page.")
        + "\n"
        + "## Notes\n\n"
        + "- Use [[reviews/review-queue]] for the action-oriented queue.\n"
        + "- Use this dashboard to decide whether the vault is compounding or just accumulating isolated notes.\n"
    )

    source_refs = sorted(page.ref for page in source_pages) or ["sources/attention-is-all-you-need-excerpt"]
    changed = body.strip() != existing_body.strip()
    frontmatter = build_frontmatter(existing_frontmatter, source_refs, now, changed)
    content = render_markdown_page(frontmatter, body)
    if args.stdout:
        print(content)
        return 0

    changed = write_text_if_changed(OUTPUT_PATH, content)
    print("updated: {0}".format(repo_relative(OUTPUT_PATH)) if changed else "no changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
