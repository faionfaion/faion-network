# M-JS-007: Monorepo Setup with Turborepo

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Advanced
- **Tags:** #dev, #javascript, #monorepo, #turborepo, #methodology
- **Agent:** faion-code-agent

---

## Problem

Managing multiple packages becomes painful with separate repositories. Version synchronization, dependency management, and cross-package changes create friction. You need a single repository that scales.

## Promise

After this methodology, you will have a monorepo that builds only what changed, shares dependencies efficiently, and enables atomic cross-package changes.

## Overview

Modern JavaScript monorepos use Turborepo for caching and task orchestration, pnpm workspaces for dependency management, and TypeScript project references for type checking.

---

## Framework

### Step 1: Initialize Monorepo

```bash
# Create with Turborepo
pnpm dlx create-turbo@latest my-monorepo

# Or initialize manually
mkdir my-monorepo && cd my-monorepo
pnpm init
```

**pnpm-workspace.yaml:**

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

**package.json (root):**

```json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "test": "turbo test",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "prettier": "^3.2.0",
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  },
  "packageManager": "pnpm@9.0.0",
  "engines": {
    "node": ">=20"
  }
}
```

### Step 2: Project Structure

```
my-monorepo/
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── turbo.json
├── tsconfig.json              # Root TS config
├── .gitignore
├── apps/
│   ├── web/                   # Next.js app
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   ├── api/                   # Express/Fastify API
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   └── admin/                 # Admin dashboard
│       └── ...
├── packages/
│   ├── ui/                    # Shared React components
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   ├── config/                # Shared configs (ESLint, TS)
│   │   ├── eslint/
│   │   └── typescript/
│   ├── database/              # Prisma schema + client
│   │   └── ...
│   └── utils/                 # Shared utilities
│       └── ...
└── tooling/
    ├── eslint-config/
    └── typescript-config/
```

### Step 3: Turborepo Configuration

**turbo.json:**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "type-check": {
      "dependsOn": ["^build"]
    }
  }
}
```

**Key concepts:**
- `^build` = build dependencies first
- `dependsOn` = task execution order
- `outputs` = what to cache
- `persistent` = long-running tasks (dev servers)

### Step 4: Shared TypeScript Config

**packages/config/typescript/base.json:**

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "isolatedModules": true
  }
}
```

**packages/config/typescript/react.json:**

```json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}
```

**apps/web/tsconfig.json:**

```json
{
  "extends": "@repo/typescript-config/react.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "next-env.d.ts"],
  "exclude": ["node_modules"]
}
```

### Step 5: Internal Packages

**packages/ui/package.json:**

```json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./button": "./src/Button.tsx",
    "./card": "./src/Card.tsx"
  },
  "scripts": {
    "lint": "eslint src --ext .ts,.tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0"
  },
  "devDependencies": {
    "@repo/typescript-config": "workspace:*",
    "@types/react": "^18.2.0",
    "typescript": "^5.4.0"
  }
}
```

**Using in apps/web:**

```json
{
  "dependencies": {
    "@repo/ui": "workspace:*"
  }
}
```

```tsx
// apps/web/src/app/page.tsx
import { Button } from '@repo/ui';
// or
import { Button } from '@repo/ui/button';
```

### Step 6: Shared ESLint Config

**tooling/eslint-config/package.json:**

```json
{
  "name": "@repo/eslint-config",
  "version": "0.0.0",
  "private": true,
  "exports": {
    "./base": "./base.js",
    "./react": "./react.js",
    "./next": "./next.js"
  },
  "dependencies": {
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "eslint-config-prettier": "^9.0.0"
  }
}
```

**tooling/eslint-config/base.js:**

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
};
```

**apps/web/.eslintrc.js:**

```javascript
module.exports = {
  extends: ['@repo/eslint-config/next'],
  root: true,
};
```

---

## Templates

### Database Package (Prisma)

```
packages/database/
├── package.json
├── prisma/
│   └── schema.prisma
└── src/
    └── index.ts
```

**package.json:**

```json
{
  "name": "@repo/database",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "scripts": {
    "generate": "prisma generate",
    "push": "prisma db push",
    "studio": "prisma studio"
  },
  "dependencies": {
    "@prisma/client": "^5.10.0"
  },
  "devDependencies": {
    "prisma": "^5.10.0"
  }
}
```

**src/index.ts:**

```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as { prisma?: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

export * from '@prisma/client';
```

### CI/CD Configuration

**.github/workflows/ci.yml:**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
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

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build

      - name: Lint
        run: pnpm lint

      - name: Test
        run: pnpm test

      - name: Type check
        run: pnpm type-check
```

---

## Examples

### Filtering Builds

```bash
# Build only the web app
turbo build --filter=web

# Build web and its dependencies
turbo build --filter=web...

# Build everything that web depends on
turbo build --filter=...web

# Build all packages that changed
turbo build --filter=[origin/main]

# Run dev for specific apps
turbo dev --filter=web --filter=api
```

### Remote Caching

```bash
# Login to Vercel (for remote cache)
npx turbo login

# Link to your Vercel team
npx turbo link

# Now builds are cached across CI and team
turbo build
```

**turbo.json with remote cache:**

```json
{
  "remoteCache": {
    "signature": true
  }
}
```

---

## Common Mistakes

1. **Not using workspace protocol** - Use `workspace:*` for internal deps
2. **Circular dependencies** - Keep clear layer separation
3. **Too many packages** - Start with few, split when needed
4. **Missing dependency declarations** - Packages must declare all dependencies
5. **Not caching properly** - Ensure outputs are correctly specified

---

## Checklist

- [ ] pnpm-workspace.yaml configured
- [ ] turbo.json with proper pipeline
- [ ] Shared TypeScript config
- [ ] Shared ESLint config
- [ ] Internal packages use workspace:*
- [ ] CI caches node_modules and turbo cache
- [ ] .gitignore includes node_modules and dist
- [ ] Remote caching configured (optional)

---

## Next Steps

- M-JS-001: Project Setup
- M-DO-001: CI/CD with GitHub Actions
- M-JS-008: Code Quality

---

*Methodology M-JS-007 v1.0*
