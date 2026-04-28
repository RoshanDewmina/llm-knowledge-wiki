---
title: A Mathematical Framework for Transformer Circuits
type: study
created: 2026-04-28T22:14:21Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.8
related:
  - sources/transformer-circuits-framework
  - concepts/residual-stream
  - concepts/virtual-weights
  - concepts/qk-circuit
  - concepts/ov-circuit
  - concepts/attention-head-decomposition
  - concepts/zero-layer-transformer
  - concepts/one-layer-attention-only-skip-trigram-model
  - concepts/path-expansion
  - concepts/head-composition
  - concepts/induction-head
source_pages:
  - sources/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
study_kind: paper
read_status: reading
rating: null
mastery_avg: 2.6
arxiv_id: null
pdf_url: null
authors:
  - Nelson Elhage
  - Neel Nanda
  - Catherine Olsson
  - Tom Henighan
  - Anthropic
tags:
  - study
  - paper
---

# A Mathematical Framework for Transformer Circuits

## Why This Paper Matters

This is a foundation paper for transformer mechanistic interpretability. The main move is to rewrite transformer computations in a form that makes internal circuits easier to reason about: residual-stream communication, virtual weights, independent additive attention heads, QK/OV factorization, path expansion, and composition between heads.

Treat it as a notation-and-framework paper. The goal is to reconstruct the framework from scratch and use it on small transformers, not just remember the prose.

## Core Claim

Transformer internals become more interpretable when viewed as compositions of linear-ish communication pathways through the residual stream, rather than only as the standard efficient implementation with embeddings, heads, concatenation, and layer blocks. The current pilot pass verifies the one-layer/QK/OV/residual-stream core and leaves deeper two-layer induction-head analysis as the next reading pass.

## Scope For First Pass

Completed first-pass scope:

1. Introduction / motivation
2. Summary of Results
3. Transformer Overview
4. Residual stream / virtual weights
5. Independent additive attention heads
6. Zero-layer transformers
7. One-layer attention-only transformers
8. QK/OV split and skip-trigram interpretation

Next pass starts with two-layer attention-only transformers and induction heads.

## Concept Map

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

## Mastery Tracker

| Topic | Concept Page | Intuition | Equation | Visual | Trace | Comparison | Practice | Mastery |
|---|---|---|---|---|---|---|---|---|
| Residual stream as communication channel | [[concepts/residual-stream]] | done | partial | partial | done | partial | todo | 3/5 |
| Virtual weights | [[concepts/virtual-weights]] | done | partial | todo | partial | partial | todo | 2/5 |
| Independent additive heads | [[concepts/attention-head-decomposition]] | done | done | partial | done | partial | done | 3/5 |
| QK vs OV circuits | [[concepts/qk-circuit]] / [[concepts/ov-circuit]] | done | done | partial | done | done | done | 4/5 |
| Zero-layer transformer = bigram model | [[concepts/zero-layer-transformer]] | done | partial | todo | partial | done | todo | 2/5 |
| One-layer attention-only = skip-trigram model | [[concepts/one-layer-attention-only-skip-trigram-model]] | done | partial | todo | partial | done | todo | 2/5 |
| Path expansion | [[concepts/path-expansion]] | done | partial | todo | partial | partial | todo | 2/5 |
| Head composition | [[concepts/head-composition]] | partial | todo | todo | todo | partial | todo | 1/5 |
| Induction heads | [[concepts/induction-head]] | partial | todo | todo | todo | partial | todo | 1/5 |

Mastery means: define it, explain it intuitively, write the key equation, trace a tiny example, compare to the nearest confusable idea, identify a pitfall, and connect it back to the paper's motivation.

## Reading Log

### 2026-04-28 — First pass completed

Completed the first-pass source-backed scaffold: source anchors, concept pages, Anki cards, and a NumPy QK/OV equivalence implementation. The paper is still marked `reading` because the two-layer/induction-head parts deserve a separate deep pass.

## Key Claims Verified

- [x] Attention heads can be treated as independent additive operations.
- [x] The residual stream is best viewed as a communication channel, not just a contextual embedding.
- [x] QK and OV are the meaningful coupled matrices for interpreting heads.
- [x] Zero-layer transformers model bigram statistics.
- [x] One-layer attention-only transformers can implement skip-trigram behavior.
- [x] Two-layer attention-only transformers enable richer head composition, including induction heads.

