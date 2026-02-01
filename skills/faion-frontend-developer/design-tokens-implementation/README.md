---
id: design-tokens-implementation
name: "Design Tokens: Implementation & Usage"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Design Tokens: Implementation & Usage

## Overview

This document covers the implementation, tooling, and usage of design tokens in real-world projects using Style Dictionary, CSS custom properties, and framework integrations.

## Style Dictionary Configuration

### Basic Setup

```javascript
// style-dictionary.config.js
const StyleDictionary = require('style-dictionary');

// Custom format for CSS custom properties
StyleDictionary.registerFormat({
  name: 'css/variables',
  formatter: function({ dictionary, file }) {
    return `:root {\n${dictionary.allProperties.map(prop =>
      `  --${prop.name}: ${prop.value};`
    ).join('\n')}\n}`;
  }
});

// Custom transform for CSS property names
StyleDictionary.registerTransform({
  name: 'name/kebab',
  type: 'name',
  transformer: (token) => {
    return token.path.join('-').toLowerCase();
  }
});

module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables',
          options: {
            showFileHeader: false
          }
        }
      ]
    },
    scss: {
      transformGroup: 'scss',
      buildPath: 'dist/scss/',
      files: [
        {
          destination: '_variables.scss',
          format: 'scss/variables'
        }
      ]
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6'
        }
      ]
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'dist/ts/',
      files: [
        {
          destination: 'tokens.ts',
          format: 'javascript/es6'
        },
        {
          destination: 'tokens.d.ts',
          format: 'typescript/es6-declarations'
        }
      ]
    },
    json: {
      transformGroup: 'js',
      buildPath: 'dist/json/',
      files: [
        {
          destination: 'tokens.json',
          format: 'json/nested'
        }
      ]
    }
  }
};
```

## Generated Outputs

### CSS Custom Properties

```css
/* dist/css/variables.css */
:root {
  /* Primitives */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-500: #6b7280;
  --color-gray-900: #111827;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;

  /* Semantic */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-border-default: #e5e7eb;
  --color-action-primary: #2563eb;
  --color-action-primary-hover: #1d4ed8;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Dark mode */
[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-bg-secondary: #1f2937;
  --color-text-primary: #f9fafb;
  --color-text-secondary: #d1d5db;
  --color-border-default: #374151;
  --color-action-primary: #3b82f6;
}
```

### TypeScript Token Types

```typescript
// tokens.ts (generated)
export const tokens = {
  color: {
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      // ...
    },
    blue: {
      500: '#3b82f6',
      600: '#2563eb',
      // ...
    },
  },
  spacing: {
    1: '0.25rem',
    2: '0.5rem',
    4: '1rem',
    // ...
  },
  // ...
} as const;

// Type helpers
type TokenPath<T, K extends keyof T = keyof T> = K extends string
  ? T[K] extends Record<string, unknown>
    ? `${K}.${TokenPath<T[K]>}` | K
    : K
  : never;

type ColorToken = TokenPath<typeof tokens.color>;
// 'gray' | 'gray.50' | 'gray.100' | 'blue' | 'blue.500' | ...

// Token getter with type safety
export function getToken<T extends TokenPath<typeof tokens>>(
  path: T
): string {
  return path.split('.').reduce((obj, key) => obj[key], tokens as any);
}

// Usage
const primaryColor = getToken('color.blue.600'); // '#2563eb'
```

## Usage in Components

### React with CSS Modules

```tsx
// Using CSS custom properties
import styles from './Button.module.css';

export function Button({ children, variant = 'primary' }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

```css
/* Button.module.css */
.button {
  padding: var(--spacing-2) var(--spacing-4);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  transition: all 0.2s;
}

.primary {
  background: var(--color-action-primary);
  color: var(--color-text-inverse);
  border: none;
}

.primary:hover {
  background: var(--color-action-primary-hover);
}

.secondary {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
}

