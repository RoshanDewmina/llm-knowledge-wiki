"""Process new files dropped into raw/inbox/ and stage them for fact extraction.

Designed to run from launchd whenever raw/inbox/ changes (and idempotent if
invoked manually). Steps per file:

  1. SHA-256 fingerprint.
  2. Try plain-text extraction:
       - .md/.txt/.json    → read as-is
       - .pdf              → pdftotext (poppler) if available
       - images / scans   → flagged needs_ocr; skipped here
  3. Move the original + extracted text into a fresh staged directory:
       raw/inbox/staged/YYYYMMDDTHHMMSSZ-<safe-name>/
  4. Drop a stage.json describing the file so an agent / MCP client can
     enumerate the queue.

After staging, the agent (via MCP `list_staged` + `propose_fact`) extracts
facts and proposes them. Approval is CLI-only. When done, run `done <stage_id>` to
move that staged dir under raw/inbox/done/.

This script never auto-mutates the JSONL.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from wiki_utils import REPO_ROOT, now_utc


INBOX_DIR = REPO_ROOT / "raw" / "inbox"
STAGED_DIR = INBOX_DIR / "staged"
DONE_DIR = INBOX_DIR / "done"
LOG_PATH = Path.home() / ".hermes" / "logs" / "inbox-watcher.log"

TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".tsv", ".log"}
PDF_SUFFIXES = {".pdf"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".webp"}
SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")
STAGE_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[A-Za-z0-9._-]{1,80}$")
OWNER_ONLY_FILE = stat.S_IRUSR | stat.S_IWUSR
OWNER_ONLY_DIR = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, OWNER_ONLY_DIR)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def require_contained_child(path: Path, root: Path) -> None:
    root_resolved = root.resolve()
    candidate = path.resolve(strict=False)
    if candidate.parent != root_resolved or not is_relative_to(candidate, root_resolved):
        raise OSError("path escapes inbox root: {0}".format(path.name))


def require_regular_file(path: Path) -> None:
    st = path.lstat()
    if path.is_symlink():
        raise OSError("refusing symlink: {0}".format(path.name))
    if not stat.S_ISREG(st.st_mode):
        raise OSError("refusing non-regular file: {0}".format(path.name))


def require_stage_id(stage_id: str) -> None:
    if not STAGE_ID_RE.fullmatch(stage_id):
        raise SystemExit("invalid stage_id: {0}".format(stage_id))


def log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write("{0} {1}\n".format(now_utc(), message))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_text(path: Path) -> Dict[str, Any]:
    """Return {extracted, status, hint}."""

    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        try:
            return {
                "extracted": path.read_text(encoding="utf-8", errors="replace"),
                "status": "extracted",
                "extractor": "read_text",
            }
        except OSError as exc:
            return {"extracted": "", "status": "error", "hint": str(exc)}

    if suffix in PDF_SUFFIXES:
        if shutil.which("pdftotext") is None:
            return {
                "extracted": "",
                "status": "needs_ocr",
                "hint": "pdftotext not installed; run `brew install poppler` or use the ocr-and-documents skill",
            }
        try:
            proc = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode == 0:
                return {
                    "extracted": proc.stdout,
                    "status": "extracted",
                    "extractor": "pdftotext",
                }
            return {
                "extracted": "",
                "status": "error",
                "hint": "pdftotext exit {0}: {1}".format(proc.returncode, proc.stderr.strip()),
            }
        except OSError as exc:
            return {"extracted": "", "status": "error", "hint": str(exc)}

    if suffix in IMAGE_SUFFIXES:
        return {
            "extracted": "",
            "status": "needs_ocr",
            "hint": "image — run the ocr-and-documents skill (marker-pdf or external OCR)",
        }

    return {
        "extracted": "",
        "status": "unknown_type",
        "hint": "unsupported suffix {0!r}".format(suffix),
    }


def safe_name(value: str) -> str:
    cleaned = SAFE_NAME.sub("-", value).strip("-")
    return cleaned[:80] or "file"


def stage_file(path: Path) -> Path:
    """Move one inbox file into a fresh staged directory."""

    require_contained_child(path, INBOX_DIR)
    require_regular_file(path)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stage_id = "{0}-{1}".format(timestamp, safe_name(path.stem))
    target_dir = STAGED_DIR / stage_id
    target_dir.mkdir(parents=True, mode=OWNER_ONLY_DIR, exist_ok=False)
    os.chmod(target_dir, OWNER_ONLY_DIR)

    new_original = target_dir / path.name
    path.rename(new_original)
    require_regular_file(new_original)
    os.chmod(new_original, OWNER_ONLY_FILE)

    digest = sha256(new_original)
    extraction = extract_text(new_original)

    if extraction.get("extracted"):
        extracted_path = target_dir / "extracted.txt"
        extracted_path.write_text(extraction["extracted"], encoding="utf-8")
        os.chmod(extracted_path, OWNER_ONLY_FILE)

    metadata = {
        "stage_id": stage_id,
        "staged_at": now_utc(),
        "original_filename": path.name,
        "original_size": new_original.stat().st_size,
        "sha256": digest,
        "extraction_status": extraction.get("status"),
        "extractor": extraction.get("extractor"),
        "hint": extraction.get("hint"),
    }
    stage_json = target_dir / "stage.json"
    stage_json.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    os.chmod(stage_json, OWNER_ONLY_FILE)

    log("staged {0} -> {1} (status={2})".format(path.name, stage_id, extraction.get("status")))
    return target_dir


def list_staged() -> List[Dict[str, Any]]:
    if not STAGED_DIR.exists():
        return []
    items: List[Dict[str, Any]] = []
    for child in sorted(STAGED_DIR.iterdir()):
        if child.is_symlink() or not child.is_dir():
            continue
        meta_file = child / "stage.json"
        if meta_file.is_symlink() or not meta_file.is_file():
            continue
        try:
            items.append(json.loads(meta_file.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return items


def mark_done(stage_id: str) -> Dict[str, Any]:
    require_stage_id(stage_id)
    ensure_private_dir(DONE_DIR)
    src = STAGED_DIR / stage_id
    root = STAGED_DIR.resolve()
    src_resolved = src.resolve(strict=False)
    if not is_relative_to(src_resolved, root) or src_resolved.parent != root:
        raise SystemExit("stage_id escapes staged dir")
    if src.is_symlink() or not src.is_dir():
        raise SystemExit("no such staged dir: {0}".format(stage_id))
    target = DONE_DIR / stage_id
    if target.exists():
        raise SystemExit("done dir already exists: {0}".format(target))
    src.rename(target)
    os.chmod(target, OWNER_ONLY_DIR)
    log("marked done {0}".format(stage_id))
    return {"moved_to": str(target.relative_to(REPO_ROOT))}


def process() -> Dict[str, Any]:
    ensure_private_dir(INBOX_DIR)
    ensure_private_dir(STAGED_DIR)
    staged: List[str] = []
    for entry in sorted(INBOX_DIR.iterdir()):
        if entry.is_symlink():
            log("refusing symlink {0}".format(entry.name))
            continue
        if entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        try:
            target = stage_file(entry)
            staged.append(target.name)
        except OSError as exc:
            log("error staging {0}: {1}".format(entry.name, exc))
    return {"staged": staged, "count": len(staged)}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    sub.required = False

    process_p = sub.add_parser("process", help="Process new files in raw/inbox (default)")
    process_p.set_defaults(func=lambda _a: print(json.dumps(process(), indent=2)))

    list_p = sub.add_parser("list", help="List staged ingest items")
    list_p.set_defaults(func=lambda _a: print(json.dumps(list_staged(), indent=2)))

    done_p = sub.add_parser("done", help="Mark a staged item complete")
    done_p.add_argument("stage_id")
    done_p.set_defaults(func=lambda a: print(json.dumps(mark_done(a.stage_id), indent=2)))

    args = parser.parse_args(argv)
    if args.command is None:
        # Default action when run without subcommand (launchd path).
        result = process()
        log("processed {0} file(s)".format(result["count"]))
        return 0
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
