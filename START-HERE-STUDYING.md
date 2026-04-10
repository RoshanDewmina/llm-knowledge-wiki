# Start Here: Studying For A Test

If this is a new Mac and you only have the zip file, do this first.

## Best Option

Double-click:

- `START-HERE.command`

That will:

1. install the tools this repo needs
2. run the onboarding checks
3. open the study guide

## Manual Option

Open Terminal, go into this folder, and run:

```bash
cd /path/to/llm-knowledge-wiki
./bin/llm-wiki onboard
open -a Obsidian .
make site-dev
```

Then read:

- [docs/use-cases/studying-for-a-test.md](docs/use-cases/studying-for-a-test.md)

## What To Add First

Put your material in `raw/`, for example:

- class notes
- lecture transcripts
- slide text
- study sheets
- readings
- practice questions

Then ingest them:

```bash
./bin/llm-wiki ingest raw/articles/2026/your-class-notes.md
./bin/llm-wiki health
```

Then ask Claude Code or Codex to build your study notes from the compiled wiki.
