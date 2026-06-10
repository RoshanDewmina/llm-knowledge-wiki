---
title: "Superposition, Memorization, and Double Descent \ Anthropic"
source_url: "https://www.anthropic.com/research/superposition-memorization-and-double-descent"
canonical_url: "https://www.anthropic.com/research/superposition-memorization-and-double-descent"
lastmod: "2024-12-19T18:59:07.000Z"
captured_at: "2026-06-08T09:06:35Z"
section: "research"
source_kind: "anthropic_web_page"
extraction_method: "sitemap_requests_bs4_main_text"
status_code: "200"
sha256_html: "630460be62064807b1f602723035b142f1d496f16c50197d87a97d1240efe4ff"
include_reason: "matches AI/LLM/ML/CS topic keywords"
---

# Superposition, Memorization, and Double Descent \ Anthropic

Source: https://www.anthropic.com/research/superposition-memorization-and-double-descent

## Description

Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.

## Clean Text

Interpretability
Superposition, Memorization, and Double Descent
Jan 5, 2023
Read Paper
Abstract
In a
recent paper
, we found that simple neural networks trained on toy tasks often exhibit a phenomenon called superposition, where they represent more features than they have neurons. Our investigation was limited to the infinite-data, underfitting regime. But there's reason to believe that understanding overfitting might be important if we want to succeed at mechanistic interpretability, and that superposition might be a central part of the story.
Why should mechanistic interpretability care about overfitting? Despite overfitting being a central problem in machine learning, we have little mechanistic understanding of what exactly is going on when deep learning models overfit or memorize examples. Additionally, previous work has hinted that there may be an important link between overfitting and learning interpretable features.
So understanding overfitting is important, but why should it be relevant to superposition? Consider the case of a language model which verbatim memorizes text. How can it do this? One naive idea is that it might use neurons to create a lookup table mapping sequences to arbitrary continuations. For every sequence of tokens it wishes to memorize, it could dedicate one neuron to detecting that sequence, and then implement arbitrary behavior when it fires. The problem with this approach is that it's extremely inefficient – but it seems like a perfect candidate for superposition, since each case is mutually exclusive and can't interfere.
In this note, we offer a very preliminary investigation of training the same toy models in our previous paper on limited datasets. Despite being extremely simple, the toy model turns out to be a surprisingly rich case study for overfitting. In particular, we find the following:
Overfitting corresponds to storing data points, rather than features, in superposition.
Depending on dataset size, our models fall into two different regimes: an overfitting regime (characterized by storing data points in superposition), and a generalizing regime (characterized by storing features in superposition).
We observe double descent as the model transitions between these regimes.
Related content
Making Claude a chemist
Read more
Coding agents in the social sciences
Results from a survey of 1,260 social scientists about AI and coding agent use.
Read more
Project Glasswing: An initial update
An early update on what we've learned from Project Glasswing.
Read more

## Main Links

- [Read Paper](https://transformer-circuits.pub/2023/toy-double-descent/index.html)
- [recent paper](https://transformer-circuits.pub/2022/toy_model/index.html)
- [https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/superposition-memorization-and-double-descent](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/superposition-memorization-and-double-descent)
- [https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/superposition-memorization-and-double-descent](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/superposition-memorization-and-double-descent)
- [Read more](https://www.anthropic.com/research/making-claude-a-chemist)
- [Read more](https://www.anthropic.com/research/coding-agents-social-sciences)
- [Read more](https://www.anthropic.com/research/glasswing-initial-update)
