---
paths:
  - "tools/**/*.py"
  - "tests/**/*.py"
  - "Makefile"
---

# Tooling Rules

- Keep Python tooling standard-library-first and readable.
- Prefer explicit CLIs with `argparse`, docstrings, and type hints.
- Avoid hidden magic and avoid fabricating summaries in Python ingest logic.
- Preserve `make check` as the main health command.
- When changing tooling that affects the site, keep `wiki/.cache/site-manifest.json` generation in sync.
