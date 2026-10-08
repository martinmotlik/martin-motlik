# Be the source: getting AEC data ready for AI search

*Insights Podcast, Episode 1 · Martin Motlík with Sarah · 14 min*

Based on the article: https://martinmotlik.com/insights/ai-visibility-for-aec/

## Chapters

- 0:00 Cold open: Sarah's story
- 1:06 "But our SEO works"
- 2:36 The gallery problem
- 4:09 The timber page
- 5:48 The Vancouver twist
- 7:09 Load path, part one
- 8:20 The PDF argument
- 9:43 Load path, part two
- 11:21 What do I tell my boss?
- 12:34 Close

## Transcript

### Cold open: Sarah's story [0:00]

**Sarah** [0:00]: So, a confession. A few weeks ago I opened ChatGPT and typed: "Which structural engineering firms in Portland have real experience with mass timber?"

**Martin** [0:10]: And?

**Sarah** [0:11]: Five firms. Nicely written answer, sources underneath. We weren't one of them. And we've designed, what, a dozen CLT buildings in the last few years.

**Martin** [0:21]: Let me guess. At least one of those five has done less than you.

**Sarah** [0:25]: One of them has done two. I checked.

**Martin** [0:29]: Welcome to Insights. I'm Martin Motlík. I work on websites and content for engineering software, for engineers in the U.S., Canada and Europe. And today I'm joined by Sarah.

**Sarah** [0:41]: Hi, Martin. So, quick context for everyone: I run marketing at a structural engineering firm in Portland. We've done SEO properly for years. Good rankings, clean meta titles, keywords, the whole thing.

**Martin** [0:54]: And the AI still picked someone else.

**Sarah** [0:57]: Right. So that's what I want to understand today. Not the theory. How you would look at my situation.

**Martin** [1:03]: Deal. Let's take it apart.

### "But our SEO works" [1:06]

**Sarah** [1:06]: Okay, the obvious question first. We rank on page one for "structural engineer Portland." Why isn't that enough anymore?

**Martin** [1:15]: Because page one isn't the finish line anymore. Think about what happened when you searched. You didn't get a list. You got an answer. And that's not only ChatGPT. Google itself is an AI search engine now. At Google I/O in May 2026, Google said AI Overviews had passed two and a half billion monthly users, and AI Mode more than a billion. And they're merging the two.

**Sarah** [1:40]: So my clients don't even have to switch to a chatbot.

**Martin** [1:43]: Exactly. The search engine they've used for twenty years quietly became one. And your clients ask the long, specific kind of question. A material, a code, a building type, a city. That's exactly the kind of search that now gets an answer instead of a list.

**Sarah** [2:00]: So... was all our SEO work wasted?

**Martin** [2:03]: No, and I want to be clear about that. SEO is still the foundation. If a page can't be crawled and indexed, it won't end up in an AI answer either. What changed is the goal. Alongside rankings, I now look at whether a page gets cited as a source. And a meta description won't get you cited. It was written for a person scanning a list.

**Sarah** [2:24]: And the AI doesn't scan.

**Martin** [2:26]: No. It reads your page, pulls out individual facts, and decides which ones it trusts enough to repeat. Keywords help it find you. They don't make it trust you.

### The gallery problem [2:36]

**Sarah** [2:36]: So how would you start with us? If I hired you tomorrow.

**Martin** [2:40]: I'd ask you a slightly annoying question. Where on your website does it say, in plain text, that you've designed a dozen CLT buildings? To which code? In which cities?

**Sarah** [2:52]: Um... it's in the projects section. We have a gallery. Really beautiful photography.

**Martin** [2:59]: With captions?

**Sarah** [3:00]: A project name. Sometimes the architect.

**Martin** [3:02]: That's the most common thing I see with engineering firms. A gallery convinces a person. But a machine can't look at a photo of a timber roof and conclude, "this firm designs CLT to NDS." For an AI system, that expertise basically doesn't exist.

**Sarah** [3:19]: So the competitor with two projects...

**Martin** [3:22]: ...probably wrote two plain pages. The project, the structural system, the material, the design code, and what their role was. That's enough to be quotable.

**Sarah** [3:33]: Okay, that honestly stings a little.

**Martin** [3:36]: It's very fixable. And it's the same lesson I learned from localization, long before anyone talked about AI search.

**Sarah** [3:44]: Tell me about that. That's your daily work, right?

