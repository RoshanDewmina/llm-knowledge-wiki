---
title: "Studying Large Language Model Generalization with Influence Functions \ Anthropic"
source_url: "https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions"
canonical_url: "https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions"
lastmod: "2024-12-19T18:58:59.000Z"
captured_at: "2026-06-08T09:06:35Z"
section: "research"
source_kind: "anthropic_web_page"
extraction_method: "sitemap_requests_bs4_main_text"
status_code: "200"
sha256_html: "2cfacc88fb7f5a81106b08f5a94796ce69d954f6091459f1136189ceb84002ee"
include_reason: "matches AI/LLM/ML/CS topic keywords"
---

# Studying Large Language Model Generalization with Influence Functions \ Anthropic

Source: https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions

## Description

Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.

## Clean Text

Alignment
Studying Large Language Model Generalization with Influence Functions
Aug 8, 2023
Read Paper
Abstract
When trying to gain better visibility into a machine learning model in order to understand and mitigate the associated risks, a potentially valuable source of evidence is: which training examples most contribute to a given behavior? Influence functions aim to answer a counterfactual: how would the model's parameters (and hence its outputs) change if a given sequence were added to the training set? While influence functions have produced insights for small models, they are difficult to scale to large language models (LLMs) due to the difficulty of computing an inverse-Hessian-vector product (IHVP). We use the Eigenvalue-corrected Kronecker-Factored Approximate Curvature (EK-FAC) approximation to scale influence functions up to LLMs with up to 52 billion parameters. In our experiments, EK-FAC achieves similar accuracy to traditional influence function estimators despite the IHVP computation being orders of magnitude faster. We investigate two algorithmic techniques to reduce the cost of computing gradients of candidate training sequences: TF-IDF filtering and query batching. We use influence functions to investigate the generalization patterns of LLMs, including the sparsity of the influence patterns, increasing abstraction with scale, math and programming abilities, cross-lingual generalization, and role-playing behavior. Despite many apparently sophisticated forms of generalization, we identify a surprising limitation: influences decay to near-zero when the order of key phrases is flipped. Overall, influence functions give us a powerful new tool for studying the generalization properties of LLMs.
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

- [Read Paper](https://arxiv.org/abs/2308.03296)
- [https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions)
- [https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions)
- [Read more](https://www.anthropic.com/research/making-claude-a-chemist)
- [Read more](https://www.anthropic.com/research/coding-agents-social-sciences)
- [Read more](https://www.anthropic.com/research/glasswing-initial-update)
