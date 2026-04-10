"""Run lightweight lexical search over the compiled wiki."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from typing import Any, Dict, List

from wiki_utils import HEADING_RE, choose_snippet, load_wiki_pages, repo_relative, tokenize

FIELD_WEIGHTS = {
    "title": 4.0,
    "headings": 2.5,
    "frontmatter": 1.5,
    "body": 1.0,
    "path": 1.0,
}
PHRASE_WEIGHTS = {
    "title": 8.0,
    "headings": 4.0,
    "body": 2.0,
}


def score_text(terms: List[str], text: str) -> int:
    """Count term occurrences using simple substring scoring."""

    lowered = text.lower()
    return sum(lowered.count(term) for term in terms)


def page_penalty(page_type: str, path_text: str, frontmatter: Dict[str, Any]) -> float:
    """Apply small penalties for less useful result classes."""

    penalty = 0.0
    if page_type == "output" and frontmatter.get("marp") is True:
        penalty += 3.0
    if path_text.endswith(".slides.md"):
        penalty += 3.0
    return penalty


def bm25_term_weight(term_frequency: int, document_length: int, average_length: float) -> float:
    """Return a small BM25-style term-frequency weight."""

    if term_frequency <= 0:
        return 0.0
    k1 = 1.2
    b = 0.75
    norm = k1 * (1.0 - b + b * (float(document_length) / max(average_length, 1.0)))
    return (term_frequency * (k1 + 1.0)) / (term_frequency + norm)


def phrase_bonus(query_text: str, field_text: str, weight: float) -> float:
    """Apply a bonus when the full query appears in a field."""

    if not query_text or not field_text:
        return 0.0
    return weight if query_text in field_text.lower() else 0.0


def extract_frontmatter_text(frontmatter: Dict[str, Any]) -> str:
    """Flatten frontmatter into search text, excluding the main title/type fields."""

    return " ".join(str(value) for key, value in frontmatter.items() if key not in {"title", "type"})


def section_from_path(path_text: str) -> str:
    """Return the top-level section for a wiki path."""

    normalized = path_text.strip().lstrip("/").removeprefix("wiki/")
    if "/" not in normalized:
        return normalized.replace(".md", "")
    return normalized.split("/", 1)[0]


def build_ranked_corpus(
    include_special: bool,
    page_type_filter: str,
    path_prefix: str,
    status_filter: str,
    section_filter: str,
    min_confidence: float | None,
) -> List[Dict[str, Any]]:
    """Load candidate pages and prepare weighted search fields."""

    corpus: List[Dict[str, Any]] = []
    for page in load_wiki_pages(include_special=include_special):
        page_type = str(page.frontmatter.get("type", "special"))
        if page_type == "special" and not include_special:
            continue
        if page_type_filter and page_type != page_type_filter:
            continue

        path_text = repo_relative(page.path)
        if path_prefix and not path_text.startswith(path_prefix):
            continue
        section = section_from_path(path_text)
        if section_filter and section != section_filter:
            continue
        page_status = str(page.frontmatter.get("status", "")).strip()
        if status_filter and page_status != status_filter:
            continue
        confidence_value = page.frontmatter.get("confidence")
        if min_confidence is not None:
            if not isinstance(confidence_value, (int, float)) or float(confidence_value) < min_confidence:
                continue

        title = str(page.frontmatter.get("title", page.ref))
        headings = "\n".join(match.group(1) for match in HEADING_RE.finditer(page.body))
        frontmatter_text = extract_frontmatter_text(page.frontmatter)
        fields = {
            "title": title,
            "headings": headings,
            "frontmatter": frontmatter_text,
            "body": page.body,
            "path": path_text,
        }
        counters = {name: Counter(tokenize(text)) for name, text in fields.items()}
        document_length = sum(sum(counter.values()) for counter in counters.values()) or 1
        all_terms = set()
        for counter in counters.values():
            all_terms.update(counter.keys())
        corpus.append(
            {
                "page": page,
                "page_type": page_type,
                "section": section,
                "path_text": path_text,
                "title": title,
                "fields": fields,
                "counters": counters,
                "document_length": document_length,
                "all_terms": all_terms,
            }
        )
    return corpus


def score_page_simple(terms: List[str], title: str, headings: str, frontmatter_text: str, body: str, page_type: str, path_text: str, frontmatter: Dict[str, Any]) -> float:
    """Keep the older direct lexical count mode available."""

    score = 0.0
    score += score_text(terms, title) * 5
    score += score_text(terms, headings) * 3
    score += score_text(terms, frontmatter_text) * 2
    score += score_text(terms, body)
    score -= page_penalty(page_type, path_text, frontmatter)
    return score


def score_page_ranked(terms: List[str], query_text: str, document_frequency: Dict[str, int], corpus_size: int, average_length: float, record: Dict[str, Any]) -> float:
    """Score a page with a small weighted BM25-style ranker."""

    score = 0.0
    for term in terms:
        df = document_frequency.get(term, 0)
        if df <= 0:
            continue
        idf = math.log(1.0 + ((corpus_size - df + 0.5) / (df + 0.5)))
        for field_name, weight in FIELD_WEIGHTS.items():
            counter = record["counters"][field_name]
            tf = counter.get(term, 0)
            if tf <= 0:
                continue
            score += weight * idf * bm25_term_weight(tf, record["document_length"], average_length)

    score += phrase_bonus(query_text, record["fields"]["title"], PHRASE_WEIGHTS["title"])
    score += phrase_bonus(query_text, record["fields"]["headings"], PHRASE_WEIGHTS["headings"])
    score += phrase_bonus(query_text, record["fields"]["body"], PHRASE_WEIGHTS["body"])
    if query_text == record["title"].strip().lower():
        score += 8.0
    score -= page_penalty(record["page_type"], record["path_text"], record["page"].frontmatter)
    return score


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Free-text query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of hits to return")
    parser.add_argument("--mode", choices=("ranked", "simple"), default="ranked", help="Search ranking mode")
    parser.add_argument("--type", dest="page_type", help="Optional page type filter")
    parser.add_argument("--status", help="Optional page status filter")
    parser.add_argument("--section", help="Optional top-level wiki section filter")
    parser.add_argument("--min-confidence", type=float, help="Optional minimum confidence filter")
    parser.add_argument("--path-prefix", help="Optional repository-relative path prefix filter")
    parser.add_argument("--include-special", action="store_true", help="Include special pages such as wiki/index.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    """CLI entry point."""

    args = build_parser().parse_args()
    terms = tokenize(args.query)
    if not terms:
        print("error: query must contain at least one alphanumeric term")
        return 2

    path_prefix = (args.path_prefix or "").strip()
    query_text = args.query.strip().lower()
    results: List[Dict[str, Any]] = []
    corpus = build_ranked_corpus(
        args.include_special,
        args.page_type or "",
        path_prefix,
        (args.status or "").strip(),
        (args.section or "").strip(),
        args.min_confidence,
    )
    document_frequency: Dict[str, int] = {}
    for record in corpus:
        for term in record["all_terms"]:
            document_frequency[term] = document_frequency.get(term, 0) + 1
    average_length = (
        sum(record["document_length"] for record in corpus) / float(len(corpus))
        if corpus
        else 1.0
    )

    for record in corpus:
        page = record["page"]
        page_type = record["page_type"]
        path_text = record["path_text"]
        title = record["title"]
        if args.mode == "simple":
            score = score_page_simple(
                terms,
                title,
                record["fields"]["headings"],
                record["fields"]["frontmatter"],
                page.body,
                page_type,
                path_text,
                page.frontmatter,
            )
        else:
            score = score_page_ranked(
                terms,
                query_text,
                document_frequency,
                len(corpus),
                average_length,
                record,
            )
        if score <= 0:
            continue

        result: Dict[str, Any] = {
            "path": path_text,
            "title": title,
            "type": page_type,
            "section": record["section"],
            "score": round(score, 3) if args.mode == "ranked" else int(score),
            "snippet": choose_snippet(page.body, terms),
        }
        if page.frontmatter.get("status"):
            result["status"] = page.frontmatter.get("status")
        if isinstance(page.frontmatter.get("confidence"), (int, float)):
            result["confidence"] = round(float(page.frontmatter["confidence"]), 3)
        for key in ("related", "source_pages", "compiled_at", "source_path", "source_url"):
            value = page.frontmatter.get(key)
            if value:
                result[key] = value
        results.append(result)

    results.sort(key=lambda item: (-item["score"], item["path"]))
    results = results[: max(args.limit, 0)]

    if args.json:
        print(json.dumps(results, indent=2))
    elif results:
        for item in results:
            print("{0} [{1}] score={2}".format(item["path"], item["type"], item["score"]))
            if item["snippet"]:
                print("  {0}".format(item["snippet"]))
    else:
        print("no matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
