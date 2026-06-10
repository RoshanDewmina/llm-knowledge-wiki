# Retrieval Autoresearch Pack

## Editable Target

- Primary: `tools/query_index.py`
- User-facing command: `./bin/llm-wiki query`
- Query set: `queries.tsv`

## Frozen Evaluator

Use `evaluator.md` and `queries.tsv` to measure top-5 hit rate before changing
query weighting or wiki structure.

## Procedure

1. Add representative queries to `queries.tsv`.
2. Run each query with `./bin/llm-wiki query`.
3. Record whether the expected page appears in the top 5.
4. Only then change query weighting, page metadata, or page links.
5. Re-run the same query set and append the result.
