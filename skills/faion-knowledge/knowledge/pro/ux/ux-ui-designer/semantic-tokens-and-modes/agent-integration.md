# Agent Integration — Semantic Tokens and Modes

## When to use
- Adding light/dark/high-contrast modes to an existing token system without forking the codebase.
- Multi-brand or white-label products where one component library serves several visual identities.
- Multi-platform builds (web + iOS + Android) that must share semantic intent but diverge in raw values (e.g., padding, type scale).
- Density modes (compact / comfortable) for data-dense enterprise UIs.
- Migrating from raw CSS custom properties to a tokens-as-source-of-truth pipeline (Figma Variables → Style Dictionary → CSS/Swift/Compose).

## When NOT to use
- A single-theme product with no foreseeable theming requirement; semantic-token plumbing adds indirection without payoff.
- Pure marketing campaigns or one-off pages that are not part of the system.
- Component libraries below ~30 components — overhead exceeds savings.
- For motion / animation primitives — semantic naming for durations rarely earns its keep.

## Where it fails / limitations
- Naming debates dominate; "surface.primary" vs "background.canvas" with no governance leads to bikeshedding and forks.
- Modes proliferate (light, dark, high-contrast, brand-A, brand-B, density, RTL...) and the matrix becomes unmanageable past 3 dimensions.
- Figma Variables modes do not map 1:1 to platform features (no native "high-contrast" variable on iOS); a translation layer is unavoidable.
- High-contrast mode often regresses in subsequent design changes because contributors edit the light mode in isolation.
- Reference tokens (raw palette) leaking into product code defeats the whole abstraction; lint rules are mandatory.

## Agentic workflow
Drive tokens through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS / Swift / Compose). Agents excel at stages 2-3 and at lint enforcement at stage 4. Use a subagent that pulls the Figma Variables API, validates collection / mode coverage (every semantic token must be defined in every mode), then runs Style Dictionary with platform-specific transforms. Keep semantic naming decisions in a human design council; agents propose, humans ratify.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the Style Dictionary build in CI and opens PRs with the generated files.
- A purpose-built `token-coverage` subagent that reads exported Figma JSON, asserts that for each token in collection `Colors`, both `Light` and `Dark` modes have a value, and fails the build with the missing list.
- A `token-lint` subagent that scans source files for forbidden raw hex values and direct references to reference (palette) tokens, suggesting the semantic equivalent.
- `faion-improver` — periodic mode coverage audit ("does every semantic token have a value in every mode?").

### Prompt pattern
"Given `figma-variables.json` exported from collection `Colors` with modes `Light, Dark, HC`, list semantic tokens missing in any mode. Propose a value for the missing mode using WCAG-AA contrast against the corresponding `surface.*` token in that mode. Do not invent reference tokens; reuse existing palette."

"Convert `tokens/semantic.json` to `style-dictionary` config that emits `tokens.css` with `[data-theme='dark'] { ... }` blocks per mode and `tokens.swift` with a `Color.Theme` struct."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Style Dictionary | Cross-platform token build | `npm i -D style-dictionary` — https://styledictionary.com |
| Theo (Salesforce) | Older but stable token transformer | https://github.com/salesforce-ux/theo |
| Tokens Studio CLI | Sync Figma Variables ↔ JSON | https://tokens.studio |
| Specify CLI | Token distribution from design source to repo | https://specifyapp.com |
| `terrazzo` (formerly cobalt-ui) | DTCG-spec token build | https://terrazzo.dev |
| Figma REST API | Pull Variables programmatically | https://www.figma.com/developers/api#variables |
| `stylelint-design-tokens` | Lint raw values in CSS | `npm i -D stylelint-design-tokens` |
| `eslint-plugin-design-tokens` | Lint hardcoded values in JS/TS | https://github.com/microsoft/eslint-plugin-design-tokens |
| `themer` | Generate quick palettes for prototypes | https://github.com/mjswensen/themer |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Figma Variables | SaaS | Yes (REST API) | De facto authoring source for modes |
| Tokens Studio | SaaS / Figma plug-in | Yes (CLI + JSON Git sync) | Multi-mode authoring + GitHub PRs |
| Supernova.io | SaaS | Yes (REST API + CLI) | Pulls Figma, transforms, publishes |
| Specify | SaaS | Yes (CLI) | Token distribution and webhooks |
| zeroheight | SaaS | Partial | Publishes token tables to docs |
| Penpot | OSS | Limited | Open-source authoring; tokens improving |
| Style Dictionary OSS | OSS | Yes | Reference build pipeline |
| Knapsack | SaaS | Yes | Multi-system + multi-brand pipelines |
| Backlight | SaaS | Yes | Token + component monorepo |
| Adobe Express variables | SaaS | Limited | Marketing / brand only |

