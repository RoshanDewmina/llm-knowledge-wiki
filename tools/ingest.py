"""Register a raw source and create or refresh its source page."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from wiki_utils import (
    RAW_DIR,
    WIKI_DIR,
    build_source_snapshot_section,
    build_source_stub_body,
    ensure_under_root,
    extract_first_heading,
    get_marker_block_lines,
    humanize_slug,
    load_markdown_page,
    load_optional_markdown_page,
    load_wiki_pages,
    normalize_domain,
    normalize_wiki_ref,
    now_utc,
    parse_timestamp,
    repo_relative,
    render_markdown_page,
    resolve_repo_path,
    sha256_file,
    slugify,
    strip_date_prefix,
    update_marker_file,
    write_text_if_changed,
)

OPTIONAL_SOURCE_FIELDS = (
    "source_url",
    "source_domain",
    "author",
    "published",
    "captured_at",
    "description",
    "tags",
    "clipper",
)
SOURCE_SNAPSHOT_RE = re.compile(r"^## Source Snapshot\n\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
TITLE_RE = re.compile(r"^# .+$", re.MULTILINE)


def clean_list(value: Any) -> List[str]:
    """Normalize an input value into a clean list of strings."""

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def optional_source_metadata(raw_frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    """Extract optional source metadata from a raw file frontmatter block."""

    source_url = str(raw_frontmatter.get("source_url", "")).strip()
    source_domain = str(raw_frontmatter.get("source_domain", "")).strip()
    if source_url and not source_domain:
        source_domain = urlparse(source_url).netloc

    metadata: Dict[str, Any] = {
        "source_url": source_url,
        "source_domain": source_domain,
        "author": str(raw_frontmatter.get("author", "")).strip(),
        "published": str(raw_frontmatter.get("published", "")).strip(),
        "captured_at": str(raw_frontmatter.get("captured_at", "")).strip(),
        "description": str(raw_frontmatter.get("description", "")).strip(),
        "clipper": str(raw_frontmatter.get("clipper", "")).strip(),
        "tags": clean_list(raw_frontmatter.get("tags", [])),
    }
    return metadata


def derive_page_title(raw_path: Path, raw_frontmatter: Dict[str, Any], raw_body: str, explicit_title: Optional[str]) -> str:
    """Derive a human-readable title for the source page."""

    if explicit_title:
        return explicit_title
    raw_title = str(raw_frontmatter.get("title", "")).strip()
    if raw_title:
        return raw_title
    heading = extract_first_heading(raw_body)
    if heading:
        return heading
    return humanize_slug(strip_date_prefix(raw_path.stem) or raw_path.stem)


def derive_page_slug(
    raw_path: Path,
    source_kind: str,
    page_title: str,
    metadata: Dict[str, Any],
    explicit_slug: Optional[str],
) -> str:
    """Derive a normalized source-page slug."""

    if explicit_slug:
        return slugify(explicit_slug)
    if source_kind == "articles":
        source_domain = str(metadata.get("source_domain", "")).strip()
        if source_domain:
            return slugify("{0} {1}".format(normalize_domain(source_domain), page_title))
        stripped = strip_date_prefix(raw_path.stem)
        if stripped:
            return slugify(stripped)
    return slugify(strip_date_prefix(raw_path.stem) or page_title)


def find_existing_source_page(source_rel: str, metadata: Dict[str, Any]) -> Optional[Path]:
    """Find an existing source page by raw path, then by source URL."""

    source_url = str(metadata.get("source_url", "")).strip()
    source_pages = [page for page in load_wiki_pages(include_special=False) if page.frontmatter.get("type") == "source"]

    for page in source_pages:
        if str(page.frontmatter.get("source_path", "")).strip() == source_rel:
            return page.path

    if source_url:
        for page in source_pages:
            if str(page.frontmatter.get("source_url", "")).strip() == source_url:
                return page.path
    return None


def build_source_frontmatter(
    existing_frontmatter: Dict[str, Any],
    title: str,
    source_rel: str,
    source_kind: str,
    source_hash: str,
    metadata: Dict[str, Any],
    now: str,
    changed: bool,
) -> Dict[str, Any]:
    """Build source-page frontmatter while preserving human-maintained fields."""

    created = str(existing_frontmatter.get("created") or now)
    status = str(existing_frontmatter.get("status") or "stub")
    confidence = existing_frontmatter.get("confidence", 0.0)
    if not isinstance(confidence, (int, float)):
        confidence = 0.0
    related = existing_frontmatter.get("related")
    if not isinstance(related, list):
        related = []
    compiled_at = str(existing_frontmatter.get("compiled_at") or now)
    updated = str(existing_frontmatter.get("updated") or created)
    if changed:
        compiled_at = now
        updated = now

    frontmatter: Dict[str, Any] = {
        "title": title,
        "type": "source",
        "created": created,
        "updated": updated,
        "status": status,
        "confidence": round(float(confidence), 3),
        "related": [normalize_wiki_ref(str(item)) for item in related if str(item).strip()],
        "source_path": source_rel,
        "source_kind": source_kind,
        "compiled_at": compiled_at,
        "source_hash": source_hash,
    }
    for key in OPTIONAL_SOURCE_FIELDS:
        value = metadata.get(key)
        if key == "tags":
            if value:
                frontmatter[key] = clean_list(value)
            continue
        if isinstance(value, str) and value.strip():
            frontmatter[key] = value.strip()
    return frontmatter


def sync_existing_source_body(
    body: str,
    title: str,
    source_rel: str,
    source_kind: str,
    metadata: Dict[str, Any],
) -> str:
    """Refresh deterministic body sections while preserving authored content."""

    snapshot_section = build_source_snapshot_section(source_rel, source_kind, metadata)
    snapshot_block = "{0}\n\n".format(snapshot_section)
    updated = body

    if TITLE_RE.search(updated):
        updated = TITLE_RE.sub("# {0}".format(title), updated, count=1)
    else:
        updated = "# {0}\n\n{1}{2}".format(title, snapshot_block, updated.strip())

    if SOURCE_SNAPSHOT_RE.search(updated):
        updated = SOURCE_SNAPSHOT_RE.sub(snapshot_block, updated, count=1)
    else:
        lines = updated.splitlines()
        if lines and lines[0].startswith("# "):
            title_line = lines[0]
            remainder = "\n".join(lines[1:]).lstrip("\n")
            updated = "{0}\n\n{1}{2}".format(title_line, snapshot_block, remainder).rstrip()
        else:
            updated = "{0}{1}".format(snapshot_block, updated.strip()).rstrip()
    return updated.rstrip() + "\n"


def build_source_registry_lines(extra_line: Optional[str] = None) -> List[str]:
    """Build the sorted source registry for the index page."""

    lines: List[str] = []
    for page in load_wiki_pages(include_special=False):
        if page.frontmatter.get("type") != "source":
            continue
        source_path = str(page.frontmatter.get("source_path", ""))
        lines.append("- [[{0}]] -> `{1}`".format(page.ref, source_path))
    if extra_line and extra_line not in lines:
        lines.append(extra_line)
    return sorted(lines)


def build_inbox_recent_source_lines(limit: int = 8) -> List[str]:
    """Build the recent-source block for the inbox page."""

    entries: List[Tuple[Any, str]] = []
    for page in load_wiki_pages(include_special=False):
        if page.frontmatter.get("type") != "source":
            continue
        timestamp_text = str(page.frontmatter.get("compiled_at") or page.frontmatter.get("updated") or "")
        try:
            timestamp = parse_timestamp(timestamp_text)
        except ValueError:
            timestamp = parse_timestamp(now_utc())
            timestamp_text = now_utc()
        source_path = str(page.frontmatter.get("source_path", "")).strip()
        entries.append(
            (
                timestamp,
                "- {0} | [[{1}]] | `{2}`".format(timestamp_text, page.ref, source_path),
            )
        )
    entries.sort(key=lambda item: item[0], reverse=True)
    lines = [line for _, line in entries[:limit]]
    return lines or ["- No source pages have been ingested yet."]


def update_log(page_ref: str, source_rel: str, timestamp: str, changed: bool) -> bool:
    """Insert or refresh an idempotent ingest entry in the wiki log."""

    log_path = WIKI_DIR / "log.md"
    existing_lines = get_marker_block_lines(log_path.read_text(encoding="utf-8"), "AUTO-LOG")
    entries: Dict[str, str] = {}
    for line in existing_lines:
        parts = [part.strip() for part in line.lstrip("- ").split("|")]
        if len(parts) >= 4:
            entries[parts[2]] = line
    key = "[[{0}]]".format(page_ref)
    if key not in entries or changed:
        entries[key] = "- {0} | ingest | {1} | {2}".format(timestamp, key, source_rel)
    lines = [entries[item_key] for item_key in sorted(entries)]
    return update_marker_file(log_path, "AUTO-LOG", lines)


def ingest(raw_path_text: str, title: Optional[str], slug: Optional[str], dry_run: bool) -> int:
    """Perform the ingest flow for a raw source file."""

    raw_path = ensure_under_root(resolve_repo_path(raw_path_text), RAW_DIR)
    if not raw_path.is_file():
        raise FileNotFoundError("raw source does not exist: {0}".format(raw_path_text))

    relative_parts = raw_path.relative_to(RAW_DIR).parts
    if len(relative_parts) < 2:
        raise ValueError("raw source must live in a subdirectory under raw/")
    source_kind = relative_parts[0]
    source_rel = repo_relative(raw_path)
    source_hash = sha256_file(raw_path)
    raw_frontmatter, raw_body = load_optional_markdown_page(raw_path)
    metadata = optional_source_metadata(raw_frontmatter)
    page_title = derive_page_title(raw_path, raw_frontmatter, raw_body, title)
    desired_slug = derive_page_slug(raw_path, source_kind, page_title, metadata, slug)
    desired_path = WIKI_DIR / "sources" / "{0}.md".format(desired_slug)
    existing_path = find_existing_source_page(source_rel, metadata)
    source_page_path = existing_path or desired_path

    now = now_utc()
    existing_frontmatter: Dict[str, Any] = {}
    body = build_source_stub_body(page_title, source_rel, source_kind, metadata)
    existing_text = ""
    if source_page_path.exists():
        existing_text = source_page_path.read_text(encoding="utf-8")
        existing_frontmatter, existing_body = load_markdown_page(source_page_path)
        if existing_body.strip():
            body = existing_body
        if title is None and existing_frontmatter.get("title"):
            page_title = str(existing_frontmatter["title"])
        if not metadata.get("description"):
            metadata["description"] = ""
        body = sync_existing_source_body(body, page_title, source_rel, source_kind, metadata).rstrip()

    frontmatter = build_source_frontmatter(
        existing_frontmatter=existing_frontmatter,
        title=page_title,
        source_rel=source_rel,
        source_kind=source_kind,
        source_hash=source_hash,
        metadata=metadata,
        now=now,
        changed=(
            not source_page_path.exists()
            or str(existing_frontmatter.get("source_hash", "")) != source_hash
            or str(existing_frontmatter.get("source_path", "")) != source_rel
            or str(existing_frontmatter.get("source_kind", "")) != source_kind
            or str(existing_frontmatter.get("title", "")) != page_title
            or str(existing_frontmatter.get("source_url", "")) != str(metadata.get("source_url", ""))
            or str(existing_frontmatter.get("source_domain", "")) != str(metadata.get("source_domain", ""))
            or str(existing_frontmatter.get("author", "")) != str(metadata.get("author", ""))
            or str(existing_frontmatter.get("published", "")) != str(metadata.get("published", ""))
            or str(existing_frontmatter.get("captured_at", "")) != str(metadata.get("captured_at", ""))
            or str(existing_frontmatter.get("description", "")) != str(metadata.get("description", ""))
            or clean_list(existing_frontmatter.get("tags", [])) != clean_list(metadata.get("tags", []))
            or str(existing_frontmatter.get("clipper", "")) != str(metadata.get("clipper", ""))
        ),
    )
    page_content = render_markdown_page(frontmatter, body)
    page_ref = "sources/{0}".format(source_page_path.stem)
    registry_line = "- [[{0}]] -> `{1}`".format(page_ref, source_rel)

    if dry_run:
        print("would sync source page: {0}".format(repo_relative(source_page_path)))
        if existing_path and existing_path != desired_path:
            print("would preserve existing page path via source_url match: {0}".format(repo_relative(existing_path)))
        print("would ensure registry entry: {0}".format(registry_line))
        print("would ensure log entry: [[{0}]]".format(page_ref))
        return 0

    changed = write_text_if_changed(source_page_path, page_content)
    writes: List[str] = []
    if changed:
        writes.append(repo_relative(source_page_path))
    if update_marker_file(WIKI_DIR / "index.md", "AUTO-SOURCES", build_source_registry_lines(registry_line)):
        writes.append("wiki/index.md")
    if update_log(page_ref, source_rel, str(frontmatter["compiled_at"]), changed):
        writes.append("wiki/log.md")
    if update_marker_file(WIKI_DIR / "inbox.md", "AUTO-RECENT-SOURCES", build_inbox_recent_source_lines()):
        writes.append("wiki/inbox.md")

    if writes:
        print("updated:")
        for item in writes:
            print("- {0}".format(item))
    else:
        print("no changes needed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_path", help="Path to an existing raw source under raw/")
    parser.add_argument("--title", help="Optional page title override")
    parser.add_argument("--slug", help="Optional slug override for wiki/sources/<slug>.md")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without writing")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    return ingest(args.raw_path, args.title, args.slug, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
