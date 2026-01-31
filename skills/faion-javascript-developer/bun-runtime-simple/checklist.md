# Bun Runtime: Implementation Checklist

Step-by-step guide for adopting Bun in your project.

## Phase 1: Assessment

- [ ] **Verify project compatibility**
  - [ ] Check for Node.js-specific dependencies (C++ addons)
  - [ ] Review AWS Lambda requirements (limited Bun support)
  - [ ] Confirm team is ready for newer runtime
  - [ ] Document current Node.js version and dependencies

- [ ] **Evaluate performance gains**
  - [ ] Identify current bottlenecks (startup time, test speed, install time)
  - [ ] Estimate expected improvements
  - [ ] Plan performance testing strategy

- [ ] **Check tooling support**
  - [ ] Verify IDE support (VS Code, WebStorm)
  - [ ] Check CI/CD platform support
  - [ ] Review Docker base image availability

## Phase 2: Project Setup

- [ ] **Install Bun**
  ```bash
  curl -fsSL https://bun.sh/install | bash
  # OR
  npm install -g bun
  ```

- [ ] **Initialize project**
  - [ ] Run `bun init` for new project
  - [ ] OR migrate existing: copy package.json
  - [ ] Create `bunfig.toml` configuration

- [ ] **Configure bunfig.toml**
  ```toml
  [install]
  frozen-lockfile = true

  [test]
  coverage = true
  timeout = 5000

  [build]
  minify = true
  sourcemap = "external"
  ```

- [ ] **Update package.json scripts**
  ```json
  {
    "scripts": {
      "dev": "bun --watch run src/index.ts",
      "build": "bun build ./src/index.ts --outdir ./dist",
      "test": "bun test",
      "start": "bun run dist/index.js"
    }
  }
  ```

## Phase 3: Dependency Migration

- [ ] **Install dependencies**
  - [ ] Run `bun install` (creates bun.lockb)
  - [ ] Verify all packages installed correctly
  - [ ] Test application functionality

- [ ] **Replace Node.js-specific packages**
  - [ ] **DON'T install:** `node-fetch` (use native `fetch`)
  - [ ] **DON'T install:** `bcrypt` (use `Bun.password`)
  - [ ] **DON'T install:** `dotenv` (Bun reads .env automatically)
  - [ ] **DO keep:** Database drivers (pg, mysql2, mongodb)
  - [ ] **DO keep:** Framework packages (Express, Fastify, Hono)

- [ ] **Update imports**
  ```typescript
  // Before (Node.js)
  import fetch from 'node-fetch';
  import bcrypt from 'bcrypt';
  import dotenv from 'dotenv';
  dotenv.config();

  // After (Bun)
  // fetch is global
  const hash = await Bun.password.hash(password);
  // Bun.env automatically loaded
  ```

## Phase 4: Framework Selection

### Option A: Native Bun.serve

- [ ] **When to use:** Maximum performance, simple API
- [ ] **Setup:**
  ```typescript
  const server = Bun.serve({
    port: 3000,
    fetch(request) {
      return new Response('Hello World');
    },
  });
  ```

### Option B: Hono Framework

- [ ] **When to use:** Need routing, middleware, validation
- [ ] **Install:** `bun add hono @hono/zod-validator`
- [ ] **Setup:**
  ```typescript
  import { Hono } from 'hono';
  import { logger } from 'hono/logger';
  import { cors } from 'hono/cors';

  const app = new Hono();
  app.use('*', logger());
  app.use('/api/*', cors());

  export default {
    port: 3000,
    fetch: app.fetch,
  };
  ```

### Option C: Express/Fastify

- [ ] **When to use:** Existing Express/Fastify codebase
- [ ] **Note:** Works but less optimal than Hono/native
- [ ] **Keep existing code:** No changes needed

## Phase 5: Testing Migration

- [ ] **Update test files**
  - [ ] Replace Jest/Vitest imports with `bun:test`
  ```typescript
  import { describe, it, expect, mock } from 'bun:test';
  ```

- [ ] **Migrate test patterns**
  - [ ] `jest.fn()` → `mock(() => {})`
  - [ ] `jest.spyOn()` → `mock.module()`
  - [ ] Keep `describe`, `it`, `expect` syntax (compatible)

- [ ] **Run tests**
  - [ ] Execute `bun test`
  - [ ] Fix any incompatibilities
  - [ ] Verify coverage reports

## Phase 6: File Operations

- [ ] **Replace fs/promises with Bun APIs**
  ```typescript
  // Before
  import fs from 'fs/promises';
  const content = await fs.readFile('file.txt', 'utf-8');

  // After
  const file = Bun.file('file.txt');
  const content = await file.text();
  ```

