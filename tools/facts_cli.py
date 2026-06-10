"""CLI for the personal-facts JSONL store.

Subcommands:
  - add        Append a new fact (validates schema, dedupes, chmods 0600).
  - approve    Approve a pending proposal staged by the MCP server.
  - reject     Reject a pending proposal staged by the MCP server.
  - query      Filter facts by category / predicate / tag / id substring.
  - validate   Schema-check every record in the JSONL.
  - dedupe     Report exact duplicate (subject, predicate, valid_from) rows.
  - expire     Set valid_to on an existing row by id.
  - rebuild-index   Regenerate the fact-index markdown from JSONL.

Wired into ./bin/llm-wiki via the `facts` subcommand in tools/cli.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from wiki_utils import REPO_ROOT, RAW_DIR, now_utc


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"
AUDIT_LOG = REPO_ROOT / "secure" / "cleartext" / "audit" / "facts.log"
PENDING_DIR = REPO_ROOT / "secure" / "cleartext" / "pending"
REJECTED_LOG = REPO_ROOT / "secure" / "cleartext" / "rejected.log"

REQUIRED_FIELDS = ["id", "category", "subject", "predicate", "value", "observed_at", "confidence", "sensitivity"]
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_SENSITIVITY = {
    "highly_sensitive_personal_data",
    "sensitive_personal_data",
    "low_sensitivity",
}
ALL_FIELDS = REQUIRED_FIELDS + ["tags", "source", "notes", "valid_from", "valid_to", "event_date"]
OWNER_ONLY = stat.S_IRUSR | stat.S_IWUSR
OWNER_ONLY_DIR = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
PENDING_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{6}$")


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_records(path: Path) -> List[Dict[str, Any]]:
    """Load a JSONL file as a list of dicts."""

    records: List[Dict[str, Any]] = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise SystemExit("invalid JSONL at line {0}: {1}".format(line_no, exc))
    return records


def save_records(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    """Write records back to JSONL with chmod 0600."""

    payload_lines = []
    for record in records:
        normalized = {k: record.get(k) for k in ALL_FIELDS if k in record}
        for k, v in record.items():
            if k not in ALL_FIELDS:
                normalized[k] = v
        payload_lines.append(json.dumps(normalized, ensure_ascii=False, sort_keys=True))
    payload = "\n".join(payload_lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    os.chmod(path, OWNER_ONLY)


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, OWNER_ONLY_DIR)


def append_audit(action: str, fact_id: str, extra: Optional[Dict[str, Any]] = None) -> None:
    """Append a mutation event to the audit log (low-sensitivity metadata only)."""

    entry: Dict[str, Any] = {
        "ts": now_utc(),
        "action": action,
        "id": fact_id,
    }
    if extra:
        entry.update(extra)
    ensure_private_dir(AUDIT_LOG.parent)
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    os.chmod(AUDIT_LOG, OWNER_ONLY)


def pending_path(pending_id: str) -> Path:
    """Return a contained pending proposal path or abort on traversal."""

    if not PENDING_ID_RE.fullmatch(pending_id):
        raise SystemExit("error: invalid pending_id: {0}".format(pending_id))
    ensure_private_dir(PENDING_DIR)
    root = PENDING_DIR.resolve()
    path = (PENDING_DIR / "{0}.json".format(pending_id)).resolve()
    if path.parent != root:
        raise SystemExit("error: pending_id escapes pending dir")
    return path


def load_pending(pending_id: str) -> Dict[str, Any]:
    path = pending_path(pending_id)
    if not path.is_file():
        raise SystemExit("error: no such pending proposal: {0}".format(pending_id))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit("error: invalid pending proposal JSON: {0}".format(exc)) from exc
    if not isinstance(payload, dict):
        raise SystemExit("error: pending proposal must be a JSON object")
    return payload


def normalize_sources(sources: Any) -> List[Dict[str, str]]:
    if sources is None:
        return []
    if not isinstance(sources, list):
        raise SystemExit("error: pending source must be a list")
    normalized: List[Dict[str, str]] = []
    for src in sources:
        if isinstance(src, str):
            path = src
        elif isinstance(src, dict) and isinstance(src.get("path"), str):
            path = src["path"]
        else:
            raise SystemExit("error: pending source entries must be paths or {path: ...} objects")
        normalized.append({"path": path})
    return normalized


def proposal_to_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": payload.get("id"),
        "category": payload.get("category"),
        "subject": payload.get("subject") or "Roshan",
        "predicate": payload.get("predicate"),
        "value": payload.get("value"),
        "observed_at": now_utc(),
        "confidence": payload.get("confidence") or "medium",
        "sensitivity": payload.get("sensitivity") or "highly_sensitive_personal_data",
        "tags": list(payload.get("tags") or []),
        "source": normalize_sources(payload.get("source") or []),
        "notes": payload.get("notes"),
        "valid_from": payload.get("valid_from"),
        "valid_to": payload.get("valid_to"),
        "event_date": payload.get("event_date"),
    }


def append_record(facts: Path, record: Dict[str, Any], *, allow_duplicate: bool) -> int:
    """Validate and append one record to the facts store."""

    errors = validate_record(record)
    if errors:
        for err in errors:
            print("error: {0}".format(err), file=sys.stderr)
        return 1

    records = load_records(facts)
    if not allow_duplicate:
        target_key = dedupe_key(record)
        existing = [r for r in records if dedupe_key(r) == target_key]
        if existing:
            existing_ids = ", ".join(r.get("id", "?") for r in existing)
            print(
                "error: dedup conflict on (subject={0!r}, predicate={1!r}, valid_from={2!r}); existing id(s): {3}".format(
                    record["subject"],
                    record["predicate"],
                    record["valid_from"],
                    existing_ids,
                ),
                file=sys.stderr,
            )
            print("hint: pass --allow-duplicate to override", file=sys.stderr)
            return 1
        if any(r.get("id") == record["id"] for r in records):
            print("error: id already exists: {0}".format(record["id"]), file=sys.stderr)
            return 1

    records.append(record)
    save_records(facts, records)
    append_audit("add", record["id"], {
        "category": record["category"],
        "predicate": record["predicate"],
    })
    print("added: {0} (records now: {1})".format(record["id"], len(records)))
    return 0


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_record(record: Dict[str, Any], line_no: Optional[int] = None) -> List[str]:
    """Return a list of human-readable errors. Empty list = valid."""

    errors: List[str] = []
    for field in REQUIRED_FIELDS:
        if field not in record or record.get(field) in (None, ""):
            errors.append("missing required field: {0}".format(field))
    if "confidence" in record and record["confidence"] not in ALLOWED_CONFIDENCE:
        errors.append("invalid confidence: {0!r}".format(record["confidence"]))
    if "sensitivity" in record and record["sensitivity"] not in ALLOWED_SENSITIVITY:
        errors.append("invalid sensitivity: {0!r}".format(record["sensitivity"]))
    if "tags" in record and not isinstance(record["tags"], list):
        errors.append("tags must be a list")
    if "source" in record:
        sources = record["source"]
        if not isinstance(sources, list):
            errors.append("source must be a list")
        else:
            for index, src in enumerate(sources):
                if not isinstance(src, dict) or "path" not in src:
                    errors.append("source[{0}] must be an object with a 'path' key".format(index))
    prefix = "line {0}: ".format(line_no) if line_no else ""
    return [prefix + msg for msg in errors]


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------


def dedupe_key(record: Dict[str, Any]) -> str:
    """Stable identity for dedup: subject + predicate + valid_from + value.

    Two rows that share subject and predicate but carry different values are
    legitimate (e.g., primary vs secondary email, multiple aliases). Only when
    the value also matches do we consider them duplicates.
    """

    value = record.get("value")
    value_repr = json.dumps(value, ensure_ascii=False, sort_keys=True) if value is not None else ""
    return "|".join([
        str(record.get("subject", "")),
        str(record.get("predicate", "")),
        str(record.get("valid_from") or ""),
        value_repr,
    ])


def find_duplicates(records: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Group records that share a dedup key."""

    groups: Dict[str, List[Dict[str, Any]]] = {}
    for record in records:
        groups.setdefault(dedupe_key(record), []).append(record)
    return [group for group in groups.values() if len(group) > 1]


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def cmd_add(args: argparse.Namespace) -> int:
    """Append a fact. --value is JSON; everything else is plain text."""

    try:
        value = json.loads(args.value)
    except json.JSONDecodeError:
        value = args.value

    record: Dict[str, Any] = {
        "id": args.id,
        "category": args.category,
        "subject": args.subject,
        "predicate": args.predicate,
        "value": value,
        "observed_at": args.observed_at or now_utc(),
        "confidence": args.confidence,
        "sensitivity": args.sensitivity,
        "tags": list(args.tag) if args.tag else [],
        "source": [{"path": p} for p in args.source] if args.source else [],
        "notes": args.notes,
        "valid_from": args.valid_from,
        "valid_to": args.valid_to,
        "event_date": args.event_date,
    }

    rc = append_record(args.facts, record, allow_duplicate=args.allow_duplicate)
    if rc != 0:
        return rc
    if not args.no_rebuild:
        return rebuild_index(args.facts)
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    """Approve a pending MCP proposal and append it to the JSONL."""

    path = pending_path(args.pending_id)
    payload = load_pending(args.pending_id)
    record = proposal_to_record(payload)
    rc = append_record(args.facts, record, allow_duplicate=args.allow_duplicate)
    if rc != 0:
        return rc
    path.unlink()
    append_audit("approve_pending", record["id"], {"pending_id": args.pending_id})
    print("approved: {0}".format(args.pending_id))
    if not args.no_rebuild:
        return rebuild_index(args.facts)
    return 0


