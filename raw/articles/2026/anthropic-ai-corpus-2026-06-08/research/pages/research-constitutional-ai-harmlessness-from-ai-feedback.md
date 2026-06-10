---
title: "Constitutional AI: Harmlessness from AI Feedback \ Anthropic"
source_url: "https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback"
canonical_url: "https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback"
lastmod: "2024-12-19T18:54:52.000Z"
captured_at: "2026-06-08T09:06:35Z"
section: "research"
source_kind: "anthropic_web_page"
extraction_method: "sitemap_requests_bs4_main_text"
status_code: "200"
sha256_html: "ed5aceb9e3f7b3be30ca1e3b57400005e69b37e6240806a347e69310c2e7be9d"
include_reason: "kept despite broad exclusion keyword because it directly concerns AI models/safety"
---

# Constitutional AI: Harmlessness from AI Feedback \ Anthropic

Source: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback

## Description

Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.

## Clean Text

Alignment
Constitutional AI: Harmlessness from AI Feedback
Dec 15, 2022
Read Paper
Abstract
As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'. The process involves both a supervised learning and a reinforcement learning phase. In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences. We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF). As a result we are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them. Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making. These methods make it possible to control AI behavior more precisely and with far fewer human labels.
Policy Memo
Constitutional AI Policy Memo
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

- [Read Paper](https://arxiv.org/abs/2212.08073)
- [Constitutional AI Policy Memo](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)
- [https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [Read more](https://www.anthropic.com/research/making-claude-a-chemist)
- [Read more](https://www.anthropic.com/research/coding-agents-social-sciences)
- [Read more](https://www.anthropic.com/research/glasswing-initial-update)
