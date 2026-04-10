"""Shared helpers for the local-first wiki tooling."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "raw"
WIKI_DIR = REPO_ROOT / "wiki"
SPECIAL_WIKI_REFS = {"index", "log", "inbox"}
VALID_STATUSES = {"stub", "draft", "reviewed", "published", "archived"}
DERIVED_TYPES = {"concept", "entity", "benchmark", "project", "synthesis", "output", "review"}
LIGHTWEIGHT_TYPES = {"journal", "question"}
CONTENT_TYPES = DERIVED_TYPES | LIGHTWEIGHT_TYPES | {"source"}
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WORD_RE = re.compile(r"[A-Za-z0-9]+")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
SAFE_SCALAR_RE = re.compile(r"^[A-Za-z0-9_./@:+-][A-Za-z0-9_./@:+\- ]*$")
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[-_]?")


class FrontmatterError(ValueError):
    """Raised when a markdown page has invalid or unsupported frontmatter."""


@dataclass
class PageRecord:
    """Loaded wiki page with canonical reference."""

    path: Path
    ref: str
    frontmatter: Dict[str, Any]
    body: str


def now_utc() -> str:
    """Return an ISO 8601 UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_timestamp(value: str) -> datetime:
    """Parse an ISO 8601 timestamp and normalize it to UTC."""

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid ISO 8601 timestamp: {0}".format(value)) from exc
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone information: {0}".format(value))
    return parsed.astimezone(timezone.utc)


def slugify(value: str) -> str:
    """Convert a string into a stable filesystem slug."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "untitled"


def humanize_slug(slug: str) -> str:
    """Turn a slug into a simple title."""

    return " ".join(part.capitalize() for part in slug.replace("_", "-").split("-") if part)


def strip_date_prefix(value: str) -> str:
    """Strip a leading YYYY-MM-DD prefix from a filename stem."""

    return DATE_PREFIX_RE.sub("", value).strip("-_")


def normalize_domain(value: str) -> str:
    """Convert a source domain into a filesystem-friendly slug fragment."""

    cleaned = value.strip().lower()
    cleaned = cleaned.removeprefix("https://").removeprefix("http://")
    cleaned = cleaned.split("/", 1)[0]
    return slugify(cleaned.replace(".", "-"))


def extract_first_heading(text: str) -> str:
    """Return the first H1 heading from markdown text, if present."""

    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def sha256_file(path: Path) -> str:
    """Compute the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_repo_path(path_text: Union[str, Path]) -> Path:
    """Resolve a path relative to the repository root."""

    path = Path(path_text)
    candidate = path if path.is_absolute() else REPO_ROOT / path
    return candidate.resolve()


def ensure_under_root(path: Path, root: Path) -> Path:
    """Ensure a path is inside a given root and return the resolved path."""

    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("path is outside {0}: {1}".format(root, path)) from exc
    return resolved


def repo_relative(path: Path) -> str:
    """Return a repository-relative POSIX path."""

    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def normalize_wiki_ref(ref: str) -> str:
    """Normalize an internal wiki reference to `folder/name` without `.md`."""

    target = ref.strip()
    if not target:
        return ""
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    target = target.removeprefix("[[").removesuffix("]]").strip()
    target = target.removeprefix("wiki/").removeprefix("/")
    if target.endswith(".md"):
        target = target[:-3]
    return target.strip("/")


def wiki_ref_to_path(ref: str) -> Path:
    """Convert a normalized wiki reference into a markdown path."""

    normalized = normalize_wiki_ref(ref)
    if not normalized:
        raise ValueError("empty wiki reference")
    return WIKI_DIR / "{0}.md".format(normalized)


def path_to_wiki_ref(path: Path) -> str:
    """Convert a wiki markdown path into its canonical reference."""

    relative = path.resolve().relative_to(WIKI_DIR.resolve()).as_posix()
    return relative[:-3] if relative.endswith(".md") else relative


def is_special_wiki_page(ref: str) -> bool:
    """Return True for special root wiki pages such as index and log."""

    return normalize_wiki_ref(ref) in SPECIAL_WIKI_REFS


def extract_wikilinks(text: str) -> List[str]:
    """Extract normalized wikilink targets from markdown body text."""

    refs: List[str] = []
    for match in WIKILINK_RE.finditer(text):
        normalized = normalize_wiki_ref(match.group(1))
        if normalized:
            refs.append(normalized)
    return refs


def extract_markdown_links(text: str) -> List[str]:
    """Extract markdown link targets from body text."""

    return [match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(text)]


def is_remote_url(target: str) -> bool:
    """Return True when the link target is a remote URL."""

    return urlparse(target).scheme in {"http", "https", "mailto"}


def has_valid_remote_url_syntax(target: str) -> bool:
    """Return True when a remote URL is syntactically usable."""

    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"}:
        return bool(parsed.netloc)
    if parsed.scheme == "mailto":
        return bool(parsed.path)
    return False


def is_absolute_local_markdown_link(target: str) -> bool:
    """Return True for non-portable absolute filesystem-like markdown links."""

    clean = target.strip()
    return clean.startswith("/") or clean.startswith("file://")


