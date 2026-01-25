# Modern JavaScript/TypeScript Standards

**Core principles for modern JS/TS development (2025-2026)**

---

## Quick Reference

**Supported Runtimes:**
- Node.js: 20 LTS, 22 LTS (prefer 22+)
- Bun: 1.x (for modern projects)
- Deno: 2.x (alternative runtime)
- Browser: ES2022+ with bundler

**Recommended Stack:**
- TypeScript 5.x with strict mode
- React 19.x / Next.js 15.x for frontend
- Express 5.x / Fastify 5.x for backend
- Vitest / Jest for testing
- ESLint 9.x (flat config) + Prettier

---

## Core Principles

### 1. TypeScript First

```typescript
// ALWAYS use TypeScript with strict mode
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

### 2. Prefer `const` and Arrow Functions

```typescript
// Prefer const for immutability
const users = ['Alice', 'Bob'];

// Arrow functions for callbacks and short functions
const double = (n: number) => n * 2;
const getUser = async (id: string) => {
  return await db.users.findById(id);
};

// Regular functions for hoisting or `this` binding
function handleRequest(req: Request, res: Response) {
  // ...
}
```

### 3. Named Exports Over Default

```typescript
// Prefer named exports - easier to refactor and search
export function createUser(data: UserData): User { ... }
export const USER_ROLES = ['admin', 'user'] as const;
export type UserRole = typeof USER_ROLES[number];

// Default only for framework requirements (Next.js pages, etc.)
export default function Page() { ... }
```

### 4. Explicit Types for Public APIs

```typescript
// Function parameters and returns - always typed
function processOrder(
  order: Order,
  options?: ProcessOptions,
): Promise<ProcessResult> {
  // ...
}

// Internal variables - infer when obvious
const count = 0;  // inferred as number
const items = []; // use explicit type: Item[] = []
```

---

## TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    // Type Checking (strict mode)
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,

    // Modules
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",

    // Paths (monorepo)
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"]
    },

    // Interop
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## Project Setup

### Package Manager Choice

| Manager | When to Use |
|---------|-------------|
| **pnpm** | Default choice - fast, disk-efficient, strict |
| **bun** | Bun runtime projects, maximum speed |
| **npm** | Legacy projects, maximum compatibility |
| **yarn** | Existing Yarn 4.x workspaces |

### pnpm Configuration

```yaml
# .npmrc
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false

# pnpm-workspace.yaml (monorepo)
packages:
  - 'apps/*'
  - 'packages/*'
```

### ESLint 9.x Flat Config

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    plugins: {
      react,
      'react-hooks': reactHooks,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_'
      }],
      '@typescript-eslint/explicit-function-return-type': ['error', {
        allowExpressions: true,
      }],
    },
  },
);
```

### Prettier Configuration

```json
// .prettierrc
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

---

## Decision Tree: Where to Put Code

```
What does the code do?
│
├─► UI rendering?
│   └─► components/
│
├─► Shared state logic?
│   └─► hooks/
│
├─► API calls?
│   └─► services/ or api/
│
├─► Data transformation?
│   └─► utils/
│
├─► Type definitions?
│   └─► types/ or colocated
│
└─► Third-party wrapper?
    └─► lib/
```

---

## Sources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/) - Official TypeScript documentation
- [Node.js Guides](https://nodejs.org/docs/) - Node.js official guides
- [Bun Documentation](https://bun.sh/docs) - Bun runtime docs
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) - Comprehensive guide (100k+ stars)
- [ESLint](https://eslint.org/) - JavaScript linting
- [Prettier](https://prettier.io/) - Code formatting
- [Vitest](https://vitest.dev/) - Fast unit testing
- [pnpm](https://pnpm.io/) - Fast, disk-efficient package manager
