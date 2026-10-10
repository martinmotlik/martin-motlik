---
name: insights-social-posts
description: Write the social post series (LinkedIn, Facebook, X, Threads, Instagram story, WhatsApp status) that promotes a new Insights article and its podcast episode, and save it to _insights/<article-slug>/social.md. Use whenever a new article or episode is published or prepared, when the user asks for posts, a caption, a CTA or a "propagace článku/podcastu", or for a reply to a comment under one of these posts.
---

# Insights article + podcast → social post series

**Rule:** every new Insights article and every new podcast episode ships with
a full series of post drafts for all of Martin's channels. The work on an
article or episode is not finished until `_insights/<article-slug>/social.md`
exists and is committed. `_insights/` starts with an underscore, so GitHub
Pages (Jekyll) does not publish it; keep it that way. This series is one part
of the article package (skill `insights-article`).

Reference series: `_insights/ai-visibility-for-aec/social.md`. Copy its structure.

## Before writing

1. Read the published article (`insights/<slug>/index.html`) and the episode
   transcript (`podcast/episodes/<episode>.md`). Every claim in a post must
   come from them. Never invent experiences, results or numbers for Martin.
2. Pick **one core line**: a short, quotable idea from Martin's own
   experience (EP 01: "A page can be perfectly correct and still invisible.").
   Every platform rephrases it, so the series feels consistent without
   repeating itself.
3. Check the podcast page (`insights/podcast/`) for the current podcast name
   (now **Insights with Martin Motlík**) and the episode number.

## Voice and content

- Promote the article's topic, framed by Martin's own work and experience
  (localization, engineering-software websites for the U.S., Canada and
  Europe). Expert, practical, no hype.
- **No concrete times or durations**: no read time, no episode length, no
  "this week", no "in 30 minutes".
- Sarah is "my co-host Sarah". Her case is "a practical case", never "a
  real-world case". The episode is not "recorded". Posts don't call Sarah AI;
  the site carries the disclosure.
- CTA in every post: read the article and listen to the episode.

## The series

| Channel | Language | Link | Shape |
|---|---|---|---|
| LinkedIn long | U.S. English | article | Hook within the first ~210 characters (before "see more"), a short story from Martin's work, 3 → bullets, CTA, 2–3 hashtags |
| LinkedIn short | U.S. English | article | 4 short paragraphs, CTA, 2 hashtags |
| LinkedIn first comment | U.S. English | `/insights/podcast/` | Podcast CTA with the episode's hook (Sarah's problem); mention Apple Podcasts and Spotify |
| Facebook | **Czech** | article | Personal, 4 paragraphs; say the article and podcast are in English |
| X | U.S. English | article | One post ≤ 280 characters (a URL counts as 23) + optional thread of 3 replies |
| Threads | U.S. English | article | Conversational, ≤ 500 characters |
| Instagram story | U.S. English | article (link sticker "Read + listen") | Video teaser via the `podcast-ig-story` skill; plus 3 static frames as a fallback |
| WhatsApp status | Czech + English | `/insights/podcast/` | One or two lines under the video clip |

Count characters for X and Threads before saving.

## Replies to comments

Short, warm and professional: thank the person by name, say you're glad the
post resonated, and affirm their point in their own words. Never correct or
narrow their point. One sentence is often enough. Ask a question only if the
user wants to start a discussion.

## Done

- `_insights/<article-slug>/social.md` with a header table (article URL, podcast URL
  and episode, dates, core line, status) and one fenced block per post, ready
  to copy.
- Commit it with the article or episode.
- After approval it goes to Drive as a Google Doc (`3 Social/`, see the
  `insights-article` skill, `references/drive.md`).
