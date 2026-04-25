# Agent Integration — Wireframing

## When to use
- Translating a product spec or user story into a structural layout before visual design begins
- Rapid exploration of multiple layout alternatives for a new page or feature
- Generating annotated wireframe documentation from existing designs for developer handoff
- Producing low-fidelity content hierarchy maps to align stakeholders on structure before aesthetics
- Auditing existing screens for missing states (empty, error, loading) and documenting them

## When NOT to use
- After visual design has already been approved — wireframing retroactively is documentation theater, not design
- For micro-interactions and animations — wireframes convey structure, not motion
- As a replacement for user research — wireframing answers "how to lay it out," not "what to build"
- When the deliverable requires interactive prototype testing — proceed directly to Figma interactive prototypes
- One-screen fixes or copy changes where layout is already established

## Where it fails / limitations
- Text-based wireframe descriptions (ASCII art or prose) are ambiguous; agents cannot produce spatial layouts that survive interpretation without a visual tool
- Agents generating wireframe annotations frequently omit states (empty, error, loading, disabled) that are not explicitly requested
- Wireframes produced without a content inventory (real copy, real data volume) mislead stakeholders about actual information density
- Responsive behavior cannot be adequately expressed in text; agents generate desktop-only wireframe specs by default
- Annotation quality degrades when agents lack access to the technical constraints driving interaction decisions

## Agentic workflow
An agent receives a user story or feature spec and produces: (1) a structured layout description in the Wireframe Documentation Template format from `templates.md`, (2) an element annotation table covering behavior, conditional states, and technical notes, and (3) an explicit list of states requiring separate wireframes (empty, error, loading). The agent flags any layout decision where user research input is needed. Output feeds a designer or directly into a Figma wireframe session.

### Recommended subagents
- General Claude subagent (haiku) — wireframe spec generation from a requirements list is mechanical pattern application
- General Claude subagent (sonnet) — annotation review and state coverage audit

### Prompt pattern
```
You are a UX designer creating a wireframe specification.
Given this user story: [story]
And this content inventory: [content list]
Generate a wireframe documentation using this structure:
- Purpose and user goal
- Layout description: header, navigation, main content zones, CTAs, footer
- Element annotation table (Element | Description | Behavior | Notes)
- States required: Default | Empty | Error | Loading | Success
- Responsive notes: Desktop | Tablet | Mobile
- Open questions requiring stakeholder input
Do not add visual design details (no colors, no typography styles). Focus on structure and behavior.
```

```
State coverage audit:
Given this wireframe specification: [spec]
List every interactive element and form field.
For each, identify which states are missing from the spec:
(Default / Hover / Focus / Active / Disabled / Loading / Error / Empty / Success)
Output a table with: Element | States Documented | States Missing | Priority to Add (H/M/L).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `figma-api` (Node SDK) | Programmatic access to Figma file structure for audit or export | `npm i figma-api` / https://github.com/Figma-Linux/figma-api |
| `penpot-cli` | OSS design tool CLI for batch operations on wireframe files | https://penpot.app/docs/technical-guide/developer/ |
| `mermaid-cli` | Generate flowcharts and simple layout diagrams from markdown | `npm i -g @mermaid-js/mermaid-cli` / https://github.com/mermaid-js/mermaid-cli |
| `whimsical` (web) | Fast wireframing; no CLI but REST API for workspace management | https://whimsical.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes (REST API) | Read/write file structure; agents can create frames and text nodes via API with plugin scripts |
| Balsamiq Cloud | SaaS | Partial (REST API) | Low-fidelity wireframes; API allows project/document CRUD but not granular frame editing |
| Whimsical | SaaS | No public API | Fast wireframing but no agent-accessible API |
| Penpot | OSS | Yes (REST API) | Self-hostable Figma alternative; REST API for file management |
| Miro | SaaS | Yes (REST API) | Whiteboard wireframing; rich REST API for frame/widget creation |
| Framer | SaaS | No | Code-based design tool; agent-generated React code can be imported but no wireframe API |

## Templates & scripts
See `templates.md` for the Wireframe Documentation Template and Component Wireframe Template.

Inline script — extract page inventory from a Figma file (requires Figma API token):
```bash
#!/usr/bin/env bash
# figma-pages.sh — list all pages and top-level frames in a Figma file
# Usage: FIGMA_TOKEN=xxx bash figma-pages.sh <file-key>
FILE_KEY=$1
curl -s "https://api.figma.com/v1/files/${FILE_KEY}?depth=2" \
  -H "X-Figma-Token: ${FIGMA_TOKEN}" \
  | jq -r '
    .document.children[] |
    "PAGE: \(.name)" ,
    (  .children[]? | "  FRAME: \(.name) [\(.type)]" )
  '
```

## Best practices
- Start with 3+ rough sketches before opening any tool — the tool commits you to a direction before you have explored enough
- Use real content volume estimates, not Lorem Ipsum — "3 items" vs "247 items" produces wildly different layouts
- Document every annotation with: what it is, how it behaves, and what happens in each relevant state — behavior is the deliverable, not the box
- Share wireframes for feedback as questions ("Does this hierarchy match how users think?"), not statements ("Here's the design")
- Never present a wireframe alongside a visual mockup in the same stakeholder review — the mockup always wins all attention
- Mobile wireframes are a separate deliverable, not a footnote — create them in the same session, not as an afterthought

## AI-agent gotchas
- Agents produce text descriptions of layouts, not actual wireframes — a Figma file cannot be generated by a text agent without a plugin/API pipeline
- State coverage is reliably incomplete in agent output; always run an explicit state audit prompt after spec generation
- Agents do not know real content volume; they assume "a few items" — provide actual data counts as input
- Responsive breakpoint behavior is omitted by default; must be explicitly requested with specific breakpoints (375px, 768px, 1280px)
- Stakeholder review of agent-generated wireframe specs must happen before any development begins — the spec is a hypothesis, not an approval

## References
- https://www.figma.com/resource-library/wireframing/
- https://www.nngroup.com/articles/wireframe-tools/
- https://sensible.com/dont-make-me-think/ (Steve Krug)
- https://balsamiq.com/learn/
- https://www.smashingmagazine.com/2023/wireframing-guide/
