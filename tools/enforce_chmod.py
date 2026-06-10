"""Force chmod 0600 on personal-sensitive files in the knowledge base.

Idempotent. Runs from the pre-commit hook and from cron. Designed to complement
the sensitivity-aware redactor in tools/build_site_manifest.py: that tool keeps
PII out of the published site-manifest.json, this tool keeps the source files
themselves owner-only on disk.

Targets:
  - wiki/syntheses/context/roshan-personal-*.md
  - wiki/syntheses/context/roshan-profile-context.md
  - wiki/sources/roshan-personal-*.md
  - wiki/sources/roshan-profile-*.md
  - raw/transcripts/**/roshan-personal-*.{md,jsonl}
  - raw/transcripts/**/roshan-profile*.md
  - secure/cleartext/**/* (any cleartext under the secure tree)
  - raw/inbox and secure directories are forced to 0700

Exit code is 0 on success (including no-op), 1 on permission errors.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Iterable, List

from wiki_utils import REPO_ROOT


PERSONAL_GLOBS = [
    "wiki/syntheses/context/roshan-personal-*.md",
    "wiki/syntheses/context/roshan-profile-context.md",
    "wiki/sources/roshan-personal-*.md",
    "wiki/sources/roshan-profile-*.md",
    "raw/transcripts/**/roshan-personal-*.md",
    "raw/transcripts/**/roshan-profile*.md",
    "raw/transcripts/**/*roshan-personal*facts*.jsonl",
    "secure/cleartext/**/*",
]

PERMISSION_FILE_GLOBS = PERSONAL_GLOBS + [
    "secure/source-hashes.json",
    "secure/encrypted/*.age",
    "raw/inbox/**/*",
]

PRIVATE_DIR_GLOBS = [
    "raw/inbox",
    "raw/inbox/**/*",
    "secure",
    "secure/cleartext",
    "secure/cleartext/**/*",
    "secure/encrypted",
]

OWNER_ONLY = stat.S_IRUSR | stat.S_IWUSR  # 0o600
OWNER_ONLY_DIR = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR  # 0o700


def iter_targets(globs: Iterable[str]) -> List[Path]:
    """Resolve all matching files under the repo root."""

    seen: set[Path] = set()
    matches: List[Path] = []
    for pattern in globs:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            matches.append(resolved)
    return sorted(matches)


def iter_dirs(globs: Iterable[str]) -> List[Path]:
    """Resolve all matching directories under the repo root."""

    seen: set[Path] = set()
    matches: List[Path] = []
    for pattern in globs:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_dir():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            matches.append(resolved)
    return sorted(matches)


def enforce(path: Path, mode: int, dry_run: bool) -> bool:
    """Force a mode on a single path. Returns True if a change was needed."""

    current = stat.S_IMODE(path.stat().st_mode)
    if current == mode:
        return False
    if not dry_run:
        os.chmod(path, mode)
    return True


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    parser.add_argument("--quiet", action="store_true", help="Only print on change or error")
    args = parser.parse_args(argv)

    file_targets = iter_targets(PERMISSION_FILE_GLOBS)
    dir_targets = iter_dirs(PRIVATE_DIR_GLOBS)
    changed = 0
    errors = 0

    for path in dir_targets:
        try:
            if enforce(path, OWNER_ONLY_DIR, args.dry_run):
                changed += 1
                rel = path.relative_to(REPO_ROOT)
                action = "would chmod" if args.dry_run else "chmod"
                print("{action} 0700 {rel}".format(action=action, rel=rel))
        except OSError as exc:
            errors += 1
            print("error: {path}: {exc}".format(path=path, exc=exc), file=sys.stderr)

    for path in file_targets:
        try:
            if enforce(path, OWNER_ONLY, args.dry_run):
                changed += 1
                rel = path.relative_to(REPO_ROOT)
                action = "would chmod" if args.dry_run else "chmod"
                print("{action} 0600 {rel}".format(action=action, rel=rel))
        except OSError as exc:
            errors += 1
            print("error: {path}: {exc}".format(path=path, exc=exc), file=sys.stderr)

    if not args.quiet:
        print("enforce_chmod: scanned {n} files, changed {c}, errors {e}".format(
            n=len(file_targets) + len(dir_targets), c=changed, e=errors,
        ))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