def tokenize(text: str) -> List[str]:
    """Tokenize free text for lightweight lexical search."""

    return [token.lower() for token in WORD_RE.findall(text)]


def slugify_heading(value: str) -> str:
    """Convert a markdown heading into a predictable anchor slug."""

    lowered = value.lower().strip()
    lowered = re.sub(r"[`*_~]", "", lowered)
    lowered = re.sub(r"[^\w\s-]", "", lowered)
    lowered = re.sub(r"\s+", "-", lowered)
    return lowered.strip("-")


def parse_scalar(raw_value: str) -> Any:
    """Parse a supported scalar from the YAML subset used by the repo."""

    value = raw_value.strip()
    if value == "[]":
        return []
    if value in {"null", "~"}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def dump_scalar(value: Any) -> str:
    """Render a supported scalar for the YAML subset used by the repo."""

    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        raise TypeError("unsupported scalar type: {0!r}".format(type(value)))
    if SAFE_SCALAR_RE.fullmatch(value) and ": " not in value and not value.startswith(("-", "?", "!", "&", "*", "#")):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return '"{0}"'.format(escaped)


def parse_yaml_subset(text: str) -> Dict[str, Any]:
    """Parse the constrained YAML subset used by the repository."""

    data: Dict[str, Any] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterError("unexpected indentation in frontmatter: {0!r}".format(line))
        if ":" not in line:
            raise FrontmatterError("missing ':' in frontmatter line: {0!r}".format(line))
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise FrontmatterError("missing key in frontmatter line: {0!r}".format(line))
        if raw_value == "":
            items: List[Any] = []
            index += 1
            while index < len(lines) and lines[index].startswith("  - "):
                items.append(parse_scalar(lines[index][4:]))
                index += 1
            data[key] = items
            continue
        data[key] = parse_scalar(raw_value)
        index += 1
    return data


def dump_yaml_subset(data: Dict[str, Any]) -> str:
    """Serialize the constrained YAML subset used by the repository."""

    lines: List[str] = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            if not value:
                lines.append("{0}: []".format(key))
                continue
            lines.append("{0}:".format(key))
            for item in value:
                lines.append("  - {0}".format(dump_scalar(item)))
            continue
        lines.append("{0}: {1}".format(key, dump_scalar(value)))
    lines.append("---")
    return "\n".join(lines)


