---
title: "How Claude Code Works"
video_id: "6bs5b4FltCU"
source_url: "https://www.youtube.com/watch?v=6bs5b4FltCU"
channel_url: "https://www.youtube.com/@claude"
tab: "videos"
captured_at: "2026-06-08T09:15:13Z"
source_kind: "youtube_transcript"
extraction_method: "yt-dlp English subtitles/auto-subtitles converted from VTT"
chosen_caption_file: "youtube/raw/6bs5b4FltCU/6bs5b4FltCU.en.vtt"
upload_date: "20260514"
duration: "2:50"
view_count: "339335"
description: "Claude Code runs on an \"agentic\" loop that gathers context, takes action, and verifies results.  In this video, we break down the loop, the context window, tools, and permission modes so that Claude Code doesn't feel like a \"magic box\".  Take the full course: claude.com/courses"
---

# How Claude Code Works

Source: https://www.youtube.com/watch?v=6bs5b4FltCU

## Transcript

We know that Claude code is different
from usual chat applications, but how
does it work?
Claude code is best explained through
the agentic loop.
You enter a prompt into Claude code.
Claude code will then gather contacts
required to complete your prompt. It
does so by interacting with the model
which will return text or a tool call
that Claude code can execute.
Then it takes action.
For example, editing a file or running a
command.
Finally, it verifies those results and
determines if they achieve what your
prompt set out to do in the first place.
If they do, then Claude finishes and
waits for the next prompt.
And if they don't, Claude goes back and
runs the loop again until the results
are complete and verifiable. Throughout
this loop, you're able to add contacts,
interrupt it, or steer the model to help
guide it towards your end goal.
Claude has a context window, which
determines how much of your
conversation, file contents, command
outputs, and more it can store and look
back on. Once you reach that limit,
Claude code compacts your conversation,
which automatically determines what it
can take out of the context window and
what it can summarize in order to bring
the context window back down.
Tools are the backbone of how agents
work.
Currently, most AI assistants are simply
input text and output text. Nothing in
between.
Tools let Claude code and other agents
determine when to execute code to get
closer to a task. This could be read
file tool or search web tool, for
example. Claude code uses semantic
searching to determine when to call a
tool and get the output of it.
Claude code also has permission modes.
Default behavior is that it has to ask
explicit permission before editing a
file or running a shell command. You can
use shift and tab to toggle between
different modes. Auto accept edits files
without asking, but still ask for
commands.
Plan mode uses read-only tools to help
compile a plan of action before
starting.
It's worth being cautious when skipping
permissions.
Giving Claude code free reign to run
commands means a mistake could be harder
to catch before even happens.
Claude code works by combining different
agentic concepts, an agentic loop, a
managed context window, tools, and
configurable permissions into your
terminal. It can read your code base,
take action, and verify its own work,
and that makes it fundamentally
different from a chat window.
