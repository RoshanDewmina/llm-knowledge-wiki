"""Validate study workflow pages."""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Any

from wiki_utils import RAW_DIR, WIKI_DIR, expand_markdown_targets, extract_wikilinks, load_markdown_page, path_to_wiki_ref, repo_relative, wiki_ref_to_path

SRC_COMMENT_RE = re.compile(r"<!--\s*src:\s*\[\[[^\]]+\]\]\s*-->")
CARD_SPLIT_RE = re.compile(r"\n(?=(?:[#>-]|.*::|.*\?))")


def extract_section(body: str, heading: str) -> str:
    capture = False; lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if capture: break
            capture = line[3:].strip().lower() == heading.lower()
            continue
        if capture: lines.append(line)
    return "\n".join(lines).strip()


def raw_lines() -> list[str]:
    lines: list[str] = []
    for path in (RAW_DIR / "papers").rglob("*.md"):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if len(stripped) > 40:
                lines.append(stripped.lower())
    return lines


def too_close_to_raw(card: str, raw: list[str]) -> bool:
    text = " ".join(card.lower().split())
    if len(text) < 40:
        return False
    for line in raw:
        words = line.split()
        if len(words) < 8:
            continue
        overlap = sum(1 for word in text.split() if word in set(words)) / max(len(text.split()), 1)
        if overlap > 0.5 and line[:60] in text:
            return True
    return False


def validate_page(path: Path, raw_cache: list[str]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    ref = path_to_wiki_ref(path)
    fm, body = load_markdown_page(path)
    if fm.get("type") != "study":
        return errors
    kind = str(fm.get("study_kind"))
    if kind == "paper":
        tracker = extract_section(body, "Mastery Tracker")
        for line in tracker.splitlines():
            if not line.startswith("|") or "---" in line or "Concept Page" in line:
                continue
            if "[[concepts/" not in line:
                errors.append({"path": repo_relative(path), "message": "mastery tracker row lacks a concepts/ wikilink"})
                break
    if kind == "anki":
        cards = [chunk.strip() for chunk in CARD_SPLIT_RE.split(extract_section(body, "Cards")) if chunk.strip() and not chunk.strip().startswith("<!--")]
        for card in cards:
            if not SRC_COMMENT_RE.search(card):
                errors.append({"path": repo_relative(path), "message": "Anki card missing `<!-- src: [[...]] -->` comment"})
                break
            if too_close_to_raw(card, raw_cache):
                errors.append({"path": repo_relative(path), "message": "Anki card appears copied from raw paper text"})
                break
    if kind == "implementation":
        checklist = extract_section(body, "Equivalence-Check Checklist")
        if "[ ]" not in checklist and "[x]" not in checklist.lower():
            errors.append({"path": repo_relative(path), "message": "toy implementation needs an equivalence-check checklist"})
    if str(fm.get("read_status")) == "done" and not extract_section(body, "Citations"):
        errors.append({"path": repo_relative(path), "message": "done studies must have non-empty Citations"})
    for source in fm.get("source_pages", []) if isinstance(fm.get("source_pages"), list) else []:
        target = wiki_ref_to_path(str(source))
        if not target.exists():
            errors.append({"path": repo_relative(path), "message": f"study source_pages entry does not exist: {source}"})
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        files = expand_markdown_targets(args.paths, default_root=WIKI_DIR / "studies") if (WIKI_DIR / "studies").exists() else []
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}")
        return 2
    raw_cache = raw_lines()
    errors: list[dict[str, Any]] = []
    for path in files:
        errors.extend(validate_page(path, raw_cache))
    if args.json:
        print(json.dumps(errors, indent=2))
    elif errors:
        for error in errors: print(f"{error['path']}: {error['message']}")
    else:
        print(f"ok: checked {len(files)} study markdown files")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
