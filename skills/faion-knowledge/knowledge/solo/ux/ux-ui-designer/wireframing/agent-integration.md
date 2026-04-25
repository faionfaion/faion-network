# Agent Integration — Wireframing

## When to use
- Generating ASCII or structured text wireframes from a feature spec or user story for rapid layout discussion
- Producing wireframe annotation documents (element table, states, interactions) from a design brief
- Reviewing a wireframe description or screenshot against a spec to flag missing states (empty, error, loading)
- Drafting wireframe critique feedback based on a checklist (hierarchy, CTA prominence, responsiveness coverage)
- Creating component wireframe templates (card, form, modal) from a design system definition

## When NOT to use
- Generating visual design — wireframes are intentionally lo-fi; agents producing polished mockups skip the structural validation step
- When stakeholders need pixel-precise layouts for developer handoff — wireframes are for alignment, not spec
- As a substitute for collaborative sketching sessions where the goal is building team buy-in, not just producing an artifact

## Where it fails / limitations
- ASCII wireframes agents produce are useful for text-based communication (markdown docs, GitHub comments) but cannot replace Figma or Balsamiq for stakeholder reviews where visual fidelity matters
- Agents cannot produce actual clickable prototypes — they can document interaction behavior but cannot make it interactive
- Wireframe completeness (all states, all responsive breakpoints) is hard for agents to self-verify without an explicit checklist passed in the prompt
- Agents tend to produce "happy path" wireframes; error states, empty states, and permission-gated views require explicit prompting to include
- Generated annotation tables may not reflect actual implementation constraints (technical limitations, backend data availability) without engineering input

## Agentic workflow
A Claude agent reads a feature spec or user story set and produces a structured wireframe document: for each screen it lists the layout description in ASCII or structured prose, an annotation table (element, description, behavior), a states checklist (default, empty, loading, error), and open questions for the design review. This document serves as the input to a Figma session, not the output. A second agent can review a completed wireframe description against the spec and flag gaps.

### Recommended subagents
- `faion-sdd-executor-agent` — validates that each wireframe screen maps to a user story AC in the SDD spec, and flags ACs with no wireframe coverage

### Prompt pattern
```
You are a UX designer producing a low-fidelity wireframe specification.
Given the user story below, produce a wireframe document for each screen in the flow:
- ASCII layout diagram (use boxes and labels, no colors)
- Annotation table: Element | Description | Behavior/Notes
- States: list all states this screen must handle (default, empty, loading, error, success)
- Responsive notes: what changes at mobile breakpoint
- Open questions: anything ambiguous that needs design decision

Do not produce high-fidelity visuals or specify colors/fonts.
```

```
Review this wireframe description against the acceptance criteria below.
Identify:
1. ACs with no wireframe coverage
2. States required by ACs (error, empty, permission-denied) missing from the wireframe
3. Interactions referenced in ACs but not annotated

Output as a gap analysis table: AC | Wireframe coverage | Gap description
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Generate flow diagrams and simple layout sketches from markdown | `npm i -g @mermaid-js/mermaid-cli` / mermaid.js.org |
| Balsamiq (desktop, no CLI) | Deliberately lo-fi wireframes; export to PNG/PDF for docs | balsamiq.com |
| Whimsical (web) | Fast wireframes + flowcharts; shareable links | whimsical.com |
| Figma CLI (`fig`) | Import wireframe components; no full wireframe generation CLI | community/unofficial |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes — REST API | Read/write frames via API; agents can add annotation comments to wireframe files |
| Whimsical | SaaS | No public API | Manual UI only; good for team collaboration, not agent automation |
| Balsamiq Cloud | SaaS | Partial — export API | Export wireframes as PNG/PDF; no programmatic creation |
| Miro | SaaS | Yes — REST API | Create sticky notes and shapes via API; approximate wireframe creation possible |
| Notion | SaaS | Yes — API | Store wireframe annotation docs as Notion pages; version and link to specs |
| Storybook | OSS | Yes | Wire-level component stories enforce structural decisions before visual design is applied |

## Templates & scripts
See `templates.md` for the Wireframe Documentation Template and Component Wireframe Template.

```
# Minimal ASCII wireframe component library for markdown docs

## Navigation bar
+------------------------------------------+
| [Logo]    [Nav 1]  [Nav 2]  [Nav 3] [CTA]|
+------------------------------------------+

## Hero section
+------------------------------------------+
|  [Headline — H1]                         |
|  [Subtext — max 2 lines]                 |
|  [ Primary CTA ]  [ Secondary CTA ]      |
+------------------------------------------+

## Card (3-up grid)
+------------+  +------------+  +----------+
| [Image]    |  | [Image]    |  | [Image]  |
| Title      |  | Title      |  | Title    |
| Body text  |  | Body text  |  | Body     |
| [Action]   |  | [Action]   |  | [Action] |
+------------+  +------------+  +----------+

## Form
Label *
[Input field                    ]
Helper text

Label *
[Input field                    ]

[ Submit ]  [ Cancel ]
```

## Best practices
- Produce at minimum 3 layout variants for key screens before settling on one — convergence too early eliminates valid alternatives
- Every wireframe must include the annotation table — undocumented behavior assumptions cause expensive rework in implementation
- Explicitly wireframe empty states before launch: "no results", "no data yet", "permission denied" — these are always missed and always noticed by users
- Include mobile breakpoint notes in every wireframe, even for desktop-first products — retrofitting responsive is always more expensive
- Use a persistent header in the annotation table: "Open Questions" section forces designers to surface assumptions before engineering starts

## AI-agent gotchas
- Agents producing wireframes from specs will default to the happy path only; always add "include all error, empty, loading, and permission-denied states" to the prompt explicitly
- ASCII wireframes generated by agents in markdown can look correct in the raw text but break in rendered markdown due to character width differences — validate rendering before sharing
- Annotation tables generated without access to the actual spec ACs will contain invented behavior descriptions; always provide the spec as context
- Agents will omit "open questions" unless explicitly instructed to flag ambiguity — this is the most valuable part of a wireframe document for early-stage design
- Human review of wireframes is mandatory before engineering starts — agents surface structure but cannot judge whether it matches user mental models or business intent

## References
- https://www.figma.com/resource-library/wireframing/
- https://www.nngroup.com/articles/wireframe-tools/
- https://sensible.com/dont-make-me-think/
- https://balsamiq.com/learn/
- https://www.smashingmagazine.com/2023/wireframing-guide/
