# A Power Outlet for AI: What MCP Means for AEC

*Insights Podcast, Episode 2 · Martin Motlík with Sarah · 14 min*

Based on the article: https://martinmotlik.com/insights/mcp-power-outlet-for-ai/

## Chapters

- 0:00 The doors that don't exist
- 0:21 Welcome
- 0:57 An outlet, not a brain
- 2:19 Guessing vs. checking
- 3:49 "Have you actually tried it?"
- 5:36 Thirteen elements, three doors
- 6:52 One server, two AI apps
- 8:03 "Why give our data to big tech?"
- 9:25 The weekend GitHub server
- 10:50 Who's actually shipping this?
- 11:43 What do I tell my boss?
- 13:09 Close

## Transcript

### The doors that don't exist [0:00]

**Martin** [0:00]: Imagine asking an AI which doors are missing a fire rating. It gives you a perfect table. There's just one problem: none of those doors exist in your model.

**Sarah** [0:11]: Then how do you get an answer you can actually check?

### Welcome [0:21]

**Martin** [0:21]: Welcome back to Insights. I'm Martin Motlík. I work where software meets structural engineering. Today we're looking at the Model Context Protocol, or MCP, through a model-review test I built myself.

**Martin** [0:36]: Sarah is back as our fictional marketing lead at an engineering firm in Portland. Her boss has a question.

**Sarah** [0:43]: He's forwarded another vendor email: "Should we be doing this MCP thing?" I need an answer I can take back to the team.

**Martin** [0:51]: Let's work through it. What can it do, what still needs checking, and where would you start?

### An outlet, not a brain [0:57]

**Sarah** [0:57]: Okay, start from zero. What is it?

**Martin** [1:00]: MCP is an open standard that lets AI apps connect to the software and data you already use. It doesn't make the AI smarter. It gives it a way to reach things outside itself. Your models, your analysis software, your project data.

**Sarah** [1:17]: So, a plug.

**Martin** [1:18]: Pretty much. Picture the temporary power spider box on a jobsite. It doesn't care if you plug in a saw, a grinder or a work light, because every tool has the same plug. Before MCP, connecting an AI to a program meant custom wiring for every single pair.

**Sarah** [1:35]: And now?

**Martin** [1:36]: Now software can expose its tools through an MCP server, and compatible AI apps can connect to it. You still need the right connection and permissions. Anthropic introduced the standard in late 2024.

**Sarah** [1:49]: We pay for Copilot. So in that picture, Copilot is...

**Martin** [1:54]: The host. The app you type into. On the other side, a small server sits next to Revit, or next to the tool that reads your IFC files, and tells the AI what it can do.

**Sarah** [2:05]: Tells it how?

**Martin** [2:06]: Each tool has a description and a structured definition of its inputs. The AI uses those to choose a tool and supply the information it needs. The application controls which tools are available.

### Guessing vs. checking [2:19]

**Sarah** [2:19]: So back to the doors. What would have been different?

**Martin** [2:22]: The AI would have a way to query the actual model. A tool can open the IFC file, find the doors and return their properties. We can check those results. The AI can still choose the wrong filter or misread an answer, so the connection alone doesn't make it reliable.

**Sarah** [2:41]: So the AI is more of a coordinator.

**Martin** [2:44]: Exactly. Like a good BIM coordinator, actually. It doesn't author the model. It knows where to look, and it brings back the answer.

**Sarah** [2:53]: But here's the thing. Copilot already reads our documents. Our BIM Execution Plan, our standards. Isn't that the same?

**Martin** [3:01]: That's a different tool, and a good one. The AI searches documents and quotes them. It answers "what does the BIM Execution Plan say?"

**Sarah** [3:10]: And MCP?

**Martin** [3:12]: MCP can connect both kinds of tools. One searches your documents; another queries the model or runs a check. The useful difference is what the tool can do. Most serious workflows will use both.

**Sarah** [3:25]: Give me something real. What would our team actually ask?

**Martin** [3:29]: Find the doors on level two with a missing fire-rating property, and show me where they are. Or total the concrete quantities in the slabs, floor by floor, if the model contains reliable quantities. Those are questions the connected tools can answer.

**Sarah** [3:45]: And the doors would have been real doors.

### "Have you actually tried it?" [3:49]

**Sarah** [3:49]: Can I be honest? Everything I read about this is a vendor demo. Have you actually tried it yourself?

**Martin** [3:56]: I have. I'm building a model-review prototype, a web app for IFC models. It already checks models against information requirements and compares versions. So I wrote a small MCP server for it. Six tools, all read-only.

