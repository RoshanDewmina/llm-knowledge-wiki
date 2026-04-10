# Studying For A Test

Use this workflow when you want to turn class material into a clean study wiki you can keep querying.

## 1. Get The Repo On The New Machine

Best option: use GitHub.

If this repo is already on GitHub:

```bash
git clone <your-repo-url> llm-knowledge-wiki
cd llm-knowledge-wiki
```

If you published it as a GitHub template, a new user can also create their own copy first, then clone that.

Zip file option:

- yes, you can share a `.zip` file for now
- this is fine if someone just needs the files quickly
- but GitHub clone is better because updates are easier later

If you use a zip:

1. download or copy the zip
2. unzip it
3. either double-click `START-HERE.command`
4. or open Terminal and `cd` into the unzipped `llm-knowledge-wiki` folder

Example:

```bash
cd ~/Downloads/llm-knowledge-wiki
```

## 2. Set Up The Repo

From the repo root:

```bash
./bin/llm-wiki onboard
open -a Obsidian .
make site-dev
```

Then open [http://localhost:3000/](http://localhost:3000/).

## 3. Add Your Study Material

Put your material into `raw/`.

Use:

- `raw/articles/YYYY/` for class notes, lecture transcripts, slide text, handouts, study sheets
- `raw/papers/` for readings, papers, textbook excerpts

Good things to add first:

- syllabus
- lecture notes
- lecture transcripts
- slide text
- assigned readings
- practice questions
- old quizzes or review sheets

Example filenames:

```text
raw/articles/2026/2026-04-10-bio101-lecture-03-notes.md
raw/articles/2026/2026-04-10-bio101-lecture-03-transcript.md
raw/articles/2026/2026-04-11-bio101-review-sheet.md
raw/papers/bio101-chapter-04-excerpt.md
```

## 4. Ingest Each File

Run this once per file:

```bash
./bin/llm-wiki ingest raw/articles/2026/2026-04-10-bio101-lecture-03-notes.md
./bin/llm-wiki ingest raw/articles/2026/2026-04-10-bio101-lecture-03-transcript.md
./bin/llm-wiki ingest raw/papers/bio101-chapter-04-excerpt.md
```

This creates or refreshes matching pages in `wiki/sources/`.

## 5. Build The Study Wiki

Open these first:

- `wiki/inbox.md`
- `wiki/reviews/daily-review.md`
- the new pages in `wiki/sources/`

Then ask Claude Code or Codex to turn the raw material into durable notes.

Use a prompt like:

```text
Read CLAUDE.md or AGENTS.md and docs/agent-contract.md. I am studying for a test. Use the newly ingested source pages, add exact evidence anchors where needed, update existing concept pages instead of creating duplicates, and create or refresh a synthesis in wiki/syntheses/research/ for this exam topic. Run ./bin/llm-wiki health when done.
```

## 6. Ask Study Questions

Search the current wiki first:

```bash
./bin/llm-wiki query "cell respiration"
./bin/llm-wiki query "causes of World War 1"
./bin/llm-wiki query "residual stream"
```

Then ask your agent:

```text
Answer this from the compiled wiki only. If the answer is useful for exam prep, save it as a brief in wiki/outputs/briefs/ with exact citations and run ./bin/llm-wiki health.
```

## 7. Save A Study Guide

Ask for one durable output per exam or topic.

Examples:

- `wiki/outputs/briefs/exam-1-study-guide.md`
- `wiki/outputs/tables/exam-1-comparison-table.md`
- `wiki/outputs/timelines/exam-1-timeline.md`

Useful prompt:

```text
Create a beginner-friendly study guide for this test in wiki/outputs/briefs/exam-1-study-guide.md. Use only the compiled wiki, keep it concise, include exact citations, and end with a short list of what I still need to review. Run ./bin/llm-wiki health when done.
```

## 8. Create Question Notes For Weak Areas

When something is still confusing:

```bash
./bin/llm-wiki question "What am I still weak on for exam 1?"
./bin/llm-wiki review-daily
```

Use `wiki/questions/` for open questions and `wiki/journal/` for working notes.

Promote stable answers into:

- `wiki/concepts/`
- `wiki/syntheses/`
- `wiki/outputs/briefs/`

## 9. Check Everything Before The Test

Run:

```bash
./bin/llm-wiki status
./bin/llm-wiki health
```

Then review:

- `wiki/reviews/daily-review.md`
- `wiki/reviews/review-queue.md`
- your saved study guide in `wiki/outputs/briefs/`

## Fastest Beginner Path

If you want the shortest version:

```bash
git clone <your-repo-url> llm-knowledge-wiki
cd llm-knowledge-wiki
./bin/llm-wiki onboard
./bin/llm-wiki ingest raw/articles/2026/your-class-notes.md
./bin/llm-wiki query "your exam topic"
./bin/llm-wiki question "What am I still weak on?"
./bin/llm-wiki health
```

Then ask Claude Code or Codex to:

1. update the source pages
2. create one synthesis
3. create one study guide brief