## Templates & scripts
See `templates.md` and `examples.md` for token JSON shapes, mode tables, and DTCG-compliant structure.

Inline mode-coverage check (CI gate):

```javascript
// check-modes.mjs — fail build if any mode is missing a semantic token
import { readFileSync } from 'node:fs';
const tokens = JSON.parse(readFileSync('tokens/semantic.json', 'utf8'));
const REQUIRED_MODES = ['light', 'dark', 'hc'];
const missing = [];
function walk(node, path = []) {
  if (node && typeof node === 'object') {
    if ('$value' in node) {
      const v = node.$value;
      const modes = (v && typeof v === 'object' && !Array.isArray(v)) ? Object.keys(v) : [];
      const lacks = REQUIRED_MODES.filter(m => !modes.includes(m));
      if (lacks.length) missing.push({ token: path.join('.'), missing: lacks });
      return;
    }
    for (const [k, child] of Object.entries(node)) walk(child, [...path, k]);
  }
}
walk(tokens);
if (missing.length) {
  console.error(JSON.stringify(missing, null, 2));
  process.exit(1);
}
```

## Best practices
- Maintain three layers explicitly: **reference** (palette / scale), **system** (semantic, mode-aware), **component** (component-scoped). Forbid jumping from component → reference.
- One semantic token = one intent. Resist "primary" doing duty for both action colour and brand colour; split into `action.primary` and `brand.primary`.
- Co-locate the token's accessibility intent in metadata (`$extensions.contrastPair`); contrast is a property of the token, not a reviewer's memory.
- Generate platform output (`tokens.css`, `tokens.swift`, `tokens.compose.kt`) — never hand-write per platform.
- Adopt the W3C Design Tokens Community Group format (DTCG / `$value`, `$type`) so tooling stays interoperable.
- Add a `data-theme` attribute switcher rather than separate stylesheets; eases mid-page mode previews.
- Treat brand modes as data, not code — a new white-label tenant should be a config row, not a deploy.
- Snapshot every mode in visual regression (Chromatic / Percy) — broken dark mode is the most common token-system regression.

## AI-agent gotchas
- Agents that "add a token" love to mint new reference colours instead of reusing the palette; lint must reject reference duplicates.
- LLMs invent contrast pairs without checking math; always pair token suggestions with a calculated WCAG ratio.
- Mode-explosion: an agent asked to "add brand B" may duplicate every token instead of overlaying only the deltas — require a `mode = override` diff.
- Style Dictionary configs generated by agents frequently miss platform-specific transforms (e.g., `size/pxToPt` for iOS); pin a known-good config.
- Figma Variables REST API has shape gotchas (alias resolution); agents must follow `valuesByMode[modeId]` rather than the top-level value.
- Agents tend to write CSS like `var(--color-blue-500)` directly in components; lint must redirect to `var(--action-primary)` semantic tokens.
- Auto-renamed tokens by an agent break consumer code unless paired with a codemod and a deprecated alias for ≥1 minor version.

## References
- W3C Design Tokens Community Group spec — https://tr.designtokens.org/format/
- Figma "Guide to variables" — https://help.figma.com/hc/en-us/articles/15339657135383
- Nathan Curtis — *Naming Tokens in Design Systems* — https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676
- Adobe Spectrum tokens — https://spectrum.adobe.com/page/design-tokens/
- Material Design 3 token system — https://m3.material.io/foundations/design-tokens/overview
- Style Dictionary architecture — https://styledictionary.com/info/architecture/
