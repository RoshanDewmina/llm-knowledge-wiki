# Academic Research

Use this lane when you want to collect papers and articles, compile them into reviewed source pages, and answer research questions from the compiled wiki instead of rereading PDFs every session.

## Put In `raw/`

- `raw/papers/` for paper excerpts, notes, or converted markdown
- `raw/articles/` for relevant blog posts, interviews, or explainers

## Maintain In `wiki/`

- `wiki/sources/` for reviewed paper or article source pages
- `wiki/concepts/` for reusable ideas
- `wiki/syntheses/research/` for literature reviews and research maps

## Best Prompt

```text
Read AGENTS.md or CLAUDE.md and docs/agent-contract.md. Ingest this paper or article, add exact evidence anchors on the source page, extend the relevant existing concept pages, update the research synthesis in wiki/syntheses/research/, and run ./bin/llm-wiki health.
```

## Checks

```bash
./bin/llm-wiki ingest raw/papers/your-paper.md
./bin/llm-wiki query "your topic"
./bin/llm-wiki health
```

## Done Looks Like

- the raw paper lives in `raw/`
- the reviewed source page has `## Evidence Extracts`
- the relevant concept or research synthesis page was updated
- a future question can be answered from `wiki/` without rereading the raw source
