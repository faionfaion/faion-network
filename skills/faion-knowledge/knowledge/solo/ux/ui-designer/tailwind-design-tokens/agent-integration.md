# Agent Integration — Tailwind + Design Tokens

## When to use
- Bootstrapping a new Tailwind project that must support theming (dark mode, brand variants, white-label)
- Migrating an existing Tailwind codebase from hardcoded utility values to CSS-variable-backed tokens
- Generating `tailwind.config.js` theme overrides from a Style Dictionary token build output
- Auditing a Tailwind codebase for arbitrary values (`text-[#3B82F6]`, `p-[13px]`) that should become tokens
- Setting up a Storybook token documentation layer alongside a Tailwind component library

## When NOT to use
- Projects not using Tailwind — use Style Dictionary + CSS custom properties directly instead
- Pure CSS/SCSS codebases where Tailwind migration is not planned — token integration is still valid but via a different path
- When design tokens are not yet defined or stable — generating Tailwind config before token taxonomy is finalized creates throwaway work
- Utility-class-only projects with zero theming requirements — the CSS variable indirection adds complexity without payoff

## Where it fails / limitations
- Tailwind JIT purges CSS variables that are not referenced in source files — agents generating config must ensure all token-mapped classes are actually used or safelisted
- CSS variable syntax in Tailwind config (`var(--color-primary)`) breaks opacity modifiers (`bg-primary/50`) unless using the `<alpha-value>` channel pattern
- Three-tier token hierarchy (global → semantic → component) is hard to express cleanly in `tailwind.config.js` — agents flatten it without explicit instruction
- Generated configs often include duplicate scale entries when the Tailwind default scale and token scale are both included
- Token-to-Tailwind class mapping is many-to-one: `spacing.md = 16px` maps to Tailwind's `4` scale — agents produce incorrect mappings without a reference table

## Agentic workflow
An agent receives a design token JSON file (W3C format or Style Dictionary output) and generates: (1) a `tailwind.config.js` theme section with CSS variable references for all token categories (color, spacing, typography, border-radius, shadow), (2) a companion CSS file with the `@layer base { :root { } }` custom property declarations, and (3) an arbitrary-value audit report listing all `[value]` usages in the codebase. A second agent verifies opacity modifier compatibility for color tokens and checks that the generated config does not conflict with Tailwind's default scale.

### Recommended subagents
- General Claude subagent (haiku) — config generation from a token file is mechanical transformation
- General Claude subagent (sonnet) — opacity modifier compatibility audit and arbitrary-value review

### Prompt pattern
```
You are a Tailwind CSS engineer. Given this design tokens JSON: [tokens]
Generate:
1. A tailwind.config.js theme section that maps each token to a CSS variable reference
   using the pattern: color.primary.default → 'var(--color-primary-default)'
2. A CSS file with :root { } declarations for all tokens as CSS custom properties
3. For color tokens: use the RGB channel pattern for opacity modifier compatibility:
   --color-primary-default: 59 130 246; (RGB values only, no #hex or rgb())
   Then in config: primary: { default: 'rgb(var(--color-primary-default) / <alpha-value>)' }
Output only valid JS and CSS. Flag any token category not covered.
```

```
Arbitrary value audit:
Scan this codebase for Tailwind arbitrary values: [list of matches from grep]
For each match, determine:
1. Does an existing design token cover this value?
2. If yes: suggest the token-backed utility class replacement
3. If no: suggest a new token name and tier placement
Output: table with columns: File:Line | Arbitrary Value | Token Match | Replacement Class | Action.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Transform token JSON to CSS vars that feed Tailwind config | `npm i -g style-dictionary` / https://amzn.github.io/style-dictionary/ |
| `tailwind-config-viewer` | Visual browser of the current Tailwind theme config | `npx tailwind-config-viewer` / https://github.com/rogden/tailwind-config-viewer |
| `prettier-plugin-tailwindcss` | Enforce class sort order; detects arbitrary values in review | `npm i -D prettier-plugin-tailwindcss` / https://github.com/tailwindlabs/prettier-plugin-tailwindcss |
| `eslint-plugin-tailwindcss` | Lint for arbitrary values and unsorted classes | `npm i -D eslint-plugin-tailwindcss` / https://github.com/francoismassart/eslint-plugin-tailwindcss |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio for Figma | Plugin (OSS) | Partial — JSON export | Exports tokens as JSON that maps cleanly to Tailwind config via Style Dictionary |
| Supernova | SaaS | Yes (REST API) | Syncs Figma tokens to code; can generate Tailwind config as part of export pipeline |
| Storybook | OSS | Yes (CLI) | Documents Tailwind token usage in component stories; `@storybook/addon-a11y` checks contrast |
| Chromatic | SaaS | Yes (CLI) | Visual regression testing of token-based component changes | 

## Templates & scripts
See `templates.md` for the base token configuration patterns.

Complete token-to-Tailwind generation pipeline (Node.js):
```javascript
// build-tailwind-tokens.mjs
// Reads tokens.json, outputs tailwind-theme.js + tokens.css
// Usage: node build-tailwind-tokens.mjs
import { readFileSync, writeFileSync } from 'fs';

