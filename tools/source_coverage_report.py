"""Audit source coverage of the personal-facts JSONL.

For each unique source.path referenced from the JSONL: is the underlying file
still resolvable on disk? Missing paths are a drift signal — the source moved,
was renamed, or was deleted.

Also lists raw/transcripts/2026 files that are NOT referenced from any JSONL
record. Those are candidates for re-mining or pruning.

Output is markdown so the report can be appended to wiki/reviews/review-queue.md
or piped into the AI briefing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from wiki_utils import RAW_DIR


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"


def load_records(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def collect_source_paths(records: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Map each source.path to the list of fact-ids that cite it."""

    citations: Dict[str, List[str]] = {}
    for record in records:
        for src in record.get("source", []) or []:
            if isinstance(src, dict):
                path = src.get("path", "")
            else:
                path = str(src)
            if path:
                citations.setdefault(path, []).append(record.get("id", "?"))
    return citations


def collect_raw_files(raw_root: Path, glob: str) -> List[Path]:
    """Walk raw/ and return matching files."""

    return sorted(p for p in raw_root.glob(glob) if p.is_file())


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--facts", type=Path, default=DEFAULT_FACTS)
    parser.add_argument(
        "--raw-glob",
        default="transcripts/2026/**/*",
        help="Glob (relative to raw/) for unmined-file scan (default: %(default)s)",
    )
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any drift detected")
    args = parser.parse_args(argv)

    records = load_records(args.facts)
    citations = collect_source_paths(records)

    missing: List[str] = []
    present: List[str] = []
    for path in sorted(citations):
        if Path(path).is_file():
            present.append(path)
        else:
            missing.append(path)

    raw_files = collect_raw_files(RAW_DIR, args.raw_glob)
    cited_raw = {Path(p).resolve() for p in citations if str(p).startswith(str(RAW_DIR))}
    facts_path_resolved = args.facts.resolve()
    unmined: List[Path] = []
    for raw_file in raw_files:
        resolved = raw_file.resolve()
        if resolved == facts_path_resolved:
            continue
        if resolved in cited_raw:
            continue
        unmined.append(raw_file)

    print("# Source coverage report")
    print()
    print("Generated against `{0}` ({1} records).".format(args.facts, len(records)))
    print()

    print("## Cited sources (resolvable)")
    print()
    print("- {0} unique paths resolve on disk.".format(len(present)))
    print()

    print("## Cited sources (missing)")
    print()
    if not missing:
        print("- None — every cited source path resolves.")
    else:
        for path in missing:
            ids = ", ".join(citations[path])
            print("- `{path}` (cited by: {ids})".format(path=path, ids=ids))
    print()

    print("## Unmined raw files")
    print()
    if not unmined:
        print("- None under `{0}`.".format(args.raw_glob))
    else:
        for path in unmined:
            print("- `{0}`".format(path))

    drift = bool(missing)
    if args.strict and drift:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
