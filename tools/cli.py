"""Unified local CLI for onboarding and daily wiki operations."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence

from doctor import REQUIRED_COMMANDS, REQUIRED_PATHS, command_status, obsidian_status, path_status
from review_queue import collect_incomplete_sources, collect_low_confidence, collect_orphans, collect_stale
from wiki_utils import RAW_DIR, REPO_ROOT, WIKI_DIR, load_wiki_pages


CLI_NAME = "llm-wiki"


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level CLI parser."""

    parser = argparse.ArgumentParser(
        prog=CLI_NAME,
        description="Native-first onboarding and daily workflow CLI for the local wiki repo.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Install host tools for this repo")
    setup_parser.set_defaults(func=cmd_setup)

    onboard_parser = subparsers.add_parser("onboard", help="Run the recommended first-run onboarding flow")
    onboard_parser.add_argument("--skip-setup", action="store_true", help="Skip host-tool bootstrap even if tools are missing")
    onboard_parser.add_argument("--skip-site-build", action="store_true", help="Skip the frontend build during doctor")
    onboard_parser.add_argument("--open-obsidian", action="store_true", help="Open this repo as an Obsidian vault at the end")
    onboard_parser.set_defaults(func=cmd_onboard)

    doctor_parser = subparsers.add_parser("doctor", help="Verify host tools, repo structure, and optional build steps")
    doctor_parser.add_argument("--json", action="store_true", help="Emit JSON output")
    doctor_parser.add_argument("--skip-site-build", action="store_true", help="Skip `bun run build` in apps/site")
    doctor_parser.add_argument("--skip-vault-checks", action="store_true", help="Skip `python3 tools/check_wiki.py`")
    doctor_parser.set_defaults(func=cmd_doctor)

    health_parser = subparsers.add_parser("health", help="Run the standard vault health checks")
    health_parser.add_argument("--json", action="store_true", help="Emit JSON output")
    health_parser.set_defaults(func=cmd_health)

    status_parser = subparsers.add_parser("status", help="Show a compact readiness and content summary")
    status_parser.add_argument("--json", action="store_true", help="Emit JSON output")
    status_parser.set_defaults(func=cmd_status)

    query_parser = subparsers.add_parser("query", help="Search the compiled wiki")
    query_parser.add_argument("query", help="Free-text query")
    query_parser.add_argument("--limit", type=int, help="Maximum number of hits to return")
    query_parser.add_argument("--mode", choices=("ranked", "simple"), help="Search ranking mode")
    query_parser.add_argument("--type", dest="page_type", help="Optional page type filter")
    query_parser.add_argument("--status", help="Optional page status filter")
    query_parser.add_argument("--section", help="Optional top-level wiki section filter")
    query_parser.add_argument("--min-confidence", type=float, help="Optional minimum confidence filter")
    query_parser.add_argument("--path-prefix", help="Optional repository-relative path prefix filter")
    query_parser.add_argument("--include-special", action="store_true", help="Include special pages such as wiki/index.md")
    query_parser.add_argument("--json", action="store_true", help="Emit JSON output")
    query_parser.set_defaults(func=cmd_query)

    ingest_parser = subparsers.add_parser("ingest", help="Register a raw source and scaffold its source page")
    ingest_parser.add_argument("raw_path", help="Path to an existing raw source under raw/")
    ingest_parser.add_argument("--title", help="Optional page title override")
    ingest_parser.add_argument("--slug", help="Optional source-page slug override")
    ingest_parser.add_argument("--dry-run", action="store_true", help="Show planned changes without writing")
    ingest_parser.set_defaults(func=cmd_ingest)

    daily_parser = subparsers.add_parser("daily", help="Scaffold today's journal note")
    daily_parser.add_argument("--stdout", action="store_true", help="Print the note instead of writing it")
    daily_parser.set_defaults(func=cmd_daily)

    question_parser = subparsers.add_parser("question", help="Scaffold a durable question note")
    question_parser.add_argument("question", help="Question title to scaffold")
    question_parser.add_argument("--slug", help="Optional slug override")
    question_parser.add_argument("--stdout", action="store_true", help="Print the note instead of writing it")
    question_parser.set_defaults(func=cmd_question)

    review_daily_parser = subparsers.add_parser("review-daily", help="Regenerate the daily review page")
    review_daily_parser.add_argument("--stdout", action="store_true", help="Print the note instead of writing it")
    review_daily_parser.set_defaults(func=cmd_review_daily)

    manifest_parser = subparsers.add_parser("manifest", help="Regenerate the frontend site manifest")
    manifest_parser.set_defaults(func=cmd_manifest)

    export_parser = subparsers.add_parser("export", help="Export a synthesis or output page to Marp markdown")
    export_parser.add_argument("input_path", help="Synthesis or output markdown file")
    export_parser.add_argument("--output", help="Optional output path")
    export_parser.add_argument("--title", help="Optional slide-deck title override")
    export_parser.set_defaults(func=cmd_export)

    completion_parser = subparsers.add_parser("completion", help="Print or install shell completion scripts")
    completion_parser.add_argument("shell", choices=("zsh", "bash", "fish"), help="Target shell")
    completion_parser.add_argument("--install", action="store_true", help="Install the completion script into the user's shell config directory")
    completion_parser.set_defaults(func=cmd_completion)

    return parser


