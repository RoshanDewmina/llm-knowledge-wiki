---
title: "Hooks in Claude Code"
video_id: "IkaPHiMDazM"
source_url: "https://www.youtube.com/watch?v=IkaPHiMDazM"
channel_url: "https://www.youtube.com/@claude"
tab: "videos"
captured_at: "2026-06-08T09:15:13Z"
source_kind: "youtube_transcript"
extraction_method: "yt-dlp English subtitles/auto-subtitles converted from VTT"
chosen_caption_file: "youtube/raw/IkaPHiMDazM/IkaPHiMDazM.en.vtt"
upload_date: "20260507"
duration: "3:21"
view_count: "197706"
description: "Hooks give you deterministic control over Claude Code's behavior at key lifecycle events.  Learn how to auto-format after edits, block dangerous operations, and share hooks with your team.  Take the full course: claude.com/courses"
---

# Hooks in Claude Code

Source: https://www.youtube.com/watch?v=IkaPHiMDazM

## Transcript

Hooks let you run commands at different
points in Claude code's life cycle.
The key difference between hooks and
everything else we covered is that hooks
are deterministic.
They always run.
So, put it this way. You can tell Claude
in your claude.md file to run prettier
after every file edit and most of the
time it will do that, but sometimes it
won't.
It's not perfect.
But a hook makes it happen every single
time with no exceptions.
Common use cases could include auto
formatting after file edits, logging all
executed commands for compliance,
blocking dangerous operations like
modifying production files, and sending
yourself notifications when Claude
finishes a task.
Hooks are configured in your
settings.json file.
You pick an event, optionally set a
matcher for which tool it applies to,
and provide a command to run.
User prompts submit runs when you submit
a prompt before Claude processes it.
Pre-tool use which runs before a tool
call, post-tool use runs after a tool
call completes.
Notification runs when Claude sends a
notification, and stop runs when Claude
finishes responding.
The most common hook.
Auto formatting after edits.
You set a post-tool use hook with a
matcher of edit or multi-edit, right?
So, it fires whenever Claude modifies a
file. The command checks the file
extension and runs the appropriate
formatter.
This could be prettier for TypeScript,
go format for go, rough for Python,
whatever your project uses.
Pre-tool use hooks can block tool calls
before they execute. So, your hook
receives the tool name and input as JSON
on stdin.
If it exits with code two, the action is
blocked and the STD error message gets
fed back to Claude's feedback so Claude
knows why it was blocked and can adjust.
Exit code zero means proceed. Exit code
two means block.
This is how you enforce hard rules.
Block writes to a production config
directory, block bash commands that
contain rm-rf,
block commits to main, whatever your
team needs to be guaranteed, not
suggested.
Hooks configured in
.Claude/settings.json
are project level and can be checked
into your repo. This means that your
entire team gets the same hooks
automatically.
Use the Claude project dir environment
variable in your commands to reference
scripts stored in your project so they
work regardless of Claude's current
working directory.
>> [music]
>> Hooks gives you deterministic control
over Claude code's behavior.
>> [music]
>> Use post-tool-use for auto-formatting
and logging. Use pre-tool-use to block
dangerous operations. Configure them in
the /hooks or in settings.json
>> [music]
>> and check them into your repository so
your team gets them, too.
If something needs to happen every time
without fail, don't put it in a prompt.
Put it in a hook.
>> [music]