**Sarah** [4:13]: Read-only meaning...

**Martin** [4:15]: It can look, it can't touch. List elements, read their properties, run a check, compare two revisions, and hand me a link into the 3D viewer. That's it.

**Sarah** [4:26]: But couldn't your model checker already do that without AI?

**Martin** [4:29]: Yes. The checker already did the validation. What I added was a way to ask follow-up questions, connect the steps, and jump straight to the affected elements.

**Sarah** [4:39]: And what did you test it on?

**Martin** [4:41]: A real model. A residential building in Prague, a concept model with a garage, three apartment floors and an attic. Plus an IDS file with the project's data requirements.

**Sarah** [4:53]: IDS. Remind me?

**Martin** [4:56]: IDS is a buildingSMART standard for expressing selected information requirements in a machine-checkable form. You specify which elements need which data. A checker then tests the model against those rules. It checks the information, not whether the building is correctly designed.

**Sarah** [5:14]: Oh. That's literally what our BIM coordinator does every Friday before a submittal. By hand.

**Martin** [5:21]: Then she'll like this part. I asked: check the model against the IDS file. Which requirements fail, and which elements are affected? Two requirements failed. Thirteen elements, mostly doors without a fire rating.

### Thirteen elements, three doors [5:36]

**Sarah** [5:36]: Doors with no fire rating. That sounds bad.

**Martin** [5:40]: The door names said the fire rating would be set in the fire safety design. That explained why the value was missing. It didn't actually provide a fire rating.

**Sarah** [5:50]: So the check found a real gap, but it didn't tell you whether the design was wrong.

**Martin** [5:55]: Exactly. You also need to know whether that information is required at this project stage. The check flags the missing value. A person decides what it means.

**Sarah** [6:06]: Then what?

**Martin** [6:07]: Then I prepared a second revision for the test, with some of the gaps filled in. And I asked the question every team asks after a revision: what got fixed, and what's still missing? Show me the rest in the model.

**Sarah** [6:21]: And?

**Martin** [6:22]: The AI called the comparison and validation tools, and the results were matched by element ID. Ten of thirteen fixed. Three doors on residential level three still without a fire rating. Then it gave me a link that opened the model, and there they were. Three doors highlighted, the rest of the building dimmed.

**Sarah** [6:41]: So the doors in the chat and the doors on screen are the same doors.

**Martin** [6:46]: Same element IDs. That's the part I'd show any project team first.

### One server, two AI apps [6:52]

**Sarah** [6:52]: Okay, but which AI did you use? We're a Copilot shop.

**Martin** [6:57]: I tested the same server with ChatGPT and with Gemini in Google Antigravity. In that test, both reached the same findings. That doesn't mean every AI app connects in the same way. With Copilot, you need to check the specific product and your company's setup.

**Sarah** [7:15]: Was building the server the hard part?

**Martin** [7:17]: Writing the code wasn't the hard part.

**Sarah** [7:19]: What was?

**Martin** [7:20]: Three things. First, the tool descriptions. The AI picks tools by reading them, so they're really the user interface. They deserve the same care as button labels.

**Sarah** [7:31]: Copywriting. Finally something in my lane.

**Martin** [7:35]: Honestly, yes. Second, summaries beat data dumps. Return counts and the top results, with details on request. Send an AI a whole model and you overload its working memory. The answers get worse.

**Sarah** [7:50]: And third?

**Martin** [7:51]: Units and IDs, always. Every number carries its unit, every element its ID. Ambiguity is exactly where the AI starts guessing again.

### "Why give our data to big tech?" [8:03]

**Sarah** [8:03]: Here's where I push back a bit. Why would we connect our projects to OpenAI or Google or Microsoft? Wouldn't it be safer to build our own chatbot?

**Martin** [8:13]: Fair question. Let me separate two things: where the model lives, and where the answers go. A local server keeps the model file on your machine. Only what the tools return goes to the AI.

**Sarah** [8:27]: Which can still be a lot.

**Martin** [8:29]: It can. So check your provider's terms on data retention and training before you connect live projects. And some clients and contracts don't allow commercial AI services at all. Then you don't.

**Sarah** [8:43]: Okay. And the chatbot idea?

**Martin** [8:45]: Building your own chatbot doesn't mean building your own language model. You can use the same commercial models behind a custom interface. The question is whether that interface solves a real problem for your team. MCP lets you reuse the engineering tools either way.

**Sarah** [9:03]: And my engineers already have Copilot open all day.

