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
		'  make check                         Alias for make health' \
		'  make status                        Show a compact readiness and content summary' \
		'  make review                        Regenerate the main review pages through the repo CLI' \
		'  make review-daily                  Regenerate the daily review page through the repo CLI' \
		'  make manifest                      Regenerate the frontend site manifest through the repo CLI' \
		'  make query QUERY="transformer"     Search the compiled wiki through the repo CLI' \
		'  make query-json QUERY="..."        Search the compiled wiki as JSON through the repo CLI' \
		'  make ingest SOURCE=raw/...         Ingest one raw source file through the repo CLI' \
		'  make ingest-demo                   Ingest the seeded demo article' \
		'  make daily                         Scaffold today'\''s journal note through the repo CLI' \
		'  make question QUESTION="..."       Scaffold a durable question note through the repo CLI' \
		'  make research-demo                 Walk the seeded academic research workflow' \
		'  make project-demo                  Walk the seeded codebase-memory workflow' \
		'  make export SYNTHESIS=wiki/...     Export a synthesis/output to Marp markdown through the repo CLI' \
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
	$(CLI) health

review:
	$(CLI) review

review-daily:
	$(CLI) review-daily

manifest:
	$(CLI) manifest

query:
	$(CLI) query "$(QUERY)"

query-json:
	$(CLI) query "$(QUERY)" --json

ingest:
	$(CLI) ingest "$(SOURCE)"

ingest-demo:
	$(CLI) ingest raw/articles/2026/2026-04-07-example-com-attention-as-interface.md

daily:
	$(CLI) daily

question:
	$(CLI) question "$(QUESTION)"

research-demo:
	$(CLI) ingest raw/papers/attention-is-all-you-need-excerpt.md
	$(CLI) query "transformer" --section syntheses --path-prefix wiki/syntheses/research/ --type synthesis
	$(CLI) health

project-demo:
	$(CLI) ingest raw/repos/example-transformer-tooling-notes.md
	$(CLI) query "project memory" --section projects
	$(CLI) health

export:
	$(CLI) export "$(SYNTHESIS)"

export-demo:
	$(CLI) export wiki/syntheses/transformer-orientation.md

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
