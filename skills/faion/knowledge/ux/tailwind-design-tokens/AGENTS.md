# Tailwind + Design Tokens

## Summary

**One-sentence:** Generate a tailwind.config.js + tokens.css + Style Dictionary config that bridges semantic design tokens to Tailwind utilities via CSS custom properties, with safelist coverage and RGB-channel opacity support.

**One-paragraph:** Map design tokens (colours, spacing, typography) to Tailwind's theme config via CSS custom properties so the design system and component library share a single source of truth. Inputs: Figma Variables export (or Style Dictionary input) + Tailwind major version. Output: a config bundle covering primitives (CSS vars), semantics (Tailwind theme references via `var(--token)`), dark-mode tokens, RGB-channel colours for opacity modifiers, and a safelist for dynamically assembled classes.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- The project uses Tailwind (v3 or v4) and has a design-system requirement.
- A token source exists (Figma Variables, Style Dictionary input, or canonical CSS file).
- The Tailwind major version is known up front.

## Skip If (ANY kills it)

- Project does not use Tailwind — use Style Dictionary alone or raw CSS variables.
- Throwaway prototype where systematic tokens add cost without payoff.
- Design ops own tokens and code edits are locked.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Token source (Figma export / SD input / canonical CSS) | JSON / CSS | design ops |
| Tailwind major version (3 or 4) | doc | engineering |
| Dark-mode requirement | doc | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/frontend-developer/component-architecture` | Components consume the tokens this config emits. |
| `solo/ux/ux-ui-designer/match-real-world` | Semantic token naming follows user mental model where possible. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the token-config bundle + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: source → primitives → semantics → dark-mode → safelist | ~600 |
| `content/05-examples.xml` | medium | Worked example: brand colour primitives + semantic mapping + dark mode | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `convert-figma-vars` | sonnet | Mechanical Figma-variable to SD-input mapping. |
| `compose-tailwind-config` | sonnet | Tailwind theme block composition with `var(--token)` refs. |
| `safelist-audit` | opus | Detect dynamically assembled class names that JIT cannot statically see. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.js` | Tailwind theme skeleton referencing `var(--token-name)`. |
| `templates/tokens.css` | CSS custom-property layer (light + dark). |
| `templates/sd.config.js` | Style Dictionary build config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind-design-tokens.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[match-real-world]]
- [[wireframing]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, Tailwind major version known, opacity modifiers required) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tailwind.config.js`

```javascript
//
// tailwind.config.js — design token integration example
// All values reference CSS custom properties defined in tokens.css
// No hardcoded hex, px, or raw values in this file

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,html}'],

  // Safelist dynamic token classes assembled via string concatenation
  safelist: [],

  theme: {
    colors: {
      // Semantic tokens — action
      primary: {
        DEFAULT: 'rgb(var(--color-primary-rgb) / <alpha-value>)',
        hover:   'rgb(var(--color-primary-hover-rgb) / <alpha-value>)',
      },
      // Semantic tokens — feedback
      error:   'rgb(var(--color-error-rgb) / <alpha-value>)',
      success: 'rgb(var(--color-success-rgb) / <alpha-value>)',
      warning: 'rgb(var(--color-warning-rgb) / <alpha-value>)',
      // Semantic tokens — surface
      surface: {
        DEFAULT: 'var(--color-surface)',
        raised:  'var(--color-surface-raised)',
      },
      // Semantic tokens — text
      text: {
        DEFAULT:   'var(--color-text)',
        secondary: 'var(--color-text-secondary)',
        disabled:  'var(--color-text-disabled)',
      },
    },

    spacing: {
      xs: 'var(--spacing-xs)',   // 4px
      sm: 'var(--spacing-sm)',   // 8px
      md: 'var(--spacing-md)',   // 16px
      lg: 'var(--spacing-lg)',   // 24px
      xl: 'var(--spacing-xl)',   // 32px
      '2xl': 'var(--spacing-2xl)', // 48px
    },

    fontFamily: {
      sans: ['var(--font-family-sans)', 'system-ui', 'sans-serif'],
      mono: ['var(--font-family-mono)', 'monospace'],
    },

    fontSize: {
      sm:   ['var(--font-size-sm)',   { lineHeight: 'var(--line-height-sm)' }],
      base: ['var(--font-size-base)', { lineHeight: 'var(--line-height-base)' }],
      lg:   ['var(--font-size-lg)',   { lineHeight: 'var(--line-height-lg)' }],
      xl:   ['var(--font-size-xl)',   { lineHeight: 'var(--line-height-xl)' }],
    },

    borderRadius: {
      sm: 'var(--radius-sm)',
      md: 'var(--radius-md)',
      lg: 'var(--radius-lg)',
      full: '9999px',
    },
  },

  plugins: [],
};
```

### `templates/tokens.css`

```css
 */

