# Insights Podcast – Episode 1 (v2)
## "Be the source: getting AEC data ready for AI search"

**Format:** Two-voice dialogue · U.S. English · ~14 minutes · ~11,865 characters in 10 scenes
**Speakers:**
- **MARTIN:** the expert. Your Professional Voice Clone, about 73 % of the speaking time.
- **SARAH:** co-host (AI voice from the Voice Library). On air she is the marketing lead at a structural engineering firm in Portland (offices in Portland and Vancouver, a dozen CLT projects). She has done SEO for years, yet ChatGPT names her competitors and not her firm. Her case runs through the whole episode, and she keeps asking how Martin sees it.

**Source article:** https://martinmotlik.com/insights/ai-visibility-for-aec/

**Sarah's story arc**
1. ChatGPT doesn't name her firm, but it names a competitor with two projects.
2. "But our SEO works." Martin explains what changed.
3. Her project gallery has no text, which is why her expertise doesn't exist for AI.
4. Martin's timber page shows how to fix it: captions and the language of the question.
5. Her Vancouver office and IP localization.
6. Her IT blocked "the AI bots."
7. She defends her PDF; Martin explains the PDF as a copy, not the source.
8. Inconsistent terms and an old address.
9. What she reports to her boss.
10. Her plan for Monday.

---

## Production notes

**Sarah – voice casting (Voice Library, not Voice Design)**
- Female, General American accent, early-to-mid 30s, warm, curious, quick, a little dry humor.
- Clearly different from your timbre. Search terms: *"conversational female American podcast"*, *"warm professional narrator"*.
- Test her with your clone on Scene 3 (the gallery problem). It has the most natural back-and-forth.
- Keep the same voice for future episodes. Sarah becomes a recurring character.

**Model & settings**
- Text to Dialogue, **Eleven v4** (compare one scene against v3 with your clone first).
- Stability around the middle. Similarity high for MARTIN.
- One scene = one request (every scene is under 2,000 characters). Generate 2–3 takes per scene and pick the best.
- Audio tags in [brackets] are deliberate and sparse. Don't add more.

**Pronunciation (already spelled out in the script)**
| In the article | In the script |
|---|---|
| CSA O86 | CSA O-eighty-six |
| hreflang | H-ref-lang |
| MERJ | Merj |
| martinmotlik.com | martinmotlik dot com |
| Motlík | Check the first take. If wrong, try "MOT-leek". |

**Post-production**
- Join scenes with 0.4–0.8 s gaps. Optional 3–5 s music sting between the cold open and "Welcome to Insights" (split Scene 1 there).
- Normalize to about −16 LUFS (stereo) and export MP3 at 128–192 kbps.

**Disclosure (recommended, not on air in the conversation)**
- Under the player: *"Audio produced with AI voices, based on this article."*
- Optional 2–3 s tag before or after the sting: *"Produced with AI voices."* (EU AI Act Art. 50 asks for audio disclosure at the beginning; see note in chat.)

**Web:** Publish the dialogue as an HTML transcript under the player (the script below, without tags), plus PodcastEpisode/AudioObject structured data.

---

## Script


### Scene 1 · Sarah's story
*958 characters*
**SARAH:** So, a confession. A few weeks ago I opened ChatGPT and typed: "Which structural engineering firms in Portland have real experience with mass timber?"

**MARTIN:** And?

**SARAH:** Five firms. Nicely written answer, sources underneath. We weren't one of them. And we've designed, what, a dozen CLT buildings in the last few years.

**MARTIN:** Let me guess. At least one of those five has done less than you.

**SARAH:** [laughs] One of them has done two. I checked.

**MARTIN:** [warmly] Welcome to Insights. I'm Martin Motlík. I work on websites and content for engineering software, for engineers in the U.S., Canada and Europe. And today I'm joined by Sarah.

**SARAH:** Hi, Martin. So, quick context for everyone: I run marketing at a structural engineering firm in Portland. We've done SEO properly for years. Good rankings, clean meta titles, keywords, the whole thing.

**MARTIN:** And the AI still picked someone else.

**SARAH:** Right. So that's what I want to understand today. Not the theory. How you would look at my situation.

**MARTIN:** Deal. Let's take it apart.


---

### Scene 2 · "But our SEO works"
*1349 characters*
**SARAH:** Okay, the obvious question first. We rank on page one for "structural engineer Portland." Why isn't that enough anymore?

**MARTIN:** Because page one isn't the finish line anymore. Think about what happened when you searched. You didn't get a list. You got an answer. And that's not only ChatGPT. Google itself is an AI search engine now. At Google I/O in May 2026, Google said AI Overviews had passed two and a half billion monthly users, and AI Mode more than a billion. And they're merging the two.

**SARAH:** So my clients don't even have to switch to a chatbot.

**MARTIN:** Exactly. The search engine they've used for twenty years quietly became one. And your clients ask the long, specific kind of question. A material, a code, a building type, a city. That's exactly the kind of search that now gets an answer instead of a list.

**SARAH:** So... was all our SEO work wasted?