**Martin** [3:47]: Since 2021, yeah. Websites and content for engineering software, adapted for the U.S., Canada and Europe. And what localization teaches you is this: translating a page is easy. Localizing it means asking how an engineer in that market actually searches. Which code they use, which terms, which spelling.

### The timber page [4:09]

**Sarah** [4:09]: Do you have an example?

**Martin** [4:10]: One that's actually very close to your world. A timber design page I optimized for engineers in the U.S. and Canada, for a software vendor. The original content came from Europe. Accurate, thorough... and it spoke Eurocode.

**Sarah** [4:26]: Nobody in Portland thinks in Eurocode.

**Martin** [4:30]: Not in Portland, not in Vancouver. They design to NDS in the U.S. and CSA O86 in Canada, and that's how they phrase their questions. So I rebuilt the page around the engineer's question, not around the product. The North American codes are named right in the text. U.S. English, U.S. terms, "design standards" as the umbrella. Nobody, human or machine, has to translate from one standards world to the other.

**Sarah** [5:00]: And the images? Because that's my gallery problem, right?

**Martin** [5:04]: Same thing exactly. A screenshot of a model checked to Eurocode, with European labels, tells an engineer this was made for someone else. So we localized the screenshots too. And every image got text: a title, alt text, a description and a caption that name the standard. The image convinces the engineer. The text around it is what a machine can quote.

**Sarah** [5:29]: So for me, every project photo gets a caption that says the system, the code, and what we actually did.

**Martin** [5:36]: That's it. Write in the language of the question. If your pages never say "NDS," you won't be named when someone asks about NDS. No matter how many buildings you've done.

### The Vancouver twist [5:48]

**Sarah** [5:48]: Here's a twist, though. We also have an office in Vancouver. And our site shows Canadian visitors different content, based on their location.

**Martin** [5:57]: Ah. That's something I work with every day, actually. One page, one URL, and visitors from France, Italy, Germany or the U.S. each see content for their market. Local contacts, language, the design standards they use. For people, it works really well.

**Sarah** [6:17]: I'm sensing a "but."

**Martin** [6:20]: But a crawler only sees the version served to its own IP address. Googlebot crawls from U.S. addresses by default, and AI crawlers largely do too. So your Vancouver content, all the CSA O86 projects...

**Sarah** [6:36]: ...might never reach an AI answer.

**Martin** [6:39]: Unless you plan for it. The fix is simple in principle. Keep the IP localization for the experience. But give every regional version of an important fact its own URL, linked with hreflang. Visitors still land on the right version automatically, and crawlers can find all of them.

**Sarah** [6:59]: That would never have shown up in our SEO reports.

**Martin** [7:02]: Usually not. Which is why I stopped counting pages when I review a website.

**Sarah** [7:07]: What do you count instead?

### Load path, part one [7:09]

**Martin** [7:09]: I follow single facts. Like yours: "we design CLT buildings to NDS." And I check whether that one fact survives the trip from your server into an AI answer. I think of it as a load path.

**Sarah** [7:24]: Of course you do.

**Martin** [7:26]: Occupational hazard. But it works. There are five members, and the fact has to make it through every one. The first is: is it reachable? Do your robots rules and your firewall actually let AI crawlers in?

**Sarah** [7:40]: Okay, now I'm nervous. Our IT guy told me last year he blocked "the AI bots." Because of the training thing.

**Martin** [7:48]: That's really common, and it's worth checking exactly what he blocked. Training bots and search bots are separate. You can opt out of model training and still let ChatGPT search and Claude search read your site. And if he blocked everything at the CDN level, your robots rules don't even matter.

**Sarah** [8:07]: So that alone could explain it.

**Martin** [8:10]: It could. Second member: is the fact readable? Is it in the HTML, or is it locked in a PDF, an image, or something a script renders?

### The PDF argument [8:20]

**Sarah** [8:20]: Well... our statement of qualifications is a PDF. It's gorgeous. And honestly, clients download it. I'm not getting rid of it.

**Martin** [8:30]: And you shouldn't. I'm not anti-PDF.

**Sarah** [8:33]: It kind of sounded like you were.

**Martin** [8:35]: Fair. Here's the distinction. Keep the PDF. Just never let it be the only place a fact lives. My rule is that HTML is the source of truth. PDFs, images and videos are copies of it. Text inside PDFs reaches AI crawlers unreliably at best.

**Sarah** [8:57]: Okay, I can live with that. What about JavaScript? Our new site is built on one of those modern frameworks.

