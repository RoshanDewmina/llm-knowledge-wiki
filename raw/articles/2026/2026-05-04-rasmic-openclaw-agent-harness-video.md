---
title: "I made my OpenClaw agent more powerful by building my own harness"
source: "https://x.com/i/status/2051496442770997399"
author: "Micky (@Rasmic)"
published_at: "2026-05-04T22:57:00Z"
captured_at: "2026-05-06T23:35:03Z"
type: "raw_video_transcript"
tags: [openclaw, ai-agents, harness, pluto, video-transcript, workflow]
---

# I made my OpenClaw agent more powerful by building my own harness

Public X video captured by browser extraction. Audio downloaded from public `video.twimg.com` m3u8 and transcribed locally with `openai-whisper` base model via `uvx`.

## Metadata visible at capture

- Author/post text: "I made my OpenClaw agent more powerful by building my own harness... My agent has access to it's own computer (courtesy of @daytonaio), email, phone number, and credit card..."
- Duration: 14:36 visible on X; media duration from browser video element: ~881 seconds.
- Views: 45.4K
- Replies/reposts/likes/bookmarks: 32 / 34 / 489 / 577
- Public video manifest: https://video.twimg.com/amplify_video/2051495513141264387/pl/_L2Qz5IydEPk5SiL.m3u8?tag=27&v=e86&variant_version=1

## Transcript

