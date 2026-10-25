# Claude Design prompt: Figure 1 (architecture) and the timeline

Two article figures redrawn in the site's visual style, replacing
`mcp-article-02-architecture` and `mcp-article-11-timeline`. Paste the block
below into Claude Design, attach the two current PNGs as references for
content (not for style).

```text
Design two static diagrams for an article on martinmotlik.com, a personal site of an AEC (architecture, engineering, construction) digital strategist. The article: "A power outlet for AI: what MCP means for AEC". Readers are structural engineers, BIM managers and AEC marketers in the U.S. All text in U.S. English, sentence case.

Redraw the two attached diagrams. Keep their content exactly as listed below; change only the look so it matches the website's design system.

DESIGN SYSTEM (match it closely)
- Look: calm, precise, Apple/Linear-like editorial UI. Light background, generous whitespace, thin hairlines, soft shadows, no gradients except a very faint blue glow if needed, no 3D, no icons or logos of the AI companies, no stock imagery, no emoji.
- Font: Inter only. Headings/labels 600–700 weight, tight letter-spacing (-0.02em); small uppercase eyebrow labels 600 weight, +0.08em letter-spacing; dates and numbers in Inter with tabular figures (no monospace).
- Colors:
  - Ink (main text, strong lines): #1C2B33
  - Body text: #33414A; secondary text: #4B5563; muted labels: #65676B
  - Accent blue (the one highlight color): #1A56DB; lighter blue #356FEF; blue tint fill: #E6EDFD
  - Surfaces: page white #FFFFFF; panel #F4F6F9; subtle fill #E9EEF5
  - Lines/borders: #D9DEE5; hairline rules: #E6E9EE
  - Do not use green or teal anywhere.
- Shapes: cards with 16 px corner radius (scale proportionally at export size), 1 px border #D9DEE5 or a soft shadow (0 1px 2px rgba(28,43,51,.06)); pills fully rounded. Strokes 1.5–2 px at 1920 px width.
- Canvas: 16:9. Deliver 3840 × 2160 PNG and 1920 × 1080 WebP. Background #F4F6F9 with the diagram content centered; keep ~8% margin on all sides.
- Keep the bottom-right corner (about 260 × 260 px at 3840 width) free of content: the website places a round "enlarge" button there.
- Legibility: the figure is shown 700 px wide in the article column (and enlarges on click). Smallest text at least 30 px at 1920 width; main labels 40–48 px. Prefer fewer, bigger words over small print.
- No title, caption, figure number, logo, watermark or copyright inside the image (the page adds the caption).

DIAGRAM 1: MCP architecture ("One standard outlet connects any AI app to any AEC tool")
Three columns, left to right, with small uppercase eyebrow labels above each column:
- Left, eyebrow "AI APPS (HOSTS)": four white cards: Claude · ChatGPT · Gemini · Copilot
- Middle, eyebrow "THE OUTLET": one tall accent card filled #1A56DB with large white "MCP", and inside it three stacked rounded rows (white at ~15% opacity, white text): Tools · Resources · Prompts
- Right, eyebrow "AEC SOFTWARE (SERVERS)": four white cards, each with a name and a secondary line:
  - Structural analysis / e.g. RFEM 6
  - BIM authoring / e.g. Revit
  - Model review / IFC and IDS checks
  - Project documents
- Connectors: one clean two-way connector from every left card to the MCP card and from the MCP card to every right card. Use straight or gently converging lines in #65676B (1.5 px at 1920) with small arrowheads at both ends; no crossing lines. The visual message: many apps, one standard socket, many tools.
- Optional, small, under the diagram in muted text: "One client per app, one server per tool."

DIAGRAM 2: timeline ("MCP in AEC: from protocol to products")
A horizontal time axis from Nov 2024 to Oct 2026 in ink #1C2B33, thin year ticks labeled "2025" and "2026", light month ticks. Milestones as dots on the axis with labels alternating above and below, connected by thin leader lines; no overlapping text. Two kinds of milestones, with a small legend at the top left ("Protocol" and "AEC products"):
- Protocol milestones: dark ink dots (#1C2B33), date in ink
- AEC product milestones: accent blue dots (#1A56DB), date in accent blue
Milestones (date, label), in this order:
1. Nov 2024 · MCP released by Anthropic (protocol)
2. Dec 2025 · MCP donated to the Agentic AI Foundation (Linux Foundation) (protocol)
3. Jan 2026 · RFEM 6 ships an MCP server (product)
4. Apr 2026 · SketchUp connector for Claude (product)
5. May 2026 · Bluebeam brings Claude to Revu (product)
6. Jun 2026 · Revit MCP server, read-only tech preview (product)
7. Jul 2026 · MCP specification 2026-07-28 (protocol)
8. Sep 2026 · Revit Trusted-Write and Experimental servers (product)
Dates as short labels ("Nov 2024"), labels in two lines max. Spread 2026 events so each label has room (the axis can give 2026 more space than 2025 if needed, but keep the order and the year ticks honest). Mark the right end of the axis with a subtle "Oct 2026" end cap in muted text.

Output both diagrams as separate artboards. Before exporting, check: no green/teal, every label from the lists above present and spelled exactly, nothing in the bottom-right corner, text readable at 700 px wide.
```

## After the design

- Export names: `mcp-article-02-architecture.png` / `.webp`,
  `mcp-article-11-timeline.png` / `.webp` (same names as now, so the page and
  the image pipeline need no change; `npm run images:force` for the
  renditions).
- Update the alt texts in `assets.md` and the CS/DE `img11_alt` and
  `fig1_alt` if the content changes (the Sep 2026 Revit point and "RFEM 6"
  instead of "RFEM 6.13" are new on the timeline; the eyebrow labels are new on
  the architecture diagram).
