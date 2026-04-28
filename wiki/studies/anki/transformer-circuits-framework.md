---
title: Transformer Circuits Framework Anki
type: study
created: 2026-04-28T22:15:53Z
updated: 2026-04-28T22:30:46Z
status: reviewed
confidence: 0.8
related:
  - studies/papers/transformer-circuits-framework
  - sources/transformer-circuits-framework
source_pages:
  - studies/papers/transformer-circuits-framework
compiled_at: 2026-04-28T22:30:46Z
study_kind: anki
read_status: done
rating: null
mastery_avg: 3.0
tags:
  - study
  - anki
---

# Transformer Circuits Framework Anki

#flashcards/transformer-circuits-framework

## Cards

Residual stream :: The shared additive channel that embeddings and prior layers write into, and later components read from; it is not just the current token embedding. <!-- src: [[sources/transformer-circuits-framework#ex-residual-stream-communication]] -->

Virtual weights :: Effective implicit connections between components obtained by multiplying an earlier component's output weights with a later component's input weights through the residual stream. <!-- src: [[sources/transformer-circuits-framework#ex-virtual-weights]] -->

Independent additive heads :: Multi-head attention can be rewritten as a sum of per-head outputs added into the residual stream, even if efficient implementations concatenate and multiply. <!-- src: [[sources/transformer-circuits-framework#ex-independent-additive-heads]] -->

QK circuit :: The effective query-key product that computes the attention pattern, i.e. which source position each destination position attends to. <!-- src: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]] -->

OV circuit :: The effective output-value product that determines what information is read from the attended source token and written to the destination residual stream. <!-- src: [[sources/transformer-circuits-framework#ex-attention-information-movement]] -->

Zero-layer transformer :: With no attention or MLP layers, the model can express bigram statistics directly through embedding-to-unembedding weights. <!-- src: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] -->

One-layer attention-only transformer :: A model that combines direct bigram behavior with attention-mediated skip-trigram behavior of the form `A ... B -> C`. <!-- src: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] -->

Path expansion :: The trick of expanding a product of layer terms into a sum of end-to-end computational paths that can be reasoned about independently. <!-- src: [[sources/transformer-circuits-framework#ex-path-expansion]] -->

Head composition :: In a two-layer attention-only model, one head can write information that another head uses, enabling algorithms richer than one-layer skip-trigrams. <!-- src: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] -->

Induction head :: A two-layer attention-head behavior tied to general in-context continuation/copying, arising from attention-head composition. <!-- src: [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] -->

QK vs OV :: QK chooses where to read from; OV chooses what transformed payload is written after attention selects a source. <!-- src: [[sources/transformer-circuits-framework#ex-qk-ov-circuit]] -->

Copying in one-layer heads :: OV can increase the probability of the attended token or similar tokens, while QK restricts copying to destinations where bigram-like statistics make sense. <!-- src: [[sources/transformer-circuits-framework#ex-copying-ov-summary]] -->

## Source Notes

- Study: [[studies/papers/transformer-circuits-framework]]
- Source: [[sources/transformer-circuits-framework]]

## Citations

- Cards are source-commented inline with HTML `src` comments pointing at exact source anchors.
