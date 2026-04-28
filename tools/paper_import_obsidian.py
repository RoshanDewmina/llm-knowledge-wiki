"""Import a legacy Obsidian paper note into raw/ and scaffold a study page."""

from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from scaffold_study import scaffold as scaffold_study
from wiki_utils import RAW_DIR, WIKI_DIR, extract_first_heading, load_optional_markdown_page, repo_relative, slugify, write_text_if_changed


def convert_legacy_body(raw_body: str) -> str:
    body = raw_body
    replacements = {
        "## Why this paper matters": "## Why This Paper Matters",
        "## Core claim": "## Core Claim",
        "## Scope for first pass": "## Scope For First Pass",
        "## Concept map": "## Concept Map",
        "## Mastery tracker": "## Mastery Tracker",
        "## Reading log": "## Reading Log",
        "## Key claims to verify": "## Key Claims To Verify",
        "## Equations / derivations to reconstruct": "## Equations / Derivations To Reconstruct",
        "## Confusions to resolve": "## Confusions To Resolve",
        "## Active recall questions": "## Active Recall Questions",
        "## Tiny examples to build": "## Tiny Examples To Build",
        "## Output artifact": "## Output Artifact Target",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    lines = []
    in_mastery = False
    for line in body.splitlines():
        if line.startswith("| Topic | Intuition | Equation"):
            lines.append("| Topic | Concept Page | Intuition | Equation | Visual | Trace | Comparison | Practice | Mastery |")
            in_mastery = True
            continue
        if in_mastery and line.startswith("|---"):
            lines.append("|---|---|---|---|---|---|---|---|---|")
            continue
        if in_mastery and line.startswith("|") and "|" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 9:
                topic = cells[0]
                concept = "concepts/" + slugify(topic.replace("=", " ").replace("/", " "))
                # Preserve paper-link signal by replacing it with concept-centric column.
                cells = [topic, f"[[{concept}]]", *cells[1:7], cells[8]]
                lines.append("| " + " | ".join(cells) + " |")
                continue
        if in_mastery and not line.startswith("|"):
            in_mastery = False
        lines.append(line)
    body = "\n".join(lines)
    if "## Quiz Log" not in body:
        body = body.replace("## Citations" if "## Citations" in body else "## Output Artifact Target", "## Quiz Log\n\n## Citations\n\n## Output Artifact Target")
    return body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_path")
    parser.add_argument("--slug")
    parser.add_argument("--copy-raw", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    old_path = Path(args.old_path).expanduser().resolve()
    if not old_path.is_file():
        print(f"error: legacy note not found: {old_path}")
        return 2
    slug = slugify(args.slug or old_path.stem)
    raw_dest = RAW_DIR / "legacy-obsidian" / "papers" / old_path.name
    study_dest = WIKI_DIR / "studies" / "papers" / f"{slug}.md"
    planned = []
    raw_differs = args.copy_raw and raw_dest.exists() and raw_dest.read_text(encoding="utf-8") != old_path.read_text(encoding="utf-8")
    if args.copy_raw and not raw_dest.exists():
        planned.append(repo_relative(raw_dest))
    if not study_dest.exists():
        planned.append(repo_relative(study_dest))
    if args.dry_run:
        if raw_differs:
            print(f"would not modify immutable raw copy with differing content: {repo_relative(raw_dest)}")
        if planned:
            print("would modify:")
            for item in planned: print(f"- {item}")
        else:
            print("would not modify: legacy import is already up to date")
        return 0
    if args.copy_raw:
        raw_dest.parent.mkdir(parents=True, exist_ok=True)
        if not raw_dest.exists():
            shutil.copyfile(old_path, raw_dest)
            print(f"created: {repo_relative(raw_dest)}")
        else:
            print(f"unchanged: {repo_relative(raw_dest)}")
            if raw_differs:
                print(f"warning: immutable raw copy differs from source note; not overwriting: {repo_relative(raw_dest)}")
    if args.copy_raw:
        ingest = subprocess.run([sys.executable, str(Path(__file__).parent / "ingest.py"), repo_relative(raw_dest), "--slug", slug], check=False)
        if ingest.returncode != 0:
            return ingest.returncode
    if not study_dest.exists():
        fm, raw_body = load_optional_markdown_page(old_path)
        title = str(fm.get("title") or extract_first_heading(raw_body) or slug)
        timestamp = __import__("wiki_utils").now_utc()
        frontmatter = {
            "title": title,
            "type": "study",
            "created": timestamp,
            "updated": timestamp,
            "status": "draft",
            "confidence": 0.3,
            "related": [f"sources/{slug}"],
            "source_pages": [f"sources/{slug}"],
            "compiled_at": timestamp,
            "study_kind": "paper",
            "read_status": str(fm.get("read_status") or "reading"),
            "rating": fm.get("rating"),
            "mastery_avg": 0.0,
            "arxiv_id": fm.get("arxiv_id"),
            "pdf_url": fm.get("pdf_url"),
            "authors": fm.get("authors") if isinstance(fm.get("authors"), list) else [],
            "tags": ["study", "paper"],
        }
        content = __import__("wiki_utils").render_markdown_page(frontmatter, convert_legacy_body(raw_body))
        write_text_if_changed(study_dest, content)
        print(f"created: {repo_relative(study_dest)}")
    else:
        print(f"unchanged: {repo_relative(study_dest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
