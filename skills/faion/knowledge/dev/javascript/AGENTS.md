# JavaScript / TypeScript Standards (2026)

## Summary

**One-sentence:** Produces a TypeScript-strict JS/TS project (tsconfig strict + noUncheckedIndexedAccess + exactOptional, named exports, pnpm, ESLint 9 flat, Prettier, Vitest, MSW, controller/service/repository for Node) ready for CI.

**One-paragraph:** Universal standards for modern JS/TS in 2026: TypeScript 5.x with `strict: true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`; never `any` in production (`unknown` instead). Named exports over default; arrow functions for callbacks; `const` everywhere mutable not required. pnpm as default package manager; ESLint 9 flat config + Prettier; Vitest for tests. React: function components + hooks + Props interface; Node: controller/service/repository layering with centralized error handling. External input validated at the boundary with zod/valibot; types trusted only for internal data. MSW for API mocking in tests (define handlers once, reuse in tests + Storybook).

**Ефективно для:** new JS/TS projects, refactors moving from `any`-heavy code to strict TS, codebases tightening lint/test foundations before scale, monorepos adopting one tsconfig + eslint base.

## Applies If (ALL must hold)

- Project uses TypeScript 5.x (or migrating from JS to TS).
- pnpm is acceptable (or workspace already uses it).
- CI can run ESLint 9 flat config + Prettier + Vitest.
- Team accepts `strict: true` and no-any policy.

## Skip If (ANY kills it)

- Codebase locked on Webpack 4 / ESLint 8 / Jest where flat config / Vitest are off-limits.
- Library deliberately optimized for size below all conventions (use a custom config).
- Pure Deno project — different toolchain.
- Pre-existing TS project that already enforces stricter rules.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Project type | one of: react / next / node-api / library / cli | tech stack ADR |
| Node version | `>=20` | engines field in package.json |
| Package manager | pnpm | repo convention |
| Existing tsconfig | JSON (optional) | repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[pnpm-package-management]]` | Pins package manager + lockfile. |
| `[[nodejs-express-fastify]]` | Server layering for the Node profile. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: strict TS, named exports, boundary validation, function components, hook return types, context guard, layering, Vitest, MSW | ~800 |
| `content/02-output-contract.xml` | essential | Required config shape (tsconfig flags, eslint flat config, prettier, vitest) | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: `any` proliferation, default exports, unchecked external input, fetch-mocking instead of MSW | ~600 |
| `content/04-procedure.xml` | medium | 5-step bootstrap | ~700 |
| `content/06-decision-tree.xml` | essential | Root: "Is this a TS 5.x project that can adopt strict?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold configs | sonnet | Template-driven. |
| any -> unknown migration | opus | AST reasoning across imports. |
| ESLint rule selection | sonnet | Pattern selection. |
| Vitest + MSW setup | sonnet | Boilerplate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.json` | Full strict tsconfig with path aliases and monorepo settings. |
| `templates/eslint.config.js` | ESLint 9 flat config with TS strict + React hooks rules. |
| `templates/prettierrc.json` | Shared Prettier config (single quotes, trailing commas, LF). |
| `templates/vitest.config.ts` | Vitest config with jsdom + coverage (v8) + setup file. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-javascript.py` | Checks tsconfig flags, eslint config, and absence of `any` in src/. | Pre-commit gate. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `free/dev/software-developer/`
- `[[pnpm-package-management]]` — package manager lock-in
- `[[nodejs-express-fastify]]` — server layering

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: TS 5.x adoptable, strict mode acceptable, pnpm acceptable. Any "no" -> defer or partial adoption.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "lib": [
      "ES2022",
      "DOM",
      "DOM.Iterable"
    ],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": ".",
    "paths": {
      "@/*": [
        "./src/*"
      ],
      "@components/*": [
        "./src/components/*"
      ],
      "@utils/*": [
        "./src/utils/*"
      ]
    },
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

### `templates/eslint.config.js`

```javascript
// eslint.config.js — ESLint 9.x flat config with TypeScript strict + React hooks
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    plugins: { react, 'react-hooks': reactHooks },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': ['error', { allowExpressions: true }],
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
);
```

### `templates/prettierrc.json`

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### `templates/vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/', '**/*.d.ts'],
      thresholds: { lines: 80, branches: 80, functions: 80, statements: 80 },
    },
  },
});
```