def run_subprocess(args: Sequence[str], cwd: Path | None = None) -> int:
    """Run one subprocess and return its exit code."""

    process = subprocess.run([str(item) for item in args], cwd=cwd or REPO_ROOT, check=False)
    return process.returncode


def run_python_tool(script_name: str, extra_args: Iterable[str] = ()) -> int:
    """Run a repo Python tool by filename."""

    return run_subprocess([sys.executable, str(REPO_ROOT / "tools" / script_name), *extra_args], cwd=REPO_ROOT)


def requirements_snapshot() -> dict[str, Any]:
    """Collect the current command/app/path availability snapshot."""

    commands = {name: command_status(name) for name in REQUIRED_COMMANDS}
    paths = {path: path_status(path) for path in REQUIRED_PATHS}
    obsidian = obsidian_status()
    return {
        "commands": commands,
        "paths": paths,
        "obsidian": obsidian,
        "ready": all(item["ok"] for item in commands.values()) and all(item["ok"] for item in paths.values()) and obsidian["ok"],
    }


def raw_document_count() -> int:
    """Count real raw documents under raw/."""

    return sum(1 for path in RAW_DIR.rglob("*") if path.is_file() and path.name != ".gitkeep")


def wiki_summary() -> dict[str, Any]:
    """Build a compact wiki content summary."""

    pages = load_wiki_pages(include_special=False)
    page_types = Counter(str(page.frontmatter.get("type", "unknown")) for page in pages)
    sections = Counter(page.ref.split("/", 1)[0] if "/" in page.ref else "root" for page in pages)
    return {
        "page_count": len(pages),
        "page_types": dict(sorted(page_types.items())),
        "sections": dict(sorted(sections.items())),
        "raw_documents": raw_document_count(),
    }


def status_payload() -> dict[str, Any]:
    """Build a high-level repo status payload."""

    snapshot = requirements_snapshot()
    summary = wiki_summary()
    issues = {
        "stale_pages": len(collect_stale()),
        "orphan_pages": len(collect_orphans()),
        "low_confidence_pages": len(collect_low_confidence()),
        "incomplete_sources": len(collect_incomplete_sources()),
    }
    generated_pages = {
        "daily_review": (WIKI_DIR / "reviews" / "daily-review.md").exists(),
        "review_queue": (WIKI_DIR / "reviews" / "review-queue.md").exists(),
        "coverage_dashboard": (WIKI_DIR / "reviews" / "coverage-dashboard.md").exists(),
        "site_manifest": (WIKI_DIR / ".cache" / "site-manifest.json").exists(),
    }
    return {
        "platform": platform.platform(),
        "requirements": snapshot,
        "wiki": summary,
        "issues": issues,
        "generated": generated_pages,
    }


def maybe_open_obsidian() -> int:
    """Open the repo as an Obsidian vault on macOS."""

    if platform.system() != "Darwin":
        print("warning: `--open-obsidian` is only implemented for macOS", file=sys.stderr)
        return 1
    return run_subprocess(["open", "-a", "Obsidian", str(REPO_ROOT)], cwd=REPO_ROOT)


def cmd_setup(_: argparse.Namespace) -> int:
    """Install host tools using the native bootstrap flow."""

    if platform.system() == "Darwin":
        return run_subprocess([str(REPO_ROOT / "scripts" / "bootstrap-macos.sh")], cwd=REPO_ROOT)
    print("Native bootstrap is only scripted for macOS right now.", file=sys.stderr)
    print("See docs/getting-started.md for manual setup on other platforms.", file=sys.stderr)
    return 1


