"""Generate a durable review queue page for the vault."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Set

from duplicate_pages import collect_duplicates
from lint_citations import collect_errors as collect_citation_errors
from stale_pages import raw_sources_for_page
from wiki_utils import (
    DERIVED_TYPES,
    WIKI_DIR,
    extract_wikilinks,
    frontmatter_refs,
    load_markdown_page,
    load_wiki_pages,
    normalize_wiki_ref,
    now_utc,
    parse_timestamp,
    render_markdown_page,
    repo_relative,
    write_text_if_changed,
)

OUTPUT_PATH = WIKI_DIR / "reviews" / "review-queue.md"
LOW_CONFIDENCE_THRESHOLD = 0.75


def collect_orphans() -> List[Dict[str, str]]:
    """Collect wiki pages with no inbound and no outbound links."""

    pages = load_wiki_pages(include_special=False)
    outbound: Dict[str, Set[str]] = {}
    inbound: Dict[str, Set[str]] = {page.ref: set() for page in pages}

    for page in pages:
        refs = set(extract_wikilinks(page.body))
        refs.update(frontmatter_refs(page.frontmatter))
        refs.discard(page.ref)
        outbound[page.ref] = refs
        for target in refs:
            if target in inbound:
                inbound[target].add(page.ref)

    return [
        {"ref": page.ref, "path": repo_relative(page.path)}
        for page in pages
        if not outbound.get(page.ref) and not inbound.get(page.ref)
    ]


def collect_stale() -> List[Dict[str, str]]:
    """Collect stale pages using the same logic as `stale_pages.py`."""

    stale: List[Dict[str, str]] = []
    for page in load_wiki_pages(include_special=False):
        page_type = str(page.frontmatter.get("type", ""))
        if page_type not in {"source"} | DERIVED_TYPES:
            continue
        try:
            compiled_at = parse_timestamp(str(page.frontmatter["compiled_at"]))
            raw_paths = raw_sources_for_page(page_type, page.frontmatter)
        except (KeyError, FileNotFoundError, ValueError) as exc:
            stale.append({"ref": page.ref, "path": repo_relative(page.path), "reason": str(exc)})
            continue
        newest_source = max(raw_paths, key=lambda raw_path: raw_path.stat().st_mtime)
        if newest_source.stat().st_mtime > compiled_at.timestamp():
            stale.append(
                {
                    "ref": page.ref,
                    "path": repo_relative(page.path),
                    "reason": f"source newer than compiled_at: {repo_relative(newest_source)}",
                }
            )
    return stale


def collect_low_confidence() -> List[Dict[str, str]]:
    """Collect pages below the preferred confidence threshold."""

    items: List[Dict[str, str]] = []
    for page in load_wiki_pages(include_special=False):
        confidence = page.frontmatter.get("confidence")
        if not isinstance(confidence, (int, float)):
            continue
        if float(confidence) >= LOW_CONFIDENCE_THRESHOLD:
            continue
        items.append(
            {
                "ref": page.ref,
                "path": repo_relative(page.path),
                "confidence": str(round(float(confidence), 3)),
            }
        )
    return sorted(items, key=lambda item: (float(item["confidence"]), item["path"]))


def collect_incomplete_sources() -> List[Dict[str, str]]:
    """Collect source pages that still need extraction work."""

    items: List[Dict[str, str]] = []
    for page in load_wiki_pages(include_special=False):
        if str(page.frontmatter.get("type", "")) != "source":
            continue
        status = str(page.frontmatter.get("status", ""))
        if status in {"reviewed", "published"}:
            continue
        items.append({"ref": page.ref, "path": repo_relative(page.path), "status": status})
    return sorted(items, key=lambda item: item["path"])


def collect_source_refs_for_issue(page_ref: str, page_lookup: Dict[str, Any]) -> Set[str]:
    """Resolve a page into the set of source refs it depends on."""

    page = page_lookup.get(page_ref)
    if page is None:
        return set()
    page_type = str(page.frontmatter.get("type", ""))
    if page_type == "source":
        return {page.ref}
    source_pages = page.frontmatter.get("source_pages", [])
    if isinstance(source_pages, list):
        return {normalize_wiki_ref(str(item)) for item in source_pages if str(item).strip()}
    return set()


def build_frontmatter(
    existing_frontmatter: Dict[str, Any],
    source_pages: List[str],
    now: str,
    changed: bool,
) -> Dict[str, Any]:
    """Build frontmatter for the generated review queue page."""

    created = str(existing_frontmatter.get("created") or now)
    updated = now if changed else str(existing_frontmatter.get("updated") or now)
    compiled_at = now if changed else str(existing_frontmatter.get("compiled_at") or updated)
    return {
        "title": "Review Queue",
        "type": "review",
        "created": created,
        "updated": updated,
        "status": "reviewed",
        "confidence": 0.9,
        "related": ["index", "inbox", "reviews/coverage-dashboard"],
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
    page_lookup = {page.ref: page for page in pages}
    stale_items = collect_stale()
    orphan_items = collect_orphans()
    low_confidence_items = collect_low_confidence()
    incomplete_source_items = collect_incomplete_sources()
    citation_items = collect_citation_errors([page.path for page in pages])
    duplicate_items = collect_duplicates()

    source_refs: Set[str] = set()
    for item in stale_items:
        source_refs.update(collect_source_refs_for_issue(item["ref"], page_lookup))
    for item in low_confidence_items:
        source_refs.update(collect_source_refs_for_issue(item["ref"], page_lookup))
    for item in incomplete_source_items:
        source_refs.add(item["ref"])
    for item in orphan_items:
        source_refs.update(collect_source_refs_for_issue(item["ref"], page_lookup))
    for item in citation_items:
        ref_text = item["path"].removeprefix("wiki/").removesuffix(".md")
        source_refs.update(collect_source_refs_for_issue(ref_text, page_lookup))
    for duplicate in duplicate_items:
        for page in duplicate["pages"]:
            source_refs.update(collect_source_refs_for_issue(page["ref"], page_lookup))

    if not source_refs:
        source_refs = {page.ref for page in pages if str(page.frontmatter.get("type", "")) == "source"}

    existing_frontmatter: Dict[str, Any] = {}
    existing_body = ""
    if OUTPUT_PATH.exists():
        existing_frontmatter, existing_body = load_markdown_page(OUTPUT_PATH)

    summary_lines = [
        "- Review this queue from top to bottom and clear the highest-signal items first.",
        "- Run `python3 tools/check_wiki.py` again after making substantial changes.",
    ]
    issue_count = (
        len(stale_items)
        + len(orphan_items)
        + len(low_confidence_items)
        + len(incomplete_source_items)
        + len(citation_items)
        + len(duplicate_items)
    )
    summary_lines.append(f"- Open issue groups: `{issue_count}`")

    stale_lines = [f"- [[{item['ref']}]] -> {item['reason']}" for item in stale_items]
    incomplete_source_lines = [
        f"- [[{item['ref']}]] -> status `{item['status']}`" for item in incomplete_source_items
    ]
    low_confidence_lines = [
        f"- [[{item['ref']}]] -> confidence `{item['confidence']}`" for item in low_confidence_items
    ]
    orphan_lines = [f"- [[{item['ref']}]] -> no inbound or outbound internal links" for item in orphan_items]
    citation_lines = [f"- `{item['path']}` -> {item['message']}" for item in citation_items]
    duplicate_lines = [
        "- duplicate group `{0}` -> {1}".format(
            duplicate["normalized_title"],
            ", ".join(f"[[{page['ref']}]]" for page in duplicate["pages"]),
        )
        for duplicate in duplicate_items
    ]

    body = (
        "# Review Queue\n\n"
        + build_section("Summary", summary_lines, "- No review metadata generated yet.")
        + "\n"
        + build_section("Stale Pages", stale_lines, "- No stale pages detected.")
        + "\n"
        + build_section("Source Pages Needing Review", incomplete_source_lines, "- No source pages remain in stub or draft status.")
        + "\n"
        + build_section("Low-Confidence Pages", low_confidence_lines, f"- No page is below confidence `{LOW_CONFIDENCE_THRESHOLD}`.")
        + "\n"
        + build_section("Citation Gaps", citation_lines, "- Exact citation coverage looks healthy.")
        + "\n"
        + build_section("Orphan Pages", orphan_lines, "- No orphan pages detected.")
        + "\n"
        + build_section("Duplicate Candidates", duplicate_lines, "- No obvious duplicate concept-like pages detected.")
        + "\n"
        + "## Recommended Next Pass\n\n"
        + "- Start with the oldest stale page or the newest source page still in `stub`/`draft` status.\n"
        + "- Add exact evidence anchors under each affected source page before revising derived pages.\n"
        + "- Prefer updating existing concept, synthesis, and output pages over creating new near-duplicates.\n"
    )

    now = now_utc()
    changed = body.strip() != existing_body.strip()
    frontmatter = build_frontmatter(existing_frontmatter, sorted(source_refs), now, changed)
    content = render_markdown_page(frontmatter, body)
    if args.stdout:
        print(content)
        return 0

    changed = write_text_if_changed(OUTPUT_PATH, content)
    print("updated: {0}".format(repo_relative(OUTPUT_PATH)) if changed else "no changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
