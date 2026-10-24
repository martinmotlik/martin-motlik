# A Power Outlet for AI: What MCP Is and Why AEC Professionals Will Need It

Oct 22, 2026 · @Martin

## The AI that can't open your model

Your AI assistant can draft the RFI response, summarize a spec section, and clean up the meeting minutes. Ask it which girder on level 3 has the highest demand-to-capacity ratio, and it guesses. Not because it isn't smart enough, but because it has no way into your model.

That gap is closing. Model Context Protocol, or MCP, is an open standard that lets AI applications connect to the software and data engineers already use. Think of it as a power outlet for AI: one standard socket, and every tool plugged into it becomes something the AI can actually work with.

I come at this from two sides. My work with Dlubal Software puts me in an environment where MCP is already part of the product, and I'm building a model-review prototype of my own on top of IFC. This article explains what MCP is, what it's good for in AEC, and why connecting our tools to the big AI platforms beats building yet another chatbot.

## What MCP is: an outlet, not a brain

MCP doesn't make AI smarter. It gives AI a standard way to reach things outside itself: your models, your analysis engines, your project data.

Picture the temporary power spider box on a jobsite. It doesn't care whether you plug in a saw, a grinder, or a work light, because every tool has the same plug. Before MCP, connecting an AI to an application meant custom wiring for every pair: five AI apps and twenty programs meant up to a hundred one-off integrations. With MCP, each program builds one server and each AI app builds one client. Twenty-five pieces instead of a hundred.

&#91;embedded content: Figure 1 · MCP architecture: hosts, the outlet, servers\]

Each AI application needs one client and each program one server; the standard in the middle does the rest.

Anthropic released MCP as an open standard in November 2024. In December 2025, it handed the standard over to the [Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) under the Linux Foundation, backed by OpenAI, Google, Microsoft, and AWS, among others. Today ChatGPT, Claude, Gemini, Microsoft Copilot, GitHub Copilot, and Cursor all support it.

**Three roles, in plain terms:**

- **Host:** the AI application you type into, such as ChatGPT, Gemini, Claude, or your company's own chatbot.
- **Client:** the connector inside the host that keeps the line open to one server.
- **Server:** a small program on the software side that tells the AI what it can do. RFEM, Revit, or an IFC review tool each get their own.

**What a server offers:**

- **Tools** are actions the AI can call: check a model against the project's data requirements, compare two model versions, start an analysis.
- **Resources** are data the AI can read: a model summary, a list of load cases.
- **Prompts** are prepared workflows: "review the changes between version A and B."

The key detail is discovery. When you ask a question, the AI reads the server's own descriptions and decides which tool fits. Nobody hard-codes which button to press.

A server can run locally, right next to your desktop application. The model file stays on your machine; only the answers the tools return are sent to the AI. Or it can run remotely over HTTPS with a proper sign-in, which suits cloud platforms. If IFC is how a model describes a building, MCP is how an AI asks that model questions.

## Why AEC needs it: guessing vs. computing

MCP turns AI from a confident guesser into a coordinator that hands each task to a tool engineers already trust. That distinction matters more in our industry than almost anywhere else.

A general-purpose language model predicts plausible text. Ask it to check a beam and you get a well-formatted, confident answer that may simply be wrong, because it never ran the numbers. With MCP, the AI delegates: the calculation goes to the analysis engine, the question about the model goes to the model, and the AI does what it's genuinely good at. It understands the question, runs the steps in the right order, and explains the result in plain language.

MCP isn't the only way to feed AI project information, so it helps to see where it fits. Copying and pasting a results table into chat works, but it's a manual snapshot that goes stale the moment the model changes. Retrieval-augmented generation (RAG) lets AI search documents such as a design standard or a product manual, but it can only read text. It can't query a live model or run a calculation.

Custom integrations, like a vendor's built-in assistant, do reach live data. Each one, however, wires one AI to one application and has to be rebuilt for every new combination. MCP gives any AI app that supports it live access to the tools and data of any program that supports it. Its only real limit is the server itself: the AI can do exactly what the tools allow, nothing more.

RAG answers "what does the standard say?" MCP answers "what does my model say, and does it pass?" Most serious AEC workflows will use both.

What does that look like on a real project? These requests are already possible with servers that exist today:

- **Model queries:** "Find every fire-rated door on level 2 without a hardware set and select them." Autodesk's official Revit server can search the model and select the results.
- **Quantities:** "How many cubic yards of concrete are in the slabs, story by story?" Open-source servers read this straight from an IFC file.
- **Coordination:** "Which issues from last week's coordination meeting are still open?" Coordination platforms such as Revizto now offer MCP servers, and community servers reach issues and RFIs in Autodesk Construction Cloud.
- **Analysis results:** "What's the maximum deflection of the floor beams under service load combinations, and is it within L/360?" The answer comes from the analysis program, not from the AI's memory.

## Why plug into the AI giants instead of building our own chatbot

Let the AI companies do language; let AEC software do engineering. Every few months someone in our industry announces a proprietary assistant. MCP points to a smarter division of labor, for five reasons.

