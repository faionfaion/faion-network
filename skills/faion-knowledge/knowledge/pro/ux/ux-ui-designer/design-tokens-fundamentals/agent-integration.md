# Agent Integration — Design Tokens Fundamentals

## When to use
- Bootstrapping a new design system that must ship to web, iOS, Android, and possibly visionOS / Quest UI.
- Migrating from ad-hoc CSS variables / Tailwind config to a single source of truth.
- Adding dark/light/high-contrast modes after a product is already shipping.
- Designer–developer round-trip workflows where Figma values drift from code values.
- Multi-brand white-label products that need theme swaps without rebuild.

## When NOT to use
- Single-page MVP with one designer/developer — overhead exceeds value until the product survives 3 months.
- Static marketing site with two pages — Tailwind defaults are fine.
- Throwaway internal tools with no design language target.
- Projects where the team doesn't yet agree on naming (start with semantic discussion, then tokens).

## Where it fails / limitations
- Token sprawl: teams reach 1,500+ tokens and can't find any of them; without governance, naming collapses.
- Pure primitive layer leaks into components ("color.blue.500" everywhere) and theming becomes impossible.
- Cross-platform output diverges silently — fonts, line-heights, and elevation translate poorly to iOS/Android.
- Figma Variables ↔ JSON sync is still fragile; renaming on either side breaks the other.
- Animation, motion, and shadow tokens are weakly standardized — most teams hand-roll them.

## Agentic workflow
Use agents to (a) generate the initial 3-tier token JSON (primitive → semantic → component) from a design brief, (b) lint token files for naming and reference-cycle violations, (c) generate platform outputs (CSS variables, iOS/Android resources, Tailwind config) via Style Dictionary, and (d) audit existing CSS for hardcoded values that should be tokenized. Human review for naming and the semantic layer is mandatory — names outlive everything.

### Recommended subagents
- `faion-sdd-executor-agent` — implements Style Dictionary build + CI lint + per-platform outputs.
- `faion-usability-agent` — reviews semantic layer for naming clarity and accessibility (contrast pairing).
- `faion-ui-designer` (knowledge methodologies under `solo/ux/ui-designer`) — supplies the brand+component vocabulary the agent maps to.

### Prompt pattern
```
Generate W3C-format token JSON from this brief:
  brand: <name>
  primary_palette: <hex list>
  modes: [light, dark]
  scale: 4|8 px base
  type_scale: minor-third|major-third|perfect-fourth
  components_in_scope: [button, input, card]

Output 3 layers:
  1. primitive (raw values, no semantic names)
  2. semantic (alias only, contrast-paired)
  3. component (only for the listed components)
Validate WCAG 2.2 AA contrast for every text/background pair in semantic layer.
Emit DTCG (W3C Design Tokens Community Group) JSON.
```

```
Audit this CSS for hardcoded values that should be tokens.
Output JSONL: {file, line, value, suggested_token, reason}.
Skip values inside @keyframes, transition timing, and z-index.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Transform tokens to platform outputs (CSS, iOS, Android, Compose) | https://amzn.github.io/style-dictionary/ |
| `Tokens Studio CLI` | Sync Figma Variables ↔ JSON | https://tokens.studio |
| `theo` | Salesforce token transformer (alt to style-dictionary) | https://github.com/salesforce-ux/theo |
| `cosmiconfig` | Centralize token config across monorepos | https://github.com/cosmiconfig/cosmiconfig |
| `chromatic` | Visual regression on token-driven components | https://www.chromatic.com |
| `axe-cli` | A11y contrast check against tokenized themes | https://github.com/dequelabs/axe-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma) | SaaS + plugin | Yes — JSON export | Most complete designer side. |
| Specify | SaaS | Yes (REST + CLI) | Centralizes tokens + assets across tools. |
| Supernova | SaaS | Yes (REST) | Documentation site + token sync. |
| Knapsack | SaaS | Partial | Design-system platform with token UI. |
| Style Dictionary | OSS | Yes (CLI/JS) | The build-step foundation. |
| Figma Variables | SaaS | Partial (REST API beta) | Native, but plugin ecosystem still maturing. |

## Templates & scripts
See `templates.md` for 3-tier JSON skeleton. Inline contrast lint:

```js
// token-contrast.mjs — fail CI if any semantic text/bg pair < 4.5:1
import tokens from "./tokens.json" assert { type: "json" };
import { hex, score } from "wcag-contrast";

const sem = tokens.color.semantic;
const fails = [];
for (const [name, pair] of Object.entries(sem.pairs ?? {})) {
  const fg = pair.fg.value, bg = pair.bg.value;
  const ratio = hex(fg, bg);
  const required = pair.size === "large" ? 3 : 4.5;
  if (ratio < required) fails.push({ name, fg, bg, ratio });
}
if (fails.length) {
  console.error(JSON.stringify(fails, null, 2));
  process.exit(1);
}
```

## Best practices
- Three layers, no exceptions: primitive → semantic → component. Components reference semantic, never primitive.
- Name semantic tokens by purpose, not appearance: `color.text.muted`, not `color.gray.600`.
- Pair every semantic foreground with its background; lint contrast in CI.
- Version tokens via SemVer; treat token rename as a breaking change with a migration codemod.
- Generate component tokens only for the components that actually need them; resist creating pre-emptively.
- Treat tokens as a published package with a changelog. Consumers depend on its stability.

## AI-agent gotchas
- LLMs love overly granular tokens (`color.button.primary.hover.background.disabled`). Pin a depth limit (≤4 levels).
- Generated tokens often skip the semantic layer entirely; force a 3-tier output schema.
- Hex/rgba conversions and OKLCH transforms produce slightly off colors silently. Round-trip and assert exact match.
- W3C DTCG schema evolves; agents may emit obsolete `value` shape vs. `$value`. Validate against current schema.
- Dark-mode inversions are not algorithmic; agents that "auto-derive dark theme" produce poor contrast. Hand-tune.
- Cross-platform unit conversion (px → dp/sp on Android, pt on iOS) needs a transform; LLMs will paste px everywhere.

## References
- W3C Design Tokens Community Group, *Design Tokens Format Module*. https://design-tokens.github.io/community-group/format/
- Amazon, *Style Dictionary Documentation*. https://amzn.github.io/style-dictionary/
- Brad Frost, *Design Tokens chapter — Atomic Design*.
- Nathan Curtis, *Tokens in Design Systems* series. https://medium.com/eightshapes-llc/tagged/design-systems
- Figma, *Variables Documentation*. https://help.figma.com/hc/en-us/articles/15145852043927
- Tailwind Labs, *Theme as Tokens* — practical CSS-variable token patterns.