## Equations / Derivations To Reconstruct

### 1. Independent additive heads

Standard implementation concatenates head results and applies a shared output matrix. The interpretability rewrite splits the output matrix into per-head blocks and shows this equals a sum of per-head outputs:

```text
W_O^H [r^{h_1}; r^{h_2}; ...] = Σ_i W_O^{h_i} r^{h_i}
```

Why it matters: each head can be treated as an additive operation that writes its result into the residual stream.

### 2. OV circuit

```text
W_OV = W_V W_O        # row-vector NumPy convention
```

Plain-English target: if a head attends from destination token i to source token j, the OV circuit says what information is read from token j's residual stream and how that information is written into token i's residual stream.

### 3. QK circuit

```text
W_QK = W_Q W_K^T      # row-vector NumPy convention
A = softmax(x W_QK x^T / sqrt(d_head))
```

Plain-English target: QK determines the attention pattern: which source positions each destination position attends to.

## Confusions Resolved / Still Open

- [x] Why is the residual stream not just "the embedding"? Because it is the sum of the original embedding and all prior component outputs, and can carry subspaces not directly about the present token.
- [x] Why are keys/queries/values described as somewhat superficial in this framework? Because QK and OV products are the effective low-rank maps; individual Q/K/V bases can be less directly interpretable.
- [x] What exactly is low-rank about `W_OV` and `W_QK`? They factor through the head dimension, so their rank is capped by `d_head` rather than `d_model`.
- [x] What does it mean for a head to "move information"? QK chooses source/destination routing and OV transforms the selected source residual information into a write at the destination.
- [ ] Why does freezing the attention pattern make a head linear? Need a separate derivation card.
- [x] Why can a zero-layer transformer be interpreted as bigram statistics? With no cross-position layers, output logits come from embedding-to-unembedding interactions for the current token.
- [x] How exactly does a skip-trigram differ from a bigram? A bigram predicts from adjacent/current token statistics; a skip-trigram captures `A ... B -> C` patterns mediated by attention to an earlier source token.

## Active Recall Questions

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
11. How does QK/OV explain copying behavior in a one-layer attention-only model?
12. What must be added in a two-layer model to get induction-head-style behavior?

## Tiny Examples Built / To Build

- [x] Implement a NumPy function that computes attention both ways: standard Q/K/V form and combined QK/OV form; verify same output.
- [ ] Write a 2-token, 2-dimensional residual-stream toy example showing a head copying one feature from token 1 to token 2.
- [ ] Make a tiny bigram table and show how a zero-layer transformer can represent next-token logits.
- [ ] Make a toy skip-trigram example: `A ... B -> C`.

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

### Residual stream explanation from memory

The residual stream is the shared workspace. Components do not hand messages to each other directly; they read from the current workspace vector and add new vectors back into it. This is why multiplying output weights from one component by input weights from another can reveal an implicit communication channel.

### QK vs OV explanation from memory

QK is routing: where does this destination token look? OV is payload: if it looks there, what transformed information gets written back? For interpretability, the product matrices are better objects than individual Q/K/V matrices because they describe the effective computation after cancelling arbitrary intermediate bases.

### One thing I still do not understand

The exact two-layer induction-head construction should get its own derivation note. I understand the high-level role of composition, but not yet the full path expansion for Q-composition/K-composition/V-composition.

## Quiz Log

- 2026-04-28: First quiz seed captured in [[studies/anki/transformer-circuits-framework]].

## Citations

- Core summary of zero/one/two-layer results: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]].
- Independent additive attention heads: [[sources/transformer-circuits-framework#ex-independent-additive-heads]].
- QK/OV split: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]].
- Residual stream as communication channel: [[sources/transformer-circuits-framework#ex-residual-stream-communication]].
- Path expansion: [[sources/transformer-circuits-framework#ex-path-expansion]].

## Output Artifact Target

By the end, produce one of these:

- a public writeup: `Transformer Circuits From Scratch`
- or a GitHub notebook: `qk-ov-circuits.ipynb`
- or a short essay in `ideas/`: `what-mechanistic-interpretability-means-by-circuits.md`

Minimum bar reached for this pass: source-backed QK vs OV explanation plus a tiny NumPy equivalence reproduction.
