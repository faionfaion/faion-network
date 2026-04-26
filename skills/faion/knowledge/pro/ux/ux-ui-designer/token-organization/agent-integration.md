# Agent Integration — Token Organization

## When to use
- Bootstrapping a new design system: setting the primitives → semantic → component hierarchy before writing the first token.
- Auditing a sprawling token set (>500 tokens) to collapse aliases, kill duplicates, and rename `blue-1` style primitives into semantic roles.
- Onboarding a second platform (mobile after web, or RN after native) and the existing names leak platform-specific assumptions.
- Preparing tokens for theming (light/dark/brand) — semantic layer is mandatory before mode switching is worth the effort.

## When NOT to use
- One-page marketing site with 8 colors and 3 font sizes. CSS variables in one file beat any token taxonomy here.
- Mid-flight design system rewrite where engineers are blocked. Renaming everything globally without a deprecation period destroys velocity.
- Without buy-in from at least one designer + one engineer. Naming wars without authority lead to abandoned conventions.

## Where it fails / limitations
- Component tokens explode without governance: every component dev wants their own `button.primary.padding.left.hover.large`.
- Semantic naming is hard for engineers without UX training; they default to color names (`blue`, `red`) instead of roles (`brand`, `danger`).
- Cross-team merges produce token forks: `color.surface.primary` vs `color.background.primary` — both correct, neither canonical.
- Hierarchy is only useful when tooling resolves aliases. Hand-managed Tailwind + CSS variables can drift silently from the JSON source.

## Agentic workflow
Use one subagent to inventory existing tokens (regex scan of CSS/SCSS, Tailwind config, Figma export), a second to cluster them by role using the three-tier hierarchy, and a third to emit a migration plan with deprecations, codemods, and a renamed token map. Force the agent to output a diff plan, not the new file directly — humans must approve the rename map before bulk rewrite.

### Recommended subagents
- `token-auditor` — counts tokens, finds duplicates, extracts naming patterns.
- `token-classifier` — assigns each token to primitive/semantic/component tier and proposes renames.
- `token-migration-planner` — outputs codemod + deprecation alias plan.

### Prompt pattern
```
Classify each token in tokens.json into one of: primitive, semantic, component.
Rules:
- primitive: raw value, no role context (e.g. blue-500, space-4).
- semantic: role-based, references a primitive (e.g. color.surface.primary).
- component: scoped to a component (e.g. button.padding.x).
Flag duplicates and naming inconsistencies. Output JSON with {token, tier, rename?, reason}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Resolve aliases, build outputs | `npm i -D style-dictionary@4` |
| `theo` | Salesforce token transformer (legacy) | `npm i -g theo` |
| `tokens-cli` (`@tokens-studio/sd-transforms`) | Tokens Studio bridge | https://docs.tokens.studio |
| `ts-prune` / `knip` | Find unused token exports in TS | `npm i -D knip` |
| `jq` | Inspect/transform token JSON | `apt install jq` |
| `eslint-plugin-design-tokens` | Lint hard-coded values vs tokens | https://github.com/zeroheight/eslint-plugin-design-tokens |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio for Figma | SaaS | Yes (sync to GitHub) | Best UX for organizing tiers visually. |
| Specify | SaaS | Yes (CLI/API) | Great for multi-source consolidation. |
| Supernova | SaaS | Partial | Good UI for hierarchies, weaker headless. |
| Zeroheight | SaaS | Limited | Documents tokens, doesn't enforce hierarchy. |
| Penpot | OSS | Partial | Newer token model, fewer integrations. |

## Templates & scripts
Inline classifier (≤40 lines) — heuristic but useful as a first pass before LLM review.

```js
// classify-tokens.mjs
import fs from "node:fs";
const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const flat = [];
const walk = (n, p = []) => {
  if (n && typeof n === "object") {
    if ("$value" in n) flat.push({ name: p.join("."), value: n.$value });
    else for (const [k, v] of Object.entries(n)) walk(v, [...p, k]);
  }
};
walk(data);
const isAlias = v => typeof v === "string" && /^\{.+\}$/.test(v);
const primitiveLike = /(^|\.)(blue|red|green|gray|neutral)-?\d+/i;
const componentLike = /^(button|input|card|modal|nav|chip|badge|tooltip)\./;
for (const t of flat) {
  let tier = "primitive";
  if (isAlias(t.value)) tier = "semantic";
  if (componentLike.test(t.name)) tier = "component";
  if (primitiveLike.test(t.name)) tier = "primitive";
  console.log(`${tier}\t${t.name}\t${typeof t.value === "string" ? t.value : "[obj]"}`);
}
```

## Best practices
- Forbid raw color names in semantic and component tiers via lint rule, not convention.
- Reserve component tokens for genuine asymmetries (button-only padding overrides). If three components share a value, it belongs in semantic.
- Version aliases for migrations: keep `color.brand.primary` as alias of `color.action.primary` for one release cycle, then delete.
- Document every semantic token's intent in the value of `$description`, not in a separate wiki — wiki rots.
- Ship a Storybook page that lists tokens by tier with live values; agents can scrape it as a source of truth.

## AI-agent gotchas
- Models love to over-classify into "component" tier because the names are concrete; force tier assignment to be justified with a written reason.
- LLM-generated semantic names often collide (`color.action.primary` vs `color.button.primary`) — require a global uniqueness check.
- Agents will suggest renames that look better but break consumers; demand a migration plan with codemod, not a unilateral rename.
- Multi-mode (light/dark) confuses agents into duplicating tokens per mode at the primitive tier; correct hierarchy keeps modes at semantic only.
- Human checkpoint: a designer must approve the semantic name list before any code rewrite. This is the single most leveraged review in the whole pipeline.

## References
- Brad Frost, "The many faces of design tokens": https://bradfrost.com/blog/post/the-many-faces-of-design-tokens/
- Nathan Curtis, "Naming tokens in design systems": https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676
- Material Design 3 token system: https://m3.material.io/foundations/design-tokens
- Salesforce Lightning Design System tokens: https://www.lightningdesignsystem.com/design-tokens/
- IBM Carbon token guidance: https://carbondesignsystem.com/elements/tokens/overview/