**MARTIN:** No, and I want to be clear about that. SEO is still the foundation. If a page can't be crawled and indexed, it won't end up in an AI answer either. What changed is the goal. Alongside rankings, I now look at whether a page gets cited as a source. And a meta description won't get you cited. It was written for a person scanning a list.

**SARAH:** And the AI doesn't scan.

**MARTIN:** No. It reads your page, pulls out individual facts, and decides which ones it trusts enough to repeat. Keywords help it find you. They don't make it trust you.


---

### Scene 3 · The gallery problem
*1313 characters*
**SARAH:** So how would you start with us? If I hired you tomorrow.

**MARTIN:** I'd ask you a slightly annoying question. Where on your website does it say, in plain text, that you've designed a dozen CLT buildings? To which code? In which cities?

**SARAH:** Um... it's in the projects section. We have a gallery. Really beautiful photography.

**MARTIN:** With captions?

**SARAH:** A project name. Sometimes the architect.

**MARTIN:** That's the most common thing I see with engineering firms. A gallery convinces a person. But a machine can't look at a photo of a timber roof and conclude, "this firm designs CLT to NDS." For an AI system, that expertise basically doesn't exist.

**SARAH:** So the competitor with two projects...

**MARTIN:** ...probably wrote two plain pages. The project, the structural system, the material, the design code, and what their role was. That's enough to be quotable.

**SARAH:** Okay, that honestly stings a little.

**MARTIN:** [gently] It's very fixable. And it's the same lesson I learned from localization, long before anyone talked about AI search.

**SARAH:** Tell me about that. That's your daily work, right?

**MARTIN:** Since 2021, yeah. Websites and content for engineering software, adapted for the U.S., Canada and Europe. And what localization teaches you is this: translating a page is easy. Localizing it means asking how an engineer in that market actually searches. Which code they use, which terms, which spelling.


---

### Scene 4 · The timber page
*1392 characters*
**SARAH:** Do you have an example?

**MARTIN:** One that's actually very close to your world. A timber design page I optimized for engineers in the U.S. and Canada, for a software vendor. The original content came from Europe. Accurate, thorough... and it spoke Eurocode.

**SARAH:** [laughs] Nobody in Portland thinks in Eurocode.

**MARTIN:** Not in Portland, not in Vancouver. They design to NDS in the U.S. and CSA O-eighty-six in Canada, and that's how they phrase their questions. So I rebuilt the page around the engineer's question, not around the product. The North American codes are named right in the text. U.S. English, U.S. terms, "design standards" as the umbrella. Nobody, human or machine, has to translate from one standards world to the other.

**SARAH:** And the images? Because that's my gallery problem, right?

**MARTIN:** Same thing exactly. A screenshot of a model checked to Eurocode, with European labels, tells an engineer this was made for someone else. So we localized the screenshots too. And every image got text: a title, alt text, a description and a caption that name the standard. The image convinces the engineer. The text around it is what a machine can quote.

**SARAH:** So for me, every project photo gets a caption that says the system, the code, and what we actually did.

**MARTIN:** That's it. Write in the language of the question. If your pages never say "NDS," you won't be named when someone asks about NDS. No matter how many buildings you've done.


---

### Scene 5 · The Vancouver twist
*1099 characters*
**SARAH:** Here's a twist, though. We also have an office in Vancouver. And our site shows Canadian visitors different content, based on their location.

**MARTIN:** Ah. That's something I work with every day, actually. One page, one URL, and visitors from France, Italy, Germany or the U.S. each see content for their market. Local contacts, language, the design standards they use. For people, it works really well.

**SARAH:** I'm sensing a "but."

**MARTIN:** [chuckles] But a crawler only sees the version served to its own IP address. Googlebot crawls from U.S. addresses by default, and AI crawlers largely do too. So your Vancouver content, all the CSA O-eighty-six projects...

**SARAH:** ...might never reach an AI answer.

**MARTIN:** Unless you plan for it. The fix is simple in principle. Keep the IP localization for the experience. But give every regional version of an important fact its own URL, linked with H-ref-lang. Visitors still land on the right version automatically, and crawlers can find all of them.

**SARAH:** That would never have shown up in our SEO reports.

**MARTIN:** Usually not. Which is why I stopped counting pages when I review a website.

**SARAH:** What do you count instead?


---

### Scene 6 · Load path, part one
*982 characters*
**MARTIN:** I follow single facts. Like yours: "we design CLT buildings to NDS." And I check whether that one fact survives the trip from your server into an AI answer. I think of it as a load path.

**SARAH:** [laughs] Of course you do.

**MARTIN:** Occupational hazard. But it works. There are five members, and the fact has to make it through every one. The first is: is it reachable? Do your robots rules and your firewall actually let AI crawlers in?

**SARAH:** Okay, now I'm nervous. Our IT guy told me last year he blocked "the AI bots." Because of the training thing.

**MARTIN:** That's really common, and it's worth checking exactly what he blocked. Training bots and search bots are separate. You can opt out of model training and still let ChatGPT search and Claude search read your site. And if he blocked everything at the CDN level, your robots rules don't even matter.

**SARAH:** So that alone could explain it.

