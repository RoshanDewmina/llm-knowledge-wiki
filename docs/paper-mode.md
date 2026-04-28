# Paper Mode

Paper mode is the one-command paper mastery workflow.

## User Phrase Mapping

- "Paper mode: <URL>" -> `./bin/llm-wiki paper start <URL>`
- "Here are my notes from §2" -> `/paper-mode` updates the active study note
- "Quiz me" -> `./bin/llm-wiki quiz [slug] --n 5` plus `/quiz-me` grading
- "Make Anki cards" -> `./bin/llm-wiki anki <slug>` plus `/anki-generate` card writing
- "Make a tiny implementation task" -> `./bin/llm-wiki impl <slug> "<task>"`
- "Promote this" -> `./bin/llm-wiki promote <slug>` plus `/promote-study` citation checks

## Current Invariants

- `wiki/studies/` is private learning scaffolding.
- `wiki/outputs/` is the durable public/private deliverable layer.
- `wiki/studies/anki/` is the only folder Obsidian Spaced Repetition should scan.
- Concept-page creation is user-confirmed; missing concept links are reported by `concept candidates`.
- Evidence anchors are exact-source objects, not agent guesses.
