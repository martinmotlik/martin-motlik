# Social posts: A power outlet for AI: what MCP means for AEC

| | |
|---|---|
| Article | https://martinmotlik.com/insights/mcp-power-outlet-for-ai/ (CS: https://martinmotlik.com/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/) |
| Podcast | Insights with Martin Motlík · EP 02 · https://martinmotlik.com/insights/podcast/ |
| Published | 2026-10-25 (article and episode) |
| Core line | "MCP doesn't make AI smarter. It makes its answers checkable." |
| Status | Drafts ready, waiting for approval |

Rules for this series are in `.claude/skills/insights-social-posts/SKILL.md`; the whole package is described in `.claude/skills/insights-article/SKILL.md`. Czech posts say "stavebnictví", not "AEC", and link the Czech article.

---

## LinkedIn: long

```
Your AI assistant can draft an RFI response and summarize a spec section. Ask it which doors in your model are missing a fire rating, and it guesses. Not because it isn't smart enough, but because it can't open your model.

That gap is closing. The Model Context Protocol, or MCP, is an open standard that connects AI apps to the software engineers already use.

I wanted to know how high the barrier really is. So I built a small read-only MCP server for the model-review software I'm developing and tested it on a concept model of a residential building, checked against an IDS file with 14 information requirements.

The AI called the check and comparison tools, matched the results by element ID and reported that 10 of 13 elements were fixed in the new revision. Then it handed me a link that opened the model with the three remaining doors highlighted. ChatGPT and Gemini reached the same findings through the same server.

MCP doesn't make AI smarter. It makes its answers checkable.

In my new article:
→ what MCP is in AEC terms: an outlet, not a brain
→ why plugging into the AI platforms your team already uses usually beats building another chatbot
→ three kinds of access, what MCP won't fix, and five questions to ask your software vendors before a pilot

📖 Read the article, or 🎧 listen to the podcast episode, where my co-host Sarah brings a practical case and we work through it together:
https://martinmotlik.com/insights/mcp-power-outlet-for-ai/

#AEC #MCP #BIM
```

## LinkedIn: short

```
MCP doesn't make AI smarter. It makes its answers checkable.

Without a connection to your model, an AI assistant guesses. With MCP, it hands the question to a tool engineers already trust, and the answer comes back with element IDs you can check in the model.

I tested this with a read-only MCP server for the model-review software I'm developing. My new article explains what MCP means for AEC, and there's a podcast episode where my co-host Sarah and I work through a practical case.

📖 Read or 🎧 listen:
https://martinmotlik.com/insights/mcp-power-outlet-for-ai/

#AEC #MCP
```

## LinkedIn: first comment (podcast CTA)

```
🎧 Prefer to listen?

This article is also episode 2 of my podcast, Insights with Martin Motlík.

Sarah's boss has forwarded another vendor email: "Should we be doing this MCP thing?" And one of her engineers has already hooked a community Revit server up to ChatGPT, on a live project. We work through her case together: what MCP can do, what still needs checking, and where to start.

Listen here: https://martinmotlik.com/insights/podcast/
Also on Apple Podcasts and Spotify.
```

Shorter alternative:

```
🎧 This article is also a podcast. In episode 2 of Insights with Martin Motlík, Sarah brings a practical case and we work through it together:
https://martinmotlik.com/insights/podcast/
```

## Facebook (Czech)

```
Nový článek na mém webu: co je MCP a proč se bude hodit i ve stavebnictví.

AI asistent dnes zvládne shrnout kapitolu specifikace nebo učesat zápis z porady. Když se ho ale zeptáte, kterým dveřím ve vašem modelu chybí požární odolnost, hádá. Ne proto, že by nebyl dost chytrý, ale protože se do modelu nemá jak dostat. MCP (Model Context Protocol) je otevřený standard, který AI propojí se softwarem, se kterým inženýři už pracují. Funguje jako zásuvka: AI nedělá chytřejší, ale její odpovědi jde ověřit.

Vyzkoušel jsem to sám. K programu na kontrolu modelů IFC, který vyvíjím, jsem postavil MCP server jen pro čtení a otestoval ho s ChatGPT i Gemini. V článku popisuji, co MCP umí, co nevyřeší a jak s ním začít.

Článek si můžete přečíst česky. Podcast, ve kterém téma se Sarah rozebíráme na praktickém případu, je v angličtině.

👉 https://martinmotlik.com/cs/insights/mcp-zasuvka-pro-ai-ve-stavebnictvi/
```

## X

Single post:

```
MCP doesn't make AI smarter. It makes its answers checkable.

I built a read-only MCP server for my model-review software and asked ChatGPT and Gemini the same question about an IFC model. Same findings, same three doors.

New article + podcast:
https://martinmotlik.com/insights/mcp-power-outlet-for-ai/
```

Optional thread (replies under the post above):

```
2/ Without a connection, an AI asked about your model guesses.

With MCP, it calls a tool: the IDS check, the version comparison, the link into the 3D viewer. The answer comes back with element IDs you can check.
```

```
3/ Why plug into ChatGPT, Copilot or Gemini instead of building your own chatbot?

Your team already has them open, and the models keep improving. Keep the engineering tools reusable, then choose the interface.
```

```
4/ The full article, what MCP won't fix, five questions for your software vendors, and the podcast with Sarah:
https://martinmotlik.com/insights/mcp-power-outlet-for-ai/
```

## Threads

```
Your AI assistant can summarize a spec. Ask it which doors in your model are missing a fire rating, and it guesses, because it can't open the model.

MCP changes that. It doesn't make AI smarter. It makes its answers checkable.

I tested it with a read-only server for the model-review software I'm developing and wrote up what I learned. There's a podcast episode too. 🎧

https://martinmotlik.com/insights/mcp-power-outlet-for-ai/
```

## Instagram story

Video teaser from the episode: `tools/ig-story/teasers/ep002-doors.json` (skill `podcast-ig-story`), the episode's opening hook, 0:00–0:14.7.
Link sticker to the article, sticker text **"Read + listen"**, in the white space under the podcast card.

Static fallback, three frames:
1. "Your AI can't open your model. MCP changes that."
2. "What I learned building an MCP server for IFC model review"
3. "New article + podcast 🎧"

## WhatsApp status (video clip from the episode)

Czech:

```
🎧 Nový díl podcastu: co je MCP a proč se bude hodit i ve stavebnictví. Celý díl (v angličtině) najdete tady 👇
https://martinmotlik.com/insights/podcast/
```

English:

```
🎧 Episode 2 is live: what MCP means for AEC, and why your AI assistant still can't open your model. Full episode 👇
https://martinmotlik.com/insights/podcast/
```