const tokens = JSON.parse(readFileSync('tokens/tokens.json', 'utf8'));
const cssVars = [];
const twColors = {};
const twSpacing = {};

function processTokens(obj, prefix = '') {
  for (const [key, val] of Object.entries(obj)) {
    const path = prefix ? `${prefix}-${key}` : key;
    if (val.value !== undefined) {
      const cssKey = `--${path}`;
      if (val.type === 'color') {
        // Convert hex to RGB channels for opacity modifier support
        const hex = val.value.replace('#', '');
        const r = parseInt(hex.slice(0, 2), 16);
        const g = parseInt(hex.slice(2, 4), 16);
        const b = parseInt(hex.slice(4, 6), 16);
        cssVars.push(`  ${cssKey}-rgb: ${r} ${g} ${b};`);
        cssVars.push(`  ${cssKey}: #${hex};`);
        setNestedKey(twColors, path.replace('color-', '').split('-'),
          `rgb(var(${cssKey}-rgb) / <alpha-value>)`);
      } else if (val.type === 'dimension') {
        cssVars.push(`  ${cssKey}: ${val.value};`);
        if (path.startsWith('spacing-')) {
          const name = path.replace('spacing-', '');
          twSpacing[name] = `var(${cssKey})`;
        }
      }
    } else {
      processTokens(val, path);
    }
  }
}

function setNestedKey(obj, keys, value) {
  keys.reduce((acc, key, i) => {
    if (i === keys.length - 1) { acc[key] = value; return acc; }
    acc[key] = acc[key] || {};
    return acc[key];
  }, obj);
}

processTokens(tokens);

writeFileSync('dist/tokens.css',
  `:root {\n${cssVars.join('\n')}\n}\n`);
writeFileSync('dist/tailwind-theme.js',
  `module.exports = ${JSON.stringify({ colors: twColors, spacing: twSpacing }, null, 2)};\n`);

console.log(`Generated: ${cssVars.length} CSS variables`);
```

## Best practices
- Always use RGB channel pattern for color tokens, not raw hex, to preserve Tailwind's opacity modifier functionality (`bg-primary/50`)
- Extend the Tailwind default theme (`theme.extend`) rather than replacing it — replacing removes useful defaults like `font-sans`
- Keep the Style Dictionary build step in the CI pipeline before `tailwind build` runs; config should never be hand-edited
- Use `eslint-plugin-tailwindcss` with `no-arbitrary-value` rule to prevent new hardcoded values entering the codebase
- Document token-to-utility-class mapping in Storybook tokens docs page — devs should not need to read `tailwind.config.js` to know which class to use
- Safelist token-generated classes that are constructed dynamically (e.g., `bg-${color}`) to prevent JIT purge

## AI-agent gotchas
- Agents frequently generate color tokens without RGB channel support, breaking opacity modifiers — explicitly request the `<alpha-value>` pattern
- Tailwind scale naming conflicts with token naming: `spacing.4 = 16px` in Tailwind default but `spacing.md = 16px` in tokens — agents produce wrong mappings without both scales as input
- Generated configs extend instead of replace by default but agents sometimes generate at `theme` level, wiping defaults — verify `theme.extend` placement
- Agents do not know which generated classes will be purged by JIT — require a safelist audit after generation
- The opacity modifier pattern (`rgb(var(--x) / <alpha-value>)`) is a Tailwind-specific syntax that agents from general training sometimes get wrong — validate generated config against Tailwind v3+ docs

## References
- https://tailwindcss.com/docs/theme
- https://tailwindcss.com/docs/customizing-colors#using-css-variables
- https://amzn.github.io/style-dictionary/
- https://www.smashingmagazine.com/2025/tailwind-design-tokens/
- https://www.designsystems.com/tailwind-integration/