.secondary:hover {
  background: var(--color-bg-tertiary);
}
```

## Framework Integrations

### Tailwind CSS Integration

```javascript
// tailwind.config.js
const tokens = require('./dist/js/tokens');

function flattenTokens(obj, prefix = '') {
  return Object.entries(obj).reduce((acc, [key, value]) => {
    const newKey = prefix ? `${prefix}-${key}` : key;
    if (typeof value === 'object' && !value.value) {
      return { ...acc, ...flattenTokens(value, newKey) };
    }
    return { ...acc, [newKey]: value.value || value };
  }, {});
}

module.exports = {
  theme: {
    colors: flattenTokens(tokens.color),
    spacing: flattenTokens(tokens.spacing),
    fontSize: flattenTokens(tokens.fontSize),
    fontWeight: flattenTokens(tokens.fontWeight),
    borderRadius: flattenTokens(tokens.borderRadius),
    boxShadow: flattenTokens(tokens.shadow),
  },
};
```

Usage:
```tsx
<button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md">
  Click me
</button>
```

### Material-UI Theme

```typescript
// theme.ts
import { createTheme } from '@mui/material/styles';
import { tokens } from './tokens';

const theme = createTheme({
  palette: {
    primary: {
      main: tokens.color.blue[600],
      light: tokens.color.blue[400],
      dark: tokens.color.blue[800],
    },
    secondary: {
      main: tokens.color.gray[600],
    },
    text: {
      primary: tokens.color.gray[900],
      secondary: tokens.color.gray[600],
    },
    background: {
      default: tokens.color.white,
      paper: tokens.color.gray[50],
    },
  },
  spacing: 8, // Base unit (0.5rem)
  typography: {
    fontSize: 16,
    fontWeightRegular: tokens.fontWeight.normal,
    fontWeightMedium: tokens.fontWeight.medium,
    fontWeightBold: tokens.fontWeight.bold,
  },
  shape: {
    borderRadius: parseInt(tokens.borderRadius.md),
  },
});

export default theme;
```

## Figma Token Sync

### Automated Sync Script

```javascript
// scripts/sync-figma-tokens.js
const fetch = require('node-fetch');
const fs = require('fs');

const FIGMA_TOKEN = process.env.FIGMA_TOKEN;
const FILE_KEY = process.env.FIGMA_FILE_KEY;

async function fetchFigmaTokens() {
  const response = await fetch(
    `https://api.figma.com/v1/files/${FILE_KEY}/variables/local`,
    {
      headers: {
        'X-Figma-Token': FIGMA_TOKEN,
      },
    }
  );

  const data = await response.json();
  return transformFigmaTokens(data);
}

function transformFigmaTokens(figmaData) {
  // Transform Figma variable format to Style Dictionary format
  const tokens = {};

  for (const variable of figmaData.meta.variables) {
    const path = variable.name.split('/');
    let current = tokens;

    for (let i = 0; i < path.length - 1; i++) {
      current[path[i]] = current[path[i]] || {};
      current = current[path[i]];
    }

    current[path[path.length - 1]] = {
      value: resolveValue(variable.valuesByMode),
    };
  }

  return tokens;
}

async function main() {
  const tokens = await fetchFigmaTokens();
  fs.writeFileSync(
    'tokens/figma-sync.json',
    JSON.stringify(tokens, null, 2)
  );
  console.log('Tokens synced from Figma!');
}

main();
```

### CI/CD Integration

```yaml
# .github/workflows/sync-tokens.yml
name: Sync Design Tokens

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Sync tokens from Figma
        env:
          FIGMA_TOKEN: ${{ secrets.FIGMA_TOKEN }}
          FIGMA_FILE_KEY: ${{ secrets.FIGMA_FILE_KEY }}
        run: node scripts/sync-figma-tokens.js

      - name: Build tokens
        run: npm run build:tokens

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: 'chore: sync design tokens from Figma'
          title: 'Update design tokens from Figma'
          branch: sync-tokens
