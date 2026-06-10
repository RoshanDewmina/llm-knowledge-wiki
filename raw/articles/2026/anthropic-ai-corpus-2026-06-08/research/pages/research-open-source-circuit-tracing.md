---
title: "Open-sourcing circuit-tracing tools \ Anthropic"
source_url: "https://www.anthropic.com/research/open-source-circuit-tracing"
canonical_url: "https://www.anthropic.com/research/open-source-circuit-tracing"
lastmod: "2025-05-29T16:14:52.000Z"
captured_at: "2026-06-08T09:06:35Z"
section: "research"
source_kind: "anthropic_web_page"
extraction_method: "sitemap_requests_bs4_main_text"
status_code: "200"
sha256_html: "97e153ea05e100ab0242477a908b994b596735e58a0c953f1f20b9311a6c22b9"
include_reason: "matches AI/LLM/ML/CS topic keywords"
---

# Open-sourcing circuit-tracing tools \ Anthropic

Source: https://www.anthropic.com/research/open-source-circuit-tracing

## Description

Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.

## Clean Text

Interpretability
Open-sourcing circuit tracing tools
May 29, 2025
In our recent interpretability research, we introduced a new method to
trace the thoughts
of a large language model. Today, we’re open-sourcing the method so that anyone can build on our research.
Our approach is to generate
attribution graphs
, which (partially) reveal the steps a model took internally to decide on a particular output. The open-source
library
we’re releasing supports the generation of attribution graphs on popular open-weights models—and a frontend hosted by Neuronpedia lets you explore the graphs interactively.
This project was led by participants in our
Anthropic Fellows
program, in collaboration with
Decode Research
.
An overview of the interactive graph explorer UI on Neuronpedia.
To get started, you can visit the
Neuronpedia interface
to generate and view your own attribution graphs for prompts of your choosing. For more sophisticated usage and research, you can view the
code repository
. This release enables researchers to:
Trace circuits
on supported models, by generating their own attribution graphs;
Visualize, annotate, and share
graphs in an interactive frontend;
Test
hypotheses
by modifying feature values and observing how model outputs change.
We’ve already used these tools to study interesting behaviors like multi-step reasoning and multilingual representations in Gemma-2-2b and Llama-3.2-1b—see our demo
notebook
for examples and analysis. We also invite the community to help us find additional interesting circuits—as inspiration, we provide additional attribution graphs that we haven’t yet analyzed in the demo notebook and on Neuronpedia.
Our CEO Dario Amodei
wrote recently
about the urgency of interpretability research: at present, our understanding of the inner workings of AI lags far behind the progress we’re making in AI capabilities. By open-sourcing these tools, we're hoping to make it easier for the broader community to study what’s going on inside language models. We’re looking forward to seeing applications of these tools to understand model behaviors—as well as extensions that improve the tools themselves.
The open-source-circuit-finding library was developed by
Anthropic Fellows
Michael Hanna and Mateusz Piotrowski with mentorship from Emmanuel Ameisen and Jack Lindsey. The Neuronpedia integration was implemented by
Decode Research
(Neuronpedia lead: Johnny Lin; Science lead/director: Curt Tigges). Our Gemma graphs are based on transcoders trained as part of the
GemmaScope
project. For questions or feedback, please open an issue on GitHub.
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

- [trace the thoughts](https://www.anthropic.com/research/tracing-thoughts-language-model)
- [library](https://github.com/safety-research/circuit-tracer)
- [Anthropic Fellows](https://alignment.anthropic.com/2024/anthropic-fellows-program/)
- [Decode Research](https://www.decoderesearch.org/)
- [Neuronpedia interface](https://www.neuronpedia.org/gemma-2-2b/graph)
- [code repository](https://github.com/safety-research/circuit-tracer)
- [notebook](https://github.com/safety-research/circuit-tracer/blob/main/demos/circuit_tracing_tutorial.ipynb)
- [wrote recently](https://www.darioamodei.com/post/the-urgency-of-interpretability)
- [GemmaScope](https://ai.google.dev/gemma/docs/gemma_scope)
- [https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/open-source-circuit-tracing](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/open-source-circuit-tracing)
- [https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/open-source-circuit-tracing](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/open-source-circuit-tracing)
- [Read more](https://www.anthropic.com/research/making-claude-a-chemist)
- [Read more](https://www.anthropic.com/research/coding-agents-social-sciences)
- [Read more](https://www.anthropic.com/research/glasswing-initial-update)
