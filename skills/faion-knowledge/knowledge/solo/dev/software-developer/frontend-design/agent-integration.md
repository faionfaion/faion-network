# Agent Integration — Frontend Design

## When to use
- Greenfield frontend (landing, dashboard, marketing site) where visual direction is open.
- Component library bootstrap before product features land (storybook.faion.net pattern).
- Rebrand / redesign passes that need 3-5 explored variants before committing.
- Solopreneur-scale projects (faion.net portfolio sites: ruslan, viktoria, art) — designer + dev are the same person + agents.
- Translating brand brief or PRD into concrete tokens (colors, type scale, spacing) and components.

## When NOT to use
- Active production UI with established design system — variant brainstorming is wasted; iterate on tokens instead.
- Pure backend or CLI projects.
- Brownfield refactors where scope is "make this page faster", not "redesign".
- Native mobile (iOS/Android) — patterns assume web (HTML/CSS/JSX); use platform-native tools.
- Engineering-driven internal admin tools where utility outweighs aesthetics.

## Where it fails / limitations
- Brainstormer agents over-index on visual novelty — outputs trendy variants that don't match brand voice.
- Tokens defined post-hoc (after components exist) — drift between Figma/CSS/Storybook is constant.
- Storybook setup churn — versions 6/7/8 differ; agents pull stale tutorials.
- A11y is afterthought — variants ship with poor color contrast, missing focus states; needs explicit a11y gate.
- Screenshots help LLMs plan but they hallucinate pixel-perfect details — request rendered HTML diffs, not vibes.
- Cross-browser quirks (Safari) absent from headless Chromium previews.
- "5 variants" without strict differentiation rule produces 5 minor variations of the same thing.

## Agentic workflow
Drive design as: (1) `AskUserQuestion` to fix type/style/tech, (2) brainstormer agent emits 3-5 **truly distinct** variants (different layout, not different colors), (3) each variant lives in `designs/variant-N-name/` as runnable HTML/JSX, (4) human picks 1, (5) refine via `frontend-design` skill iteratively, (6) `faion-storybook-agent` scaffolds Storybook + design tokens, (7) `faion-frontend-component-agent` produces components one at a time. Always render variants to actual screenshots (Playwright) and feed back to LLM for selection — text-only review misses obvious problems.

### Recommended subagents
- `faion-frontend-brainstormer-agent` — diverge phase, emits N variants with rationale.
- `faion-storybook-agent` — Storybook scaffold + tokens + a11y addons.
- `faion-frontend-component-agent` — component + story + tests under SDD gates.
- `faion-browser-agent` — render variants to PNG, runs visual regression.
- `faion-software-architect-agent` — picks framework / tooling stack when ambiguous.

### Prompt pattern
```
Brief: <copy from .product/brief.md>. Tech: React+TS+Tailwind. Style: minimalist.
Generate 5 DISTINCT layout variants. Each must differ in:
(a) primary navigation pattern, (b) hero composition, (c) information density.
Output to designs/variant-{1..5}-<name>/index.html with inline tokens.
After each, run Playwright screenshot at 1440x900 + 375x812.
Show me screenshot grid. Do not iterate yet.
```

```
Refine designs/variant-3-grid/. Target a11y AA: contrast >= 4.5,
visible focus rings, semantic landmarks. Re-screenshot.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx storybook init` | Scaffold Storybook in any framework | https://storybook.js.org |
| `npx storybook build` | Static Storybook (already used at storybook.faion.net) | bundled |
| `style-dictionary` | Compile tokens.json → CSS/SCSS/JS/iOS/Android | npm i -D style-dictionary |
| `npx tailwindcss` | Tailwind compile + JIT | https://tailwindcss.com |
| `figma-rest` / `figma-tokens` | Sync Figma tokens to repo | various |
| `playwright` | Visual regression, screenshot diff | npm i -D @playwright/test |
| `axe-core` / `pa11y` | A11y audit CLI | npm i -g pa11y |
| `chromatic` | Visual review SaaS for Storybook | npm i --save-dev chromatic |
| `lhci` (Lighthouse CI) | Perf / a11y / best-practice budget gates | npm i -g @lhci/cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma + Dev Mode | SaaS | partial (REST API) | Source of truth for tokens; agent reads via `figma-rest`. |
| Penpot | OSS | yes (API) | Self-hostable Figma alternative; faion-stack friendly. |
| Chromatic | SaaS | yes (CLI) | Visual diffs on Storybook PRs. |
| v0.dev (Vercel) | SaaS | yes (chat → JSX) | Generates React components; useful for variant gen. |
| shadcn/ui | OSS (templates) | yes (CLI: `npx shadcn add`) | Copy-paste primitive components; perfect for solo. |
| Tailwind UI | SaaS (license) | yes | Premium component snippets. |
| Builder.io | SaaS | yes | Visual page builder + code export. |
| Storybook (self-hosted) | OSS | yes | Already at storybook.faion.net. |
| Galileo AI / Uizard | SaaS | partial | Sketch → mockup; weak for code gen. |

