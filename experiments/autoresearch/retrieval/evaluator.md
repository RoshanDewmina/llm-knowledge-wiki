# Retrieval Frozen Evaluator v1

Score a fixed query set from 0 to 5.

## Metric

`top5_hit_rate = hits / total_queries`

A hit means the expected wiki page appears in the first five results from:

```bash
./bin/llm-wiki query "<query>"
```

## Scoring

- 5: top5_hit_rate >= 0.90
- 4: top5_hit_rate >= 0.75
- 3: top5_hit_rate >= 0.60
- 2: top5_hit_rate >= 0.40
- 1: top5_hit_rate > 0.00
- 0: no expected pages found