- [ ] **Use native Bun methods**
  - [ ] Read: `Bun.file(path).text()`, `.json()`, `.arrayBuffer()`
  - [ ] Write: `Bun.write(path, content)`
  - [ ] Stream: `Bun.file(path).stream()`
  - [ ] Copy: `Bun.write(dest, Bun.file(src))`

## Phase 7: Environment Variables

- [ ] **Remove dotenv**
  - [ ] Delete `import 'dotenv/config'`
  - [ ] Remove `dotenv` package

- [ ] **Use Bun.env directly**
  ```typescript
  const dbUrl = Bun.env.DATABASE_URL;
  const port = Bun.env.PORT || 3000;
  ```

- [ ] **Create type-safe env wrapper**
  ```typescript
  interface Env {
    DATABASE_URL: string;
    JWT_SECRET: string;
    PORT?: string;
  }

  function getEnv(): Env {
    const required = ['DATABASE_URL', 'JWT_SECRET'];
    for (const key of required) {
      if (!Bun.env[key]) {
        throw new Error(`Missing env var: ${key}`);
      }
    }
    return Bun.env as unknown as Env;
  }
  ```

## Phase 8: Build & Bundle

- [ ] **Configure build**
  ```bash
  bun build ./src/index.ts \
    --outdir ./dist \
    --target bun \
    --minify \
    --sourcemap=external
  ```

- [ ] **For Node.js compatibility**
  ```bash
  bun build ./src/index.ts \
    --outdir ./dist \
    --target node \
    --minify
  ```

- [ ] **Multi-entry builds**
  ```bash
  bun build ./src/index.ts ./src/worker.ts --outdir ./dist
  ```

## Phase 9: Docker Deployment

- [ ] **Create Dockerfile**
  ```dockerfile
  FROM oven/bun:1-alpine

  WORKDIR /app
  COPY package.json bun.lockb ./
  RUN bun install --frozen-lockfile

  COPY . .
  RUN bun build ./src/index.ts --outdir ./dist

  EXPOSE 3000
  CMD ["bun", "run", "dist/index.js"]
  ```

- [ ] **Test Docker build**
  - [ ] Build: `docker build -t myapp .`
  - [ ] Run: `docker run -p 3000:3000 myapp`
  - [ ] Verify functionality

## Phase 10: CI/CD Integration

- [ ] **Update GitHub Actions**
  ```yaml
  - name: Setup Bun
    uses: oven-sh/setup-bun@v1
    with:
      bun-version: latest

  - name: Install dependencies
    run: bun install --frozen-lockfile

  - name: Run tests
    run: bun test

  - name: Build
    run: bun build ./src/index.ts --outdir ./dist
  ```

- [ ] **Update other CI platforms**
  - [ ] GitLab CI: Install Bun via curl
  - [ ] CircleCI: Use Docker image `oven/bun`
  - [ ] Jenkins: Install Bun on agents

## Phase 11: Production Validation

- [ ] **Performance benchmarks**
  - [ ] Measure startup time
  - [ ] Measure request latency
  - [ ] Compare memory usage
  - [ ] Test concurrent load

- [ ] **Functionality validation**
  - [ ] Run E2E tests
  - [ ] Test all API endpoints
  - [ ] Verify database connections
  - [ ] Check external service integrations

- [ ] **Error handling**
  - [ ] Test error scenarios
  - [ ] Verify logging works
  - [ ] Check crash recovery

## Phase 12: Team Onboarding

- [ ] **Documentation**
  - [ ] Update README with Bun setup
  - [ ] Document Bun-specific patterns
  - [ ] Add troubleshooting guide

- [ ] **Developer setup**
  - [ ] Install Bun on all dev machines
  - [ ] Update IDE configurations
  - [ ] Run local testing

- [ ] **Training**
  - [ ] Share Bun vs Node.js differences
  - [ ] Review new APIs (Bun.file, Bun.password, etc.)
  - [ ] Discuss performance improvements

## Anti-Pattern Checklist

Verify you're NOT doing these:

- [ ] **NOT** installing `node-fetch`, `bcrypt`, `dotenv`
- [ ] **NOT** using `require()` (use ES modules)
- [ ] **NOT** ignoring incompatibilities (test thoroughly)
- [ ] **NOT** using Node.js-specific APIs without fallback
- [ ] **NOT** skipping performance benchmarks
- [ ] **NOT** deploying without testing in Bun environment

## Quick Decision Matrix

| Current Setup | Recommended Action |
|---------------|-------------------|
| New TypeScript project | ✅ Use Bun from start |
| Existing simple Node.js app | ✅ Migrate to Bun |
| Monorepo with complex deps | ⚠️ Test thoroughly first |
| AWS Lambda deployment | ❌ Stay with Node.js |
| C++ native modules | ❌ Stay with Node.js |
| Enterprise with strict policies | ⚠️ Get approval first |
