"""Run the standard local health checks for the vault."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

TOOLS_DIR = Path(__file__).resolve().parent


def run_check(args: List[str]) -> Dict[str, Any]:
    """Run one check script and capture its output."""

    process = subprocess.run(
        [sys.executable] + args,
        cwd=TOOLS_DIR.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": " ".join(args),
        "exit_code": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    generators = {
        "coverage_dashboard": ["tools/coverage_dashboard.py"],
        "review_queue": ["tools/review_queue.py"],
        "daily_review": ["tools/daily_review.py"],
        "build_site_manifest": ["tools/build_site_manifest.py"],
    }
    checks = {
        "lint_frontmatter": ["tools/lint_frontmatter.py"],
        "lint_links": [
            "tools/lint_links.py",
            "README.md",
            "AGENTS.md",
            "CLAUDE.md",
            "docs",
            "examples",
            "templates",
            "wiki",
        ],
        "orphan_pages": ["tools/orphan_pages.py"],
        "stale_pages": ["tools/stale_pages.py"],
        "duplicate_pages": ["tools/duplicate_pages.py"],
        "lint_citations": ["tools/lint_citations.py"],
    }

    results = {name: run_check(command) for name, command in generators.items()}
    results.update({name: run_check(command) for name, command in checks.items()})
    has_failures = any(result["exit_code"] != 0 for result in results.values())

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for name, result in results.items():
            status = "ok" if result["exit_code"] == 0 else "fail"
            print("[{0}] {1}".format(status, name))
            if result["stdout"]:
                print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"])
        if not has_failures:
            print("ok: all standard vault checks passed")
    return 1 if has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
