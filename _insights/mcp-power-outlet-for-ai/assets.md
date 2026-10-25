# Obrázky článku „A Power Outlet for AI“

*Copy of `article-assets/assets.md` from the BIM Platform repo (2026-10-24); figures 02 and 11 updated here after the redesign (2026-10-25). The page builder reads this file.*

Generováno skriptem `scripts/render.mjs` ze stejného seznamu jako obrázky (`scripts/figures.mjs`). Obrázky nemají titulky, popisky ani poznámky. Je v nich jen prostředí aplikace přes celou plochu 16 : 9, nebo schéma s vlastními popisky. Prostředí i data modelu jsou v americké angličtině. Každý obrázek je v `final/` jako PNG 3840 × 2160 a WebP 1920 × 1080, schéma 02 i jako SVG. Title, Alt text a Description níž jsou metadata pro web, v obrázku nejsou.

## mcp-article-01-hero

- **Place in the article:** Article header and link preview
- **Files:** `final/mcp-article-video-chat-poster.png` (2560 × 1440, the last frame of the cover video; replaces the earlier hero, 2026-10-25)
- **Status:** final
- **Title:** A Power Outlet for AI
- **Alt text:** ChatGPT's answer comparing revisions R02 and R03 of a residential building, next to a web-based 3D viewer of revision R03: the three doors on Residential Level 3 that still lack a fire rating are red, the building services are colored by system, and the Checks panel shows 13 of 14 requirements passed.
- **Tags:** MCP, Model Context Protocol, AI, BIM, IFC, IDS, AEC
- **Description:** ChatGPT answers a model question through MCP, and the 3D viewer shows the three doors that still lack a fire rating.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-02-architecture

