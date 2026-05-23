# Agent Integration — Design Tokens

## When to use
- Building or refactoring a design system that ships to web + mobile + email
- Introducing dark mode / theming / white-label without forking components
- Bridging a Figma file to code so designers and engineers stop drifting
- Standardizing brand across multiple apps in a monorepo
- Letting LLM agents pick visual values from a constrained vocabulary instead of hex literals

## When NOT to use
- Single one-off marketing page — overhead beats payoff
- Apps that fully hand off to a UI library (Material, Mantine) and never re-skin — use the lib's theme API directly
- Prototype work where designers iterate hourly — token churn will outpace pipeline cost
- Pure server-rendered emails using an external template SaaS that owns its tokens

## Where it fails / limitations
- Token explosion: 800+ tokens you can't `grep` for. Need lifecycle (deprecate / merge / split) before you cross 200
- "Semantic" naming collapses when product surfaces grow (marketing vs app vs admin all want different "primary")
- Designer-engineer feedback loops break if Figma → tokens → code is not automated; manual sync rots fast
- Dark/light parity bugs: tokens get dark variants but components hardcode light ones; visual regression tests are mandatory
- Accessibility: tokens don't enforce contrast — agents pair `text-primary` on `bg-secondary` without checking ratios
- Cross-platform pipeline (Style Dictionary, Tokens Studio) has many moving parts; agents skip parts and ship inconsistent outputs

## Agentic workflow
A token agent maintains the canonical JSON, runs Style Dictionary to emit per-platform outputs (CSS vars, JS const, Tailwind config, iOS/Android), and runs a contrast-check pass on every semantic pairing. A second agent watches Figma via the Tokens Studio plugin or Variables API and proposes a PR diff for the JSON. A reviewer agent checks naming rules and flags dead tokens.

### Recommended subagents
- `faion-sdd-executor-agent` — design + implement + verify with visual regression as quality gate
- A custom `token-linter` (haiku) — enforces naming rules and detects unused tokens via repo grep
- A custom `contrast-auditor` (sonnet) — reads semantic pairings (`text-primary` on `bg-primary`) and runs WCAG 2.2 contrast math
- A custom `figma-syncer` (sonnet) — pulls Figma Variables → emits JSON diff PR

### Prompt pattern
```
Audit tokens/ in this repo:
- list primitive vs semantic vs component tiers
- find primitives referenced 0 times (dead tokens)
- find semantic pairings whose contrast < 4.5:1 for body text
- propose rename PR: any name containing a value (e.g. blue-500 used as semantic)
Output: report.md + suggested diff. Do not auto-apply.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Compile token JSON to per-platform outputs | `npm i -D style-dictionary` · https://styledictionary.com |
| `token-transformer` | Tokens Studio → Style Dictionary bridge | `npm i -D token-transformer` |
| `terrazzo` (formerly Cobalt) | Modern token compiler with W3C DTCG support | https://terrazzo.app |
| `theo` | Salesforce's token compiler (legacy but stable) | https://github.com/salesforce-ux/theo |
| `figma-tokens` / Tokens Studio plugin | Authoring tokens inside Figma | https://tokens.studio |
| `axe-core` / `pa11y` | A11y/contrast checks against rendered components | https://github.com/dequelabs/axe-core |
| `chromatic` / `loki` / `playwright` | Visual regression for theme switches | https://www.chromatic.com |
| `tailwindcss` | Consume token JSON via `tailwind.config` | https://tailwindcss.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma plugin) | SaaS | Yes | Has REST/Sync API; agents can read JSON exports |
| Specify | SaaS | Yes | Token sync platform with API |
| Supernova | SaaS | Yes | Design system platform; CLI for export |
| Knapsack | SaaS | Partial | Design system docs; less agent-driven |
| Storybook + addon-themes | OSS | Yes | Theme-switch playground + docs |
| Chromatic | SaaS | Yes | CI gate for theme regressions |
| GitHub Actions | SaaS | Yes | Run Style Dictionary on every PR; commit generated outputs |

## Templates & scripts
See `templates.md` for full Style Dictionary config. Inline minimal pipeline that emits CSS vars + JS const from `tokens/`:

```js
// build-tokens.mjs
import StyleDictionary from 'style-dictionary';
const sd = new StyleDictionary({
  source: ['tokens/primitive.json', 'tokens/semantic.json'],
  platforms: {
    css:  { transformGroup: 'css', buildPath: 'dist/css/',
            files: [{ destination: 'tokens.css', format: 'css/variables' }] },
    js:   { transformGroup: 'js',  buildPath: 'dist/js/',
            files: [{ destination: 'tokens.js', format: 'javascript/es6' }] },
    ios:  { transformGroup: 'ios-swift', buildPath: 'dist/ios/',
            files: [{ destination: 'Tokens.swift', format: 'ios-swift/class.swift', className: 'Tokens' }] },
  },
});
await sd.buildAllPlatforms();
```

```yaml
# semantic with dark theme override pattern
{
  "color": {
    "bg": {
      "primary": { "value": "{color.gray.50}",  "$extensions": {"theme": {"dark": "{color.gray.900}"}} }
    }
  }
}
```

## Best practices
- Three tiers, not two: primitive → semantic → component. Mixing primitive into components hides drift
- Forbid value-bearing names in semantic tokens (`color-primary` not `color-blue-500-primary`)
- One source of truth — the JSON. Figma is a view onto it, not the truth itself
- Generate, don't write: CSS variables, Tailwind config, and platform constants are build outputs, not source files
- Run contrast checks in CI for every semantic `text-on-bg` pairing; block PRs that drop below WCAG 2.2 AA
- Visual-regression test the theme switch path; tokens that look right alone often clash in composition
- Version the token package separately (`@org/tokens@x.y.z`) so consumers can adopt at their own pace; semver carefully
- Mark deprecations in JSON with `"$deprecated": "use color.bg.primary"`; lints can refuse new usages while letting old code compile

## AI-agent gotchas
- Agents create new tokens instead of reusing — require a "search before add" rule with `rg` against the JSON
- LLMs invent semantic names that bake in values (`color-blue-action`) — token-linter must reject
- Agents change a primitive value to "fix" a single component, breaking N other consumers — require ownership review per primitive
- Agents skip dark-mode entries, leaving theme parity gaps; CI must require both light and dark for every semantic key
- Tailwind: agents bypass tokens by writing `bg-[#3b82f6]` arbitrary values — lint with `eslint-plugin-tailwindcss` `no-custom-classname`
- Human-in-loop checkpoint: any change to brand-tier primitives (logo color, brand blue) must require explicit design owner approval
- Agents forget to regenerate platform outputs on token edits — make Style Dictionary build a pre-commit hook

## References
- https://styledictionary.com
- https://tr.designtokens.org/format/ — W3C Design Tokens Community Group format
- https://www.designtokens.dev
- https://tokens.studio
- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum
- https://primer.style/foundations/design-tokens — GitHub Primer reference
- https://spectrum.adobe.com/page/design-tokens — Adobe Spectrum reference
