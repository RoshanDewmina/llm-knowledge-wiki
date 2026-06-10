"""Scan the published site-manifest and git tree for PII needles.

Complements tools/build_site_manifest.py: that file redacts sensitive page
bodies before publishing, this script verifies the redaction held and that no
sensitive value slipped into a non-sensitive page or a tracked file.

Strategy:
  1. Load the personal-facts JSONL and harvest high-risk needles (specific
     scalar value fields and specific keys inside dict-valued facts).
  2. Scan wiki/.cache/site-manifest.json for any needle. Hits indicate the
     redactor missed a page or a non-sensitive page leaked the value.
  3. Scan git-tracked files (`git ls-files`) for any needle. Hits indicate a
     file that should be gitignored or had PII pasted into it.

Exit codes: 0 clean, 1 leak found, 2 setup error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, List, Set, Tuple

from wiki_utils import REPO_ROOT, RAW_DIR


DEFAULT_FACTS = RAW_DIR / "transcripts" / "2026" / "2026-05-09-roshan-personal-facts.jsonl"
SITE_MANIFEST = REPO_ROOT / "wiki" / ".cache" / "site-manifest.json"

# Predicates whose scalar `value` field is fully sensitive and should be a needle.
TOP_LEVEL_PREDICATES = {
    "passport_number",
    "uci_client_id",
    "work_permit_application_number",
    "study_permit_application_number",
    "work_permit_document_number",
    "study_permit_document_number",
    "study_permit_secondary_control_number",
    "carleton_student_id",
    "ontario_education_number",
    "date_of_birth",
    "phone",
    "email",
    "sin_document_path",
    "canadian_trv_counterfoil",
}

# Keys inside dict-valued facts whose scalar leaves should be needles. Third-
# party professional names (supervisor, manager, instructor, professor) are
# intentionally NOT included — those are usually public and would generate
# false positives against syllabi, profile pages, etc.
NESTED_VALUE_KEYS = {
    "account_number",
    "branch_transit",
    "direct_deposit_masked_account",
    "transit",
    "policy_number",
    "policy",
    "booking_ref",
    "booking_confirmation",
    "ticket_number",
    "confirmation",
    "frequent_flyer",
    "aeroplan",
    "evisa_number",
    "control_number",
    "guarantor_name",
    "roommate",
    "lease_number",
    "lease_id",
}

# Strings shorter than this are too generic to flag.
MIN_NEEDLE_LEN = 6

# Generic strings that may be values but are public knowledge / non-sensitive.
ALLOWLIST: Set[str] = {
    "Canada",
    "Ontario",
    "Ottawa",
    "Toronto",
    "Malaysia",
    "Carleton",
    "CIBC",
    "Cathay",
    "Booking",
    "Roshan",  # first name appears in many public contexts (cover letters, headers)
    "December",
    "April",
    "Single",
    "Male",
    "Female",
    "MR",
}


def harvest_strings(node: Any, key_filter: Set[str] | None = None) -> List[str]:
    """Recursively collect string leaves; if key_filter given, keep only those keys."""

    out: List[str] = []
    if isinstance(node, str):
        if key_filter is None:
            out.append(node)
        return out
    if isinstance(node, dict):
        for k, v in node.items():
            if key_filter is not None and k in key_filter:
                if isinstance(v, str):
                    out.append(v)
                else:
                    out.extend(harvest_strings(v, key_filter=None))
            else:
                out.extend(harvest_strings(v, key_filter=key_filter))
        return out
    if isinstance(node, list):
        for item in node:
            out.extend(harvest_strings(item, key_filter=key_filter))
        return out
    return out


def needle_acceptable(text: str) -> bool:
    """Filter generic short strings and allowlist hits."""

    cleaned = text.strip()
    if len(cleaned) < MIN_NEEDLE_LEN:
        return False
    if cleaned in ALLOWLIST:
        return False
    # Strip pure-alpha titles like "Roshan Dewmina Imalsha Silva Pulle" — keep
    # multi-word names since they are distinctive PII.
    return True


def build_needles(facts_path: Path) -> Tuple[Set[str], int]:
    """Read JSONL and assemble the needle set."""

    needles: Set[str] = set()
    record_count = 0
    with facts_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            record_count += 1
            predicate = record.get("predicate", "")
            value = record.get("value")

            if predicate in TOP_LEVEL_PREDICATES and isinstance(value, str):
                if needle_acceptable(value):
                    needles.add(value)

            if isinstance(value, (dict, list)):
                for harvested in harvest_strings(value, key_filter=NESTED_VALUE_KEYS):
                    if needle_acceptable(harvested):
                        needles.add(harvested)

    return needles, record_count


def scan_manifest(manifest_path: Path, needles: Set[str]) -> List[Tuple[str, str]]:
    """Return (needle, page_path) for each leak found in the manifest."""

    if not manifest_path.exists():
        return []
    text = manifest_path.read_text(encoding="utf-8")
    hits: List[Tuple[str, str]] = []
    # Per-page granularity for better diagnostics.
    try:
        manifest = json.loads(text)
        pages = manifest.get("pages", [])
    except json.JSONDecodeError:
        # Fall back to whole-text scan if structure changes.
        for needle in needles:
            if needle in text:
                hits.append((needle, str(manifest_path.relative_to(REPO_ROOT))))
        return hits
    for page in pages:
        page_path = page.get("relative_path", "<unknown>")
        page_text = json.dumps(page, ensure_ascii=False)
        for needle in needles:
            if needle in page_text:
                hits.append((needle, page_path))
    return hits


def git_tracked_files() -> List[Path]:
    """Return the list of git-tracked files."""

    try:
        out = subprocess.check_output(
            ["git", "ls-files"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    files: List[Path] = []
    for line in out.decode("utf-8").splitlines():
        if not line.strip():
            continue
        path = REPO_ROOT / line
        if path.is_file():
            files.append(path)
    return files


def scan_git_tree(needles: Set[str]) -> List[Tuple[str, str]]:
    """Return (needle, file_path) for each leak found in git-tracked files."""

    hits: List[Tuple[str, str]] = []
    for path in git_tracked_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for needle in needles:
            if needle in text:
                rel = path.relative_to(REPO_ROOT).as_posix()
                hits.append((needle, rel))
    return hits


def redact(needle: str) -> str:
    """Return a safe placeholder for stdout, never printing the raw needle."""

    if len(needle) <= 4:
        return "*" * len(needle)
    return needle[:1] + "*" * (len(needle) - 2) + needle[-1:]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--facts",
        type=Path,
        default=DEFAULT_FACTS,
        help="Path to the personal-facts JSONL (default: %(default)s)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=SITE_MANIFEST,
        help="Path to the published site-manifest JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat manifest absence as failure",
    )
    parser.add_argument(
        "--show-needles",
        action="store_true",
        help="Print redacted previews of each needle (debug)",
    )
    args = parser.parse_args(argv)

    if not args.facts.exists():
        print("error: facts file not found: {0}".format(args.facts), file=sys.stderr)
        return 2

    needles, record_count = build_needles(args.facts)
    if not needles:
        print("warning: no needles harvested from {0}".format(args.facts), file=sys.stderr)
        return 0

    if args.show_needles:
        for needle in sorted(needles):
            print("needle: {0}".format(redact(needle)))

    if args.strict and not args.manifest.exists():
        print("error: manifest missing: {0}".format(args.manifest), file=sys.stderr)
        return 2

    manifest_hits = scan_manifest(args.manifest, needles)
    git_hits = scan_git_tree(needles)

    if not manifest_hits and not git_hits:
        print("audit_pii_leaks: clean ({0} records, {1} needles, manifest+git scanned)".format(
            record_count, len(needles),
        ))
        return 0

    print("LEAK DETECTED", file=sys.stderr)
    for needle, location in manifest_hits:
        print("manifest leak: {0} -> {1}".format(redact(needle), location), file=sys.stderr)
    for needle, location in git_hits:
        print("git-tracked leak: {0} -> {1}".format(redact(needle), location), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
