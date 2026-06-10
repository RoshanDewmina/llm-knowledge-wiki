"""Refresh the `source_hash:` frontmatter on wiki source pages.

Every wiki/sources/*.md that declares both `source_path:` and `source_hash:` is
checked: the actual SHA-256 of the referenced raw file is recomputed and
written back when it has drifted. This keeps the existing stale_pages health
check happy after legitimate JSONL/raw mutations.

Idempotent. Safe to run from cron, the facts CLI, or by hand. Output mirrors
build_site_manifest.py's style (one line per change).
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import List

from wiki_utils import REPO_ROOT, WIKI_DIR, now_utc, read_text, write_text_if_changed


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def update_frontmatter(text: str, key: str, value: str) -> str:
    """Replace a single-line frontmatter key in-place. No-op if key missing."""

    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    head = text[: end + 5]
    body = text[end + 5 :]
    new_lines = []
    replaced = False
    for line in head.splitlines(keepends=True):
        if line.startswith("{0}:".format(key)) and not replaced:
            new_lines.append("{0}: {1}\n".format(key, value))
            replaced = True
        else:
            new_lines.append(line)
    return "".join(new_lines) + body if replaced else text


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="Exit non-zero if any source page would change")
    args = parser.parse_args(argv)

    sources_dir = WIKI_DIR / "sources"
    if not sources_dir.is_dir():
        print("no wiki/sources/ directory")
        return 0

    changes = 0
    for md in sorted(sources_dir.glob("*.md")):
        text = read_text(md)
        if not text.startswith("---\n"):
            continue
        head_end = text.find("\n---\n", 4)
        if head_end == -1:
            continue
        head = text[4:head_end]
        source_path: str | None = None
        recorded_hash: str | None = None
        for line in head.splitlines():
            if line.startswith("source_path:"):
                source_path = line.split(":", 1)[1].strip()
            elif line.startswith("source_hash:"):
                recorded_hash = line.split(":", 1)[1].strip()
        if not source_path or not recorded_hash:
            continue
        raw = source_path if Path(source_path).is_absolute() else (REPO_ROOT / source_path)
        if not raw.is_file():
            continue
        current = sha256(raw)
        if current == recorded_hash:
            continue
        if args.check:
            print("would update {0}: {1}... -> {2}...".format(
                md.relative_to(REPO_ROOT),
                recorded_hash[:8],
                current[:8],
            ))
            changes += 1
            continue
        updated = update_frontmatter(text, "source_hash", current)
        updated = update_frontmatter(updated, "updated", now_utc())
        if write_text_if_changed(md, updated):
            print("refreshed {0}: {1}... -> {2}...".format(
                md.relative_to(REPO_ROOT),
                recorded_hash[:8],
                current[:8],
            ))
            changes += 1

    if not changes:
        print("refresh_source_hashes: all source pages up to date")
    elif args.check:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
