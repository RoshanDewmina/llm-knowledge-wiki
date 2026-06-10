"""SHA-256 drift detection for personal-fact source documents.

For each unique source path cited from the personal-facts JSONL, computes a
SHA-256 digest and compares against a snapshot file. If a digest changes, the
source document was modified, replaced, or a path collision exists — facts
extracted from it may be stale.

Snapshot file: secure/source-hashes.json (kept under secure/ so it lives
alongside other sensitive bookkeeping; chmod 0600).

First run records the baseline. Subsequent runs report new, missing, and
changed paths. --strict exits non-zero on drift; --update overwrites the
snapshot to accept the current state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Dict, List

from wiki_utils import REPO_ROOT, RAW_DIR

_HOME = str(Path.home())


def _display_path(path_str: str) -> str:
    """Sanitize absolute paths to ~/... to avoid leaking iCloud directory structure."""
    if path_str.startswith(_HOME + "/"):
        return "~/" + path_str[len(_HOME) + 1:]
    return path_str


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"
DEFAULT_SNAPSHOT = REPO_ROOT / "secure" / "source-hashes.json"
OWNER_ONLY = stat.S_IRUSR | stat.S_IWUSR


def load_records(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def collect_paths(records: List[Dict[str, Any]]) -> List[str]:
    seen: List[str] = []
    visited: set[str] = set()
    for record in records:
        for src in record.get("source", []) or []:
            path = src.get("path") if isinstance(src, dict) else str(src)
            if path and path not in visited:
                visited.add(path)
                seen.append(path)
    return sorted(seen)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_state(paths: List[str]) -> Dict[str, Any]:
    state: Dict[str, Any] = {}
    for path_str in paths:
        path = Path(path_str)
        if not path.is_file():
            state[path_str] = {"present": False}
            continue
        st = path.stat()
        state[path_str] = {
            "present": True,
            "sha256": sha256(path),
            "size": st.st_size,
            "mtime": int(st.st_mtime),
        }
    return state


def diff_state(prev: Dict[str, Any], curr: Dict[str, Any]) -> Dict[str, List[str]]:
    new = [p for p in curr if p not in prev]
    missing = [p for p in prev if p not in curr]
    changed: List[str] = []
    became_missing: List[str] = []
    for path_str, entry in curr.items():
        if path_str not in prev:
            continue
        old = prev[path_str]
        if not entry.get("present") and old.get("present"):
            became_missing.append(path_str)
            continue
        if entry.get("present") and old.get("present") and entry.get("sha256") != old.get("sha256"):
            changed.append(path_str)
    return {
        "new": sorted(new),
        "missing": sorted(missing),
        "became_missing": sorted(became_missing),
        "changed": sorted(changed),
    }


def write_snapshot(snapshot_path: Path, state: Dict[str, Any]) -> None:
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    os.chmod(snapshot_path, OWNER_ONLY)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--facts", type=Path, default=DEFAULT_FACTS)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--update", action="store_true", help="Overwrite the snapshot")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on drift")
    args = parser.parse_args(argv)

    if not args.facts.exists():
        print("error: facts file not found: {0}".format(args.facts), file=sys.stderr)
        return 2

    records = load_records(args.facts)
    paths = collect_paths(records)
    current = compute_state(paths)

    if not args.snapshot.exists():
        write_snapshot(args.snapshot, current)
        print("source_drift_check: baseline written ({0} paths)".format(len(paths)))
        return 0

    previous = json.loads(args.snapshot.read_text(encoding="utf-8"))
    diff = diff_state(previous, current)

    print("# Source drift report")
    print()
    print("- {0} cited paths".format(len(paths)))
    for kind, items in diff.items():
        print("- {0}: {1}".format(kind, len(items)))
    print()
    for kind, items in diff.items():
        if not items:
            continue
        print("## {0}".format(kind))
        for item in items:
            print("- `{0}`".format(_display_path(item)))
        print()

    drift = any(diff[kind] for kind in ("became_missing", "changed", "new"))

    if args.update:
        write_snapshot(args.snapshot, current)
        print("source_drift_check: snapshot updated")

    if args.strict and drift:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