def split_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Split a markdown file into frontmatter and body."""

    if not text.startswith("---\n"):
        raise FrontmatterError("missing opening frontmatter delimiter")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise FrontmatterError("missing closing frontmatter delimiter")
    frontmatter_text = parts[0][4:]
    body = parts[1]
    return parse_yaml_subset(frontmatter_text), body.lstrip("\n")


def load_markdown_page(path: Path) -> Tuple[Dict[str, Any], str]:
    """Load a markdown file with frontmatter."""

    text = path.read_text(encoding="utf-8")
    return split_frontmatter(text)


def load_optional_markdown_page(path: Path) -> Tuple[Dict[str, Any], str]:
    """Load a markdown file and parse frontmatter only when present."""

    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        return split_frontmatter(text)
    return {}, text


def render_markdown_page(frontmatter: Dict[str, Any], body: str) -> str:
    """Render a frontmatter-bearing markdown page."""

    return "{0}\n\n{1}\n".format(dump_yaml_subset(frontmatter), body.rstrip())


def read_text(path: Path) -> str:
    """Read UTF-8 text from disk."""

    return path.read_text(encoding="utf-8")


def write_text_if_changed(path: Path, content: str) -> bool:
    """Write UTF-8 text if the content changed."""

    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def get_marker_bounds(text: str, marker: str) -> Tuple[int, int, str, str]:
    """Return the slice positions for a marker block."""

    start_marker = "<!-- {0}:START -->".format(marker)
    end_marker = "<!-- {0}:END -->".format(marker)
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError("marker block not found: {0}".format(marker))
    return start, end + len(end_marker), start_marker, end_marker


def get_marker_block_lines(text: str, marker: str) -> List[str]:
    """Extract lines between a marker block."""

    _, _, start_marker, end_marker = get_marker_bounds(text, marker)
    block_start = text.find(start_marker) + len(start_marker)
    block_end = text.find(end_marker)
    block_text = text[block_start:block_end]
    return [line for line in block_text.strip("\n").splitlines() if line.strip()]


def replace_marker_block(text: str, marker: str, lines: List[str]) -> str:
    """Replace the contents of a marker block."""

    start, end, start_marker, end_marker = get_marker_bounds(text, marker)
    replacement_lines = [start_marker]
    replacement_lines.extend(lines)
    replacement_lines.append(end_marker)
    replacement = "\n".join(replacement_lines)
    return "{0}{1}{2}".format(text[:start], replacement, text[end:])


def update_marker_file(path: Path, marker: str, lines: List[str]) -> bool:
    """Replace a marker block in a file, writing only when changed."""

    text = read_text(path)
    updated = replace_marker_block(text, marker, lines)
    return write_text_if_changed(path, updated)


def iter_markdown_files(root: Path) -> List[Path]:
    """Return all markdown files under a directory."""

    return sorted(path for path in root.rglob("*.md") if path.is_file())


def expand_markdown_targets(targets: List[str], default_root: Path = WIKI_DIR) -> List[Path]:
    """Expand file and directory targets into markdown files."""

    if not targets:
        return iter_markdown_files(default_root)
    files: List[Path] = []
    for raw_target in targets:
        candidate = resolve_repo_path(raw_target)
        if not candidate.exists():
            raise FileNotFoundError("target does not exist: {0}".format(raw_target))
        if candidate.is_dir():
            files.extend(iter_markdown_files(candidate))
            continue
        if candidate.suffix != ".md":
            raise ValueError("target is not a markdown file: {0}".format(raw_target))
        files.append(candidate)
    return sorted(dict.fromkeys(path.resolve() for path in files))


def load_wiki_pages(include_special: bool = True) -> List[PageRecord]:
    """Load all markdown pages from the wiki directory."""

    pages: List[PageRecord] = []
    for path in iter_markdown_files(WIKI_DIR):
        ref = path_to_wiki_ref(path)
        if not include_special and is_special_wiki_page(ref):
            continue
        frontmatter: Dict[str, Any] = {}
        body = read_text(path)
        if not is_special_wiki_page(ref):
            frontmatter, body = load_markdown_page(path)
        pages.append(PageRecord(path=path, ref=ref, frontmatter=frontmatter, body=body))
    return pages


def frontmatter_refs(frontmatter: Dict[str, Any]) -> List[str]:
    """Collect internal wiki references stored in frontmatter."""

    refs: List[str] = []
    for key in ("related", "source_pages"):
        value = frontmatter.get(key, [])
        if isinstance(value, list):
            refs.extend(normalize_wiki_ref(str(item)) for item in value if str(item).strip())
    return [ref for ref in refs if ref]


def build_source_stub_body(
    title: str,
    source_rel: str,
    source_kind: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Create a deterministic source page body without summarizing the source."""

    details = metadata or {}
    snapshot_lines = build_source_snapshot_lines(source_rel, source_kind, details, include_state=True)

    return (
        "# {0}\n\n".format(title)
        + build_source_snapshot_section(source_rel, source_kind, details, include_state=True)
        + "\n\n"
        + "## Extraction Queue\n\n"
        + "- [ ] Read the raw file carefully.\n"
        + "- [ ] Add verified claims with direct traceability to this source page.\n"
        + "- [ ] Link related concept, synthesis, entity, benchmark, or project pages.\n\n"
        + "## Raw Description\n\n"
        + "- {0}\n\n".format(str(details.get("description", "")).strip() or "No description recorded yet.")
        + "## Verified Claims\n\n"
        + "- No durable claims recorded yet.\n\n"
        + "## Evidence Extracts\n\n"
        + "- Add `### ex-...` headings here once exact supporting passages or bullet-level traces are identified.\n\n"
        + "## Contradictions\n\n"
        + "- No contradictions recorded yet.\n\n"
        + "## Related Pages\n\n"
        + "- Add wikilinks after reviewing the source.\n\n"
        + "## Compilation Notes\n\n"
        + "- This page was created by ingest and is ready for LLM completion.\n"
    )


def build_source_snapshot_lines(
    source_rel: str,
    source_kind: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_state: bool = False,
) -> List[str]:
    """Build deterministic source snapshot lines."""

    details = metadata or {}
    snapshot_lines = [
        "- Raw file: `{0}`".format(source_rel),
        "- Source kind: `{0}`".format(source_kind),
    ]
    source_url = str(details.get("source_url", "")).strip()
    if source_url:
        snapshot_lines.append("- Source URL: [{0}]({0})".format(source_url))
    source_domain = str(details.get("source_domain", "")).strip()
    if source_domain:
        snapshot_lines.append("- Source domain: `{0}`".format(source_domain))
    author = str(details.get("author", "")).strip()
    if author:
        snapshot_lines.append("- Author: `{0}`".format(author))
    published = str(details.get("published", "")).strip()
    if published:
        snapshot_lines.append("- Published: `{0}`".format(published))
    captured_at = str(details.get("captured_at", "")).strip()
    if captured_at:
        snapshot_lines.append("- Captured: `{0}`".format(captured_at))
    clipper = str(details.get("clipper", "")).strip()
    if clipper:
        snapshot_lines.append("- Clipper: `{0}`".format(clipper))
    if include_state:
        snapshot_lines.append("- Current state: deterministic ingest scaffold")
    return snapshot_lines


def build_source_snapshot_section(
    source_rel: str,
    source_kind: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_state: bool = False,
) -> str:
    """Render the source snapshot heading and bullet list."""

    return "## Source Snapshot\n\n{0}".format(
        "\n".join(build_source_snapshot_lines(source_rel, source_kind, metadata, include_state=include_state))
    )


def choose_snippet(body: str, terms: List[str], fallback_length: int = 160) -> str:
    """Return the first line in the body that matches a query term."""

    for line in body.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if stripped and any(term in lowered for term in terms):
            return stripped
    compact = " ".join(body.split())
    return compact[:fallback_length].strip()