1. **You get the most capable AI models, and they keep improving.** No engineering firm or AEC vendor can match the research budgets of Anthropic, Google, OpenAI, or Microsoft. A good MCP server gets better every time the model behind the host does, without a single line of new code.
2. **Engineers already work there.** Many firms already pay for Microsoft 365 Copilot, ChatGPT, Claude, or Gemini. A new standalone chatbot is another login nobody opens after week two. An MCP server shows up inside the assistant people use every day.
3. **Build once, plug in anywhere.** The same server works in Claude, ChatGPT, Gemini, Copilot, and AI assistants a firm builds for itself. If your firm switches AI providers next year, nothing gets rewired. Even direct competitors such as OpenAI, Google, and Microsoft back the standard.
4. **Tools start working together.** One conversation can query the model, run an analysis, fill a spreadsheet, and file the result in your document system. That kind of cross-tool workflow used to require a custom script for every step.
5. **Your expertise stays yours.** The vendor keeps the validated solver, the design-standard checks, and the data model. The AI platform supplies the conversation layer on top. Domain knowledge stays the competitive advantage, which is exactly where it belongs.

There is a sixth, quieter benefit. The big hosts bring enterprise plumbing that a small AEC tool would never build on its own: admin approval of connectors, permission prompts before a tool runs, and sign-in through standard protocols. In Microsoft 365 Copilot and Gemini Enterprise, for example, an IT admin can register a custom MCP server once for the whole organization.

## Three levels of trust

The right question isn't whether to let AI into your model, but how far. Your firm decides that, not the AI, and MCP makes the boundary explicit because every server declares exactly which tools exist.

**Level one is reading.** The AI queries models and data: it lists the load-bearing walls or pulls the properties of a single element. The risk is low, especially when the server is read-only and runs locally.

**Level two is checking and computing.** The AI checks the model against an IDS file or analyzes design options. IDS is a buildingSMART format that turns the data requirements in your BIM Execution Plan into a file a computer can check. The risk is moderate because the results feed into decisions, so an engineer reviews every result and every tool call is logged.

**Level three is writing.** The AI changes the model itself, for example changing member sizes from a W14x48 to a W14x61 or adding load combinations. Few production servers allow this yet, and for good reason. It calls for a separate server, approval of each change, and version control, so any step can be rolled back.

Autodesk took the same view: its Revit MCP server launched in technical preview as read-only, with write tools planned as a separate server so the two kinds of access stay apart. For most firms, level 1 is the right place to start. It already saves hours, and nothing in the model can break.

## What I built: \[TK: two evenings\] and six tools

To test how high the barrier really is, I built a read-only MCP server for the model-review prototype I'm developing. The prototype already checks IFC models against IDS requirements and compares model versions. The server simply hands those abilities to AI.

*\[Figure 2: Code card. One complete MCP tool in about ten lines of Python.\]*

The server is called `ifc-review` and exposes six tools, all read-only:

- `get_model_summary`: project, versions, stories, element counts
- `list_elements`: find elements by IFC class, story, or load-bearing flag
- `get_properties`: property sets, quantities, and materials of one element
- `run_ids_check`: validate a version against an IDS file
- `compare_versions`: what was added, removed, or modified between two versions
- `get_viewer_link`: a link that opens the 3D viewer with the relevant elements highlighted

*\[Figure 3: The tool list as ChatGPT shows it, with the descriptions the AI reads.\]*

Then I asked the question every project team asks after a design revision: "Which load-bearing walls changed in version B, and do they still meet the IDS requirements?" The AI called `compare_versions`, then `run_ids_check`, matched the two results by element ID, and answered: \[TK: final answer from the demo, e.g. two walls went from 8 in. to 6 in. and one of them lost its fire-resistance rating\]. Then it handed me a link that opened the model with exactly those walls highlighted. Autodesk's official Revit server works on the same principle: its Select Elements and Zoom to Elements tools hand the AI's findings straight back to the model on screen.

*\[Figure 4: Main figure. The answer in chat on the left, the highlighted walls in the model on the right.\]*

*\[Figure 5: The tool call expanded: what the AI sent to the server and what came back.\]*

I ran the whole demo in two different AI apps: ChatGPT, and Gemini in Google Antigravity. Same server, same question, same tools, same answer. The server doesn't care which AI is asking. That is the whole point of a standard.

*\[Figure 6: ChatGPT and Gemini in Antigravity side by side, one server.\]*

Writing the code was the easy part. Three things mattered more:

- **Tool descriptions are the user interface.** The AI picks tools by reading them, so they deserve the same care as button labels.
- **Summaries beat data dumps.** Return counts and the top results, with details on request. Sending the AI an entire model overloads its working memory and makes answers worse.
- **Units and IDs, always.** Every number carries its unit and every element its GUID. Ambiguity is where AI starts guessing again.

&#91;TK: one honest sentence from the build log about what went wrong or surprised you.\]

## Where the industry stands

In under two years, MCP went from an experiment to a feature that major AEC vendors ship with their products.

