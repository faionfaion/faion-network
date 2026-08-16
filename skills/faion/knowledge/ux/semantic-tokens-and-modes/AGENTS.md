# Semantic Tokens and Modes

## Summary

**One-sentence:** Produces a three-layer design-token configuration (reference / system / component) in DTCG format with full mode coverage and a Style Dictionary pipeline that emits CSS / Swift / Compose outputs.

**One-paragraph:** Design tokens are decoupled into three explicit layers — reference (raw palette/scale), system (semantic, mode-aware), component (component-scoped) — and driven through a four-stage pipeline: author (Figma Variables) → export (REST API) → transform (Style Dictionary) → consume (CSS/Swift/Compose). Every semantic token MUST have a value in every required mode (light / dark / high-contrast / brand). Raw reference values MUST NOT appear in component code; lint rules enforce. Component layer MUST NOT reference the reference layer directly — only through the system layer.

**Ефективно для:**

- Adding light/dark/high-contrast modes до існуючої token system без коду-forks.
- Multi-brand / white-label products де одна бібліотека обслуговує кілька visual identities.
- Multi-platform builds (web + iOS + Android) які діляться semantic intent.
- Density modes (compact / comfortable) для data-heavy enterprise UIs.

## Applies If (ALL must hold)

- Component library has ≥30 components or there is a foreseeable theming requirement.
- A Figma source-of-truth exists for token authoring (Figma Variables / Tokens Studio).
- Build pipeline can run Node/Style Dictionary in CI.

## Skip If (ANY kills it)

- Single-theme product with no future theming need — overhead exceeds payoff.
- One-off marketing pages outside the system.
- Motion / animation primitives — semantic naming rarely earns its keep there.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Figma Variables export | JSON via REST API | design system Figma file |
| Required-mode list | YAML or Markdown | design system charter |
| Platform output targets | list (css/swift/compose) | engineering |
| Lint config | ESLint / Stylelint | repo root |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[token-organization]] | Defines the naming convention this token configuration uses |
| [[design-tokens-fundamentals]] | Upstream conceptual baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: three-layer-strict, one-intent-per-token, mode-coverage-required, dtcg-format, no-raw-hex-in-components, visual-regression-per-mode | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for token-config artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: reference-jumping, brand-mode-duplication, missing-platform-transform, raw-hex-in-component | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: model layers → declare modes → wire pipeline → lint → visual-regression | 900 |
| `content/06-decision-tree.xml` | essential | Routing: scope-of-theming → number-of-modes → multi-platform yes/no → pipeline choice | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-figma-variables` | haiku | Mechanical REST API call. |
| `propose-semantic-naming` | sonnet | Light judgment on intent grouping. |
| `generate-style-dictionary-config` | sonnet | Template fill + transform selection. |
| `audit-mode-coverage` | haiku | Boolean check per token × mode. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens-semantic.json` | DTCG-format semantic-layer skeleton with mode collection |
| `templates/style-dictionary.config.cjs` | Style Dictionary build config emitting CSS / Swift / Compose |
| `templates/check-modes.mjs` | CI gate: fails build if any semantic token is missing a value in any required mode |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-semantic-tokens-and-modes.py` | Validate the token-config artefact against the schema | Pre-commit; CI before Style Dictionary build |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[token-organization]]
- [[cross-platform-token-distribution]]
- [[design-tokens-fundamentals]]
- [[w3c-design-tokens-standard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on scope-of-theming (single / light+dark / multi-brand / density-aware) and platform count (web-only / multi-platform). Each leaf references a rule from `01-core-rules.xml` and dictates whether the system layer must add a mode collection, whether Style Dictionary needs a platform transform, and whether visual regression must snapshot every mode.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tokens-semantic.json`

```json
{
  "color": {
    "action": {
      "primary": {
        "$type": "color",
        "intent": "primary interactive surface",
        "values_by_mode": {
          "light": "{color.blue.600}",
          "dark": "{color.blue.400}",
          "high-contrast": "{color.blue.900}"
        }
      },
      "primary-hover": {
        "$type": "color",
        "intent": "primary interactive surface \u2014 hover state",
        "values_by_mode": {
          "light": "{color.blue.700}",
          "dark": "{color.blue.300}",
          "high-contrast": "{color.blue.950}"
        }
      }
    },
    "surface": {
      "page": {
        "$type": "color",
        "intent": "page background",
        "values_by_mode": {
          "light": "{color.gray.50}",
          "dark": "{color.gray.950}",
          "high-contrast": "{color.gray.1000}"
        }
      }
    }
  }
}
```

### `templates/style-dictionary.config.cjs`

```javascript
module.exports = {
  source: ['tokens/reference.json', 'tokens/semantic.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        { destination: 'tokens.css', format: 'css/variables', options: { selector: ':root' } },
        { destination: 'tokens-dark.css', format: 'css/variables', options: { selector: '[data-theme="dark"]' }, filter: (t) => t.attributes && t.attributes.mode === 'dark' },
        { destination: 'tokens-hc.css', format: 'css/variables', options: { selector: '[data-theme="high-contrast"]' }, filter: (t) => t.attributes && t.attributes.mode === 'high-contrast' }
      ]
    },
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'dist/ios/',
      files: [
        { destination: 'Tokens.swift', format: 'ios-swift/class.swift', className: 'TokensTheme' }
      ]
    },
    android: {
      transformGroup: 'compose',
      buildPath: 'dist/android/',
      files: [
        { destination: 'Tokens.kt', format: 'compose/object', className: 'TokensTheme', packageName: 'com.example.tokens' }
      ]
    }
  }
};
```

### `templates/check-modes.mjs`

```javascript
// Usage: node check-modes.mjs [tokens/semantic.json] [light,dark,hc]
import { readFileSync } from 'node:fs';

const tokenFile = process.argv[2] ?? 'tokens/semantic.json';
const REQUIRED_MODES = (process.argv[3] ?? 'light,dark,hc').split(',').map(m => m.trim());

let tokens;
try {
  tokens = JSON.parse(readFileSync(tokenFile, 'utf8'));
} catch (e) {
  console.error(`Cannot read ${tokenFile}: ${e.message}`);
  process.exit(1);
}

const missing = [];

function walk(node, path = []) {
  if (!node || typeof node !== 'object') return;
  if ('$value' in node) {
    const v = node.$value;
    // DTCG per-mode value: { light: '#fff', dark: '#000', hc: '#000' }
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      const definedModes = Object.keys(v);
      const lacking = REQUIRED_MODES.filter(m => !definedModes.includes(m));
      if (lacking.length) missing.push({ token: path.join('.'), missing: lacking });
    }
    return;
  }
  for (const [k, child] of Object.entries(node)) {
    if (!k.startsWith('$')) walk(child, [...path, k]);
  }
}

walk(tokens);

if (missing.length) {
  console.error(`\nToken mode coverage failures (${missing.length}):\n`);
  console.error(JSON.stringify(missing, null, 2));
  process.exit(1);
}

console.log(`All semantic tokens have values for modes: ${REQUIRED_MODES.join(', ')}`);
```
