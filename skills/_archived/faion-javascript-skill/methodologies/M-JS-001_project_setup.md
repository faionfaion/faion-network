# M-JS-001: JavaScript/TypeScript Project Setup

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Beginner
- **Tags:** #dev, #javascript, #typescript, #setup, #methodology
- **Agent:** faion-code-agent

---

## Problem

JavaScript projects can become messy without proper structure. Package managers, bundlers, and configuration files multiply quickly. You need a standardized setup that scales from small projects to enterprise applications.

## Promise

After this methodology, you will have a professional JavaScript/TypeScript project with proper tooling, linting, formatting, and type safety configured from the start.

## Overview

Modern JavaScript development uses npm/pnpm/yarn for dependencies, TypeScript for type safety, and ESLint/Prettier for code quality. This methodology covers all three ecosystems.

---

## Framework

### Step 1: Choose Package Manager

```bash
# npm (default, comes with Node.js)
npm --version

# pnpm (faster, disk-efficient)
npm install -g pnpm
pnpm --version

# yarn (legacy projects)
npm install -g yarn
yarn --version

# bun (fastest, new runtime)
curl -fsSL https://bun.sh/install | bash
bun --version
```

**Recommendation:** Use pnpm for new projects. It is faster and saves disk space.

### Step 2: Initialize Project

```bash
# Create project directory
mkdir my-project && cd my-project

# Initialize with npm
npm init -y

# Or with pnpm
pnpm init

# Or with bun
bun init
```

### Step 3: Add TypeScript

```bash
# Install TypeScript
pnpm add -D typescript @types/node

# Initialize tsconfig.json
npx tsc --init
```

**tsconfig.json (recommended):**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM"],
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Step 4: Configure ESLint

```bash
# Install ESLint with TypeScript support
pnpm add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Or use the new flat config
pnpm add -D eslint @eslint/js typescript-eslint
```

**eslint.config.js (flat config):**

```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strict,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'warn',
    },
  },
  {
    ignores: ['dist/**', 'node_modules/**'],
  }
);
```

### Step 5: Configure Prettier

```bash
# Install Prettier
pnpm add -D prettier eslint-config-prettier
```

**.prettierrc:**

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

**.prettierignore:**

```
dist
node_modules
*.md
```

### Step 6: Add Scripts

**package.json:**

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "format": "prettier --write 'src/**/*.{ts,tsx,json}'",
    "check": "tsc --noEmit && eslint src && prettier --check src",
    "test": "vitest"
  }
}
```

---

## Templates

### Project Structure

```
my-project/
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── eslint.config.js
├── .prettierrc
├── .gitignore
├── .env.example
├── README.md
├── src/
│   ├── index.ts
│   ├── config/
│   │   └── index.ts
│   ├── utils/
│   │   └── index.ts
│   └── types/
│       └── index.ts
├── tests/
│   └── index.test.ts
└── dist/           # Generated, gitignored
```

### .gitignore

```
# Dependencies
node_modules/
.pnpm-store/

# Build output
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
pnpm-debug.log*

# Test coverage
coverage/
```

### Minimal package.json

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "lint": "eslint src",
    "test": "vitest"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "eslint": "^9.0.0",
    "prettier": "^3.2.0",
    "tsx": "^4.7.0",
    "typescript": "^5.4.0",
    "typescript-eslint": "^7.0.0",
    "vitest": "^1.3.0"
  }
}
```

---

## Examples

### Node.js CLI Tool

```bash
pnpm init
pnpm add -D typescript @types/node tsx
pnpm add commander chalk

# Add to package.json
"bin": {
  "mycli": "./dist/cli.js"
}
```

### Express API

```bash
pnpm add express
pnpm add -D @types/express tsx
```

```typescript
// src/index.ts
import express from 'express';

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### React Application

```bash
# Vite is recommended for React
pnpm create vite my-react-app --template react-ts
```

---

## Common Mistakes

1. **Missing "type": "module"** - Required for ESM in Node.js
2. **Wrong moduleResolution** - Use "bundler" for modern tooling
3. **Ignoring strict mode** - Always enable `strict: true` in TypeScript
4. **Mixing CommonJS and ESM** - Pick one and be consistent
5. **Not pinning versions** - Use lockfiles and consider pinning major versions

---

## Checklist

- [ ] Package manager chosen (pnpm recommended)
- [ ] TypeScript configured with strict mode
- [ ] ESLint configured with TypeScript rules
- [ ] Prettier configured and integrated with ESLint
- [ ] Scripts defined for dev, build, lint, test
- [ ] .gitignore includes node_modules, dist, .env
- [ ] Project structure follows conventions

---

## Next Steps

- M-JS-002: React Patterns
- M-JS-004: TypeScript Patterns
- M-JS-005: Testing with Jest/Vitest

---

*Methodology M-JS-001 v1.0*
