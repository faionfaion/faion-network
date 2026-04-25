# Agent Integration — Generative UI Design

## When to use
- Rapid ideation: generating 5–10 UI layout variants from a feature brief before any human design work starts
- Converting a written product spec into interactive HTML/React prototypes for early stakeholder feedback
- Producing low-fidelity wireframe candidates that a designer then refines — not for production use directly
- Generating alternative component implementations (card, list, grid) when the team is undecided on layout pattern
- Bootstrapping a new screen's structure when the design system tokens are already defined (v0/Claude Artifacts can reference them)

## When NOT to use
- When a final, production-ready UI is expected — generative output requires significant designer refinement
- When strict brand compliance is mandatory from the first iteration — AI tools ignore brand guidelines unless explicitly constrained
- When the component must integrate with an existing codebase — generated code often uses different component libraries or naming
- When accessibility (WCAG AA/AAA) is non-negotiable from day one — generated UIs consistently miss aria attributes, focus management, and contrast
- When the client or legal team cannot review IP of AI-generated design artifacts

## Where it fails / limitations
- Generated layouts are often visually safe/generic — they optimize for "looks like a UI" rather than solving the specific design problem
- Color and typography decisions are shallow; no understanding of visual hierarchy principles beyond surface patterns
- Generated React/HTML code rarely matches the project's actual component library (shadcn/ui vs. MUI vs. Ant Design)
- Galileo and Uizard outputs are not directly Figma-compatible; import requires manual layer cleanup
- v0 (Vercel) generates Tailwind + shadcn/ui exclusively — breaks if the project uses a different stack
- Claude Artifacts prototypes have no persistent state and cannot connect to real APIs in the preview
- No tool produces accessible keyboard navigation, skip-to-content, or screen-reader-friendly markup by default

## Agentic workflow
An agent drives generative UI design by translating a structured product spec (feature name, user goal, key actions, component constraints) into tool-specific prompts, calling the generation API, and presenting ranked variants for human selection. Claude Artifacts is the most agent-native path: the agent writes a React or HTML prototype in the `<artifact>` block, the human reviews it, and the agent iterates based on feedback. For v0, the agent constructs the prompt and provides the v0 URL — a human must click and inspect. Galileo has no public API; it is UI-only. The agent's role is prompt construction, iteration tracking, and documenting which variant was selected and why.

### Recommended subagents
- `faion-sdd-executor-agent` — generates a prototype artifact as a task subtask within an SDD feature
- Custom UI-generation agent — takes a spec file, constructs a v0/Claude prompt, logs variants to a decision file

### Prompt pattern
```
Generate a UI for: {feature_name}

User goal: {user_goal}
Key actions: {action_1}, {action_2}, {action_3}
Constraints:
- Use Tailwind CSS + shadcn/ui components
- Mobile-first, max width 768px
- No placeholder lorem ipsum — use realistic content
- Must include: {required_elements}

Output a complete React component. No external imports beyond shadcn/ui and lucide-react.
```

```
# Iterative refinement pattern
Previous variant: [paste component code]

Changes requested:
1. Move the CTA button above the fold
2. Replace the card grid with a list view
3. Add a loading skeleton state

Return the updated component only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| v0 CLI | Generate React components from prompts via terminal | npm i -g v0 (v0.dev/docs/cli) |
| shadcn/ui CLI | Scaffold shadcn component library in project | npx shadcn-ui@latest init |
| create-react-app / Vite | Bootstrap environment for testing generated code | npm create vite@latest |
| Playwright | Test generated prototypes for basic interaction | npm i -D playwright |
| axe-cli | Accessibility audit on rendered generated UI | npm i -g axe-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| v0 by Vercel | SaaS | Partial — CLI + API beta | CLI available; API access is in beta as of 2026. Outputs Tailwind + shadcn/ui only. |
| Claude Artifacts | SaaS | Yes — via Claude API | Most agent-native: agent generates artifact inline. No separate API call needed. |
| Galileo AI | SaaS | No | UI-only; no public API. Figma plugin for export. |
| Uizard | SaaS | Partial | Has a project API in beta; main UX is browser-based. Best for wireframe-to-mockup. |
| Relume | SaaS | No public API | UI-only; generates Figma-compatible wireframes from sitemap prompts. |
| Builder.io | SaaS | Yes — REST + SDK | Can receive AI-generated component specs and render them visually; agent-compatible. |

## Templates & scripts
See templates.md for UI generation prompt templates.

v0 CLI batch generation script (bash, ~20 lines):

```bash
#!/bin/bash
# Generates UI variants from a prompts file and saves outputs
# Usage: ./gen-ui.sh prompts.txt output-dir/

PROMPTS_FILE="$1"
OUT_DIR="${2:-ui-variants}"
mkdir -p "$OUT_DIR"

i=1
while IFS= read -r prompt; do
  echo "Generating variant $i..."
  v0 generate "$prompt" --format react > "$OUT_DIR/variant_$i.tsx" 2>&1
  echo "Saved variant_$i.tsx"
  ((i++))
done < "$PROMPTS_FILE"

echo "Done. $((i-1)) variants generated in $OUT_DIR/"
```

## Best practices
- Always start with a written spec before prompting — "generate a dashboard" produces garbage; "generate a SaaS analytics dashboard with date-range filter, KPI cards, and a line chart component" produces useful starting points
- Generate 3–5 variants per screen, not 1 — comparison is faster than iteration from a single bad start
- Use Claude Artifacts for agent-loop iteration: it is the only tool where the agent can see and modify the output without a human browser session
- Impose component constraints explicitly in every prompt: library, responsive breakpoints, realistic content, no Lorem Ipsum
- Document why a variant was rejected — this becomes the training signal for better next prompts
- Run axe-cli on any generated prototype before a stakeholder review to prevent presenting inaccessible UIs as viable designs
- Treat generated code as a sketch, not a PR — always refactor before merging into a real codebase

## AI-agent gotchas
- v0 API is not GA as of 2026; availability and rate limits are unpredictable for automated pipelines
- Claude Artifacts previews are sandboxed: no fetch(), no localStorage, no external assets — generated code using these will appear broken in preview
- Generative tools produce non-deterministic output; the same prompt across two runs may yield structurally different components — do not rely on reproducibility
- Generated component names often conflict with existing project components (e.g., `Button`, `Card`) — always namespace or rename before integration
- Galileo exports to Figma via a plugin that requires a human to manually trigger — no agent path exists
- Models hallucinate component APIs: generated code may reference props or methods that do not exist in the actual library version the project uses
- Never auto-deploy generated UI code to production without a designer and developer review — the human-in-loop checkpoint is mandatory here

## References
- https://v0.dev/docs
- https://www.usegalileo.ai/
- https://www.anthropic.com/news/claude-artifacts
- https://www.nngroup.com/articles/generative-ui/
- https://uxtools.co/ai-design-survey/
- https://ui.shadcn.com/