- **Place in the article:** Figure 1
- **Files:** `final/mcp-article-02-architecture.png`, `final/mcp-article-02-architecture.webp` (redrawn in the site's style with Claude Design, 2026-10-25, variant v2/2a)
- **Status:** final
- **Title:** One standard outlet connects any AI app to any AEC tool
- **Alt text:** Diagram in three tiers. Top, four AI apps (hosts) with their logos: Claude, ChatGPT, Gemini and Copilot. Middle, a blue bar labeled "The outlet", MCP, with Tools, Resources and Prompts. Bottom, four kinds of AEC software (servers): structural analysis such as RFEM 6, BIM authoring such as Revit, model review with IFC and IDS checks, and project documents. A line joins every app and every tool to MCP, under the note "One client per app, one server per tool."
- **Tags:** MCP, architecture, AI applications, AEC software, interoperability
- **Description:** Figure 1. MCP sits between AI applications and AEC software: one protocol instead of one integration per pair.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-03-code

- **Place in the article:** Figure 2
- **Files:** `final/mcp-article-03-code.png`, `final/mcp-article-03-code.webp`
- **Status:** final
- **Title:** What an MCP tool looks like in code
- **Alt text:** Source code of the get_properties tool from packages/mcp-server/src/server.ts: its name, the plain-English description the AI reads to decide when to use it, an input schema that takes the element's GlobalId, the read-only annotations and an output schema for a structured result. The name, description and output schema lines are tinted.
- **Tags:** MCP, TypeScript, tool definition, code
- **Description:** Figure 2. One tool of the ifc-review server: a name, a description the AI reads and a structured result.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-04-tools

- **Place in the article:** Figure 3
- **Files:** `final/mcp-article-04-tools.png`, `final/mcp-article-04-tools.webp`
- **Status:** final
- **Title:** The ifc-review server in ChatGPT
- **Alt text:** ChatGPT's settings, Plugins, MCPs tab: the ifc-review server switched on in the list of servers, next to the app's own ones.
- **Tags:** MCP, ChatGPT, Codex, MCP server
- **Description:** Figure 3. Connected once, ifc-review is one more MCP server in ChatGPT's settings.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-05-permission

- **Place in the article:** Chapter "Three levels of trust"
- **Files:** `final/mcp-article-05-permission.png`, `final/mcp-article-05-permission.webp`
- **Status:** final
- **Title:** The AI asks before it runs a tool
- **Alt text:** Google Antigravity, running Gemini, asks "Allow using this MCP tool?" before it calls run_ids_check of the ifc-review server. Above the question are the arguments the AI wants to send; below it the choices: allow this time, always allow in this conversation, always allow, or no.
- **Tags:** MCP, permissions, trust, Gemini, Google Antigravity
- **Description:** Before a tool runs, the user approves it: once, always, or not at all.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-06-main

- **Place in the article:** Figure 4 (main image)
- **Files:** `final/mcp-article-06-main.png`, `final/mcp-article-06-main.webp`
- **Status:** final
- **Title:** A question in chat, the answer in the model
- **Alt text:** Left, ChatGPT's answer comparing revisions R02 and R03 of a residential building: 10 of 13 elements fixed, three doors still missing a fire rating, and an "Open in 3D viewer" link. A teal line runs from the link to the 3D viewer on the right, where the three doors on Residential Level 3 are red, the elements fixed since R02 are teal and the Checks panel lists the one requirement that still fails.
- **Tags:** MCP, IDS, IFC, model review, ChatGPT, 3D viewer
- **Description:** Figure 4. ChatGPT compares two revisions through MCP and links to the three doors that still miss a fire rating. Building services are hidden in the view for legibility.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-07-under-the-hood

- **Place in the article:** Figure 5
- **Files:** `final/mcp-article-07-under-the-hood.png`, `final/mcp-article-07-under-the-hood.webp`
- **Status:** final
- **Title:** What the AI actually sent, and what came back
- **Alt text:** ChatGPT with its ifc-review calls unfolded: Model summary, then Check against IDS opened to show the summary and the structured JSON result the server returned, followed by ChatGPT's answer that 13 of 14 requirements pass and three doors fail KOM-14.
- **Tags:** MCP, tool calls, JSON, ChatGPT
- **Description:** Figure 5. One tool call as ChatGPT shows it, matched against the server's own trace.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-08-two-ais

- **Place in the article:** Figure 6
- **Files:** `final/mcp-article-08-two-ais.png`, `final/mcp-article-08-two-ais.webp`
- **Status:** final
- **Title:** Same MCP server, same tools, same answer
- **Alt text:** Side by side, ChatGPT (left) and Gemini in Google Antigravity (right) answer the same question about revisions R02 and R03 through the same ifc-review MCP server: 10 of 13 elements fixed, three doors still failing.
- **Tags:** MCP, ChatGPT, Gemini, interoperability
- **Description:** Figure 6. Two AI applications from two companies, one server: the answer does not depend on the chat app.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-09-ids-check

- **Place in the article:** Supplementary (podcast, LinkedIn)
- **Files:** `final/mcp-article-09-ids-check.png`, `final/mcp-article-09-ids-check.webp`
- **Status:** final
- **Title:** Revision R02 against the project IDS
- **Alt text:** A web-based 3D viewer with revision R02 of a residential building drawn see-through in light gray. Thirteen elements are red: eleven doors and two roof windows. The Checks panel shows 12 requirements passed and 2 failed, with the two failing requirements expanded.
- **Tags:** IDS, IFC, model checking, BIM
- **Description:** R02 fails two of fourteen requirements on thirteen elements. Building services are hidden in the view for legibility.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-10-revision-diff

- **Place in the article:** Supplementary
- **Files:** `final/mcp-article-10-revision-diff.png`, `final/mcp-article-10-revision-diff.webp`
- **Status:** final
- **Title:** What changed between R02 and R03
- **Alt text:** Two halves of the 3D viewer side by side. Left, in the comparison of R02 and R03, a door whose FireRating went from empty to EI 30 DP3. Right, a roof window in R03 whose Pset_WindowCommon now holds a ThermalTransmittance of 1.1 W/(m²·K).
- **Tags:** IFC, revision, change tracking, BIM
- **Description:** The two kinds of fix in R03: a fire rating on doors and a U-value on the roof windows. R03 is a demo revision made for this article.
- **Copyright:** © 2026 Martin Motlík

## mcp-article-11-timeline

- **Place in the article:** Chapter "Where the industry stands"
- **Files:** `final/mcp-article-11-timeline.png`, `final/mcp-article-11-timeline.webp` (redrawn in the site's style with Claude Design, 2026-10-25, variant v2/2a)
- **Status:** final
- **Title:** MCP in AEC: from protocol to products
- **Alt text:** Timeline from November 2024 to October 2026, protocol milestones in dark and AEC products in blue: MCP released by Anthropic (November 2024); MCP donated to the Agentic AI Foundation under the Linux Foundation (December 2025); RFEM 6 ships an MCP server (January 2026); SketchUp connector for Claude (April 2026); Bluebeam brings Claude to Revu (May 2026); Revit MCP server, read-only tech preview (June 2026); MCP specification 2026-07-28 (July 2026); Revit Trusted-Write and Experimental servers (September 2026).
- **Tags:** MCP, timeline, AEC software, industry
- **Description:** Under two years from an open protocol to MCP servers in structural, BIM and document tools.
- **Copyright:** © 2026 Martin Motlík
