---
title: "Donating our open-source alignment tool \ Anthropic"
source_url: "https://www.anthropic.com/research/donating-open-source-petri"
canonical_url: "https://www.anthropic.com/research/donating-open-source-petri"
lastmod: "2026-05-07T21:27:38.000Z"
captured_at: "2026-06-08T09:06:35Z"
section: "research"
source_kind: "anthropic_web_page"
extraction_method: "sitemap_requests_bs4_main_text"
status_code: "200"
sha256_html: "845921ff6d49a1cb28398c537df5f4eefc50e5375becf707c261d045c809f58e"
include_reason: "matches AI/LLM/ML/CS topic keywords"
---

# Donating our open-source alignment tool \ Anthropic

Source: https://www.anthropic.com/research/donating-open-source-petri

## Description

Updating Petri to version 3.0 and donating it to Meridian Labs

## Clean Text

Alignment
Donating our open-source alignment tool
May 7, 2026
In October 2025, we launched
Petri
, an open-source toolbox of alignment tests that can be applied to any large language model. Petri, which was developed as part of our Anthropic Fellows program, can be used to rapidly and easily test AI models for concerning tendencies like deception, sycophancy, and cooperation with harmful requests. It’s part of our efforts to develop alignment tools that are open and useful for the whole AI development community.
Petri has been part of our alignment assessment for every Claude model since Claude Sonnet 4.5. It compares how the new model behaves across a range of alignment-relevant scenarios that are simulated by a separate “auditor” model. A further “judge” model then scores the resulting transcripts for misaligned behaviors.
We’ve been pleased to see Petri being used by external organizations: for example, the UK’s AI Security Institute (AISI) made it a
major part
of how they evaluate models for their propensity to sabotage AI research.
We’re now updating Petri to its third version. Here are some of the biggest changes:
Adaptability.
Petri 3.0 involves major architectural changes that allow users to adapt it to more uses, in particular by splitting the auditor model and the target model into separate components that can be tweaked separately;
Realism.
Despite the fact that alignment researchers try to make tests appear realistic, a model can often deduce from various artificialities in the setup that it’s actually part of a test. And if the model is aware it’s being evaluated, the researcher is no longer able to see how the model behaves
in general
. An add-on to Petri, which we’re calling “Dish,” makes the setup far more realistic, for example by running the tests using the model’s real system prompt and the real “scaffold” (the software that wraps around the model to help it meet its goals) that would be used in genuine model deployments;
Depth
. We’ve now integrated Petri with our other open-source alignment tool,
Bloom
, which can perform much more in-depth assessments of specific chosen behaviors (in comparison to Petri’s wider-ranging approach).
We’re also giving Petri a new home. We have handed over its development to
Meridian Labs
, an AI evaluation nonprofit. This move—similar to when we
donated
the Model Context Protocol (MCP) to the Linux Foundation—will help ensure that Petri remains independent of any AI lab, so that its results will be seen as neutral and credible by those across the industry and beyond.
As part of Meridian Labs, Petri joins other tools like
Inspect
and
Scout
, building a technology stack that is open to labs, independent researchers, and governments alike, at a time when reliable tests of AI model behavior matter more than ever.
You can read more about Petri 3.0 on
the Meridian Labs blog
.
Instructions to install and use Petri can be found on the
Petri website
.
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

- [Petri](https://www.anthropic.com/research/petri-open-source-auditing)
- [major part](https://arxiv.org/abs/2604.00788)
- [Bloom](https://www.anthropic.com/research/bloom)
- [Meridian Labs](https://meridianlabs.ai/)
- [donated](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [Inspect](https://inspect.aisi.org.uk/)
- [Scout](https://meridianlabs-ai.github.io/inspect_scout/)
- [the Meridian Labs blog](https://meridianlabs.ai/blog/posts/introducing-petri-3/)
- [Petri website](https://meridianlabs-ai.github.io/inspect_petri/)
- [https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/donating-open-source-petri](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/donating-open-source-petri)
- [https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/donating-open-source-petri](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/donating-open-source-petri)
- [Read more](https://www.anthropic.com/research/making-claude-a-chemist)
- [Read more](https://www.anthropic.com/research/coding-agents-social-sciences)
- [Read more](https://www.anthropic.com/research/glasswing-initial-update)
