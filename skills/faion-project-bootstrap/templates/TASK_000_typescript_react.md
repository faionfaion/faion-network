# TASK_000: Project Setup (TypeScript + React)

<!-- SUMMARY: Initialize {project_name} React/TypeScript project with full development infrastructure -->

## Complexity: normal
## Created: {YYYY-MM-DD}
## Project: {project_name}
## Depends on: none

---

## Description

Bootstrap React/TypeScript project with:
- Vite build tool
- ESLint + Prettier
- TypeScript strict mode
- Vitest testing
- Husky + lint-staged
- GitHub Actions CI

---

## Context

- **Constitution:** `aidocs/sdd/{project_name}/constitution.md`
- **Node Version:** 20+
- **Package Manager:** npm / pnpm
- **Build Tool:** Vite
- **Target Directory:** `{project_path}/`

---

## Goals

1. Initialize Vite React TypeScript project
2. Configure ESLint with TypeScript rules
3. Set up Prettier
4. Configure Vitest for testing
5. Set up Husky + lint-staged
6. Create GitHub Actions workflow
7. Create README with getting started

---

## Acceptance Criteria

- [ ] `npm run dev` starts dev server
- [ ] `npm run lint` passes
- [ ] `npm run format` passes
- [ ] `npm run typecheck` passes
- [ ] `npm run test` runs
- [ ] Git hooks work (lint on commit)
- [ ] CI pipeline is green
- [ ] README has getting started

---

## Technical Notes

```
vite.config.ts - Vite + Vitest config
tsconfig.json - TypeScript config
eslint.config.js - ESLint flat config
.prettierrc - Prettier config
src/ - Source code
tests/ - Test files
```

---

## Out of Scope

- Application components
- State management setup
- API integration
- Deployment config

---

## Subtasks

- [ ] 01. Create project with Vite:
  ```bash
  npm create vite@latest {project_name} -- --template react-ts
  cd {project_name}
  ```
- [ ] 02. Install dependencies:
  ```bash
  npm install
  ```
- [ ] 03. Install dev dependencies:
  ```bash
  npm install -D eslint @eslint/js typescript-eslint eslint-plugin-react-hooks eslint-plugin-react-refresh prettier eslint-config-prettier vitest @testing-library/react @testing-library/jest-dom jsdom husky lint-staged
  ```
- [ ] 04. Create directory structure:
  ```
  src/
  ├── components/
  ├── hooks/
  ├── services/
  ├── types/
  ├── utils/
  └── __tests__/
  ```
- [ ] 05. Configure ESLint (eslint.config.js):
  ```javascript
  import js from '@eslint/js'
  import tseslint from 'typescript-eslint'
  import reactHooks from 'eslint-plugin-react-hooks'
  import reactRefresh from 'eslint-plugin-react-refresh'
  import prettier from 'eslint-config-prettier'

  export default tseslint.config(
    { ignores: ['dist'] },
    js.configs.recommended,
    ...tseslint.configs.strictTypeChecked,
    prettier,
    {
      plugins: {
        'react-hooks': reactHooks,
        'react-refresh': reactRefresh,
      },
      rules: {
        ...reactHooks.configs.recommended.rules,
        'react-refresh/only-export-components': 'warn',
      },
      languageOptions: {
        parserOptions: {
          project: ['./tsconfig.json'],
        },
      },
    }
  )
  ```
- [ ] 06. Configure Prettier (.prettierrc):
  ```json
  {
    "semi": false,
    "singleQuote": true,
    "tabWidth": 2,
    "trailingComma": "es5",
    "printWidth": 100
  }
  ```
- [ ] 07. Configure TypeScript (tsconfig.json):
  - Enable strict mode
  - Set proper paths
  - Configure for React
- [ ] 08. Configure Vitest (vite.config.ts):
  ```typescript
  /// <reference types="vitest" />
  import { defineConfig } from 'vite'
  import react from '@vitejs/plugin-react'

  export default defineConfig({
    plugins: [react()],
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
    },
  })
  ```
- [ ] 09. Create test setup (src/test/setup.ts):
  ```typescript
  import '@testing-library/jest-dom'
  ```
- [ ] 10. Set up Husky:
  ```bash
  npx husky init
  echo "npx lint-staged" > .husky/pre-commit
  ```
- [ ] 11. Configure lint-staged (package.json):
  ```json
  {
    "lint-staged": {
      "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
      "*.{json,md}": ["prettier --write"]
    }
  }
  ```
- [ ] 12. Add npm scripts (package.json):
  ```json
  {
    "scripts": {
      "dev": "vite",
      "build": "tsc && vite build",
      "preview": "vite preview",
      "lint": "eslint .",
      "format": "prettier --write .",
      "typecheck": "tsc --noEmit",
      "test": "vitest",
      "test:run": "vitest run"
    }
  }
  ```
- [ ] 13. Create .gitignore
- [ ] 14. Create .github/workflows/ci.yml:
  ```yaml
  name: CI
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-node@v4
          with:
            node-version: 20
            cache: npm
        - run: npm ci
        - run: npm run lint
        - run: npm run typecheck
        - run: npm run test:run
        - run: npm run build
  ```
- [ ] 15. Create README.md
- [ ] 16. Initial commit

---

## Implementation

<!-- To be filled by executor -->

---

## Summary

<!-- To be filled after completion -->
