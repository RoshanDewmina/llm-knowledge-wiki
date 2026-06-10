---
title: "A Mathematical Framework for Transformer Circuits"
source: "https://transformer-circuits.pub/2021/framework/index.html"
source_alt: "https://www.anthropic.com/research/a-mathematical-framework-for-transformer-circuits"
captured_at: "2026-04-28"
tags: ["ml/llm", "ml/interpretability", "ml/mechanistic-interpretability", "transformers"]
type: source
created: "2026-04-28T22:14:05Z"
updated: "2026-04-30T11:44:53Z"
status: archived
confidence: 0.75
related:
  - sources/transformer-circuits-framework
  - studies/papers/transformer-circuits-framework
source_path: raw/legacy-obsidian/papers/2026-04-28-a-mathematical-framework-for-transformer-circuits.md
source_kind: legacy-obsidian
compiled_at: "2026-04-30T11:44:53Z"
source_hash: ba18546a655166ab2930f8a754d0099d687de3ebd33eeaa9dd8cd8227c5eec98
authors: ["Nelson Elhage", "Neel Nanda", "Catherine Olsson", "Tom Henighan", "Anthropic"]
arxiv_id: null
pdf_url: null
read_status: reading
rating: null
---

# A Mathematical Framework for Transformer Circuits

## Why this paper matters

This is a foundation paper for transformer mechanistic interpretability. The main move is to rewrite transformer computations in a form that makes internal circuits easier to reason about: residual stream communication, virtual weights, independent additive attention heads, QK/OV factorization, path expansion, and composition between heads.

Do not treat this as a paper to skim. Treat it as a notation-and-framework paper. The goal is not to memorize the claims; the goal is to be able to reconstruct the framework from scratch and use it on small transformers.

## Core claim

Transformer internals become more interpretable when viewed as compositions of linear-ish communication pathways through the residual stream, rather than only as the standard efficient implementation with embeddings, heads, concatenation, and layer blocks.

## Scope for first pass

Read only these sections first:

1. Introduction / motivation
2. Summary of Results
3. Transformer Overview
4. Zero-Layer Transformers
5. One-Layer Attention-Only Transformers

Stop before two-layer attention-only transformers unless the above is solid.

## Concept map

```text
Transformer circuits
├── Residual stream as communication channel
│   ├── components read from residual stream
│   ├── components write back by addition
│   ├── information can persist unless deleted
│   └── different subspaces carry different information
├── Virtual weights
│   ├── implicit connections between components
│   └── products of output and input matrices
├── Attention heads as independent additive operations
│   ├── standard concatenate form
│   └── equivalent sum-over-heads form
├── Attention as information movement
│   ├── QK circuit: where to attend
│   ├── OV circuit: what information to move/write
│   └── attention pattern is nonlinear; OV is linear
├── Zero-layer transformers
│   └── bigram statistics
├── One-layer attention-only transformers
│   └── bigram + skip-trigram behavior
└── Two-layer attention-only transformers
    └── head composition and induction heads
```

## Mastery tracker

| Topic | Intuition | Equation | Visual | Trace | Comparison | Practice | Paper Link | Mastery |
|---|---|---|---|---|---|---|---|
| Residual stream as communication channel | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Virtual weights | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Independent additive heads | todo | todo | todo | todo | todo | todo | source | 0/5 |
| QK vs OV circuits | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Zero-layer transformer = bigram model | todo | todo | todo | todo | todo | todo | source | 0/5 |
| One-layer attention-only = skip-trigram model | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Path expansion | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Head composition | todo | todo | todo | todo | todo | todo | source | 0/5 |
| Induction heads | todo | todo | todo | todo | todo | todo | source | 0/5 |

Mastery means: define it, explain it intuitively, write the key equation, trace a tiny example, compare to the nearest confusable idea, identify a pitfall, and connect it back to the paper's motivation.

## Reading log

### 2026-04-28 — Start

Goal: build the framework slowly. Do not summarize the whole paper yet.

## Key claims to verify

