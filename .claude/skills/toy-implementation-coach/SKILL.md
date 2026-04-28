---
name: toy-implementation-coach
description: Coach tiny paper implementation tasks
paths:
  - "wiki/studies/implementations/**/*"
  - "experiments/papers/**/*"
metadata:
  short-description: Coach tiny paper implementation tasks
---

# toy-implementation-coach

Use when the user asks for a tiny implementation task.

Steps:
1. Run `./bin/llm-wiki impl <study-slug> "<task>" --lang numpy` unless PyTorch is requested.
2. Fill the implementation study spec with a three-step plan and an equivalence-check checklist.
3. Put code under `experiments/papers/<study-slug>/<task-slug>/`.
4. The equivalence check is mandatory: shape checks, tolerance, and one failure case.
5. Do not turn experiments into polished library code prematurely.
