PYTHON ?= python3
CLI ?= ./bin/llm-wiki
QUERY ?= transformer
SOURCE ?= raw/articles/2026/2026-04-07-example-com-attention-as-interface.md
SYNTHESIS ?= wiki/syntheses/transformer-orientation.md
QUESTION ?= What should this vault explain next?

.PHONY: help onboard setup doctor health status check review review-daily manifest query query-json ingest ingest-demo daily question research-demo project-demo export export-demo test site-dev site-build site-lint site-test

help:
	@printf '%s\n' \
		'Available targets:' \
		'  make onboard                       Run the OpenClaw-style first-run onboarding flow' \
		'  make setup                         Run the native macOS bootstrap script' \
		'  make doctor                        Verify host tools, repo structure, site build, and vault checks' \
		'  make health                        Run the standard vault health checks through the repo CLI' \
		'  make status                        Show a compact readiness and content summary' \
		'  make check                         Run the standard vault health checks' \
		'  make review                        Regenerate the review queue and coverage dashboard' \
		'  make review-daily                  Regenerate the daily review page' \
		'  make manifest                      Regenerate the frontend site manifest' \
		'  make query QUERY="transformer"     Search the compiled wiki' \
		'  make query-json QUERY="..."        Search the compiled wiki as JSON' \
		'  make ingest SOURCE=raw/...         Ingest one raw source file' \
		'  make ingest-demo                   Ingest the seeded demo article' \
		'  make daily                         Scaffold today'\''s journal note' \
		'  make question QUESTION="..."       Scaffold a durable question note' \
		'  make research-demo                 Walk the seeded academic research workflow' \
		'  make project-demo                  Walk the seeded codebase-memory workflow' \
		'  make export SYNTHESIS=wiki/...     Export a synthesis/output to Marp markdown' \
		'  make export-demo                   Export the seeded demo synthesis' \
		'  make test                          Run Python tests plus frontend lint/build/e2e' \
		'  make site-dev                      Run the Next.js frontend with Bun' \
		'  make site-build                    Build the Next.js frontend with Bun' \
		'  make site-lint                     Lint the Next.js frontend' \
		'  make site-test                     Run the Playwright browser smoke suite'

onboard:
	$(CLI) onboard

setup:
	$(CLI) setup

doctor:
	$(CLI) doctor

health:
	$(CLI) health

status:
	$(CLI) status

check:
	$(PYTHON) tools/check_wiki.py

review:
	$(PYTHON) tools/coverage_dashboard.py
	$(PYTHON) tools/review_queue.py
	$(PYTHON) tools/daily_review.py

review-daily:
	$(PYTHON) tools/daily_review.py

manifest:
	$(PYTHON) tools/build_site_manifest.py

query:
	$(PYTHON) tools/query_index.py "$(QUERY)"

query-json:
	$(PYTHON) tools/query_index.py "$(QUERY)" --json

ingest:
	$(PYTHON) tools/ingest.py "$(SOURCE)"

ingest-demo:
	$(PYTHON) tools/ingest.py raw/articles/2026/2026-04-07-example-com-attention-as-interface.md

daily:
	$(PYTHON) tools/scaffold_daily.py

question:
	$(PYTHON) tools/scaffold_question.py "$(QUESTION)"

research-demo:
	$(PYTHON) tools/ingest.py raw/papers/attention-is-all-you-need-excerpt.md
	$(PYTHON) tools/query_index.py "transformer" --section syntheses --path-prefix wiki/syntheses/research/ --type synthesis
	$(PYTHON) tools/check_wiki.py

project-demo:
	$(PYTHON) tools/ingest.py raw/repos/example-transformer-tooling-notes.md
	$(PYTHON) tools/query_index.py "project memory" --section projects
	$(PYTHON) tools/check_wiki.py

export:
	$(PYTHON) tools/export_marp.py "$(SYNTHESIS)"

export-demo:
	$(PYTHON) tools/export_marp.py wiki/syntheses/transformer-orientation.md

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
	cd apps/site && bun run lint
	cd apps/site && bun run build
	cd apps/site && bun run test:e2e

site-dev:
	$(PYTHON) tools/build_site_manifest.py
	cd apps/site && bun run dev

site-build:
	$(PYTHON) tools/build_site_manifest.py
	cd apps/site && bun run build

site-lint:
	cd apps/site && bun run lint

site-test:
	$(PYTHON) tools/build_site_manifest.py
	cd apps/site && bun run test:e2e