- [ ] Attention heads can be treated as independent additive operations.
- [ ] The residual stream is best viewed as a communication channel, not just a contextual embedding.
- [ ] QK and OV are the meaningful coupled matrices for interpreting heads.
- [ ] Zero-layer transformers model bigram statistics.
- [ ] One-layer attention-only transformers can implement skip-trigram behavior.
- [ ] Two-layer attention-only transformers enable richer head composition, including induction heads.

## Equations / derivations to reconstruct

### 1. Independent additive heads

Standard implementation concatenates head results and applies a shared output matrix. The interpretability rewrite splits the output matrix into per-head blocks and shows this equals a sum of per-head outputs.

Need to reconstruct:

```text
W_O^H [r^{h_1}; r^{h_2}; ...] = Σ_i W_O^{h_i} r^{h_i}
```

Symbols to define later:

| Symbol | Meaning |
|---|---|
| `h_i` | attention head i |
| `r^{h_i}` | result vector produced by head i before output projection |
| `W_O^H` | combined output matrix for the whole attention layer |
| `W_O^{h_i}` | output matrix block corresponding to head i |

Checkpoint: why is this rewrite useful for interpretability even though the concatenate form is better for efficient implementation?

### 2. OV circuit

Need to reconstruct:

```text
W_OV = W_O W_V
```

Plain-English target: if a head attends from destination token i to source token j, the OV circuit says what information is read from token j's residual stream and how that information is written into token i's residual stream.

### 3. QK circuit

Need to reconstruct:

```text
W_QK = W_Q^T W_K
A = softmax(x^T W_Q^T W_K x)
```

Plain-English target: QK determines the attention pattern: which source positions each destination position attends to.

## Confusions to resolve

- [ ] Why is the residual stream not just "the embedding"?
- [ ] Why are keys/queries/values described as somewhat superficial in this framework?
- [ ] What exactly is low-rank about `W_OV` and `W_QK`?
- [ ] What does it mean for a head to "move information"?
- [ ] Why does freezing the attention pattern make a head linear?
- [ ] Why can a zero-layer transformer be interpreted as bigram statistics?
- [ ] How exactly does a skip-trigram differ from a bigram?

## Active recall questions

Do not answer these by looking unless stuck.

1. In one sentence, what problem is this paper trying to solve?
2. Why do the authors focus on attention-only toy transformers?
3. What is the residual stream, and why do the authors call it a communication channel?
4. What are virtual weights?
5. Show why concatenated multi-head attention output is equivalent to adding independent head outputs.
6. What does the OV circuit control?
7. What does the QK circuit control?
8. Why are QK and OV better interpretability objects than Q, K, V separately?
9. What does a zero-layer transformer learn?
10. What is a skip-trigram?

## Tiny examples to build

- [ ] Write a 2-token, 2-dimensional residual-stream toy example showing a head copying one feature from token 1 to token 2.
- [ ] Make a tiny bigram table and show how a zero-layer transformer can represent next-token logits.
- [ ] Make a toy skip-trigram example: `A ... B -> C`.
- [ ] Implement a NumPy function that computes attention both ways: standard Q/K/V form and combined QK/OV form; verify same output.

## Connections

### Prior prerequisites

- [[sources/attention-is-all-you-need-excerpt|Attention Is All You Need]]
- residual connections
- linear algebra: matrix multiplication, rank, SVD, change of basis
- softmax and attention
- autoregressive language modeling

### Later Anthropic papers this unlocks

- In-context Learning and Induction Heads
- Toy Models of Superposition
- Towards Monosemanticity
- Mapping the Mind of a Large Language Model

## My notes

Use this section for your own explanations, not copied paper text.

### Residual stream explanation from memory



### QK vs OV explanation from memory



### One thing I still do not understand



## Output artifact

By the end, produce one of these:

- a public writeup: `Transformer Circuits From Scratch`
- or a GitHub notebook: `qk-ov-circuits.ipynb`
- or a short essay in `ideas/`: `what-mechanistic-interpretability-means-by-circuits.md`

Minimum bar: one clean explanation of QK vs OV plus one tiny NumPy reproduction.
