"""Stdio MCP server for the personal-fact knowledge base.

Read tools (always safe):
  - query_facts(category?, predicate?, tag?, id_contains?, expired_only?)
  - expiring_facts(within_days=60)
  - source_coverage()
  - drift_check()
  - validate_facts()
  - list_pending()

Write tool (proposal-only, never directly mutates JSONL):
  - propose_fact(...)        → writes a JSON proposal under
                               secure/cleartext/pending/ for human review.

Approval/rejection is intentionally CLI-only:
    ./bin/llm-wiki facts approve <pending_id>
    ./bin/llm-wiki facts reject <pending_id> --reason "..."

Transport: JSON-RPC 2.0 over stdio, newline-delimited (per MCP stdio spec).

This server is scoped to the KB project via .mcp.json at the repo root.
It is intentionally NOT registered globally or in Claude Desktop, because
Claude Desktop shares session context with OAuth MCP servers (Gmail, Drive,
Figma) — a cross-MCP data-flow risk for personal facts.

To activate: open Claude Code from inside ~/.hermes/knowledge-base/.
The .mcp.json file is gitignored (contains absolute machine path).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import stat
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from wiki_utils import REPO_ROOT, RAW_DIR, now_utc


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "personal-kb"
SERVER_VERSION = "0.1.0"

PENDING_DIR = REPO_ROOT / "secure" / "cleartext" / "pending"
DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"
OWNER_ONLY = stat.S_IRUSR | stat.S_IWUSR
OWNER_ONLY_DIR = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR

IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,119}$")
DATE_RE = re.compile(r"^[0-9]{4}(-[0-9]{2}){0,2}$")
MAX_QUERY_LIMIT = 100
MAX_STRING_LEN = 4096
MAX_PROPOSAL_BYTES = 16384
MAX_TAGS = 20
MAX_SOURCES = 20


# ---------------------------------------------------------------------------
# Shared helpers (delegate to existing tools where possible)
# ---------------------------------------------------------------------------


def run_python(script: str, args: List[str]) -> subprocess.CompletedProcess[str]:
    """Run a tools/* script and capture output."""

    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / script), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def load_records() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    if not DEFAULT_FACTS.exists():
        return records
    try:
        with DEFAULT_FACTS.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        print("warning: skipping malformed JSONL line", file=sys.stderr)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"warning: could not read facts file: {exc}", file=sys.stderr)
    return records


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, OWNER_ONLY_DIR)


def require_string(args: Dict[str, Any], field: str, *, max_len: int = 120) -> str:
    value = args.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError("{0} must be a non-empty string".format(field))
    value = value.strip()
    if len(value) > max_len:
        raise ValueError("{0} is too long".format(field))
    return value


def optional_string(args: Dict[str, Any], field: str, *, max_len: int = MAX_STRING_LEN) -> Optional[str]:
    value = args.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("{0} must be a string".format(field))
    value = value.strip()
    if len(value) > max_len:
        raise ValueError("{0} is too long".format(field))
    return value or None


def require_identifier(args: Dict[str, Any], field: str) -> str:
    value = require_string(args, field)
    if not IDENT_RE.fullmatch(value):
        raise ValueError("{0} contains unsupported characters".format(field))
    return value


def optional_identifier(args: Dict[str, Any], field: str) -> Optional[str]:
    value = optional_string(args, field, max_len=120)
    if value is None:
        return None
    if not IDENT_RE.fullmatch(value):
        raise ValueError("{0} contains unsupported characters".format(field))
    return value


def optional_date(args: Dict[str, Any], field: str) -> Optional[str]:
    value = optional_string(args, field, max_len=32)
    if value is None:
        return None
    if not DATE_RE.fullmatch(value):
        raise ValueError("{0} must be YYYY, YYYY-MM, or YYYY-MM-DD".format(field))
    return value


def bounded_int(args: Dict[str, Any], field: str, default: int, minimum: int, maximum: int) -> int:
    value = args.get(field, default)
    if isinstance(value, bool):
        raise ValueError("{0} must be an integer".format(field))
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("{0} must be an integer".format(field)) from exc
    if parsed < minimum or parsed > maximum:
        raise ValueError("{0} must be between {1} and {2}".format(field, minimum, maximum))
    return parsed


def validate_value(value: Any) -> Any:
    try:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("value must be JSON-serializable") from exc
    if len(encoded.encode("utf-8")) > MAX_STRING_LEN:
        raise ValueError("value is too large")
    if isinstance(value, str) and len(value) > MAX_STRING_LEN:
        raise ValueError("value is too large")
    return value


def validate_tags(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("tags must be an array")
    if len(value) > MAX_TAGS:
        raise ValueError("too many tags")
    tags: List[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("tags must be non-empty strings")
        tag = item.strip()
        if len(tag) > 80 or not re.fullmatch(r"^[A-Za-z0-9_.-]+$", tag):
            raise ValueError("tag contains unsupported characters")
        tags.append(tag)
    return tags


def validate_sources(value: Any) -> List[Dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("source must be an array")
    if len(value) > MAX_SOURCES:
        raise ValueError("too many sources")
    sources: List[Dict[str, str]] = []
    for item in value:
        if isinstance(item, str):
            path = item
        elif isinstance(item, dict) and isinstance(item.get("path"), str):
            path = item["path"]
        else:
            raise ValueError("source entries must be paths or {path: ...} objects")
        path = path.strip()
        if not path or len(path) > 512 or "\x00" in path:
            raise ValueError("invalid source path")
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("source path must be relative and must not traverse directories")
        sources.append({"path": path})
    return sources


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


def tool_query_facts(args: Dict[str, Any]) -> Dict[str, Any]:
    records = load_records()
    category = optional_identifier(args, "category")
    predicate = optional_identifier(args, "predicate")
    tag = optional_string(args, "tag", max_len=80)
    id_contains = optional_string(args, "id_contains", max_len=80)
    expired_only = args.get("expired_only", False)
    if not isinstance(expired_only, bool):
        raise ValueError("expired_only must be a boolean")
    limit = bounded_int(args, "limit", 50, 1, MAX_QUERY_LIMIT)

    def matches(record: Dict[str, Any]) -> bool:
        if category and record.get("category") != category:
            return False
        if predicate and record.get("predicate") != predicate:
            return False
        if tag and tag not in (record.get("tags") or []):
            return False
        if id_contains and id_contains not in str(record.get("id", "")):
            return False
        if expired_only and not record.get("valid_to"):
            return False
        return True

    hits = [record for record in records if matches(record)]
    truncated = len(hits) > limit
    return {
        "matched": len(hits),
        "total": len(records),
        "truncated": truncated,
        "records": hits[:limit],
    }


def tool_expiring_facts(args: Dict[str, Any]) -> Dict[str, Any]:
    within = bounded_int(args, "within_days", 60, 1, 3650)
    proc = run_python("check_expiring_facts.py", ["--within", "{0}d".format(within)])
    return {"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode}


def tool_source_coverage(_: Dict[str, Any]) -> Dict[str, Any]:
    proc = run_python("source_coverage_report.py", [])
    return {"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode}


def tool_drift_check(_: Dict[str, Any]) -> Dict[str, Any]:
    proc = run_python("source_drift_check.py", [])
    return {"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode}


def tool_validate_facts(_: Dict[str, Any]) -> Dict[str, Any]:
    proc = run_python("facts_cli.py", ["validate"])
    return {"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode}


def tool_list_pending(_: Dict[str, Any]) -> Dict[str, Any]:
    ensure_private_dir(PENDING_DIR)
    proposals: List[Dict[str, Any]] = []
    for path in sorted(PENDING_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, FileNotFoundError):
            continue
        proposals.append({"pending_id": path.stem, "proposal": payload})
    return {"count": len(proposals), "pending": proposals}


def tool_propose_fact(args: Dict[str, Any]) -> Dict[str, Any]:
    fact_id = require_identifier(args, "id")
    category = require_identifier(args, "category")
    predicate = require_identifier(args, "predicate")
    if "value" not in args:
        raise ValueError("value is required")
    value = validate_value(args["value"])

    proposal = {
        "proposed_at": now_utc(),
        "proposed_by": optional_string(args, "proposed_by", max_len=120) or "mcp-agent",
        "id": fact_id,
        "category": category,
        "subject": optional_string(args, "subject", max_len=120) or "Roshan",
        "predicate": predicate,
        "value": value,
        "confidence": optional_string(args, "confidence", max_len=16) or "medium",
        "sensitivity": optional_string(args, "sensitivity", max_len=64) or "highly_sensitive_personal_data",
        "tags": validate_tags(args.get("tags")),
        "source": validate_sources(args.get("source")),
        "notes": optional_string(args, "notes", max_len=1000),
        "valid_from": optional_date(args, "valid_from"),
        "valid_to": optional_date(args, "valid_to"),
        "event_date": optional_date(args, "event_date"),
        "rationale": optional_string(args, "rationale", max_len=1000) or "",
    }
    if proposal["confidence"] not in {"high", "medium", "low"}:
        raise ValueError("confidence must be high, medium, or low")
    if proposal["sensitivity"] not in {"highly_sensitive_personal_data", "sensitive_personal_data", "low_sensitivity"}:
        raise ValueError("unsupported sensitivity")

    encoded = json.dumps(proposal, indent=2, ensure_ascii=False)
    if len(encoded.encode("utf-8")) > MAX_PROPOSAL_BYTES:
        raise ValueError("proposal is too large")

    ensure_private_dir(PENDING_DIR)
    pending_id = "{ts}-{rand}".format(
        ts=now_utc().replace(":", "").replace("-", ""),
        rand=secrets.token_hex(6),
    )
    path = PENDING_DIR / "{0}.json".format(pending_id)
    path.write_text(encoded, encoding="utf-8")
    os.chmod(path, OWNER_ONLY)
    return {"pending_id": pending_id, "path": str(path.relative_to(REPO_ROOT))}


def tool_list_staged(_: Dict[str, Any]) -> Dict[str, Any]:
    proc = run_python("process_inbox.py", ["list"])
    if proc.returncode != 0:
        return {"error": proc.stderr.strip() or "list failed", "exit_code": proc.returncode}
    try:
        items = json.loads(proc.stdout) if proc.stdout.strip() else []
    except json.JSONDecodeError:
        items = []
    return {"count": len(items), "staged": items}


_STAGE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


def tool_mark_staged_done(args: Dict[str, Any]) -> Dict[str, Any]:
    stage_id = args.get("stage_id")
    if not isinstance(stage_id, str) or not stage_id.strip():
        return {"error": "stage_id required"}
    stage_id = stage_id.strip()
    if not _STAGE_ID_RE.fullmatch(stage_id):
        return {"error": "stage_id contains unsupported characters"}
    proc = run_python("process_inbox.py", ["done", stage_id])
    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def tool_process_inbox(_: Dict[str, Any]) -> Dict[str, Any]:
    proc = run_python("process_inbox.py", ["process"])
    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------


TOOLS: Dict[str, Dict[str, Any]] = {
    "query_facts": {
        "handler": tool_query_facts,
        "description": "Filter the personal-facts JSONL. All filters are optional.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Exact category match (banking, contact, education, employment, housing, identity, immigration, passport, travel, ...)"},
                "predicate": {"type": "string"},
                "tag": {"type": "string"},
                "id_contains": {"type": "string"},
                "expired_only": {"type": "boolean", "default": False},
                "limit": {"type": "integer", "default": 50},
            },
            "additionalProperties": False,
        },
    },
    "expiring_facts": {
        "handler": tool_expiring_facts,
        "description": "List facts whose valid_to is within N days (default 60).",
        "inputSchema": {
            "type": "object",
            "properties": {"within_days": {"type": "integer", "default": 60}},
            "additionalProperties": False,
        },
    },
    "source_coverage": {
        "handler": tool_source_coverage,
        "description": "Report cited sources that resolve, those that are missing, and unmined raw files.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "drift_check": {
        "handler": tool_drift_check,
        "description": "Compare cited source SHA-256 hashes against the snapshot. Reports new/missing/changed paths.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "validate_facts": {
        "handler": tool_validate_facts,
        "description": "Schema-check every record in the JSONL.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "list_pending": {
        "handler": tool_list_pending,
        "description": "List unapproved fact proposals waiting in the review queue.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "propose_fact": {
        "handler": tool_propose_fact,
        "description": "Propose a new fact. Writes to the pending review queue — DOES NOT mutate the JSONL until approved.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Stable fact id, e.g. 'medical.allergies'"},
                "category": {"type": "string"},
                "predicate": {"type": "string"},
                "value": {
                    "description": "Any JSON-serializable value (string, number, boolean, object, array, null)",
                    "oneOf": [
                        {"type": "string"},
                        {"type": "number"},
                        {"type": "boolean"},
                        {"type": "object"},
                        {"type": "array"},
                        {"type": "null"},
                    ],
                },
                "subject": {"type": "string", "default": "Roshan"},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"], "default": "medium"},
                "sensitivity": {"type": "string", "default": "highly_sensitive_personal_data"},
                "tags": {"type": "array", "items": {"type": "string"}, "default": []},
                "source": {
                    "type": "array",
                    "description": "Either string paths or {path: ...} objects",
                    "items": {
                        "oneOf": [
                            {"type": "string"},
                            {
                                "type": "object",
                                "properties": {"path": {"type": "string"}},
                                "required": ["path"],
                                "additionalProperties": False,
                            },
                        ]
                    },
                },
                "notes": {"type": "string"},
                "valid_from": {"type": "string"},
                "valid_to": {"type": "string"},
                "event_date": {"type": "string"},
                "rationale": {"type": "string", "description": "Why the agent thinks this fact should be added"},
                "proposed_by": {"type": "string"},
            },
            "required": ["id", "category", "predicate", "value"],
            "additionalProperties": False,
        },
    },
    "list_staged": {
        "handler": tool_list_staged,
        "description": "List items in raw/inbox/staged/ awaiting fact extraction.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    "mark_staged_done": {
        "handler": tool_mark_staged_done,
        "description": "Move a staged ingest item from raw/inbox/staged/ to raw/inbox/done/ once its facts are extracted.",
        "inputSchema": {
            "type": "object",
            "properties": {"stage_id": {"type": "string"}},
            "required": ["stage_id"],
            "additionalProperties": False,
        },
    },
    "process_inbox": {
        "handler": tool_process_inbox,
        "description": "Manually run the inbox processor (normally triggered by launchd on raw/inbox/ change).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
}


# ---------------------------------------------------------------------------
# JSON-RPC plumbing
# ---------------------------------------------------------------------------


def respond(message_id: Any, result: Any = None, error: Optional[Dict[str, Any]] = None) -> None:
    payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": message_id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    try:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except (TypeError, ValueError) as exc:
        # Fall back to a safe error response if the payload is not serializable.
        print(f"respond: serialization failed: {exc}", file=sys.stderr)
        fallback = json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": "response serialization failed"}})
        sys.stdout.write(fallback + "\n")
        sys.stdout.flush()


def handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    }


def handle_tools_list(_: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": name,
                "description": spec["description"],
                "inputSchema": spec["inputSchema"],
            }
            for name, spec in TOOLS.items()
        ]
    }


def handle_tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(params, dict):
        raise ValueError("params must be an object")
    name = params.get("name")
    if name not in TOOLS:
        raise ValueError("unknown tool: {0}".format(name))
    arguments = params.get("arguments") or {}
    if not isinstance(arguments, dict):
        raise ValueError("arguments must be an object")
    result = TOOLS[name]["handler"](arguments)
    return {
        "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
        "structuredContent": result,
    }


METHODS: Dict[str, Callable[[Dict[str, Any]], Any]] = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
    "ping": lambda _params: {},
}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--describe", action="store_true", help="Print tool listing as JSON and exit (no stdio loop)")
    args = parser.parse_args(argv)

    if args.describe:
        print(json.dumps(handle_tools_list({}), indent=2))
        return 0

    try:
        _stdin_loop()
    except (BrokenPipeError, KeyboardInterrupt):
        pass
    return 0


def _stdin_loop() -> None:  # noqa: C901
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            respond(None, error={"code": -32700, "message": "parse error: {0}".format(exc)})
            continue

        method = message.get("method")
        message_id = message.get("id")
        raw_params = message.get("params")
        params = raw_params if isinstance(raw_params, dict) else ({} if raw_params is None else raw_params)

        # Notifications (no id) are silently acknowledged.
        if message_id is None:
            continue

        if method not in METHODS:
            respond(message_id, error={"code": -32601, "message": "method not found: {0}".format(method)})
            continue

        try:
            result = METHODS[method](params)
            respond(message_id, result=result)
        except ValueError as exc:
            respond(message_id, error={
                "code": -32602,
                "message": str(exc),
            })
        except Exception:  # noqa: BLE001
            traceback.print_exc(file=sys.stderr)
            respond(message_id, error={
                "code": -32000,
                "message": "internal server error",
            })


if __name__ == "__main__":
    sys.exit(main())