/* tokens.css — design token CSS custom properties
   Imported in global stylesheet (e.g., globals.css or main.css)
   This file is the single source of actual values.
   tailwind.config.js references var(--token-name), never raw values. */

:root {
  /* === Colors (RGB channels for opacity modifier support) === */
  --color-primary-rgb:       26 115 232;
  --color-primary-hover-rgb: 21  94 193;
  --color-error-rgb:        197  34  31;
  --color-success-rgb:       52 168  83;
  --color-warning-rgb:      251 188   4;

  /* Colors (non-opacity-modified) */
  --color-surface:        #ffffff;
  --color-surface-raised: #f8f9fa;
  --color-text:           #202124;
  --color-text-secondary: #5f6368;
  --color-text-disabled:  #9aa0a6;

  /* === Spacing === */
  --spacing-xs:  4px;
  --spacing-sm:  8px;
  --spacing-md:  16px;
  --spacing-lg:  24px;
  --spacing-xl:  32px;
  --spacing-2xl: 48px;

  /* === Typography === */
  --font-family-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --font-size-sm:   0.875rem; /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg:   1.125rem; /* 18px */
  --font-size-xl:   1.25rem;  /* 20px */

  --line-height-sm:   1.5;
  --line-height-base: 1.5;
  --line-height-lg:   1.4;
  --line-height-xl:   1.3;

  /* === Border Radius === */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
}

/* Dark mode token overrides */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface:        #202124;
    --color-surface-raised: #303134;
    --color-text:           #e8eaed;
    --color-text-secondary: #9aa0a6;
    --color-text-disabled:  #5f6368;
  }
}
```

### `templates/sd.config.js`

```javascript
//
// sd.config.js — Style Dictionary: W3C DTCG token JSON → Tailwind config + CSS variables
// Run: node sd.config.js
// Input:  tokens/**/*.json (W3C DTCG format)
// Output: src/styles/tokens.css + src/tw-tokens.js

const StyleDictionary = require('style-dictionary');

StyleDictionary.registerTransform({
  name: 'css/var-name',
  type: 'name',
  transformer: (token) =>
    `--${token.path.join('-').toLowerCase().replace(/\s+/g, '-')}`,
});

StyleDictionary.registerFormat({
  name: 'tailwind/tokens',
  formatter: ({ dictionary }) => {
    const colors  = {};
    const spacing = {};

    dictionary.allTokens.forEach((token) => {
      const varRef = `var(--${token.name})`;
      if (token.path[0] === 'color') {
        // Nested structure: color.primary.default → colors.primary.DEFAULT
        let obj = colors;
        token.path.slice(1, -1).forEach((seg) => {
          obj[seg] = obj[seg] || {};
          obj = obj[seg];
        });
        const last = token.path[token.path.length - 1];
        obj[last === 'default' ? 'DEFAULT' : last] = varRef;
      } else if (token.path[0] === 'spacing') {
        const key = token.path.slice(1).join('-');
        spacing[key] = varRef;
      }
    });

    return `// Auto-generated by sd.config.js — do not edit manually
module.exports = ${JSON.stringify({ colors, spacing }, null, 2)};
`;
  },
});

module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transforms: ['attribute/cti', 'css/var-name', 'color/hsl'],
      buildPath: 'src/styles/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }],
    },
    tailwind: {
      transforms: ['attribute/cti', 'css/var-name'],
      buildPath: 'src/',
      files: [{ destination: 'tw-tokens.js', format: 'tailwind/tokens' }],
    },
  },
};
```
