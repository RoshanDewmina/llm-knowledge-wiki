# Anthropic / Claude AI Corpus (2026-06-08)

Purpose: AI-agent-readable local corpus from:

- YouTube channel: https://www.youtube.com/@claude
- Anthropic Research: https://www.anthropic.com/research
- Anthropic Learn: https://www.anthropic.com/learn

## What is here

- `youtube/transcripts/`: clean Markdown transcripts for videos with YouTube captions/subtitles.
- `youtube/raw/`: raw yt-dlp metadata and VTT caption files.
- `research/pages/`: clean Markdown pages extracted from Anthropic Research and filtered for AI/LLM/ML/deep-learning/math/CS relevance.
- `learn/pages/`: clean Markdown pages extracted from `/learn` sitemap pages.
- `manifests/`: JSON coverage manifests, included/excluded URL lists, and extraction summaries.
- `logs/`: command logs for verification.
- `scripts/`: extraction/conversion scripts used for this corpus.

## Coverage summary

- YouTube @claude enumerated videos/shorts/streams: 126
- YouTube clean transcripts saved: 82
- YouTube videos with no captions/subtitles exposed by YouTube: 44
- Anthropic sitemap total URLs inspected: 437
- Research sitemap URLs: 124
- Research AI/LLM/ML/CS pages saved: 107
- Research pages excluded by requested scope: 17
- Learn sitemap pages saved: 4

## Important caveat

For YouTube, this corpus downloads official/manual or automatic captions when YouTube exposes them. yt-dlp reported no subtitles/automatic captions for 44 of 126 enumerated @claude videos. Those videos are listed in `manifests/youtube-summary.json` and `00-INDEX.md`; they were not silently skipped.

Generated: 2026-06-08T09:15:13Z
