# M-JS-008: JavaScript/TypeScript Code Quality

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Beginner
- **Tags:** #dev, #javascript, #typescript, #quality, #linting, #methodology
- **Agent:** faion-code-agent

---

## Problem

Code quality degrades over time without automation. Inconsistent formatting causes merge conflicts. Bugs slip through without linting. Code reviews waste time on style issues instead of logic.

## Promise

After this methodology, your code will be automatically formatted, linted, and type-checked. Pull requests will focus on logic, not style. Bugs will be caught before review.

## Overview

Modern JavaScript quality tools include ESLint for linting, Prettier for formatting, TypeScript for type checking, and Husky for git hooks. This methodology shows how to integrate them.

---

## Framework

### Step 1: ESLint Setup (Flat Config)

```bash
pnpm add -D eslint @eslint/js typescript-eslint globals
```

**eslint.config.js:**

```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';

export default tseslint.config(
  // Base configs
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...tseslint.configs.stylistic,

  // Global settings
  {
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.browser,
      },
    },
  },

  // Custom rules
  {
    rules: {
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },

  // Ignored paths
  {
    ignores: ['dist/**', 'node_modules/**', 'coverage/**', '*.config.js'],
  }
);
```

### Step 2: Prettier Setup

```bash
pnpm add -D prettier eslint-config-prettier
```

**.prettierrc:**

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

**.prettierignore:**

```
node_modules
dist
coverage
pnpm-lock.yaml
*.md
```

**Add to ESLint (disable conflicting rules):**

```javascript
// eslint.config.js
import eslintConfigPrettier from 'eslint-config-prettier';

export default tseslint.config(
  // ... other configs
  eslintConfigPrettier, // Must be last
);
```

### Step 3: TypeScript Strict Mode

**tsconfig.json:**

```json
{
  "compilerOptions": {
    // Strict checks
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    // Module
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### Step 4: Git Hooks with Husky

```bash
# Install Husky
pnpm add -D husky

# Initialize Husky
pnpm exec husky init
```

**.husky/pre-commit:**

```bash
#!/bin/sh
pnpm lint-staged
```

**.husky/commit-msg:**

```bash
#!/bin/sh
npx --no -- commitlint --edit ${1}
```

### Step 5: Lint-Staged

```bash
pnpm add -D lint-staged
```

**package.json:**

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yaml,yml}": [
      "prettier --write"
    ]
  }
}
```

### Step 6: Commitlint

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

**commitlint.config.js:**

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting (no code change)
        'refactor', // Code change (no feat/fix)
        'perf',     // Performance
        'test',     // Tests
        'build',    // Build system
        'ci',       // CI config
        'chore',    // Maintenance
        'revert',   // Revert commit
      ],
    ],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 72],
  },
};
```

**Commit examples:**
```
feat: add user authentication
fix: resolve memory leak in cache
docs: update API documentation
refactor: simplify error handling
```

### Step 7: Scripts Configuration

**package.json:**

```json
{
  "scripts": {
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "format": "prettier --write 'src/**/*.{ts,tsx,json}'",
    "format:check": "prettier --check 'src/**/*.{ts,tsx,json}'",
    "type-check": "tsc --noEmit",
    "check": "pnpm lint && pnpm format:check && pnpm type-check",
    "prepare": "husky"
  }
}
```

---

## Templates

### VS Code Settings

**.vscode/settings.json:**

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

**.vscode/extensions.json:**

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "yoavbls.pretty-ts-errors"
  ]
}
```

### EditorConfig

**.editorconfig:**

```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### CI Quality Check

**.github/workflows/quality.yml:**

```yaml
name: Quality Check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Type Check
        run: pnpm type-check

      - name: Lint
        run: pnpm lint

      - name: Format Check
        run: pnpm format:check

      - name: Test
        run: pnpm test
```

---

## Examples

### ESLint Rule Customization

```javascript
// For React projects
{
  rules: {
    'react/prop-types': 'off', // Using TypeScript
    'react/react-in-jsx-scope': 'off', // React 17+
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
}

// For Node.js projects
{
  rules: {
    'no-console': 'off', // Allow console in Node
    '@typescript-eslint/no-require-imports': 'off',
  },
}
```

### Disabling Rules Inline

```typescript
// Disable for next line
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const data: any = response.data;

// Disable for file (at top)
/* eslint-disable no-console */

// Disable specific rule for block
/* eslint-disable @typescript-eslint/no-unused-vars */
const unusedVariable = 'intentionally unused';
/* eslint-enable @typescript-eslint/no-unused-vars */
```

### Ignoring Prettier

```typescript
// prettier-ignore
const matrix = [
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1],
];
```

---

## Common Mistakes

1. **Prettier and ESLint conflicts** - Always use eslint-config-prettier
2. **Too strict too fast** - Enable strict rules gradually
3. **No CI checks** - Local hooks can be bypassed
4. **Ignoring warnings** - Warnings eventually become errors
5. **Not configuring IDE** - Team should share VS Code settings

---

## Checklist

- [ ] ESLint configured with TypeScript
- [ ] Prettier configured and integrated
- [ ] TypeScript strict mode enabled
- [ ] Husky git hooks installed
- [ ] lint-staged for pre-commit
- [ ] Commitlint for commit messages
- [ ] VS Code settings shared
- [ ] CI runs all checks
- [ ] Team aligned on rules

---

## Next Steps

- M-JS-001: Project Setup
- M-JS-005: Testing
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-JS-008 v1.0*
