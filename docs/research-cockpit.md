# Research Cockpit

Research Cockpit is the native macOS validation app for the local wiki. It is intentionally not a generic RAG chat app: the wedge is source-grounded course-pack study workflows with local file ownership.

## Product Position

- NotebookLM-style source grounding, but the user owns the Markdown vault.
- Obsidian-style file transparency, but with a guided nontechnical workflow.
- Hermes-powered automation stays hidden until advanced mode is enabled.
- BYOK ships first; managed subscriptions can layer on later through provider status and usage accounting.
- Direct-download macOS distribution comes before Mac App Store distribution because V1 needs local filesystem, CLI, provider, and launchd control.

## Vault Contract

- Originals are copied into `raw/courses/<course-slug>/`.
- App metadata is stored in `.research-cockpit/courses/<course-slug>.json`.
- Course-facing notes live in `wiki/studies/courses/<course-slug>/`.
- Generated outputs are files in the vault when possible.
- The app calls `./bin/llm-wiki` and Hermes commands; Markdown remains canonical.

## Normal User Surface

- Research: select a vault, import a course pack, and ingest each source.
- Study: scaffold a study guide, generate quizzes, generate flashcards, and search the compiled wiki.
- Schedule: regenerate review files and inspect scheduled work.
- Health: run status, doctor, health, Obsidian, and Hermes checks with plain-language repair guidance.

Advanced mode reveals Hermes status, gateway, cron jobs, skills, launchd status, and raw command logs.

## Build And Verify

```bash
make cockpit-test
make cockpit-run
make cockpit-package
```

The app package itself lives under `apps/research-cockpit`. Its run script stages `dist/ResearchCockpit.app`, launches it as a foreground bundle, and supports `--verify`, `--logs`, and `--telemetry`.