**Martin** [9:07]: Then it makes sense to start with the interface they already use, if it supports the connection you need. A custom assistant may still be useful for a specific workflow.

**Sarah** [9:17]: So it's not either-or.

**Martin** [9:19]: No. Keep the engineering tools reusable, then choose the interface that works for your team.

### The weekend GitHub server [9:25]

**Sarah** [9:25]: Okay, confession number two. One of our younger engineers found a community Revit server on GitHub and hooked it up to ChatGPT over the weekend. On a live project.

**Martin** [9:38]: Of course he did.

**Sarah** [9:39]: Our IT guy is not amused.

**Martin** [9:42]: Your IT guy has a point. I separate three kinds of access. First, reading: querying the model and pulling properties. That limits changes to the model, but the information can still be sensitive.

**Sarah** [9:56]: And the second?

**Martin** [9:57]: Checking: IDS checks, clash reports, comparisons between revisions. People need to review the findings because they inform decisions. Third is writing: changing parameters or moving and creating elements. That needs controlled permissions and a way to review and undo changes.

**Sarah** [10:16]: And the GitHub server?

**Martin** [10:18]: You need to inspect what that particular server can do and what access it has. Autodesk now offers separate read, write and experimental server options as technical previews. The capabilities and permissions matter more than the label.

**Sarah** [10:32]: Anything else I should tell IT?

**Martin** [10:34]: Model data can contain text that tries to steer the AI. Read-only limits changes to the model; it doesn't prevent misleading answers or data exposure. Start with a trusted server, restricted access and a test model your firm has approved.

### Who's actually shipping this? [10:50]

**Sarah** [10:50]: Who is actually shipping this in our industry?

**Martin** [10:53]: Autodesk has Revit servers in technical preview. Bluebeam connects Revu with Claude. Trimble has a SketchUp connector, and Dlubal provides access to its analysis applications. The capabilities, supported clients and licenses differ. But these are actual products you can evaluate.

**Sarah** [11:14]: Do they all give the AI the same kind of access?

**Martin** [11:17]: No. Some expose a few defined actions. Others let the AI write scripts against an API. The reach depends on what the server exposes and the permissions behind it.

**Sarah** [11:29]: Which would you start with?

**Martin** [11:31]: A small set of read-only tools for one task. Scripting can go further, but you need to review and test the code. I've linked the product details in the article, because those are changing quickly.

### What do I tell my boss? [11:43]

**Sarah** [11:43]: Okay. That email from my boss. And our senior engineer asked me to ask you one thing: who's liable if the AI gets it wrong?

**Martin** [11:53]: Using AI doesn't remove the engineer's responsibility to review the result. The AI doesn't stamp drawings. How liability is allocated is a separate question for the firm's contracts and legal advice.

**Sarah** [12:07]: So we still need a review process. What else do I write back?

**Martin** [12:12]: That it won't clean up your data. It automates a messy process just as faithfully as a clean one. If your parameters are inconsistent, you'll just find out faster. And that it isn't free. AI subscriptions, and sometimes API access or add-on licenses on the software side.

**Sarah** [12:30]: And then?

**Martin** [12:31]: Then a few questions for every vendor. Do you ship an MCP server, official or community? Is it read-only, and are read and write separated? Where does project data go? The full list is in the article.

**Sarah** [12:44]: And how do we know if it's worth it?

**Martin** [12:46]: Choose one recurring task and a test model your firm has approved. Compare your current workflow, including any checker you already use, with the AI-assisted version. Count the review time, missed issues and false alarms as well as the time saved. Repeat it on another revision before deciding.

**Sarah** [13:04]: That's our Friday model check.

**Martin** [13:06]: That's your Friday model check.

### Close [13:09]

**Sarah** [13:09]: If you had to sum it up in one sentence?

**Martin** [13:12]: MCP lets AI reach the engineering tools we already use. We still need to verify the result.

**Sarah** [13:20]: And personally? Would you share your own models with these AI companies?

**Martin** [13:25]: I would. Sharing building data with AI models is how they get better at our work, and I trust the large U.S. providers with it. Your contracts still set the rules for each project. In a few years, asking an AI about a model will be as ordinary as searching Google.

**Sarah** [13:42]: And the first question to take back to the office?

**Martin** [13:44]: Pick one question you ask about a model every week. Check whether your existing software can expose the answer, and how your team would verify it.

**Sarah** [13:53]: In the article, you can see the tool result and the same three doors highlighted in the model. It's on martinmotlik.com, under Insights.

**Martin** [14:01]: Thanks for listening. See you in the next one.