**Martin** [9:03]: Then that's the first thing I'd test. Many modern frameworks can render the page on the server, and then you're fine. The only question is whether the text is in the HTML before any script runs. Because according to crawl data from Vercel and MERJ, the major AI crawlers don't execute JavaScript at all. Google does. So a page can rank in Google, show up in AI Overviews, and still be completely empty to ChatGPT, Claude and Perplexity.

**Sarah** [9:33]: Wait. So we could be invisible to them and never notice, because Google looks fine.

**Martin** [9:39]: Right. Google looks fine, so nobody thinks to check.

### Load path, part two [9:43]

**Sarah** [9:43]: Okay, reachable, readable. What are the other three?

**Martin** [9:47]: Third: understood. The page says plainly what it's about. The service, the design code, the units, the market. Fourth: consistent. Every page, every file, every listing states the fact the same way.

**Sarah** [10:03]: Hm. We say "mass timber" on the homepage, "CLT" on the project pages, and a couple of directory listings still have our old office address.

**Martin** [10:14]: That's the kind of thing that quietly weakens trust. My rule there is one fact, one canonical page. State it there clearly, and identically everywhere else. And if you use structured data, the markup never says more than the visible page. Markup that contradicts the page doesn't fix confusion. It automates it.

**Sarah** [10:35]: And the fifth?

**Martin** [10:36]: Corroborated. Others confirm it. Clients, architects you work with, publications, conference talks. And like any load path, it fails at its weakest member. In my experience, the first two fail far more often than people expect.

**Sarah** [10:52]: Any rule for how we should actually write the pages?

**Martin** [10:55]: Answer first. Lead with the answer and make every passage stand on its own. AI systems quote passages, not whole pages.

**Sarah** [11:04]: And llms.txt? Half my LinkedIn feed says I need one.

**Martin** [11:09]: On documentation and API sites, it makes sense. On a marketing site, it's a cheap experiment at best, and Google says its Search ignores it. Fix crawlability first.

### What do I tell my boss? [11:21]

**Sarah** [11:21]: Practical question. My boss is going to ask how we know any of this is working. What do I report?

**Martin** [11:27]: Keep reporting rankings. But add the test you already did by accident. Take ten real questions your clients ask. Put them into Google's AI Mode, ChatGPT, Claude and Perplexity. Write down whether you're named, how you're described, and whom the answers cite instead.

**Sarah** [11:46]: And repeat it in a few months.

**Martin** [11:48]: Yes. Same questions, same tools. That's your baseline. And that last part, who gets cited instead, is usually the wake-up call.

**Sarah** [11:57]: What else can I do this week, without an agency?

**Martin** [12:01]: Two more checks. First, fetch one key page the way a crawler does. No browser, no JavaScript. Then search the result for a sentence that matters, like "CLT" or "NDS." If it's not there, AI crawlers can't see it either. The exact command is in the article. Second, read every robots file you own, including subdomains, and ask whoever runs your CDN whether AI bots are blocked.

**Sarah** [12:28]: So, basically: talk to my IT guy.

**Martin** [12:31]: Talk to your IT guy. Nicely.

### Close [12:34]

**Sarah** [12:34]: If you had to pick one thing for me to start with on Monday?

**Martin** [12:38]: One page. Your strongest mass timber project. Rewrite it so it plainly states the structural system, the material, the design code, the location and your role. Make sure that text is in the HTML. Then make sure your other pages say the same thing.

**Sarah** [12:57]: That's... surprisingly doable.

**Martin** [12:59]: That's the good news. Most AEC companies already own the material. Project pages, datasheets, references, documentation. It's not new content. It's the content you have, made readable.

**Sarah** [13:15]: And the bigger picture?

**Martin** [13:16]: Make the technical facts your clients need easy to find, understand and verify. Be explicit about what you do, which standards apply, which markets you serve, and where your limits are.

**Sarah** [13:29]: So, my list. Captions on every project. A friendly talk with my IT guy. The PDF stays, but the facts go into HTML. And one name for what we do, not "mass timber" here and "CLT" there.

**Martin** [13:45]: That's the whole episode in one sentence.

**Sarah** [13:49]: The full article, with the checklist and a copy-paste robots file, is on martinmotlik.com, under Insights.

**Martin** [13:56]: And if you're working on something similar, regional content, technical documentation, AI visibility, message me on LinkedIn. I'm always happy to compare notes.

**Sarah** [14:06]: Thanks for listening.

**Martin** [14:07]: See you in the next one.