def cmd_onboard(args: argparse.Namespace) -> int:
    """Run the recommended OpenClaw-style onboarding sequence."""

    snapshot = requirements_snapshot()
    ran_setup = False
    if not snapshot["ready"] and not args.skip_setup:
        if platform.system() != "Darwin":
            print("Missing required tools and no native bootstrap script exists for this platform.", file=sys.stderr)
            print("Use docs/getting-started.md for manual setup, then rerun `./bin/llm-wiki doctor`.", file=sys.stderr)
            return 1
        exit_code = cmd_setup(args)
        if exit_code != 0:
            return exit_code
        ran_setup = True
    elif not snapshot["ready"]:
        print("warning: setup skipped even though required tools are missing", file=sys.stderr)

    doctor_args = ["doctor"]
    if args.skip_site_build:
        doctor_args.append("--skip-site-build")
    doctor_exit = cmd_doctor(build_parser().parse_args(doctor_args))
    if doctor_exit != 0:
        return doctor_exit

    if args.open_obsidian:
        open_exit = maybe_open_obsidian()
        if open_exit != 0:
            return open_exit

    print("")
    print("Onboarding complete.")
    if ran_setup:
        print("- Host tools were installed or verified through the native bootstrap flow.")
    else:
        print("- Required host tools were already available, so setup was skipped.")
    print("- The repo passed doctor and is ready to use.")
    print("- Next: `./bin/llm-wiki health`, `./bin/llm-wiki query \"transformer\"`, or `make site-dev`.")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Wrap tools/doctor.py."""

    extra_args: list[str] = []
    if args.json:
        extra_args.append("--json")
    if args.skip_site_build:
        extra_args.append("--skip-site-build")
    if args.skip_vault_checks:
        extra_args.append("--skip-vault-checks")
    return run_python_tool("doctor.py", extra_args)


def cmd_health(args: argparse.Namespace) -> int:
    """Wrap tools/check_wiki.py."""

    extra_args = ["--json"] if args.json else []
    return run_python_tool("check_wiki.py", extra_args)


def cmd_status(args: argparse.Namespace) -> int:
    """Show a compact status summary."""

    payload = status_payload()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Platform: {payload['platform']}")
        print(f"Requirements ready: {'yes' if payload['requirements']['ready'] else 'no'}")
        print(
            "Wiki: {page_count} pages across {raw_documents} raw documents".format(
                page_count=payload["wiki"]["page_count"],
                raw_documents=payload["wiki"]["raw_documents"],
            )
        )
        type_summary = ", ".join(f"{name}={count}" for name, count in payload["wiki"]["page_types"].items())
        section_summary = ", ".join(f"{name}={count}" for name, count in payload["wiki"]["sections"].items())
        print(f"Page types: {type_summary}")
        print(f"Sections: {section_summary}")
        print(
            "Issues: stale={stale_pages}, orphan={orphan_pages}, low-confidence={low_confidence_pages}, incomplete-sources={incomplete_sources}".format(
                **payload["issues"]
            )
        )
        generated = payload["generated"]
        print(
            "Generated pages: daily-review={daily_review}, review-queue={review_queue}, coverage-dashboard={coverage_dashboard}, site-manifest={site_manifest}".format(
                **{key: "yes" if value else "no" for key, value in generated.items()}
            )
        )
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    """Wrap tools/query_index.py."""

    extra_args: list[str] = [args.query]
    for flag, value in (
        ("--limit", args.limit),
        ("--mode", args.mode),
        ("--type", args.page_type),
        ("--status", args.status),
        ("--section", args.section),
        ("--min-confidence", args.min_confidence),
        ("--path-prefix", args.path_prefix),
    ):
        if value is not None:
            extra_args.extend([flag, str(value)])
    if args.include_special:
        extra_args.append("--include-special")
    if args.json:
        extra_args.append("--json")
    return run_python_tool("query_index.py", extra_args)


def cmd_ingest(args: argparse.Namespace) -> int:
    """Wrap tools/ingest.py."""

    extra_args: list[str] = [args.raw_path]
    if args.title:
        extra_args.extend(["--title", args.title])
    if args.slug:
        extra_args.extend(["--slug", args.slug])
    if args.dry_run:
        extra_args.append("--dry-run")
    return run_python_tool("ingest.py", extra_args)


def cmd_daily(args: argparse.Namespace) -> int:
    """Wrap tools/scaffold_daily.py."""

    extra_args = ["--stdout"] if args.stdout else []
    return run_python_tool("scaffold_daily.py", extra_args)


def cmd_question(args: argparse.Namespace) -> int:
    """Wrap tools/scaffold_question.py."""

    extra_args: list[str] = [args.question]
    if args.slug:
        extra_args.extend(["--slug", args.slug])
    if args.stdout:
        extra_args.append("--stdout")
    return run_python_tool("scaffold_question.py", extra_args)


def cmd_review_daily(args: argparse.Namespace) -> int:
    """Wrap tools/daily_review.py."""

    extra_args = ["--stdout"] if args.stdout else []
    return run_python_tool("daily_review.py", extra_args)


def cmd_manifest(_: argparse.Namespace) -> int:
    """Wrap tools/build_site_manifest.py."""

    return run_python_tool("build_site_manifest.py")


def cmd_export(args: argparse.Namespace) -> int:
    """Wrap tools/export_marp.py."""

    extra_args: list[str] = [args.input_path]
    if args.output:
        extra_args.extend(["--output", args.output])
    if args.title:
        extra_args.extend(["--title", args.title])
    return run_python_tool("export_marp.py", extra_args)


def zsh_completion() -> str:
    """Return a zsh completion script."""

    return f"""#compdef {CLI_NAME}

