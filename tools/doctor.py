"""Verify that the local wiki repository is ready to use."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from wiki_utils import REPO_ROOT


REQUIRED_COMMANDS = ("python3", "git", "gh", "rg", "bun", "claude", "codex")
REQUIRED_PATHS = (
    "raw",
    "wiki",
    "docs",
    "templates",
    "tools",
    "apps/site",
    "Brewfile",
    "scripts/bootstrap-macos.sh",
)


def command_status(name: str) -> Dict[str, Any]:
    """Return availability metadata for one command."""

    location = shutil.which(name)
    return {"ok": bool(location), "detail": location or "not found"}


def obsidian_status() -> Dict[str, Any]:
    """Return whether Obsidian appears to be installed."""

    cli_path = shutil.which("obsidian")
    if cli_path:
        return {"ok": True, "detail": cli_path}

    mac_app = Path("/Applications/Obsidian.app")
    if platform.system() == "Darwin" and mac_app.exists():
        return {"ok": True, "detail": str(mac_app)}

    return {"ok": False, "detail": "missing `obsidian` command and /Applications/Obsidian.app"}


def path_status(relative_path: str) -> Dict[str, Any]:
    """Return whether a required repo path exists."""

    path = REPO_ROOT / relative_path
    return {"ok": path.exists(), "detail": relative_path}


def run_subprocess(args: List[str], cwd: Path) -> Dict[str, Any]:
    """Run a subprocess and capture a compact result."""

    process = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "ok": process.returncode == 0,
        "exit_code": process.returncode,
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
        "command": " ".join(args),
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--skip-site-build", action="store_true", help="Skip `bun run build` in apps/site")
    parser.add_argument("--skip-vault-checks", action="store_true", help="Skip `python3 tools/check_wiki.py`")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    results: Dict[str, Any] = {
        "platform": platform.platform(),
        "commands": {name: command_status(name) for name in REQUIRED_COMMANDS},
        "obsidian": obsidian_status(),
        "paths": {path: path_status(path) for path in REQUIRED_PATHS},
    }

    if not args.skip_vault_checks:
        results["vault_checks"] = run_subprocess([sys.executable, "tools/check_wiki.py"], REPO_ROOT)
    if not args.skip_site_build:
        results["site_build"] = run_subprocess(["bun", "run", "build"], REPO_ROOT / "apps" / "site")

    failures: List[str] = []
    for command, status in results["commands"].items():
        if not status["ok"]:
            failures.append(f"missing command: {command}")
    if not results["obsidian"]["ok"]:
        failures.append("missing Obsidian")
    for path, status in results["paths"].items():
        if not status["ok"]:
            failures.append(f"missing path: {path}")

    for key in ("vault_checks", "site_build"):
        status = results.get(key)
        if status and not status["ok"]:
            failures.append(f"{key} failed")

    results["failures"] = failures

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Platform: {results['platform']}")
        for command, status in results["commands"].items():
            label = "ok" if status["ok"] else "fail"
            print(f"[{label}] command `{command}` -> {status['detail']}")
        label = "ok" if results["obsidian"]["ok"] else "fail"
        print(f"[{label}] Obsidian -> {results['obsidian']['detail']}")
        for path, status in results["paths"].items():
            label = "ok" if status["ok"] else "fail"
            print(f"[{label}] repo path `{path}`")
        for key in ("vault_checks", "site_build"):
            status = results.get(key)
            if not status:
                continue
            label = "ok" if status["ok"] else "fail"
            print(f"[{label}] {key} -> {status['command']}")
            if status["stdout"]:
                print(status["stdout"])
            if status["stderr"]:
                print(status["stderr"])
        if not failures:
            print("ok: environment and repository look ready")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
