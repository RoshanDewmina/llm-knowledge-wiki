"""Emit study-note quiz prompts."""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from typing import List

from wiki_utils import WIKI_DIR, load_markdown_page, repo_relative, slugify


def extract_section(body: str, heading: str) -> str:
    capture = False
    lines: list[str] = []
    target = heading.lower()
    for line in body.splitlines():
        if line.startswith("## "):
            if capture:
                break
            capture = line[3:].strip().lower() == target
            continue
        if capture:
            lines.append(line)
    return "\n".join(lines).strip()


def numbered_or_tasks(text: str) -> list[str]:
    prompts: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        m = re.match(r"(?:\d+\.|- \[[ xX]\]|-)\s+(.*)", stripped)
        if m and m.group(1).strip():
            prompts.append(m.group(1).strip())
    return prompts


def study_path(slug: str | None) -> Path:
    if slug:
        return WIKI_DIR / "studies" / "papers" / f"{slugify(slug)}.md"
    candidates = sorted((WIKI_DIR / "studies" / "papers").glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError("no study pages found under wiki/studies/papers")
    return candidates[0]


def build_questions(path: Path, kind: str, n: int) -> list[str]:
    _, body = load_markdown_page(path)
    recall = numbered_or_tasks(extract_section(body, "Active Recall Questions"))
    confusions = [f"Resolve this confusion: {q}" for q in numbered_or_tasks(extract_section(body, "Confusions To Resolve"))]
    derivations = [f"Reconstruct this derivation: {q}" for q in numbered_or_tasks(extract_section(body, "Equations / Derivations To Reconstruct"))]
    if kind == "recall": pool = recall
    elif kind == "confusion": pool = confusions
    elif kind == "derivation": pool = derivations
    else:
        pool = recall[:2] + confusions[:2] + derivations[:1] + recall[2:] + confusions[2:] + derivations[1:]
    return pool[:n]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", nargs="?")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--kind", choices=("recall", "confusion", "derivation", "mixed"), default="mixed")
    args = parser.parse_args()
    try:
        path = study_path(args.slug)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    questions = build_questions(path, args.kind, args.n)
    print(f"Study: {repo_relative(path)}")
    if not questions:
        print("No quiz prompts found. Add Active Recall Questions, Confusions To Resolve, or Derivations sections.")
        return 1
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