def cmd_reject(args: argparse.Namespace) -> int:
    """Reject a pending MCP proposal without mutating the JSONL."""

    path = pending_path(args.pending_id)
    payload = load_pending(args.pending_id)
    ensure_private_dir(REJECTED_LOG.parent)
    with REJECTED_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "ts": now_utc(),
            "pending_id": args.pending_id,
            "id": payload.get("id"),
            "reason": args.reason or "",
        }, ensure_ascii=False, sort_keys=True) + "\n")
    os.chmod(REJECTED_LOG, OWNER_ONLY)
    path.unlink()
    append_audit("reject_pending", str(payload.get("id") or "?"), {"pending_id": args.pending_id})
    print("rejected: {0}".format(args.pending_id))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    """Filter and print fact records."""

    records = load_records(args.facts)

    def matches(record: Dict[str, Any]) -> bool:
        if args.category and record.get("category") != args.category:
            return False
        if args.predicate and record.get("predicate") != args.predicate:
            return False
        if args.tag and args.tag not in (record.get("tags") or []):
            return False
        if args.id_contains and args.id_contains not in str(record.get("id", "")):
            return False
        if args.expired_only:
            if not record.get("valid_to"):
                return False
        return True

    hits = [record for record in records if matches(record)]
    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2 if args.pretty else None))
    else:
        for record in hits:
            print("{id}\t{category}\t{predicate}\t{summary}".format(
                id=record.get("id"),
                category=record.get("category"),
                predicate=record.get("predicate"),
                summary=summarize_value(record.get("value")),
            ))
    print("---", file=sys.stderr)
    print("matched {0}/{1} records".format(len(hits), len(records)), file=sys.stderr)
    return 0


