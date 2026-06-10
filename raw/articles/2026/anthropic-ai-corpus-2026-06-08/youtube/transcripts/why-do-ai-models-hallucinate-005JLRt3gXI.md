---
title: "Why do AI models hallucinate?"
video_id: "005JLRt3gXI"
source_url: "https://www.youtube.com/watch?v=005JLRt3gXI"
channel_url: "https://www.youtube.com/@claude"
tab: "videos"
captured_at: "2026-06-08T09:15:13Z"
source_kind: "youtube_transcript"
extraction_method: "yt-dlp English subtitles/auto-subtitles converted from VTT"
chosen_caption_file: "youtube/raw/005JLRt3gXI/005JLRt3gXI.en.vtt"
upload_date: "20260415"
duration: "5:13"
view_count: "360670"
description: "Learn what AI researchers mean when they talk about hallucination in AI models, why it may occur, and tactics you can use to spot this in your conversations.  Learn more: anthropic.com/ai-fluency"
---

# Why do AI models hallucinate?

Source: https://www.youtube.com/watch?v=005JLRt3gXI

## Transcript

[music]
>> If AI is so advanced, why does it
sometimes make stuff up?
My name is Jordan and I work at
Anthropic. We make Claude, an AI
assistant, and we do a lot to make sure
it gives you accurate information.
But sometimes AI still make things up.
We call these errors hallucinations, and
they're often worse than just making a
mistake, because the AI will appear very
confident, or even try to convince you
that it's right.
Hallucinations can show up in a lot of
ways. The AI might cite a research paper
that doesn't exist, make up fake
statistics, or get facts wrong about
real people or real events.
Here's what it looks like. You ask
Claude to tell you about some papers
written by Jared Kaplan. It confidently
gives you answers.
None of those titles actually exist.
Claude hallucinates much less than even
a year ago. Honestly, it took us a while
to find an example like this, because
we've put a lot of work into reducing
hallucinations in Claude.
But that's kind of the point.
Hallucinations are hard to anticipate,
hard to catch, and the wrong answer
often looks exactly like it could be the
right one.
And since hallucinations are becoming
more rare, people often don't bother to
check the AI's work.
So let's talk about why this happens,
what we're doing about it, and how you
can catch hallucinations when you use
AI.
AI assistants like Claude learn by
reading huge amounts of text from the
internet. They get really good at
figuring out what words or ideas
typically come next. Kind of like how
your phone suggests the next word as you
type. This works well most of the time.
But when you ask about something
obscure, like specific research papers
from a relatively unknown researcher,
there just isn't enough information for
the AI to draw from.
So, it tries to be helpful and takes a
guess. And sometimes that guess is
wrong.
It's a bit like asking a friend who's
read every popular book and takes a lot
of pride in knowing all of the random
facts about them.
But, because they want to seem like the
expert, they sometimes say something
confidently wrong instead of admitting,
"I don't know."
AIs are trained to be helpful. So, they
want to give you some answer even when
they're not sure.
But, we have ways to mitigate this.
During training, we teach Claude to be
honest and to say, "I don't know." when
it's not sure.
We try to teach Claude that being honest
is both the right thing to do and also
part of how to be more helpful.
We regularly test Claude with thousands
of questions specifically designed to
trip it up. Obscure facts, niche topics,
questions where the truthful answer is,
"I don't know."
We measure things like how often does
Claude correctly say it's unsure? Does
it make up citations or statistics? How
often does it hedge appropriately versus
stating something false with confidence?
These tests help us catch problems and
track our progress.
With each new version of Claude, we've
seen improvements. But, we're honest
that this is an ongoing challenge for
the entire AI field. Not at all a solved
problem.
If you're wondering how to spot when
this happens, hallucinations are most
likely to happen in a few types of
situations. For example, if you're
asking for specific facts, statistics,
or citations.
Or if the topic is obscure, niche, or
very recent.
If you're asking about real but not
widely known people or places, or when
you need exact details like dates,
names, or numbers.
Here some tips you can use to reduce
hallucinations. First, ask the AI to
find sources to back up its claims. And
if it already gave sources, ask it to
check that those sources actually
support what it's saying.
Try telling the AI up front, "It's okay
if you don't know."
And if you're unsure about an answer,
ask the AI how confident it is and
whether anything might be wrong.
Often the AI knows it's wrong, but just
wanted to sound confident.
If you have an answer you're unsure
about, start a new chat and ask the AI
to find errors in the answer and to
confirm that the sources support the
statements.
For critical work, you should
cross-reference with trusted sources.
Be skeptical and double-check specific
numbers, dates, and citations.
If something sounds off, ask follow-up
questions.
Reducing hallucinations is an important
goal to make AIs more trustworthy and
useful to everyone.
We'll continue to share our progress in
this area on our blog.
You can learn about other tools and
frameworks for working with AI in the
Anthropic Academy.
>> [music]
