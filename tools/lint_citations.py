"""Validate exact source citations across compiled wiki pages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from wiki_utils import (
    WIKI_DIR,
    expand_markdown_targets,
    is_special_wiki_page,
    load_markdown_page,
    load_wiki_pages,
    normalize_wiki_ref,
    path_to_wiki_ref,
    repo_relative,
    slugify_heading,
    wiki_ref_to_path,
)

CITATION_REQUIRED_TYPES = {"concept", "entity", "benchmark", "synthesis", "output"}
EVIDENCE_REQUIRED_SOURCE_STATUSES = {"reviewed", "published"}
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
LEVEL_THREE_HEADING_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


def extract_section(body: str, heading: str) -> str:
    """Return the contents of a `## Heading` section."""

    capture = False
    lines: List[str] = []
    target = heading.strip().lower()
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            if capture:
                break
            capture = current == target
            continue
        if capture:
            lines.append(line)
    return "\n".join(lines).strip()


def extract_source_anchors(body: str) -> Set[str]:
    """Return normalized evidence anchor IDs from a source page."""

    section = extract_section(body, "Evidence Extracts")
    anchors: Set[str] = set()
    for match in LEVEL_THREE_HEADING_RE.finditer(section):
        anchor = slugify_heading(match.group(1))
        if anchor.startswith("ex-"):
            anchors.add(anchor)
    return anchors


def extract_citation_targets(body: str) -> List[Tuple[str, str]]:
    """Return `(source_ref, anchor)` tuples from the citations section."""

    section = extract_section(body, "Citations")
    citations: List[Tuple[str, str]] = []
    for match in WIKILINK_RE.finditer(section):
        raw_target = match.group(1).split("|", 1)[0].strip()
        target_path, anchor = raw_target.split("#", 1) if "#" in raw_target else (raw_target, "")
        citations.append((normalize_wiki_ref(target_path), slugify_heading(anchor)))
    return citations


def build_source_anchor_map() -> Dict[str, Set[str]]:
    """Load all source pages and map them to evidence anchor IDs."""

    anchors: Dict[str, Set[str]] = {}
    for page in load_wiki_pages(include_special=False):
        if str(page.frontmatter.get("type", "")) != "source":
            continue
        anchors[page.ref] = extract_source_anchors(page.body)
    return anchors


def validate_page(path: Path, source_anchor_map: Dict[str, Set[str]]) -> List[Dict[str, Any]]:
    """Validate one wiki page against the citation contract."""

    errors: List[Dict[str, Any]] = []
    ref = path_to_wiki_ref(path)
    if is_special_wiki_page(ref):
        return errors
    frontmatter, body = load_markdown_page(path)
    page_type = str(frontmatter.get("type", ""))

    if page_type == "source":
        status = str(frontmatter.get("status", ""))
        anchors = source_anchor_map.get(ref, set())
        if status in EVIDENCE_REQUIRED_SOURCE_STATUSES and not anchors:
            errors.append(
                {
                    "path": repo_relative(path),
                    "message": "reviewed or published source pages must include `## Evidence Extracts` with `### ex-...` headings",
                }
            )
        return errors

    if page_type not in CITATION_REQUIRED_TYPES:
        return errors

    if page_type == "output" and frontmatter.get("marp") is True:
        return errors

    citations = extract_citation_targets(body)
    if not citations:
        errors.append(
            {
                "path": repo_relative(path),
                "message": "missing exact citations: add a `## Citations` section with `[[sources/...#ex-...]]` links",
            }
        )
        return errors

    cited_source_refs: Set[str] = set()
    for source_ref, anchor in citations:
        if not source_ref:
            errors.append({"path": repo_relative(path), "message": "citations contains an empty wiki reference"})
            continue
        target_path = wiki_ref_to_path(source_ref)
        if not target_path.exists():
            errors.append({"path": repo_relative(path), "message": f"cited source page does not exist: {source_ref}"})
            continue
        cited_source_refs.add(source_ref)
        if not anchor:
            errors.append(
                {
                    "path": repo_relative(path),
                    "message": f"citation must point to an exact source anchor: {source_ref}",
                }
            )
            continue
        anchors = source_anchor_map.get(source_ref, set())
        if anchor not in anchors:
            errors.append(
                {
                    "path": repo_relative(path),
                    "message": f"missing cited evidence anchor: {source_ref}#{anchor}",
                }
            )

    source_pages = frontmatter.get("source_pages", [])
    if isinstance(source_pages, list):
        normalized_source_pages = {normalize_wiki_ref(str(item)) for item in source_pages if str(item).strip()}
        uncited = sorted(normalized_source_pages - cited_source_refs)
        if uncited:
            errors.append(
                {
                    "path": repo_relative(path),
                    "message": "source_pages missing exact citations: {0}".format(", ".join(uncited)),
                }
            )
    return errors


def collect_errors(files: List[Path]) -> List[Dict[str, Any]]:
    """Collect citation errors for a list of wiki markdown files."""

    source_anchor_map = build_source_anchor_map()
    errors: List[Dict[str, Any]] = []
    for path in files:
        errors.extend(validate_page(path, source_anchor_map))
    return errors


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional wiki markdown files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    try:
        files = expand_markdown_targets(args.paths, default_root=WIKI_DIR)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}")
        return 2

    errors = collect_errors(files)
    if args.json:
        print(json.dumps(errors, indent=2))
    elif errors:
        for error in errors:
            print(f"{error['path']}: {error['message']}")
    else:
        print(f"ok: checked exact citations for {len(files)} markdown files")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