```

## Build & Distribution

### NPM Package Setup

```json
// package.json
{
  "name": "@company/design-tokens",
  "version": "1.0.0",
  "description": "Design tokens for Company Design System",
  "main": "dist/js/tokens.js",
  "types": "dist/ts/tokens.d.ts",
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "style-dictionary build",
    "build:watch": "nodemon --watch tokens --exec npm run build",
    "prepublishOnly": "npm run build"
  },
  "devDependencies": {
    "style-dictionary": "^3.8.0"
  }
}
```

### Multi-Package Distribution

```
packages/
├── tokens/                 # Core tokens package
│   ├── tokens/
│   ├── style-dictionary.config.js
│   └── package.json
├── tokens-react/           # React-specific package
│   ├── src/
│   │   ├── useTheme.ts
│   │   └── ThemeProvider.tsx
│   └── package.json
├── tokens-vue/             # Vue-specific package
└── tokens-ios/             # iOS-specific package
```

## Testing Tokens

### Visual Regression Testing

```typescript
// tests/tokens.visual.test.ts
import { tokens } from '../dist/ts/tokens';

describe('Design Tokens Visual Tests', () => {
  it('renders all color tokens', () => {
    const container = document.createElement('div');

    Object.entries(tokens.color).forEach(([name, shades]) => {
      Object.entries(shades).forEach(([shade, value]) => {
        const swatch = document.createElement('div');
        swatch.style.background = value;
        swatch.style.width = '50px';
        swatch.style.height = '50px';
        swatch.setAttribute('data-token', `${name}-${shade}`);
        container.appendChild(swatch);
      });
    });

    expect(container).toMatchSnapshot();
  });
});
```

### Accessibility Testing

```typescript
// tests/tokens.a11y.test.ts
import { tokens } from '../dist/ts/tokens';

function getContrastRatio(color1: string, color2: string): number {
  // Calculate WCAG contrast ratio
  // Implementation details...
}

describe('Color Contrast Compliance', () => {
  it('text colors meet WCAG AA on backgrounds', () => {
    const textPrimary = tokens.color.text.primary;
    const bgPrimary = tokens.color.bg.primary;

    const ratio = getContrastRatio(textPrimary, bgPrimary);
    expect(ratio).toBeGreaterThanOrEqual(4.5); // WCAG AA
  });
});
```

## Best Practices

### Token Versioning

- Use semantic versioning
- Document breaking changes
- Provide deprecation warnings
- Support migration paths

### Documentation

```markdown
# Token: color-action-primary

**Value**: {color.blue.600} (#2563eb)
**Usage**: Primary action buttons, links, focused states
**Platforms**: Web, iOS, Android

## Examples

- Submit buttons
- Primary CTAs
- Navigation active states

## Accessibility

- Meets WCAG AA against white backgrounds
- Use color-action-primary-text for button text
```

### Performance Optimization

- Minimize CSS custom property reflows
- Use tokens at build time when possible
- Tree-shake unused tokens in production
- Cache compiled token outputs

## Related

- [design-tokens-basics.md](design-tokens-basics.md) - Token concepts and structure
- [tailwind.md](tailwind.md) - Tailwind CSS integration
- [storybook-setup.md](storybook-setup.md) - Document tokens in Storybook

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Fix CSS typo, update Tailwind class, run prettier | haiku | Direct text replacement and formatting |
| Code review component accessibility compliance | sonnet | WCAG standards evaluation |
| Debug responsive layout issues across breakpoints | sonnet | Testing and debugging |
| Design system architecture and token structure | opus | Complex organization and scaling |
| Refactor React component for performance | sonnet | Optimization and code quality |
| Plan design token migration across 50+ components | opus | Large-scale coordination |
| Build storybook automation and interactions | sonnet | Testing and documentation setup |
