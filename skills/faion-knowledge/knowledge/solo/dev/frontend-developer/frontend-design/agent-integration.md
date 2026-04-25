# Agent Integration — Frontend Design

## When to use
- Starting a new UI surface (landing, dashboard, form, component set) where multiple visual directions need exploration before committing.
- Solo dev or small team where you want LLMs to produce 3–5 diverging design variants instead of one safe answer.
- You already have requirements (purpose, audience, brand) but not visual decisions; brainstorming variants accelerates kickoff.
- Storybook is the deliverable shape — you want each variant explorable in isolation.

## When NOT to use
- Existing product with a mature design system; converging is more important than diverging.
- One-off internal tool where any reasonable UI suffices.
- Marketing pages where copy + photography drive design more than component patterns.
- Strict brand guideline enforcement; variant exploration generates ineligible options.

## Where it fails / limitations
- LLM "design variants" tend to converge on the same SaaS aesthetic; force constraints (era, mood, density, typography) to break the average.
- Generated CSS often ignores responsive breakpoints unless the prompt enumerates them.
- Without a Storybook scaffold, variants live as orphan HTML files no one revisits.
- The 3–5-variant ceiling is a UX choice; more options paralyze human selection — do not raise the count.
- Refinement loops can drift from the original requirements; pin the spec doc and re-quote it each iteration.

## Agentic workflow
Four-phase loop driven by `faion-frontend-brainstormer-agent`, `faion-storybook-agent`, and `faion-frontend-component-agent` (referenced in this methodology's `README.md`). (1) Capture requirements via `AskUserQuestion`. (2) Brainstorm 3–5 distinct variants in `designs/variant-N-<name>/` — each must justify its aesthetic and ship working code. (3) User picks one; refinement subagent iterates against feedback. (4) Storybook subagent builds stories for the chosen direction; component subagent finalizes typed components. Persist the chosen variant's tokens to `tailwind.config` or `globals.css` so future agents inherit them.

### Recommended subagents
- `faion-frontend-brainstormer-agent` — produce 3–5 distinct visual directions per request (referenced in this skill; create from `frontend-design/templates.md` if absent).
- `faion-storybook-agent` — scaffold Storybook + stories for each chosen variant.
- `faion-frontend-component-agent` — convert HTML mocks into typed React components with stories.
- `faion-sdd-executor-agent` — run quality gates (a11y, lint, typecheck) before committing.

### Prompt pattern
```
Brainstorm 3–5 DISTINCT design variants for: <requirements>.
Tech: <React+TS|HTML/CSS|Vue|Next.js>. Style direction: <Minimalist|Bold|Corporate|Playful>.
Each variant must:
- Have a unique aesthetic identity (typography, density, color, motion).
- Ship working code under designs/variant-{N}-{name}/.
- Include rationale (problem solved, audience fit, trade-offs).
- Avoid converging — explicitly contrast the variants in a comparison table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` | Story scaffolding for variants | `npx storybook@latest init` |
| `figma-export` / `figma-to-react` | Pull design tokens / HTML | `npm i -D @figma-export/cli` |
| `svgo` | Optimize SVGs in mocks | `npm i -D svgo` |
| `playwright` | Visual regression across variants | `npm init playwright@latest` |
| `axe-core` / `@axe-core/cli` | A11y audit on each variant | `npm i -D @axe-core/cli` |
| `lighthouse` | Perf + a11y score per variant | `npm i -D lighthouse` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| v0.dev | SaaS | Yes (chat + API) | Generates shadcn/ui-style React for variants |
| Figma | SaaS | Yes (REST + Plugin API) | Source of constraints + tokens |
| Penpot | OSS | Yes (REST API) | Self-hosted alternative to Figma |
| Chromatic | SaaS | Yes | Visual regression of variants |
| Storybook Cloud | SaaS | Yes | Hosted previews per variant |
| Linear / Notion | SaaS | Yes | Persist requirements + decisions |

## Templates & scripts
See `templates.md` and `examples.md`. Helper to scaffold a variant directory:

```bash
#!/usr/bin/env bash
# scripts/new-variant.sh <slug>
set -euo pipefail
slug="${1:?slug required}"
n=$(printf '%02d' "$(($(ls designs 2>/dev/null | grep -c '^variant-') + 1))")
dir="designs/variant-${n}-${slug}"
mkdir -p "$dir"
cat > "$dir/README.md" <<EOF
# Variant ${n} — ${slug}
## Rationale
- Audience fit: …
- Aesthetic levers: …
- Trade-offs: …
## Files
- index.html — runnable preview
- tokens.css — variant-local tokens
EOF
echo "Created $dir"
```

## Best practices
- Force diversity: prompt explicitly bans variants from sharing typeface, density tier, or palette family.
- Persist tokens (color, type scale, spacing) per variant in a local `tokens.css`; promote chosen tokens to global config only after selection.
- Run accessibility (axe) and Lighthouse on every variant before user selects — bad scores often eliminate options early.
- Keep variants runnable as static HTML or Storybook stories; reviewers must click, not read code.
- Capture the **why** for each variant in its README; design without rationale becomes orphan in 6 months.
- Limit to 3–5 variants; cognitive load past 5 leads to indecision.

## AI-agent gotchas
- LLMs default to one "safe" variant cloned 5×. Diversity must be enforced via explicit, contrastive constraints.
- Generated HTML often hardcodes English copy and pixel widths; require tokens (rem/em) and i18n placeholders.
- Refinement chats accumulate token bloat; reset context per refinement and pass only the chosen variant's files.
- Agents tend to skip a11y until the end; run axe per variant in the brainstorm phase, not after selection.
- The recommended subagents (brainstormer, storybook, component) may not exist in `agents/` yet — create them from `templates.md` or fall back to ad-hoc Task() calls with the prompts above.
- Variants get committed and never cleaned up; add a `designs/` cleanup step on PR merge so the repo does not bloat.

## References
- https://www.designsystems.com/
- https://storybook.js.org/docs
- https://v0.dev/
- https://www.figma.com/developers/api
- https://playwright.dev/docs/test-snapshots
