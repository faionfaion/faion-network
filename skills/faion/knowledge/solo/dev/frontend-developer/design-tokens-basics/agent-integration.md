# Agent Integration — Design Tokens Basics

## When to use
- Starting a design system from scratch — define primitive → semantic → component token tiers before writing components.
- Migrating ad-hoc CSS variables / hex values to a single source of truth (`tokens.json` or W3C Design Tokens Format Module).
- Setting up theming (light/dark, brand white-label) where switching only the semantic layer is enough.
- Bridging Figma variables and code via Tokens Studio + Style Dictionary.

## When NOT to use
- One-off project with a single brand and no theming — direct CSS variables suffice.
- The entire app is built with Tailwind and the team is happy with `tailwind.config.ts` as the de facto token layer — adding Style Dictionary on top is duplicate work.
- The product is in pre-PMF iteration — token churn will be brutal and the abstraction slows experiments.

## Where it fails / limitations
- Naming the semantic layer is the hardest part and gets stale: `color.primary` vs `color.brand.primary` vs `color.action.default` — every team picks differently and migrations are painful.
- Figma variables and Tokens Studio diverge on resolution rules; round-tripping breaks aliases.
- Style Dictionary v3 changed config from JS to JSON in some flows; agents copying v2 examples produce broken builds.
- W3C Design Tokens Format Module is still a Working Group note (2024-2026); tooling implements partial subsets.
- Component tokens explode in count quickly — 20 components × 5 states × 3 themes = 300 tokens; without naming discipline they become unmaintainable.

## Agentic workflow
Run a "tokens architect" subagent that proposes the three-tier hierarchy from a Figma export or existing CSS audit. Commit primitives first, then semantics, then component tokens — each as its own PR with a Storybook page that renders the swatches. Use Style Dictionary to emit per-platform output (CSS vars, Tailwind config, JS module, iOS/Android if multi-platform). Keep human review on the semantic layer naming — it becomes the public design API.

### Recommended subagents
- `faion-brainstorm` — diverge/converge on naming for the semantic layer (e.g., `color.action.primary` vs `color.interactive.primary`).
- `faion-feature-executor` — once the hierarchy is decided, mechanical primitive/semantic/component generation per category.
- `faion-sdd-executor-agent` — full design-system bring-up where tokens are one of several deliverables.

### Prompt pattern
- "Given `tokens/primitive.json` (provided), propose a semantic layer for: action, surface, text, border, status (success/warn/danger/info). Output a JSON file referencing primitives by path. Naming must follow `category.role.state`."
- "Convert the existing `:root { --... }` CSS variables in `src/styles/globals.css` into a primitive `tokens/colors.json` and regenerate the CSS via Style Dictionary. Diff before/after must keep the rendered swatches identical."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm add -D style-dictionary` | Multi-platform token build (CSS, JS, Swift, XML) | https://styledictionary.com |
| `pnpm dlx @tokens-studio/sd-transforms` | Bridge Tokens Studio → Style Dictionary | https://github.com/tokens-studio/sd-transforms |
| `pnpm add -D @design-tokens/tokens-validator` | Validate W3C DTFM tokens | https://design-tokens.github.io/community-group/format/ |
| `npx terrazzo build` | Modern alternative to Style Dictionary, native TS | https://terrazzo.app |
| `npx tokens-studio sync` | Pull/push Figma tokens via the plugin's GitHub sync | https://docs.tokens.studio |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma plugin) | SaaS (free tier) + OSS bridge | Partial (GitHub sync) | Designers edit in Figma; agents pull JSON via the sync repo. |
| Specify | SaaS | Yes (REST + CLI) | Centralized token store with platform exports; replaces Style Dictionary if budget allows. |
| Knapsack | SaaS | Partial | Heavy enterprise tool; agent integration limited to docs export. |
| Style Dictionary | OSS | Yes | Default for code-first teams; trivial to script. |
| Terrazzo | OSS | Yes | Smaller, TS-native, supports W3C DTFM out of the box. |

## Templates & scripts
See `templates.md` for the primitive/semantic/component JSON shape. Minimal Style Dictionary build:

```js
// build-tokens.mjs
import StyleDictionary from 'style-dictionary';
StyleDictionary.extend({
  source: ['tokens/**/*.json'],
  platforms: {
    css:  { transformGroup: 'css', files: [{ destination: 'src/tokens.css', format: 'css/variables' }] },
    js:   { transformGroup: 'js',  files: [{ destination: 'src/tokens.ts',  format: 'javascript/es6'  }] },
    tw:   {
      transformGroup: 'js',
      files: [{ destination: 'tailwind.tokens.cjs', format: 'javascript/module-flat' }],
    },
  },
}).buildAllPlatforms();
```

## Best practices
- Three tiers, no more, no less. Skipping the semantic layer turns components into hex-code sponges; skipping component tokens hard-codes states across 50 files.
- Primitive names describe the value (`blue.500`, `space.4`); semantic names describe the role (`color.action.primary`); component names describe the slot (`button.bg.primary`).
- Number scales (50/100/.../900) must be perceptually uniform — borrow Tailwind's or Radix Colors' palette before rolling your own.
- Pin the token format to W3C Design Tokens Format Module ($value, $type, $description) so future tooling switches don't require migration.
- Keep token files atomic and reviewable — one PR per category change, never "rename 200 tokens" megacommits.

## AI-agent gotchas
- LLMs invent semantic names that don't appear in the project (`color.brand.fancy`); prompt them to read existing semantic tokens first.
- Agents often reference primitives by raw hex inside semantic layers (`{ "$value": "#3b82f6" }`) instead of the alias (`"{color.blue.500}"`), defeating the abstraction.
- When generating dark-mode tokens, agents flip lightness without checking contrast — pair every output with `axe-core` or a manual contrast check.
- Style Dictionary `transforms` are agent-hostile; agents pick `transformGroup: 'web'` (deprecated) instead of `'css'` / `'js'`.
- For Tailwind output, agents emit nested objects but Tailwind v3 expects flat `'color-action-primary'` keys at some layers — verify by running `tailwindcss build` after generation.
- W3C DTFM `$type` values are forgotten on numeric tokens (`spacing`, `dimension`); some tools error out without them.

## References
- W3C Design Tokens Format Module — https://design-tokens.github.io/community-group/format/
- Style Dictionary — https://styledictionary.com
- Tokens Studio for Figma — https://tokens.studio
- Radix Colors (perceptual scales) — https://www.radix-ui.com/colors
- Brad Frost, "Design Tokens" — https://bradfrost.com/blog/post/the-many-faces-of-design-tokens/
- Nathan Curtis, "Naming Tokens" — https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676
