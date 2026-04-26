# Agent Integration — Design Tokens Fundamentals

## When to use
- Setting up a new design system from scratch — tokens are the foundation before any component library is built
- Adding dark mode, theme switching, or white-label support to an existing codebase
- Auditing a codebase for hardcoded color/spacing/font values that should be tokenized
- Migrating from inline Tailwind classes or CSS magic numbers to a governed token layer
- Generating token documentation from a Figma Variables export or Style Dictionary config

## When NOT to use
- Single-component quick fixes — token infrastructure has setup cost not worth it for one-off styling
- Projects with a single theme and no planned theming requirements — token indirection adds complexity without benefit
- When the design tool (Figma) and codebase are not synchronized — tokens create false confidence if the sources diverge
- Legacy jQuery / server-rendered projects without a CSS variable pipeline — CSS custom properties are the required runtime layer

## Where it fails / limitations
- Token naming is the hardest part and agents will produce inconsistent naming conventions without a strict schema input
- Three-tier token hierarchy (global → semantic → component) is conceptually clean but operationally complex; agents collapse tiers without explicit constraints
- Figma Variables ≠ W3C Design Tokens format — agents conflate them; transformation step (Style Dictionary) is required
- Token sprawl: agents generate excessively granular tokens (one per component state) that defeat the scalability benefit
- Without a governance process, tokens diverge between design files and code within weeks of the initial sync

## Agentic workflow
An agent receives a color palette, type scale, and spacing scale (from a design brief or Figma export) and generates a W3C-compliant design token JSON file with global, semantic, and component tiers. A second agent reviews for naming consistency (camelCase vs. kebab-case, tier prefixes), alias correctness (semantic tokens referencing global tokens, not raw values), and coverage of required token categories (color, spacing, typography, border, shadow, motion). Output is a validated tokens.json ready for Style Dictionary transformation.

### Recommended subagents
- General Claude subagent (haiku) — token file generation from a defined schema is mechanical pattern application
- General Claude subagent (sonnet) — token naming review and alias correctness audit

### Prompt pattern
```
You are a design systems engineer. Generate a W3C Design Token Community Group compliant
tokens.json for the following design values:
Colors: [list]
Spacing: [list]
Typography: [list]

Requirements:
- Three tiers: global (raw values), semantic (aliases with meaningful names), component (optional)
- Semantic color tokens must reference global tokens using {global.token.path} syntax, not raw hex values
- Naming: kebab-case, tier-prefixed (e.g., color.primary.default, spacing.md)
- Include "type" and "description" fields for every token
Output only valid JSON.
```

```
Token audit prompt:
Given this codebase search result of hardcoded values: [list of hex/px values found in CSS/TS files]
Map each value to the nearest existing design token in this tokens.json: [tokens]
For values with no matching token, suggest a new semantic token name and tier placement.
Output: a table with columns: Hardcoded Value | File:Line | Nearest Token | Action (Use existing / Create new / Leave as-is).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Transform token JSON to CSS vars, JS/TS exports, Android, iOS | `npm i -g style-dictionary` / https://amzn.github.io/style-dictionary/ |
| `token-transformer` | Convert Figma Tokens plugin export to Style Dictionary format | `npm i -g token-transformer` / https://github.com/tokens-studio/token-transformer |
| `theo` | Salesforce token transformer (alternative to Style Dictionary) | `npm i theo` / https://github.com/salesforce-ux/theo |
| `design-tokens-cli` | W3C DTCG format validator and transformer | `npm i -g @design-tokens/cli` / https://github.com/design-tokens/community-group |
| `jq` | JSON query tool for inspecting and diffing token files | `brew install jq` / https://jqlang.github.io/jq/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma Variables | SaaS | Yes (REST API) | Read/write variables via Figma API; requires Figma Pro for full variable support |
| Tokens Studio for Figma | SaaS/OSS plugin | Partial — JSON export | Export tokens as JSON that feeds Style Dictionary; no direct API |
| Supernova | SaaS | Yes (REST API) | Token sync between Figma and code; API allows automated export on design change |
| Zeroheight | SaaS | Partial | Design system documentation; embeds Figma; no direct token API |
| Backlight.dev | SaaS | Yes (CLI + API) | Design system platform with token governance; CI/CD integration |

## Templates & scripts
See `templates.md` for token structure examples.

Style Dictionary build config for CSS variables + JS/TS export:
```javascript
// sd.config.js — run with: npx style-dictionary build --config sd.config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      prefix: 'fn',
      buildPath: 'dist/tokens/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/tokens/',
      files: [{ destination: 'tokens.js', format: 'javascript/es6' }],
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'dist/tokens/',
      files: [{
        destination: 'tokens.d.ts',
        format: 'typescript/es6-declarations',
      }],
    },
  },
};
```

## Best practices
- Establish the three-tier hierarchy before generating any tokens: global (primitives) → semantic (intent) → component (scoped)
- Semantic tokens must never hold raw values; they must always alias a global token — enforce this in CI via Style Dictionary transforms
- Use a single source of truth: either Figma Variables or a tokens JSON file in the repo — not both independently maintained
- Commit the generated CSS/JS token outputs to the repo so consumers do not need build-time Style Dictionary access
- Name semantic tokens by intent, not by value: `color.feedback.error` not `color.red` — the value may change, the intent should not
- Add a token changelog discipline: breaking token renames (not additions) require a major version bump

## AI-agent gotchas
- Agents default to two-tier (global + component) token structures; the semantic tier must be explicitly requested
- Generated token names often mix conventions (camelCase in some, kebab in others) within a single file — specify convention in the prompt
- Agents frequently produce semantic tokens that reference raw hex values instead of global token paths — validate with jq or Style Dictionary build
- Token generation without a design reference produces arbitrary spacing and color scales; always provide the actual design values as input
- Do not use agents to decide the token taxonomy; the taxonomy is an architecture decision requiring human consensus across design and engineering

## References
- https://design-tokens.github.io/community-group/
- https://amzn.github.io/style-dictionary/
- https://www.figma.com/blog/introducing-variables/
- https://css-tricks.com/what-are-design-tokens/
- https://www.designsystems.com/design-tokens/
