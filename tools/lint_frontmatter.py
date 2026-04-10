"""Validate frontmatter keys and value shapes for wiki pages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from wiki_utils import (
    CONTENT_TYPES,
    DERIVED_TYPES,
    LIGHTWEIGHT_TYPES,
    RAW_DIR,
    VALID_STATUSES,
    WIKI_DIR,
    ensure_under_root,
    expand_markdown_targets,
    is_special_wiki_page,
    load_markdown_page,
    normalize_wiki_ref,
    parse_timestamp,
    path_to_wiki_ref,
    repo_relative,
    resolve_repo_path,
    wiki_ref_to_path,
)

COMMON_REQUIRED = {"title", "type", "created", "updated", "status", "confidence", "related"}
SOURCE_REQUIRED = {"source_path", "source_kind", "compiled_at", "source_hash"}
DERIVED_REQUIRED = {"source_pages", "compiled_at"}
LIGHTWEIGHT_REQUIRED = {"source_pages", "compiled_at"}


def validate_page(path: Path) -> list[dict[str, Any]]:
    """Validate frontmatter for one page."""

    errors: list[dict[str, Any]] = []
    ref = path_to_wiki_ref(path)
    if is_special_wiki_page(ref):
        return errors

    try:
        frontmatter, _ = load_markdown_page(path)
    except Exception as exc:
        return [{"path": repo_relative(path), "message": str(exc)}]

    missing = sorted(COMMON_REQUIRED - set(frontmatter))
    if missing:
        errors.append({"path": repo_relative(path), "message": f"missing required keys: {', '.join(missing)}"})
        return errors

    page_type = str(frontmatter.get("type"))
    if page_type not in CONTENT_TYPES:
        errors.append({"path": repo_relative(path), "message": f"unsupported page type: {page_type}"})
        return errors

    required = set(COMMON_REQUIRED)
    if page_type == "source":
        required |= SOURCE_REQUIRED
    elif page_type in DERIVED_TYPES:
        required |= DERIVED_REQUIRED
    elif page_type in LIGHTWEIGHT_TYPES:
        required |= LIGHTWEIGHT_REQUIRED

    missing = sorted(required - set(frontmatter))
    if missing:
        errors.append({"path": repo_relative(path), "message": f"missing required keys: {', '.join(missing)}"})

    for key in ("created", "updated"):
        try:
            parse_timestamp(str(frontmatter[key]))
        except (KeyError, ValueError) as exc:
            errors.append({"path": repo_relative(path), "message": f"{key}: {exc}"})

    if "compiled_at" in required:
        try:
            parse_timestamp(str(frontmatter["compiled_at"]))
        except (KeyError, ValueError) as exc:
            errors.append({"path": repo_relative(path), "message": f"compiled_at: {exc}"})

    status = str(frontmatter.get("status"))
    if status not in VALID_STATUSES:
        errors.append({"path": repo_relative(path), "message": f"invalid status: {status}"})

    confidence = frontmatter.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        errors.append({"path": repo_relative(path), "message": "confidence must be a number in [0, 1]"})

    related = frontmatter.get("related")
    if not isinstance(related, list):
        errors.append({"path": repo_relative(path), "message": "related must be a list"})

    if page_type == "source":
        source_path = frontmatter.get("source_path")
        if not isinstance(source_path, str) or not source_path.strip():
            errors.append({"path": repo_relative(path), "message": "source_path must be a non-empty string"})
        else:
            try:
                resolved = ensure_under_root(resolve_repo_path(source_path), RAW_DIR)
                if not resolved.is_file():
                    raise FileNotFoundError(source_path)
                expected_kind = resolved.relative_to(RAW_DIR).parts[0]
                if str(frontmatter.get("source_kind")) != expected_kind:
                    errors.append(
                        {
                            "path": repo_relative(path),
                            "message": f"source_kind should match raw subdirectory: expected {expected_kind}",
                        }
                    )
            except (FileNotFoundError, ValueError, IndexError):
                errors.append({"path": repo_relative(path), "message": f"source_path is invalid: {source_path}"})

        source_hash = frontmatter.get("source_hash")
        if not isinstance(source_hash, str) or not source_hash.strip():
            errors.append({"path": repo_relative(path), "message": "source_hash must be a non-empty string"})

    if page_type in DERIVED_TYPES:
        source_pages = frontmatter.get("source_pages")
        if not isinstance(source_pages, list) or not source_pages:
            errors.append({"path": repo_relative(path), "message": "source_pages must be a non-empty list"})
        else:
            for item in source_pages:
                ref_value = normalize_wiki_ref(str(item))
                if not ref_value:
                    errors.append({"path": repo_relative(path), "message": "source_pages contains an empty entry"})
                    continue
                target = wiki_ref_to_path(ref_value)
                if not target.exists():
                    errors.append({"path": repo_relative(path), "message": f"source page does not exist: {ref_value}"})

    if page_type in LIGHTWEIGHT_TYPES:
        source_pages = frontmatter.get("source_pages")
        if not isinstance(source_pages, list):
            errors.append({"path": repo_relative(path), "message": "source_pages must be a list"})
        else:
            for item in source_pages:
                ref_value = normalize_wiki_ref(str(item))
                if not ref_value:
                    errors.append({"path": repo_relative(path), "message": "source_pages contains an empty entry"})
                    continue
                target = wiki_ref_to_path(ref_value)
                if not target.exists():
                    errors.append({"path": repo_relative(path), "message": f"source page does not exist: {ref_value}"})

    return errors


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional markdown files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    try:
        files = expand_markdown_targets(args.paths, default_root=WIKI_DIR)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}")
        return 2

    errors: list[dict[str, Any]] = []
    for path in files:
        errors.extend(validate_page(path))

    if args.json:
        print(json.dumps(errors, indent=2))
    elif errors:
        for error in errors:
            print(f"{error['path']}: {error['message']}")
    else:
        print(f"ok: checked {len(files)} markdown files")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