def summarize_value(value: Any, limit: int = 80) -> str:
    if value is None:
        return "(none)"
    if isinstance(value, str):
        return value if len(value) <= limit else value[: limit - 1] + "…"
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def cmd_validate(args: argparse.Namespace) -> int:
    records = load_records(args.facts)
    error_count = 0
    seen_ids: set[str] = set()
    for line_no, record in enumerate(records, 1):
        for err in validate_record(record, line_no=line_no):
            print(err, file=sys.stderr)
            error_count += 1
        rid = record.get("id")
        if rid in seen_ids:
            print("line {0}: duplicate id: {1}".format(line_no, rid), file=sys.stderr)
            error_count += 1
        if rid:
            seen_ids.add(rid)
    if error_count:
        print("validate: {0} errors across {1} records".format(error_count, len(records)), file=sys.stderr)
        return 1
    print("validate: ok ({0} records)".format(len(records)))
    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    records = load_records(args.facts)
    duplicate_groups = find_duplicates(records)
    if not duplicate_groups:
        print("dedupe: clean ({0} records)".format(len(records)))
        return 0
    for group in duplicate_groups:
        ids = ", ".join(record.get("id", "?") for record in group)
        print("dup key={key} ids=[{ids}]".format(key=dedupe_key(group[0]), ids=ids))
    return 1


def cmd_expire(args: argparse.Namespace) -> int:
    records = load_records(args.facts)
    found = False
    for record in records:
        if record.get("id") == args.id:
            record["valid_to"] = args.valid_to
            if args.note:
                existing_note = record.get("notes") or ""
                record["notes"] = (existing_note + " " if existing_note else "") + args.note
            found = True
            break
    if not found:
        print("error: id not found: {0}".format(args.id), file=sys.stderr)
        return 1
    save_records(args.facts, records)
    append_audit("expire", args.id, {"valid_to": args.valid_to})
    print("expired: {0} valid_to={1}".format(args.id, args.valid_to))
    if not args.no_rebuild:
        return rebuild_index(args.facts)
    return 0