local -a commands
commands=(
  'setup:install host tools for this repo'
  'onboard:run the recommended first-run onboarding flow'
  'doctor:verify host tools and repo readiness'
  'health:run the standard vault health checks'
  'status:show a compact readiness summary'
  'query:search the compiled wiki'
  'ingest:register a raw source and scaffold its source page'
  'daily:scaffold today\\'s journal note'
  'question:scaffold a durable question note'
  'review-daily:regenerate the daily review page'
  'manifest:regenerate the frontend site manifest'
  'export:export a synthesis or output page to Marp markdown'
  'completion:print or install shell completion scripts'
)

_arguments -C \\
  '1:command:->command' \\
  '*::arg:->args'

case $state in
  command)
    _describe 'command' commands
    ;;
  args)
    case $words[2] in
      onboard)
        _arguments '--skip-setup[skip bootstrap setup]' '--skip-site-build[skip frontend build during doctor]' '--open-obsidian[open this repo as an Obsidian vault]'
        ;;
      doctor)
        _arguments '--json[emit JSON output]' '--skip-site-build[skip frontend build]' '--skip-vault-checks[skip tools/check_wiki.py]'
        ;;
      health|status)
        _arguments '--json[emit JSON output]'
        ;;
      query)
        _arguments '--limit=[maximum number of hits]:limit:' '--mode=[search ranking mode]:mode:(ranked simple)' '--type=[page type filter]:page type:' '--status=[status filter]:status:' '--section=[wiki section filter]:section:' '--min-confidence=[minimum confidence]:confidence:' '--path-prefix=[repository-relative path prefix]:path prefix:' '--include-special[include wiki/index and other special pages]' '--json[emit JSON output]'
        ;;
      ingest)
        _arguments '--title=[page title override]:title:' '--slug=[source slug override]:slug:' '--dry-run[show planned changes without writing]'
        _files
        ;;
      daily|review-daily)
        _arguments '--stdout[print the generated note instead of writing it]'
        ;;
      question)
        _arguments '--slug=[question slug override]:slug:' '--stdout[print the generated note instead of writing it]'
        ;;
      export)
        _arguments '--output=[output markdown path]:output:' '--title=[slide deck title override]:title:'
        _files
        ;;
      completion)
        _arguments '--install[install the completion script]' '1:shell:(zsh bash fish)'
        ;;
    esac
    ;;
esac
"""


def bash_completion() -> str:
    """Return a bash completion script."""

    return f"""_{CLI_NAME.replace('-', '_')}_complete() {{
  local cur prev cmd
  COMPREPLY=()
  cur="${{COMP_WORDS[COMP_CWORD]}}"
  prev="${{COMP_WORDS[COMP_CWORD-1]}}"
  cmd="${{COMP_WORDS[1]}}"

  if [[ $COMP_CWORD -eq 1 ]]; then
    COMPREPLY=( $(compgen -W "setup onboard doctor health status query ingest daily question review-daily manifest export completion" -- "$cur") )
    return 0
  fi

  case "$cmd" in
    onboard)
      COMPREPLY=( $(compgen -W "--skip-setup --skip-site-build --open-obsidian" -- "$cur") )
      ;;
    doctor)
      COMPREPLY=( $(compgen -W "--json --skip-site-build --skip-vault-checks" -- "$cur") )
      ;;
    health|status)
      COMPREPLY=( $(compgen -W "--json" -- "$cur") )
      ;;
    query)
      COMPREPLY=( $(compgen -W "--limit --mode --type --status --section --min-confidence --path-prefix --include-special --json ranked simple" -- "$cur") )
      ;;
    ingest)
      COMPREPLY=( $(compgen -W "--title --slug --dry-run" -- "$cur") )
      ;;
    daily|review-daily)
      COMPREPLY=( $(compgen -W "--stdout" -- "$cur") )
      ;;
    question)
      COMPREPLY=( $(compgen -W "--slug --stdout" -- "$cur") )
      ;;
    export)
      COMPREPLY=( $(compgen -W "--output --title" -- "$cur") )
      ;;
    completion)
      COMPREPLY=( $(compgen -W "zsh bash fish --install" -- "$cur") )
      ;;
  esac
}}