```srt
1
00:00:00,000 --> 00:00:05,640
I made OpenClaw better now if you've watched my last few videos, then you'll know that I'm a big fan of OpenClaw

2
00:00:05,840 --> 00:00:12,160
Reason being is I've actually seen productivity using it as an agent as an assistant to help me in my business now

3
00:00:12,160 --> 00:00:17,040
There's a split voice on one hand. You have a camp that says this is the best thing ever on another hand

4
00:00:17,040 --> 00:00:18,720
You have people who say this is completely trash

5
00:00:18,720 --> 00:00:24,320
I truly believe that divide exists because there's a time requirement in terms of investment that you have to make

6
00:00:24,720 --> 00:00:27,440
Configuring it and making it the right assistant for you

7
00:00:27,840 --> 00:00:33,200
I truly believe I'm building towards that that I've built a harness for a lack of a better term

8
00:00:33,360 --> 00:00:38,160
That's going to make your OpenClaw agent super powerful. We're talking about deployment

9
00:00:38,320 --> 00:00:41,760
We're talking about giving it tools that you use so it has context on you

10
00:00:41,920 --> 00:00:44,960
But we're also talking about giving it tools so we can do things for you

11
00:00:45,120 --> 00:00:49,760
And this is what it looks like if you go to higher Pluto dot AI or use Pluto dot xyz

12
00:00:50,000 --> 00:00:54,160
I know xyz URLs are not cool. So I'm gonna drop that but if you go there

13
00:00:54,160 --> 00:00:58,320
You can sign up for the wait list because ladies and gents. I've been building this for the last couple of weeks

14
00:00:58,560 --> 00:01:04,800
And we have customers we have people who are actually beta testing giving us actual money on to use this

15
00:01:05,200 --> 00:01:08,960
I genuinely believe I've cooked with this. I'm super excited about this

16
00:01:09,280 --> 00:01:15,760
This is what it looks like, but let's get into the nitty gritty. Let's talk about how I made OpenClaw better

17
00:01:16,080 --> 00:01:20,080
The first thing that I want to talk about is the four lane dispatcher

18
00:01:20,160 --> 00:01:25,040
This is getting into the agent architecture now if you're familiar with OpenClaw

19
00:01:25,280 --> 00:01:29,440
You'll then realize that OpenClaw has what's called a queue system

20
00:01:29,760 --> 00:01:35,360
Meaning if I text my OpenClaw agent through telegram to check the weather and right after that

21
00:01:35,520 --> 00:01:38,160
I also tell it to check the weather some other place

22
00:01:38,560 --> 00:01:42,000
It's not going to do the second task until the first task is done

23
00:01:42,240 --> 00:01:46,960
Meaning it does not have the ability out of the gate to do two things at at the same time

24
00:01:47,120 --> 00:01:50,720
There's a queue system right now with telegram. You can use multiple threads

25
00:01:51,040 --> 00:01:54,400
Or you can tell the agent to use a sub agent to do this task

26
00:01:54,640 --> 00:01:57,840
But that gets very annoying and tiring and let's see you forget to do that now

27
00:01:57,840 --> 00:02:05,440
You have to wait for the OpenClaw agent to finish this four lane dispatcher makes it so that my agent is always free to take care of me

28
00:02:05,600 --> 00:02:10,800
What does that mean? Let's say I send a prompt when I send a prompt the main agent is going to check

29
00:02:11,200 --> 00:02:13,040
Is this something that I can handle quickly?

30
00:02:13,440 --> 00:02:15,840
Is this something that I have to delegate to a sub agent?

31
00:02:16,320 --> 00:02:19,760
Is this something that I do the work or the sub agent does the work

32
00:02:19,920 --> 00:02:25,440
But there needs to be human in the loop aka draft or is this something I completely bought because it's some nonsense

33
00:02:25,760 --> 00:02:29,120
Let's focus on the first three direct this something like check the weather

34
00:02:29,200 --> 00:02:33,760
It's going to be a quick API call it's going to get it done quick the main agent can handle that for you

35
00:02:34,000 --> 00:02:38,560
But let's say you wanted to generate a report based on the previous email that you got

36
00:02:38,880 --> 00:02:42,800
And the latest invoice that you received and you want some analytics to be checked

37
00:02:42,880 --> 00:02:44,400
This is a pretty beefy task

38
00:02:44,480 --> 00:02:49,840
So when you send this prompt the main agent is going to know this needs to be delegated to a sub agent

39
00:02:50,000 --> 00:02:52,960
And the way this works is it's going to spawn a sub agent

40
00:02:52,960 --> 00:02:58,560
It's going to give that sub agent all the context and needs it's going to give that sub agent the tools that it needs

41
00:02:58,880 --> 00:03:02,400
The sub agent is going to go do its thing the main agent is now free

42
00:03:02,480 --> 00:03:07,040
So I can keep going back and forward the main agent while this is being worked on

43
00:03:07,200 --> 00:03:12,080
Once it's done the sub agent is going to tell the main agent the main agent is going to tell me now

44
00:03:12,640 --> 00:03:18,880
Draft the third type of task is when you're sending emails or maybe you're making a payment right because you can give

45
00:03:19,040 --> 00:03:22,080
Believe it or not your open clock agent a virtual card or a credit card

46
00:03:22,080 --> 00:03:24,560
And I'll show you how that works in a second and

47
00:03:25,360 --> 00:03:28,960
These things at least in my opinion require a human in the loop

48
00:03:28,960 --> 00:03:34,080
It requires me to confirm what's being done especially when you're sending emails to other people

49
00:03:34,400 --> 00:03:38,160
So what happens is the agents are going to ask me this is the email that I've drafted

50
00:03:38,160 --> 00:03:42,640
This is the payment I'm going to make does this look good and then I'm going to say yes

51
00:03:42,960 --> 00:03:48,560
And the agent is going to continue on with the task and last but not least is the agent blocking tasks

52
00:03:48,640 --> 00:03:52,480
And this is particularly if you're doing some disgusting sickle stuff

53
00:03:52,640 --> 00:03:56,960
Then the agent is going to straight up block you and I truly believe with this four lane dispatcher

54
00:03:56,960 --> 00:04:02,240
Not only does this make the agent perform it but it also makes it safe adding the right guardrails

55
00:04:02,320 --> 00:04:06,960
But you know what else helps you makes things safe the sponsor of today's video if you've been watching my videos

56
00:04:06,960 --> 00:04:11,760
Then you know I'm a big fan of macroscope the sponsor of today's video one of my favorite AI coding agents

57
00:04:11,840 --> 00:04:15,840
Here's a simple example of how it caught a bug if this had shipped into production

58
00:04:16,080 --> 00:04:21,200
I'd have been in a lot of trouble, but because I use macroscope it saved me anytime I get a medium or a high

59
00:04:21,280 --> 00:04:24,000
I make sure I pay attention, but that's not what I want to show you today

60
00:04:24,080 --> 00:04:28,160
What I want to show you is the dashboard you can see I'm working on a top secret project

61
00:04:28,240 --> 00:04:32,000
And I've pulled in 159 hours of coding time

62
00:04:32,000 --> 00:04:39,440
And it also shows you here the breakdown of the project like 74% spent on the desktop agent 12% on safety and input guardrails

63
00:04:39,440 --> 00:04:45,840
The AI labs would be so disappointed 7% on long running task orchestration and 7% on UI cleanup

64
00:04:45,840 --> 00:04:47,360
And I get a sprint summary here

65
00:04:47,520 --> 00:04:53,440
But something cool that they shipped recently are almost these automations that are directly connected to my select

66
00:04:53,440 --> 00:04:54,720
So I have two setup right now

67
00:04:54,800 --> 00:04:58,160
I have weekly release notes which basically you can read it here

68
00:04:58,160 --> 00:05:05,120
Focuses only on changes that directly impact users like new features user visible changes and performance improvements

69
00:05:05,120 --> 00:05:09,280
I get this directly on Slack. I also get a sprint progress review

70
00:05:09,280 --> 00:05:13,120
But here over on Slack there's a couple of cool things that they should recently as well

71
00:05:13,120 --> 00:05:17,040
For example, I can directly communicate with the macroscope agent

72
00:05:17,040 --> 00:05:20,160
You can see here. I asked to tell me about this project open agent

73
00:05:20,160 --> 00:05:24,000
And it gave me a huge blur of the text stack the project structure

74
00:05:24,000 --> 00:05:27,440
It tells me that it's a monorepo and I can also ask it

75
00:05:27,440 --> 00:05:29,840
Tell me the things I've shipped in the last two weeks

76
00:05:29,840 --> 00:05:35,440
Now this is a great way for me to keep my team in check to make sure that we're making progress for client projects

77
00:05:35,440 --> 00:05:38,800
And last but not least I can also see the active branches and PRs

78
00:05:38,800 --> 00:05:43,280
We have right here on macroscope and they have this cool toggle where I can see the technical description

79
00:05:43,280 --> 00:05:44,880
And then not so technical description

80
00:05:44,880 --> 00:05:49,280
If you want an AI code review agent that gives you full visibility and catches pesky bugs

81
00:05:49,280 --> 00:05:52,320
Then make sure to check out macroscope the link is in the description

82
00:05:52,400 --> 00:05:56,720
Now the second change in agent architecture is the medium in which you can communicate with the agent

83
00:05:56,720 --> 00:06:00,560
You can obviously communicate with telegram iMessage and Slack

84
00:06:00,560 --> 00:06:04,880
But there's a built-in chat and I'm going to show you why I went with a built-in chat

85
00:06:04,880 --> 00:06:09,280
There's a canaban board and there's what we call routines or what cloud calls routines

86
00:06:09,280 --> 00:06:12,880
Now if I go back to the web app right here here is the built-in chat app

87
00:06:12,880 --> 00:06:17,360
I just sent it saying what's up G and then it responded back all is well

88
00:06:17,360 --> 00:06:20,560
But what you see on the right side is you see desktop

89
00:06:20,560 --> 00:06:28,880
Every open-cloud agent deployed through Pluto has its own full-fledged linux computer with a browser and a terminal

90
00:06:28,880 --> 00:06:33,520
So I can tell the agent to do x, y and z using the computer

91
00:06:33,520 --> 00:06:38,800
And I can see it do the work live. What's pretty awesome is I can open this in a new tab

92
00:06:38,800 --> 00:06:43,120
I can actually use this computer myself and that's what I like about this chat form factor

93
00:06:43,120 --> 00:06:45,920
I can directly communicate here when it's using the computer

94
00:06:45,920 --> 00:06:48,640
I can see what it's doing on the computer

95
00:06:48,640 --> 00:06:51,360
Now tasks are for those list of things

96
00:06:51,360 --> 00:06:54,640
You just want to dump on the agent and you want to track the progress

97
00:06:54,640 --> 00:06:58,480
And you just want to dump a huge list and let the agent cook

98
00:06:58,480 --> 00:07:01,360
Some agents will be deployed so it can do things in parallel

99
00:07:01,360 --> 00:07:05,280
And for whatever needs human in the loop whatever is a draft

100
00:07:05,280 --> 00:07:08,560
Is going to be stuck in review meaning it's going to be in review

101
00:07:08,560 --> 00:07:11,600
You're going to have to accept or give it permissions to do so

102
00:07:11,600 --> 00:07:14,240
And then it moves on to done

103
00:07:14,240 --> 00:07:17,600
Routines are basically similar to tasks

104
00:07:17,600 --> 00:07:19,680
Right, but these are for more repetitive things

105
00:07:19,680 --> 00:07:21,600
I can set up a specific crontime

106
00:07:21,600 --> 00:07:24,720
I can set up you know every minute every hour every day

107
00:07:24,720 --> 00:07:28,000
I can do one shot, but really you should just use a task for that

108
00:07:28,000 --> 00:07:33,280
Right, and I can be reminded via email that this is done or I can get a notification sent to me

109
00:07:33,280 --> 00:07:36,960
And this is for a myriad of tasks, but anything that you want repeated

110
00:07:36,960 --> 00:07:38,960
Routines are where you're going to set them up

111
00:07:38,960 --> 00:07:41,760
So with the four lane dispatcher and these agent mediums

112
00:07:41,760 --> 00:07:45,680
I genuinely believe this is the best way to work with an open cloud agent

113
00:07:45,680 --> 00:07:47,120
Now let's talk about the tools

114
00:07:47,120 --> 00:07:50,480
You saw that I gave the agent access to its own computer

115
00:07:50,480 --> 00:07:53,360
The agent also believe it or not has its own email

116
00:07:53,360 --> 00:07:56,720
So if I go to email you can see I have this inbox

117
00:07:56,720 --> 00:07:59,760
RMV3 at agentmail.io

118
00:07:59,760 --> 00:08:04,400
I can also connect my own domain and have a domain specific email

119
00:08:04,400 --> 00:08:05,920
I don't need to do that right now

120
00:08:05,920 --> 00:08:07,600
So I'm just going to use this email

121
00:08:07,600 --> 00:08:10,160
And I can get the agent to send emails

122
00:08:10,160 --> 00:08:12,560
I can also send emails on the agents behalf

123
00:08:12,560 --> 00:08:14,720
The agent can receive emails as well

124
00:08:14,720 --> 00:08:17,440
And not only have I given it access to its own email

125
00:08:17,440 --> 00:08:21,760
But it has its own phone number, a credit card and a thousand plus connectors

126
00:08:21,760 --> 00:08:25,680
Right, so if I go back to the app and I click on connectors

127
00:08:25,680 --> 00:08:27,200
Every connector you can think of

128
00:08:27,200 --> 00:08:30,400
Notion, Google Drive, GitHub, Slack, G-Rub

129
00:08:30,400 --> 00:08:32,400
There's literally a thousand plus

130
00:08:32,400 --> 00:08:34,000
I'm using Composier for this

131
00:08:34,000 --> 00:08:37,440
If you want me to dive deep into the tools I use and why I use them

132
00:08:37,440 --> 00:08:38,880
Let me know in the comments down below

133
00:08:38,880 --> 00:08:40,480
I might move off Composier

134
00:08:40,480 --> 00:08:42,240
I'm still thinking about that decision

135
00:08:42,240 --> 00:08:45,200
And again for phone numbers in order to link a phone number

136
00:08:45,200 --> 00:08:48,320
I need to have a tool you account with a tool you'll number set up

137
00:08:48,320 --> 00:08:49,520
It's a pretty simple setup

138
00:08:49,520 --> 00:08:53,280
I just fill this in and I can communicate with my agent through the phone

139
00:08:53,280 --> 00:08:55,280
And last but not least is the credit cards

140
00:08:55,280 --> 00:08:57,680
Now there's two ways to set up credit cards are cards

141
00:08:57,680 --> 00:09:00,880
Right, there's agent card which is a virtual card provider

142
00:09:00,880 --> 00:09:04,720
Or there's link which is basically stripes, wallet

143
00:09:04,720 --> 00:09:06,320
For agents or people

144
00:09:06,320 --> 00:09:08,960
Right, so unfortunately because I'm in Canada

145
00:09:08,960 --> 00:09:10,720
This is not available in Canada

146
00:09:10,720 --> 00:09:12,320
It's available in US and UK

147
00:09:12,320 --> 00:09:14,960
I should probably add that instead of seeing available worldwide

148
00:09:14,960 --> 00:09:15,760
Except India

149
00:09:15,760 --> 00:09:17,760
And agent card is available everywhere

150
00:09:17,760 --> 00:09:22,320
Right, what's cool with link is it basically uses your stripe account for my understanding

151
00:09:22,320 --> 00:09:23,520
So that's pretty awesome

152
00:09:23,520 --> 00:09:25,120
Agent card is a virtual card

153
00:09:25,120 --> 00:09:27,120
So I can set up either or

154
00:09:27,120 --> 00:09:31,920
And what now happens is I have an agent that has access to its own computer

155
00:09:31,920 --> 00:09:33,120
Its own email

156
00:09:33,120 --> 00:09:34,400
Its own phone number

157
00:09:34,400 --> 00:09:35,600
Its own credit card

158
00:09:35,600 --> 00:09:38,000
And access to tools that you wanted to have

159
00:09:38,000 --> 00:09:39,520
Connections that you wanted to have

160
00:09:39,520 --> 00:09:41,760
Context that you wanted to have

161
00:09:41,760 --> 00:09:44,640
This combination of computer email and credit card

162
00:09:44,640 --> 00:09:47,120
Honestly makes this a truly useful agent

163
00:09:47,120 --> 00:09:49,760
You wanted to, you know, order Uber Eats for you

164
00:09:49,760 --> 00:09:52,320
You wanted to post on TikTok

165
00:09:52,320 --> 00:09:54,560
Right, you wanted to do whatever

166
00:09:54,560 --> 00:09:56,560
It can fully do that

167
00:09:56,560 --> 00:09:59,040
Because it has the right tools, the right environment

168
00:09:59,040 --> 00:10:00,240
Its own computer

169
00:10:00,240 --> 00:10:02,720
And all this setup took me time

170
00:10:02,720 --> 00:10:05,040
When I was building this out from scratch

171
00:10:05,040 --> 00:10:07,120
But now for people who are going to use Pluto

172
00:10:07,120 --> 00:10:09,360
This is available to them out of the box

173
00:10:09,360 --> 00:10:10,880
Now let's talk about the text tag

174
00:10:10,880 --> 00:10:12,480
What text tag did I use

175
00:10:12,480 --> 00:10:16,080
And I'm also going to show you an architectural diagram of how this app works

176
00:10:16,080 --> 00:10:20,480
We're going to hop on my trusted, trusted harness which is cursor

177
00:10:20,480 --> 00:10:22,000
So there are three clients

178
00:10:22,000 --> 00:10:23,600
The first one is an admin site

179
00:10:23,600 --> 00:10:24,880
And I can actually

180
00:10:24,880 --> 00:10:26,160
Locke show you

181
00:10:26,160 --> 00:10:27,920
What the admin site looks like

182
00:10:28,640 --> 00:10:30,560
Its own local host right now

183
00:10:30,560 --> 00:10:33,760
And basically this admin site gives me full visibility

184
00:10:33,760 --> 00:10:34,880
On all the errors

185
00:10:34,880 --> 00:10:36,080
Where things went wrong

186
00:10:36,080 --> 00:10:37,600
I have traces

187
00:10:37,600 --> 00:10:39,120
Just to make sure I'm running emails

188
00:10:39,120 --> 00:10:42,800
Just to make sure that people have an excellent experience

189
00:10:42,800 --> 00:10:44,400
With the agent

190
00:10:44,400 --> 00:10:46,240
Right, so we do have an admin site

191
00:10:46,240 --> 00:10:47,840
Then there is the main app

192
00:10:47,840 --> 00:10:49,040
Right, the dashboard app

193
00:10:49,040 --> 00:10:51,760
And then there's a desktop app that I'm actually working on

194
00:10:51,760 --> 00:10:53,120
Right, so that's pretty awesome

195
00:10:53,120 --> 00:10:54,720
Now I'm using SvelteKit

196
00:10:54,720 --> 00:10:55,360
I told you

197
00:10:55,360 --> 00:10:56,160
I'm SvelteKit

198
00:10:56,160 --> 00:10:56,880
I love Svelte

199
00:10:56,880 --> 00:10:58,240
If you haven't checked out the video

200
00:10:58,240 --> 00:10:58,800
Check it out

201
00:10:58,800 --> 00:11:00,800
It's on my channel it's like the fourth video

202
00:11:00,800 --> 00:11:03,360
I've uploaded in the last couple of weeks

203
00:11:03,360 --> 00:11:05,280
By the way, I haven't uploaded in like 30 days

204
00:11:05,280 --> 00:11:06,000
I hope you missed me

205
00:11:06,000 --> 00:11:06,800
I missed you too

206
00:11:06,800 --> 00:11:08,080
Let's get back into this

207
00:11:08,080 --> 00:11:10,240
So I'm using SvelteKit for my front end

208
00:11:10,240 --> 00:11:11,920
And for some APIs

209
00:11:11,920 --> 00:11:13,600
And then Convex for my back

210
00:11:13,600 --> 00:11:15,680
And now Convex does a lot of heavy lifting

211
00:11:15,680 --> 00:11:18,320
Right, Convex is managing the deployments

212
00:11:18,320 --> 00:11:19,760
The API keys

213
00:11:19,760 --> 00:11:22,480
Handles the off connection with Work OS

214
00:11:22,480 --> 00:11:24,480
Right, it's my gateway transport

215
00:11:24,480 --> 00:11:26,240
It manages the tools

216
00:11:26,240 --> 00:11:28,320
Right, there's a catalog of tools

217
00:11:28,320 --> 00:11:30,480
All the deployment connections

218
00:11:30,480 --> 00:11:31,680
Dispatching

219
00:11:31,680 --> 00:11:33,120
The agent status

220
00:11:33,120 --> 00:11:35,840
All of that stuff is handled by Convex

221
00:11:35,840 --> 00:11:38,400
And there's no better way to do that stuff

222
00:11:38,400 --> 00:11:39,840
And then when it comes to deployments

223
00:11:39,840 --> 00:11:41,840
I have a deployment provider

224
00:11:41,840 --> 00:11:43,840
And mainly we're using Daytona

225
00:11:43,840 --> 00:11:45,600
But you have the option to use Hetzner

226
00:11:45,600 --> 00:11:46,400
Hostinger

227
00:11:46,400 --> 00:11:47,680
OVH Zebra

228
00:11:47,680 --> 00:11:49,520
And then there's like a mock one that uses

229
00:11:49,520 --> 00:11:51,120
Like you know, your local computer

230
00:11:51,120 --> 00:11:53,040
Might actually make that an option for people

231
00:11:53,040 --> 00:11:54,880
Want to use their Mac Minis

232
00:11:54,960 --> 00:11:59,360
And then we have the actual OpenClaw Gateway

233
00:11:59,360 --> 00:12:01,040
Right, we're using Caddy

234
00:12:01,040 --> 00:12:02,800
As a WebSocket Proxy

235
00:12:02,800 --> 00:12:05,840
The OpenClaw Gateway is where all the chatting

236
00:12:05,840 --> 00:12:07,440
The sessions, the tools

237
00:12:07,440 --> 00:12:09,120
All that good stuff happens

238
00:12:09,120 --> 00:12:11,920
And then there's also external services we use

239
00:12:11,920 --> 00:12:14,000
Right, the models, Composio, Twilio

240
00:12:14,000 --> 00:12:15,520
Supermemory for the memory

241
00:12:15,520 --> 00:12:17,520
Now, some of you might ask

242
00:12:17,520 --> 00:12:20,080
Why are you using Supermemory as a memory layer

243
00:12:20,080 --> 00:12:23,280
And the reason being is I actually want people to own their memory

244
00:12:23,280 --> 00:12:25,920
Meaning if they want to move away from Pluto

245
00:12:25,920 --> 00:12:27,840
They shouldn't feel like they're stuck with Pluto

246
00:12:27,840 --> 00:12:30,320
Because, you know, their memory layer lives in Pluto

247
00:12:30,320 --> 00:12:31,920
But if you're using a third party service

248
00:12:31,920 --> 00:12:33,600
A cloud provider like Supermemory

249
00:12:33,600 --> 00:12:35,360
You can take your memory elsewhere

250
00:12:35,360 --> 00:12:37,360
Right, and I think that's pretty awesome

251
00:12:37,360 --> 00:12:40,400
Mistral OCR, I love Mistral OCR

252
00:12:40,400 --> 00:12:42,720
Product basically use it for files

253
00:12:42,720 --> 00:12:44,400
Using auto for payments

254
00:12:44,400 --> 00:12:47,920
Agent mail for the email service for the agents

255
00:12:47,920 --> 00:12:49,840
And then Cloudflare R2

256
00:12:49,840 --> 00:12:52,640
For any sort of storage requirements for files

257
00:12:52,640 --> 00:12:55,840
And then for observability we're using brain trust, axiom

258
00:12:55,840 --> 00:12:59,040
And sentry, I don't know what Pino is or Pino is

259
00:12:59,040 --> 00:13:01,520
And then for auth we're using WorkOS

260
00:13:01,520 --> 00:13:04,080
Now, I can already hear the questions

261
00:13:04,080 --> 00:13:06,720
Mike, why didn't you build your own agent

262
00:13:06,720 --> 00:13:09,280
Reason being is I wanted to focus more on the product

263
00:13:09,280 --> 00:13:11,040
And the harness around the product

264
00:13:11,040 --> 00:13:14,000
Why did you bet on OpenClaw and not pick Hermes

265
00:13:14,000 --> 00:13:15,680
The reason why I bet on OpenClaw

266
00:13:15,680 --> 00:13:18,160
Is OpenClaw has a lot of support

267
00:13:18,160 --> 00:13:20,160
Meaning from different companies

268
00:13:20,160 --> 00:13:22,560
I mean, for example, Convics, one of our developers

269
00:13:22,560 --> 00:13:24,720
Helps with making cloud hub better

270
00:13:24,720 --> 00:13:26,560
Right, and I know there's other different companies

271
00:13:26,560 --> 00:13:28,960
I can video and engineers from OpenAI

272
00:13:28,960 --> 00:13:30,960
And their own contributors that are helping

273
00:13:30,960 --> 00:13:32,480
To make OpenClaw better

274
00:13:32,480 --> 00:13:35,600
Number one, number two, the founder Peter

275
00:13:35,600 --> 00:13:37,120
Works at OpenAI

276
00:13:37,120 --> 00:13:39,440
Right, and him working in OpenAI means

277
00:13:39,440 --> 00:13:42,160
He has access to the best talent, knowledge

278
00:13:42,160 --> 00:13:45,760
And wisdom, and although yes, OpenAI does not own OpenClaw

279
00:13:45,760 --> 00:13:48,800
There is a benefit of him being in OpenAI employee

280
00:13:49,360 --> 00:13:52,080
And number three, the reason why I didn't pick Hermes

281
00:13:52,080 --> 00:13:53,600
Is because I was just familiar with OpenClaw

282
00:13:53,600 --> 00:13:55,040
Use OpenClaw a lot more

283
00:13:55,040 --> 00:13:56,240
I was familiar with it

284
00:13:56,240 --> 00:13:58,720
And the OpenClaw team has been shipping a lot of updates

285
00:13:58,720 --> 00:14:00,800
They're making it leaner and meaner

286
00:14:00,800 --> 00:14:03,840
Now for those of you who are Hermes agent apologists

287
00:14:03,840 --> 00:14:05,760
And are asking why didn't you pick it

288
00:14:05,760 --> 00:14:07,760
Truth be told, I haven't used it

289
00:14:07,760 --> 00:14:08,960
I haven't tested it out

290
00:14:08,960 --> 00:14:10,640
But I am working on an adapter

291
00:14:10,640 --> 00:14:12,880
So that you can either pick OpenClaw

292
00:14:12,880 --> 00:14:15,920
Or Hermes when you're deploying your agent on Pluto

293
00:14:15,920 --> 00:14:18,160
So either way, everyone's going to be happy

294
00:14:18,160 --> 00:14:19,360
And everyone's going to win

295
00:14:19,360 --> 00:14:22,560
And ladies and gentlemen, that is how I made OpenClaw better

296
00:14:22,560 --> 00:14:24,400
We actually have customers using Pluto

297
00:14:24,400 --> 00:14:26,000
My team is using Pluto

298
00:14:26,000 --> 00:14:27,120
I'm using Pluto

299
00:14:27,120 --> 00:14:28,160
This is an exciting time

300
00:14:28,160 --> 00:14:30,800
If you'd like a deeper dive on a specific feature

301
00:14:30,800 --> 00:14:31,600
Or toolset

302
00:14:31,600 --> 00:14:32,880
Or why I did what

303
00:14:32,880 --> 00:14:35,680
Or what I picked for to do X, Y and Z

304
00:14:35,680 --> 00:14:37,040
Let me know in the comments down below

305
00:14:37,040 --> 00:14:37,760
You've been awesome

306
00:14:37,760 --> 00:14:38,400
I've been Ross

307
00:14:38,400 --> 00:14:39,200
Thank you for watching

308
00:14:39,200 --> 00:14:40,160
I'll see you in the next one

309
00:14:40,160 --> 00:14:41,360
Peace


```