**MARTIN:** It could. Second member: is the fact readable? Is it in the HTML, or is it locked in a PDF, an image, or something a script renders?


---

### Scene 7 · The PDF argument
*1131 characters*
**SARAH:** Well... our statement of qualifications is a PDF. It's gorgeous. And honestly, clients download it. I'm not getting rid of it.

**MARTIN:** And you shouldn't. I'm not anti-PDF.

**SARAH:** It kind of sounded like you were.

**MARTIN:** [laughs] Fair. Here's the distinction. Keep the PDF. Just never let it be the only place a fact lives. My rule is that HTML is the source of truth. PDFs, images and videos are copies of it. Text inside PDFs reaches AI crawlers unreliably at best.

**SARAH:** Okay, I can live with that. What about JavaScript? Our new site is built on one of those modern frameworks.

**MARTIN:** Then that's the first thing I'd test. Many modern frameworks can render the page on the server, and then you're fine. The only question is whether the text is in the HTML before any script runs. Because according to crawl data from Vercel and Merj, the major AI crawlers don't execute JavaScript at all. Google does. So a page can rank in Google, show up in AI Overviews, and still be completely empty to ChatGPT, Claude and Perplexity.

**SARAH:** [surprised] Wait. So we could be invisible to them and never notice, because Google looks fine.

**MARTIN:** Right. Google looks fine, so nobody thinks to check.


---

### Scene 8 · Load path, part two
*1339 characters*
**SARAH:** Okay, reachable, readable. What are the other three?

**MARTIN:** Third: understood. The page says plainly what it's about. The service, the design code, the units, the market. Fourth: consistent. Every page, every file, every listing states the fact the same way.

**SARAH:** Hm. We say "mass timber" on the homepage, "CLT" on the project pages, and a couple of directory listings still have our old office address.

**MARTIN:** That's the kind of thing that quietly weakens trust. My rule there is one fact, one canonical page. State it there clearly, and identically everywhere else. And if you use structured data, the markup never says more than the visible page. Markup that contradicts the page doesn't fix confusion. It automates it.

**SARAH:** And the fifth?

**MARTIN:** Corroborated. Others confirm it. Clients, architects you work with, publications, conference talks. And like any load path, it fails at its weakest member. In my experience, the first two fail far more often than people expect.

**SARAH:** Any rule for how we should actually write the pages?

**MARTIN:** Answer first. Lead with the answer and make every passage stand on its own. AI systems quote passages, not whole pages.

**SARAH:** And llms.txt? Half my LinkedIn feed says I need one.

**MARTIN:** [chuckles] On documentation and API sites, it makes sense. On a marketing site, it's a cheap experiment at best, and Google says its Search ignores it. Fix crawlability first.


---

### Scene 9 · What do I tell my boss?
*1014 characters*
**SARAH:** Practical question. My boss is going to ask how we know any of this is working. What do I report?

**MARTIN:** Keep reporting rankings. But add the test you already did by accident. Take ten real questions your clients ask. Put them into Google's AI Mode, ChatGPT, Claude and Perplexity. Write down whether you're named, how you're described, and whom the answers cite instead.

**SARAH:** And repeat it in a few months.

**MARTIN:** Yes. Same questions, same tools. That's your baseline. And that last part, who gets cited instead, is usually the wake-up call.

**SARAH:** What else can I do this week, without an agency?

**MARTIN:** Two more checks. First, fetch one key page the way a crawler does. No browser, no JavaScript. Then search the result for a sentence that matters, like "CLT" or "NDS." If it's not there, AI crawlers can't see it either. The exact command is in the article. Second, read every robots file you own, including subdomains, and ask whoever runs your CDN whether AI bots are blocked.

**SARAH:** So, basically: talk to my IT guy.

**MARTIN:** [laughs] Talk to your IT guy. Nicely.


---

### Scene 10 · Close
*1288 characters*
**SARAH:** If you had to pick one thing for me to start with on Monday?

**MARTIN:** One page. Your strongest mass timber project. Rewrite it so it plainly states the structural system, the material, the design code, the location and your role. Make sure that text is in the HTML. Then make sure your other pages say the same thing.

**SARAH:** That's... surprisingly doable.

**MARTIN:** That's the good news. Most AEC companies already own the material. Project pages, datasheets, references, documentation. It's not new content. It's the content you have, made readable.

**SARAH:** And the bigger picture?

**MARTIN:** Make the technical facts your clients need easy to find, understand and verify. Be explicit about what you do, which standards apply, which markets you serve, and where your limits are.

**SARAH:** So, my list. Captions on every project. A friendly talk with my IT guy. The PDF stays, but the facts go into HTML. And one name for what we do, not "mass timber" here and "CLT" there.

**MARTIN:** [chuckles] That's the whole episode in one sentence.

**SARAH:** The full article, with the checklist and a copy-paste robots file, is on martinmotlik dot com, under Insights.

**MARTIN:** And if you're working on something similar, regional content, technical documentation, AI visibility, message me on LinkedIn. I'm always happy to compare notes.

**SARAH:** Thanks for listening.

**MARTIN:** [warmly] See you in the next one.


---