complete -F _{CLI_NAME.replace('-', '_')}_complete {CLI_NAME}
"""


def fish_completion() -> str:
    """Return a fish completion script."""

    return f"""complete -c {CLI_NAME} -f
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a setup -d 'Install host tools for this repo'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a onboard -d 'Run the recommended first-run onboarding flow'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a doctor -d 'Verify host tools and repo readiness'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a health -d 'Run the standard vault health checks'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a status -d 'Show a compact readiness summary'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a query -d 'Search the compiled wiki'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a ingest -d 'Register a raw source and scaffold its source page'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a daily -d 'Scaffold today\\'s journal note'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a question -d 'Scaffold a durable question note'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a review-daily -d 'Regenerate the daily review page'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a manifest -d 'Regenerate the frontend site manifest'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a export -d 'Export a synthesis or output page to Marp markdown'
complete -c {CLI_NAME} -n '__fish_use_subcommand' -a completion -d 'Print or install shell completion scripts'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from onboard' -l skip-setup -d 'Skip bootstrap setup'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from onboard' -l skip-site-build -d 'Skip frontend build during doctor'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from onboard' -l open-obsidian -d 'Open the repo in Obsidian'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from doctor health status query' -l json -d 'Emit JSON output'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from doctor' -l skip-site-build -d 'Skip frontend build'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from doctor' -l skip-vault-checks -d 'Skip tools/check_wiki.py'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l limit -r -d 'Maximum number of hits'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l mode -r -a 'ranked simple' -d 'Search ranking mode'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l type -r -d 'Page type filter'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l status -r -d 'Status filter'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l section -r -d 'Section filter'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l min-confidence -r -d 'Minimum confidence'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l path-prefix -r -d 'Path prefix filter'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from query' -l include-special -d 'Include special pages'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from ingest' -l title -r -d 'Page title override'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from ingest question' -l slug -r -d 'Slug override'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from ingest' -l dry-run -d 'Show planned changes without writing'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from daily question review-daily' -l stdout -d 'Print output instead of writing'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from export' -l output -r -d 'Output markdown path'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from export' -l title -r -d 'Slide deck title override'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from completion' -a 'zsh bash fish'
complete -c {CLI_NAME} -n '__fish_seen_subcommand_from completion' -l install -d 'Install the completion script'
"""


def completion_script(shell: str) -> str:
    """Return the completion script for one shell."""

    if shell == "zsh":
        return zsh_completion()
    if shell == "bash":
        return bash_completion()
    return fish_completion()


def completion_install_path(shell: str) -> Path:
    """Return the user-local install path for one shell."""

    home = Path.home()
    if shell == "zsh":
        return home / ".zsh" / "completions" / f"_{CLI_NAME}"
    if shell == "bash":
        return home / ".local" / "share" / "bash-completion" / "completions" / CLI_NAME
    return home / ".config" / "fish" / "completions" / f"{CLI_NAME}.fish"


def cmd_completion(args: argparse.Namespace) -> int:
    """Print or install shell completion support."""

    script = completion_script(args.shell)
    if not args.install:
        print(script)
        return 0

    path = completion_install_path(args.shell)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(script, encoding="utf-8")
    print(f"installed {args.shell} completion: {path}")
    if args.shell == "zsh":
        print('If needed, add `fpath+=("$HOME/.zsh/completions")` to ~/.zshrc and rerun `autoload -Uz compinit && compinit`.')
    elif args.shell == "bash":
        print("Open a new shell or source your bash completion setup to activate it.")
    else:
        print("Open a new fish shell or run `source ~/.config/fish/completions/llm-wiki.fish`.")
    return 0


def main() -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
