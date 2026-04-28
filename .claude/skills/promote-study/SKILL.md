---
name: promote-study
description: Promote mastered study notes into durable outputs
paths:
  - "wiki/outputs/**/*"
  - "wiki/studies/**/*"
  - "wiki/concepts/**/*"
metadata:
  short-description: Promote mastered study notes into durable outputs
---

# promote-study

Use when the user says "Promote this".

Steps:
1. Run `./bin/llm-wiki promote <slug> --target brief` unless another target is specified.
2. Seed the output from `## My Notes` plus linked concepts.
3. Ensure `## Citations` is non-empty and uses exact source anchors before setting any output to reviewed/published.
4. Only flip the study to `read_status: done` or `status: reviewed` after user confirmation.
5. Run `./bin/llm-wiki health`.