Anthropic released the standard in November 2024. In January 2026, Dlubal Software added an MCP server to the standard installation of RFEM 6; the details are in Dlubal's [knowledge base article](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/002032) and [API documentation](https://apidocs.dlubal.com/installation_mcp.html). In April, Trimble released an MCP connector for SketchUp. In May, Bluebeam brought Claude into Revu through MCP with its [Bluebeam Max](https://blog.cadalyst.com/architecture-infrastructure-construction-solutions/mcp-a-new-standard-for-connecting-ai-to-aec-software) tier. In June, Autodesk released a read-only [Revit MCP server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/) as a technical preview add-on for Revit 2027. And in July, the [2026-07-28 specification](https://github.com/modelcontextprotocol/specification/releases/tag/2026-07-28) made servers easier to run at company scale and added proper handling for long-running jobs.

Vendors also make different design choices. Some servers expose a few narrow, purpose-built tools. Others let the AI write scripts against the program's API, much like a Dynamo or Grasshopper script, except the AI writes it. Anything the API can do, the AI can then do. Narrow tools give everyone safe defaults; scripting gives power users full reach, at the price of reviewing the code the AI writes. My own server sits firmly at the narrow end.

The July 2026 specification matters for structural work in particular. A finite element analysis isn't a two-second lookup, and the specification now gives long-running jobs a proper home: the AI starts the run, checks on it, and collects the results when it finishes.

## What MCP won't fix

MCP removes the friction between engineering judgment and its execution. It does not replace the judgment, and it brings a few new risks of its own.

- **Responsibility stays put.** The AI doesn't stamp drawings. The engineer of record reviews the result and signs, exactly as before.
- **Garbage in, garbage out, faster.** MCP automates a messy process just as faithfully as a clean one. Inconsistent parameters and missing classification codes (UniFormat, OmniClass) will surface sooner, not disappear.
- **AI-written code needs review.** When a server runs scripts the model writes, the model can write a wrong one. Review the code, test on a copy, and keep analysis results under version control.
- **Know where the data goes.** A local server keeps the model on your machine, but the AI host still sees whatever the tools return. Check your AI provider's data-retention and training terms before connecting live projects.
- **Model data can carry instructions.** A property value or a document comment that reads like a command can mislead an AI that takes it at face value. Giving the AI only the access it needs, read-only by default, is the practical defense.
- **It isn't free.** Budget for AI subscriptions, API access or add-on licenses on the software side, and workstations that can keep up.

## How to start on Monday

Start small: one project, one read-only task, one person who's curious. Before that, ask your software vendors five questions:

1. Do you ship an MCP server, and is it official or community-built?
2. Is it read-only, or can it change the model? Are the two separated?
3. Does it run locally or in the cloud, and where does project data go?
4. Which AI applications have you tested it with?
5. How is it licensed and billed?

Then run a pilot. Pick a task your team repeats every week, such as checking a model revision against the project's information requirements. Do it once by hand and once through an AI with MCP, and compare the time and what each version caught. That comparison will tell you more than any vendor demo.

## A bridge, not a replacement

MCP won't design a building. What it does is let AI reach the tools that already do the engineering, so the hours between a question and its answer shrink.

Picture the next step. One outlet finds the girders that changed in the latest model revision. A second outlet sends them to the analysis program for a rerun, provided the BIM model and the analysis model are linked, which is still one of the hardest parts of the job. The AI connects the two and puts the result in front of the engineer who decides. Every piece of that workflow exists today; what's missing is mostly the habit of plugging things in.

The AEC software we rely on is excellent at engineering. The AI platforms are excellent at language and reasoning. MCP is the outlet between them, and it's worth learning how it works before your competitors do.

&#91;TK: one line pointing to the companion episode of the podcast.\]

## Sources

- [Anthropic: Donating the Model Context Protocol and establishing the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [Model Context Protocol: 2026-07-28 specification release](https://github.com/modelcontextprotocol/specification/releases/tag/2026-07-28)
- [The Register: Model Context Protocol prepares to break with its stateful past](https://www.theregister.com/a/5276722)
- [Dlubal Software: Integration of RFEM 6 into AI applications via MCP server](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/002032)
- [Dlubal API documentation: MCP server](https://apidocs.dlubal.com/installation_mcp.html)
- [Autodesk: Introducing the Revit Public MCP Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/)
- [Cadalyst: MCP, a new standard for connecting AI to AEC software](https://blog.cadalyst.com/architecture-infrastructure-construction-solutions/mcp-a-new-standard-for-connecting-ai-to-aec-software)
- [Microsoft 365 Roadmap: Custom MCP connectors in Microsoft 365 Copilot](https://www.microsoft.com/microsoft-365/roadmap?id=501585)
- [Google: Set up a custom MCP server connection in Gemini Enterprise](https://support.google.com/g/answer/17106276)
- [ifcopenshell-mcp: open-source MCP server for IFC models](https://glama.ai/mcp/servers/kd8f7alqr6)
- [Revizto MCP Server](https://revizto.com/legal/revizto-mcp-server)
