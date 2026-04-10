# Thinking Partner

Use this lane when Obsidian is your working space for daily thinking, and you want questions and insights to graduate into durable knowledge over time.

## Put In `raw/`

- only add sources here when a working note depends on real external material

## Maintain In `wiki/`

- `wiki/journal/` for daily notes
- `wiki/questions/` for durable open questions
- `wiki/reviews/daily-review.md` for daily triage

## Best Prompt

```text
Read AGENTS.md or CLAUDE.md and docs/agent-contract.md. Help me think through this topic inside the vault. Use or create a daily note or question page first, then promote any stable insight into a synthesis, project page, or output if warranted, and run make check.
```

## Checks

```bash
make daily
make question QUESTION="your question"
make review-daily
make check
```

## Done Looks Like

- the exploratory note lives in `wiki/journal/` or `wiki/questions/`
- stable ideas were promoted instead of left only in chat
- the daily review page points to the next useful action