def cmd_rebuild_index(args: argparse.Namespace) -> int:
    return rebuild_index(args.facts)


def rebuild_index(facts: Path) -> int:
    """Invoke tools/rebuild_fact_index.py and tools/refresh_source_hashes.py."""

    rc = subprocess.call(
        [sys.executable, str(REPO_ROOT / "tools" / "rebuild_fact_index.py"), "--facts", str(facts)],
        cwd=REPO_ROOT,
    )
    if rc != 0:
        return rc
    return subprocess.call(
        [sys.executable, str(REPO_ROOT / "tools" / "refresh_source_hashes.py")],
        cwd=REPO_ROOT,
    )


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="facts", description=__doc__.splitlines()[0])
    parser.add_argument("--facts", type=Path, default=DEFAULT_FACTS, help="Path to the JSONL store")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Append a new fact")
    p_add.add_argument("--id", required=True, help="Stable identifier (e.g., medical.allergies)")
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--predicate", required=True)
    p_add.add_argument("--value", required=True, help="Value (parsed as JSON if possible)")
    p_add.add_argument("--subject", default="Roshan")
    p_add.add_argument("--confidence", choices=sorted(ALLOWED_CONFIDENCE), default="high")
    p_add.add_argument("--sensitivity", choices=sorted(ALLOWED_SENSITIVITY), default="highly_sensitive_personal_data")
    p_add.add_argument("--tag", action="append", help="Tag (repeatable)")
    p_add.add_argument("--source", action="append", help="Source path (repeatable)")
    p_add.add_argument("--notes")
    p_add.add_argument("--valid-from", dest="valid_from")
    p_add.add_argument("--valid-to", dest="valid_to")
    p_add.add_argument("--event-date", dest="event_date")
    p_add.add_argument("--observed-at", dest="observed_at", help="Override observed_at (default: now UTC)")
    p_add.add_argument("--allow-duplicate", action="store_true", help="Skip dedup check")
    p_add.add_argument("--no-rebuild", action="store_true", help="Skip fact-index rebuild after add")
    p_add.set_defaults(func=cmd_add)

    p_approve = sub.add_parser("approve", help="Approve a pending MCP fact proposal")
    p_approve.add_argument("pending_id")
    p_approve.add_argument("--allow-duplicate", action="store_true", help="Skip dedup check")
    p_approve.add_argument("--no-rebuild", action="store_true", help="Skip fact-index rebuild after approve")
    p_approve.set_defaults(func=cmd_approve)

    p_reject = sub.add_parser("reject", help="Reject a pending MCP fact proposal")
    p_reject.add_argument("pending_id")
    p_reject.add_argument("--reason", default="")
    p_reject.set_defaults(func=cmd_reject)

    p_query = sub.add_parser("query", help="Filter facts")
    p_query.add_argument("--category")
    p_query.add_argument("--predicate")
    p_query.add_argument("--tag")
    p_query.add_argument("--id-contains", dest="id_contains")
    p_query.add_argument("--expired-only", action="store_true", help="Only rows with valid_to set")
    p_query.add_argument("--json", action="store_true")
    p_query.add_argument("--pretty", action="store_true", help="Indent JSON output")
    p_query.set_defaults(func=cmd_query)

    p_validate = sub.add_parser("validate", help="Schema-check JSONL")
    p_validate.set_defaults(func=cmd_validate)

    p_dedupe = sub.add_parser("dedupe", help="Report duplicate (subject,predicate,valid_from) groups")
    p_dedupe.set_defaults(func=cmd_dedupe)

    p_expire = sub.add_parser("expire", help="Set valid_to on a fact by id")
    p_expire.add_argument("--id", required=True)
    p_expire.add_argument("--valid-to", dest="valid_to", required=True)
    p_expire.add_argument("--note", help="Append a note explaining the expiry")
    p_expire.add_argument("--no-rebuild", action="store_true")
    p_expire.set_defaults(func=cmd_expire)

    p_rebuild = sub.add_parser("rebuild-index", help="Regenerate the fact-index markdown")
    p_rebuild.set_defaults(func=cmd_rebuild_index)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
