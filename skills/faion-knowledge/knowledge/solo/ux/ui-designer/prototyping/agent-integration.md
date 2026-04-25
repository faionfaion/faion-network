# Agent Integration — Prototyping

## When to use
- Validating interaction flows before writing production code
- Presenting design concepts to stakeholders who cannot read wireframes
- Running usability tests when no real product exists yet
- Deciding between two competing UX patterns before committing to development
- Documenting expected behavior for handoff to engineers

## When NOT to use
- When the feature scope is a single static content page with no interaction
- When a fully working staging environment already exists and can be tested directly
- When the only unknown is visual aesthetics (use static mockups instead)
- When the timeline is so compressed that prototype iteration would delay actual build

## Where it fails / limitations
- High-fidelity Figma prototypes create false confidence: engineers still discover interaction gaps during implementation
- Paper and clickable prototypes cannot test real performance, latency, or loading states
- Prototypes built in tools like ProtoPie or Framer rarely survive design system updates — they become stale fast
- LLM-generated prototype code (React/HTML) often works in isolation but breaks under realistic data or edge states
- Prototype findings are biased by participant familiarity with the test setup, not the real product

## Agentic workflow
A Claude subagent can receive a user story and a list of screens from a design spec, then generate a clickable HTML/React prototype that covers the critical flow end-to-end. The agent should be constrained to a single flow at one fidelity level — attempting to automate a full high-fidelity prototype in one pass produces unmaintainable code. Human review is required after generation: the designer must walk through the prototype and confirm hotspots, transitions, and edge states before any user testing begins.

### Recommended subagents
- `faion-sdd-executor-agent` — executes implementation tasks including generating prototype scaffolding from a design spec
- Any general-purpose Claude subagent (Sonnet or Opus) — generates HTML/React prototype code from screen descriptions

### Prompt pattern
```
You are a UI prototyping assistant. Given the screens and interaction spec below, generate a self-contained HTML prototype covering the [checkout / onboarding / etc.] flow.

Constraints:
- Single HTML file with inline CSS and vanilla JS
- Clickable hotspots only, no backend
- Label each screen clearly at the top
- Use placeholder text [LOREM] for copy you do not know

Screens: [list]
Interaction spec: [describe]
```

```
Analyze this Figma prototype link [URL] and extract: list of screens, clickable elements, transitions, and missing edge states (empty, error, loading). Return as structured JSON.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `figma-cli` (community) | Export frames and assets from Figma via API | `npm i -g figma-cli` / [figma.com/developers](https://www.figma.com/developers/api) |
| `storybook` | Build interactive component demos as live prototypes | `npx storybook@latest init` / [storybook.js.org](https://storybook.js.org) |
| `playwright` | Automate prototype walkthroughs for regression checks | `npm i -D @playwright/test` / [playwright.dev](https://playwright.dev) |
| `framer-cli` | Publish Framer prototypes from CI | `npm i -g @framer/cli` / [framer.com/developers](https://www.framer.com/developers/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes — REST API | Agent can read frames, comments, components via API; cannot drive the UI editor |
| ProtoPie | SaaS | Partial | Export/import via files; no public REST API for automation |
| Framer | SaaS | Partial | CLI publish supported; no programmatic prototype creation |
| Storybook | OSS | Yes | Fully scriptable; agents can generate stories from component props |
| CodeSandbox / StackBlitz | SaaS | Yes | Agents can push prototype code via API or git; share URL for review |

## Templates & scripts
See `templates.md` for Prototype Plan and Prototype Testing Notes templates.

Minimal script — export all Figma frames from a page to PNG for offline reference:
```bash
#!/usr/bin/env bash
# Usage: FIGMA_TOKEN=xxx FILE_KEY=yyy bash export-frames.sh
PAGE_NAME="${1:-Page 1}"
curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY" \
  | jq -r --arg p "$PAGE_NAME" \
    '.document.children[] | select(.name==$p) | .children[] | "\(.id) \(.name)"' \
  | while read id name; do
      url=$(curl -s -H "X-Figma-Token: $FIGMA_TOKEN" \
        "https://api.figma.com/v1/images/$FILE_KEY?ids=$id&format=png" \
        | jq -r ".images[\"$id\"]")
      curl -s "$url" -o "${name// /_}.png"
      echo "Saved: ${name}.png"
    done
```

## Best practices
- Define one specific learning objective per prototype — prototypes that try to test everything teach nothing
- Prototype the highest-risk interaction first, not the most visually interesting screen
- Use real data samples (even anonymized) rather than "Lorem ipsum" — fake data hides copy-length bugs
- Version prototypes (v1, v2) and keep old versions accessible during iteration; do not overwrite
- Document what the prototype intentionally does NOT cover at the top of the file — prevents misuse in handoff
- After testing, write findings as discrete issues with severity ratings before sharing with engineers; raw notes get ignored

## AI-agent gotchas
- LLMs generating prototype code do not know the design system; inject component library docs or a token file into context first
- Agents over-scope: constrain to a single named flow in the prompt or the output will be unmanageable
- Figma API returns node IDs, not screen names — pre-map IDs to names before passing to an agent
- Generated React prototypes often use `useState` in ways that break multi-step flows; agent should be told to use a simple state machine or step counter
- Prototype quality review requires a human designer — do not let an agent declare the prototype "ready for testing"
- When agents write session scripts (facilitator guides), they omit think-aloud instructions; always append the standard preamble manually

## References
- [Figma Prototyping Guide](https://help.figma.com/hc/en-us/articles/360040314193)
- [NNG: Prototyping Tools](https://www.nngroup.com/articles/prototyping-tools/)
- [Sprint by Jake Knapp — GV](https://www.gv.com/sprint/)
- [Framer Developer Docs](https://www.framer.com/developers/)
- [Storybook Docs](https://storybook.js.org/docs)
