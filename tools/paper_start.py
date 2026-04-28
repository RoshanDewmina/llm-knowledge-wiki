"""Start paper mode from a URL or arXiv identifier."""

from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from scaffold_study import scaffold as scaffold_study
from wiki_utils import RAW_DIR, humanize_slug, now_utc, render_markdown_page, slugify, write_text_if_changed


def metadata(value: str, explicit_slug: str | None) -> dict[str, str | None]:
    text = value.strip()
    arxiv_match = re.search(r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?", text)
    if arxiv_match:
        arxiv_id = arxiv_match.group(1)
        title = f"Arxiv {arxiv_id}"
        slug = explicit_slug or f"arxiv-{arxiv_id.replace('.', '-') }"
        return {"title": title, "slug": slug, "source_url": f"https://arxiv.org/abs/{arxiv_id}", "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}", "arxiv_id": arxiv_id, "source_domain": "arxiv.org"}
    parsed = urlparse(text)
    host = parsed.netloc or "paper"
    stem = Path(parsed.path).stem or host
    title = humanize_slug(stem)
    slug = explicit_slug or slugify(stem if stem else host)
    return {"title": title, "slug": slug, "source_url": text, "pdf_url": None, "arxiv_id": None, "source_domain": host}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper")
    parser.add_argument("--slug")
    parser.add_argument("--no-open", action="store_true")
    parser.add_argument("--no-concepts", action="store_true", help="Deprecated no-op; concept pages are never auto-created")
    args = parser.parse_args()
    meta = metadata(args.paper, args.slug)
    slug = slugify(str(meta["slug"]))
    timestamp = now_utc()
    raw_path = RAW_DIR / "papers" / timestamp[:4] / f"{timestamp[:10]}-{slug}.md"
    raw_fm = {
        "title": str(meta["title"]),
        "source_url": str(meta["source_url"]),
        "source_domain": str(meta["source_domain"]),
        "author": "",
        "published": "",
        "captured_at": timestamp,
        "arxiv_id": meta["arxiv_id"],
        "pdf_url": meta["pdf_url"],
    }
    body = f"# {meta['title']}\n\nSource: see source_url. Full text intentionally not auto-fetched.\n"
    if not raw_path.exists():
        write_text_if_changed(raw_path, render_markdown_page(raw_fm, body))
        print(f"created: {raw_path.relative_to(RAW_DIR.parent)}")
    else:
        print(f"unchanged: {raw_path.relative_to(RAW_DIR.parent)}")
    ingest = subprocess.run([sys.executable, str(Path(__file__).parent / "ingest.py"), str(raw_path.relative_to(RAW_DIR.parent)), "--slug", slug], check=False)
    if ingest.returncode != 0:
        return ingest.returncode
    scaffold_study("paper", slug, str(meta["title"]), [f"sources/{slug}"], [f"sources/{slug}"], False)
    print(f"study: wiki/studies/papers/{slug}.md")
    print(f"next: ./bin/llm-wiki concept candidates {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