## Templates & scripts
See `templates.md` for tokens scaffold + Storybook config. Inline variant comparison helper:

```bash
#!/usr/bin/env bash
# scripts/render-variants.sh — render all design variants to PNG for review
set -euo pipefail
ROOT="${1:-designs}"
OUT="${2:-.tmp/variants}"
mkdir -p "$OUT"

for variant in "$ROOT"/variant-*/; do
  name=$(basename "$variant")
  for size in "1440x900" "375x812"; do
    npx playwright screenshot \
      --viewport-size="$size" \
      --wait-for-timeout=500 \
      "file://$(realpath $variant/index.html)" \
      "$OUT/${name}-${size}.png"
  done
done

# Stitch grid for review (requires imagemagick)
montage "$OUT"/*-1440x900.png -tile 3x -geometry +5+5 "$OUT/grid-desktop.png"
montage "$OUT"/*-375x812.png  -tile 3x -geometry +5+5 "$OUT/grid-mobile.png"

echo "review: $OUT/grid-desktop.png $OUT/grid-mobile.png"
```

## Best practices
- Tokens first, components second; never let components define their own colors.
- Use `style-dictionary` (or W3C design-tokens format) — single JSON source compiles to all targets.
- Lock variants to **5 max**; more options = decision paralysis, not better outcome.
- Each variant must justify its existence in 2-3 sentences (`rationale.md`); kills lookalikes.
- Run a11y audit on every variant; reject those failing AA before showing to human.
- Co-locate stories with components (`Button.tsx` + `Button.stories.tsx`).
- Use Storybook a11y addon (`@storybook/addon-a11y`) — surfaces violations during review.
- Pin Storybook + Tailwind versions; updates routinely break CSS isolation.
- Brand voice → tone → tokens → components — top-down. Bottom-up component-first builds drift.
- Capture decisions in `designs/DECISIONS.md` so the next iteration knows why variant-2 was rejected.

## AI-agent gotchas
- LLMs default to "modern minimalist with gradient hero" — explicitly forbid clichés in the prompt.
- Variant rationales tend to all sound the same; ask for distinctness criteria upfront.
- Agents copy Tailwind class soup without abstracting tokens — break out colors/spacing first, then components.
- Storybook story files generated by LLMs use outdated CSF format; pin to CSF3 + Storybook 8.
- Visual quality cannot be judged from code alone — always render to screenshot before shipping; LLM "looks good" reviews of code are unreliable.
- Agents producing JSX often hardcode hex colors instead of CSS vars / token references — add lint rule (`stylelint`, custom) to forbid raw colors.
- A11y: agents add `aria-label` on already-accessible elements (icon button has visible text) and skip it on icon-only buttons. Run `pa11y` on each variant.
- Human-in-loop checkpoint: variant selection — design choice is taste, not logic. Agent ranks but human picks.
- Component library scope creep: agents implement 30 components when you need 8. Maintain explicit `components-needed.md` list and refuse new ones.

## References
- Storybook docs (CSF3) — https://storybook.js.org/docs/writing-stories
- W3C Design Tokens spec — https://www.w3.org/community/design-tokens/
- Tailwind CSS docs — https://tailwindcss.com/docs
- shadcn/ui — https://ui.shadcn.com
- Anthropic computer-use + UI gen — https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- Material Design 3 system — https://m3.material.io
- Inclusive Components — https://inclusive-components.design
- A11y patterns: WAI-ARIA APG — https://www.w3.org/WAI/ARIA/apg/
