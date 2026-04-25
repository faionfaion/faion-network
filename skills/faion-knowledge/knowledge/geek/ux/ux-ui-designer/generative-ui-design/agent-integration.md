# Agent Integration — Generative UI Design

## When to use
- Rapid ideation phase: generating 5–10 UI variants from a brief to explore design space quickly
- Prototyping flows for investor demos or usability tests where visual polish is secondary to concept
- Generating React/HTML component code from design descriptions (v0, Claude Artifacts)
- Reducing blank-canvas paralysis on new projects — use generated output as a forcing function for critique
- Creating low-fidelity wireframe sets across multiple screen sizes in parallel

## When NOT to use
- Brand-critical production interfaces — AI generation does not understand brand nuance reliably
- Accessibility-first projects — generative outputs routinely miss focus management, ARIA roles, color contrast
- Design system contributions — generated components bypass token and variant governance
- When the design problem requires deep user research insight — generation amplifies assumptions, not insights
- Final developer handoff — generated code (v0, Galileo) requires significant cleanup before production

## Where it fails / limitations
- AI-generated UI converges on modal patterns (cards, hero banners, nav bars) — novel interaction models are underrepresented
- Brand consistency degrades with each iteration; AI drifts from style guide without explicit anchoring
- Generated code (v0) often uses deprecated library APIs or lacks responsive breakpoints
- Galileo and Uizard outputs are image-based, not editable component trees — import into Figma requires manual rebuild
- Claude Artifacts are single-page; complex multi-state flows require manual stitching
- Relume wireframes assume marketing/SaaS site structure; product app patterns are weaker

## Agentic workflow
Claude subagents can generate multiple UI variants from a single brief by running parallel generation calls with different style constraints (minimal, data-dense, mobile-first). The agent produces structured HTML/React code or Figma-paste-ready specifications. Human curates: selects variants, marks off-brand elements, flags accessibility issues. A second agent pass refines the selected variant based on critique notes. The loop is: agent generates → human selects → agent refines → human verifies accessibility → done.

### Recommended subagents
- `haiku` — high-volume variant generation (10+ options), design token application to boilerplate
- `sonnet` — complex multi-state component generation, critique synthesis, design brief interpretation

### Prompt pattern
```
Generate 3 UI variants for: [screen name, e.g. "user onboarding step 2 — email verification"].
Design system: [Tailwind / Material / custom tokens: list].
Constraints: mobile-first, WCAG AA, max 2 primary actions per screen.
Output: React functional components, one per variant, with comments marking decisions.
Variant styles: (1) minimal/clean, (2) warm/approachable, (3) information-dense.
```

```
Critique this generated UI component for: (1) WCAG AA contrast failures, (2) missing ARIA attributes,
(3) violations of [brand style guide summary], (4) deprecated React patterns.
Output: issues list with line references and specific fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `v0` CLI | Generate React components from text prompts | https://v0.dev/docs/cli |
| `shadcn/ui` CLI | Scaffold components from design system | npx shadcn@latest add |
| `storybook` CLI | Preview and document generated components | npx storybook@latest init |
| `axe-cli` | Accessibility audit on generated HTML | npm i -g axe-cli |
| `prettier` | Normalize generated code formatting | npm i -g prettier |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| v0 by Vercel | SaaS | Yes (API) | REST API for component generation; output is React/TSX |
| Claude Artifacts | SaaS | Yes (native) | Claude generates interactive HTML/React in-context |
| Galileo AI | SaaS | No | No public API; browser-only generation |
| Uizard | SaaS | No | No headless API; browser-based |
| Relume | SaaS | No | Figma plugin + browser; no API |
| Locofy.ai | SaaS | No | Figma-to-code; no generation API |
| Builder.io | SaaS | Partial | Visual CMS with AI generation; REST API for content, not generation |

## Templates & scripts
Generate multiple UI variants via Claude API in a single batch:

```python
import anthropic

client = anthropic.Anthropic()

VARIANTS = ["minimal", "warm-approachable", "information-dense"]

def generate_ui_variant(screen_brief: str, variant_style: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": (
                f"Generate a React functional component for: {screen_brief}.\n"
                f"Style: {variant_style}. Mobile-first. WCAG AA. Tailwind CSS.\n"
                "Output only the component code, no explanation."
            )
        }]
    )
    return response.content[0].text

for style in VARIANTS:
    code = generate_ui_variant("email verification screen, step 2 of onboarding", style)
    with open(f"variant_{style.replace('-','_')}.tsx", "w") as f:
        f.write(code)
    print(f"Written: variant_{style}.tsx")
```

## Best practices
- Treat generated UI as a rough draft that costs ~0 and deserves ~0 reverence — critique aggressively
- Always run `axe-cli` or equivalent on generated HTML before presenting to stakeholders
- Pin design tokens explicitly in every prompt — without them, AI defaults to generic Bootstrap-esque aesthetics
- Generate in batches of 3–5 variants, not 1 — single-variant generation anchors too early
- Keep generated components isolated from production codebase until manually reviewed and refactored
- Document AI-generated components with a `// AI-generated — review before production` comment

## AI-agent gotchas
- Agents generating code will hallucinate library APIs (especially for newer React versions or niche component libraries); always test generated code in a sandbox before accepting
- WCAG compliance prompts produce code that looks accessible but often has broken focus order or missing live regions — automated axe audit is mandatory
- Design brief ambiguity amplifies in generation: "modern" means different things every run; add concrete style references
- Agents tend to propose complex component trees; generated code often violates design system composition rules silently

## References
- https://v0.dev/docs (v0 by Vercel)
- https://www.usegalileo.ai/ (Galileo AI)
- https://www.nngroup.com/articles/generative-ui/ (NNGroup on generative UI)
- https://www.w3.org/WAI/WCAG21/quickref/ (WCAG 2.1 quick reference)
- https://uxtools.co/ai-design-survey/ (AI design tools survey)
