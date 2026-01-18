# M-JS-006: Bun Runtime and Toolchain

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Intermediate
- **Tags:** #dev, #javascript, #bun, #runtime, #methodology
- **Agent:** faion-code-agent

---

## Problem

Node.js is slow for development tasks. npm install takes minutes, tests are sluggish, and bundling requires additional tools. You want a faster development experience without changing your code.

## Promise

After this methodology, you will use Bun as a drop-in replacement for Node.js, npm, and bundlers. Your development workflow will be 10-30x faster.

## Overview

Bun is an all-in-one JavaScript runtime that includes a package manager, bundler, and test runner. It runs TypeScript natively and is compatible with most Node.js code.

---

## Framework

### Step 1: Installation

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows (via WSL or PowerShell)
powershell -c "irm bun.sh/install.ps1 | iex"

# Homebrew
brew install oven-sh/bun/bun

# Verify
bun --version
```

### Step 2: Project Initialization

```bash
# Create new project
bun init

# This creates:
# - package.json
# - tsconfig.json
# - index.ts
# - .gitignore
# - README.md
```

**package.json (Bun-optimized):**

```json
{
  "name": "my-project",
  "module": "index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun --watch index.ts",
    "start": "bun index.ts",
    "test": "bun test",
    "build": "bun build ./index.ts --outdir ./dist"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

### Step 3: Package Management

```bash
# Install dependencies (faster than npm/pnpm)
bun install

# Add dependency
bun add express zod

# Add dev dependency
bun add -d typescript @types/node

# Remove dependency
bun remove express

# Update all dependencies
bun update

# Run binary from node_modules
bunx eslint .
```

**Bun lockfile (bun.lockb):**
- Binary format (faster parsing)
- Commit to git
- Use `bun install --frozen-lockfile` in CI

### Step 4: Running Scripts

```bash
# Run TypeScript directly (no build step)
bun run index.ts
bun index.ts  # shorthand

# Watch mode
bun --watch index.ts

# Run package.json scripts
bun run dev
bun run test

# Run with environment variables
bun --env-file=.env index.ts
```

### Step 5: Built-in APIs

**File System:**

```typescript
// Read file
const file = Bun.file('data.json');
const content = await file.text();
const json = await file.json();

// Write file
await Bun.write('output.txt', 'Hello World');
await Bun.write('data.json', JSON.stringify({ key: 'value' }));

// File info
const size = file.size;
const type = file.type; // MIME type
```

**HTTP Server:**

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === '/') {
      return new Response('Hello from Bun!');
    }

    if (url.pathname === '/api/users') {
      return Response.json({ users: [] });
    }

    return new Response('Not Found', { status: 404 });
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

**SQLite (built-in):**

```typescript
import { Database } from 'bun:sqlite';

const db = new Database('mydb.sqlite');

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

// Insert
const insert = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
insert.run('John', 'john@example.com');

// Query
const query = db.prepare('SELECT * FROM users WHERE name = ?');
const user = query.get('John');

// All results
const all = db.query('SELECT * FROM users').all();
```

**Password Hashing:**

```typescript
// Hash password
const hash = await Bun.password.hash('mypassword', {
  algorithm: 'argon2id', // or 'bcrypt'
  memoryCost: 65536,
  timeCost: 2,
});

// Verify password
const isValid = await Bun.password.verify('mypassword', hash);
```

### Step 6: Testing

```typescript
// tests/example.test.ts
import { describe, expect, it, beforeEach, mock } from 'bun:test';

describe('math', () => {
  it('adds numbers', () => {
    expect(1 + 1).toBe(2);
  });

  it('works with async', async () => {
    const result = await Promise.resolve(42);
    expect(result).toBe(42);
  });
});

// Mocking
const mockFetch = mock(() => Promise.resolve({ json: () => ({ data: 'test' }) }));
globalThis.fetch = mockFetch;

// Run tests
// bun test
// bun test --watch
// bun test --coverage
```

### Step 7: Bundling

```bash
# Bundle for production
bun build ./src/index.ts --outdir ./dist --minify

# Bundle with external dependencies
bun build ./src/index.ts --outdir ./dist --external express

# Bundle for browser
bun build ./src/app.ts --outdir ./dist --target browser

# Multiple entry points
bun build ./src/index.ts ./src/worker.ts --outdir ./dist
```

```typescript
// Programmatic bundling
const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  minify: true,
  splitting: true,
  target: 'browser',
  external: ['react', 'react-dom'],
});

if (!result.success) {
  console.error('Build failed:', result.logs);
}
```

---

## Templates

### Express-like Server

```typescript
// server.ts
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

const app = new Hono();

// Middleware
app.use('*', cors());
app.use('*', logger());

// Routes
app.get('/', (c) => c.json({ message: 'Hello Bun!' }));

app.get('/users/:id', (c) => {
  const id = c.req.param('id');
  return c.json({ id, name: 'User' });
});

app.post('/users', async (c) => {
  const body = await c.req.json();
  return c.json({ id: crypto.randomUUID(), ...body }, 201);
});

// Start server
export default {
  port: process.env.PORT || 3000,
  fetch: app.fetch,
};
```

### Configuration File

```typescript
// bunfig.toml
[install]
# Install exact versions
exact = true

# Use global cache
globalBin = "~/.bun/bin"

[test]
# Test configuration
coverage = true
coverageDir = "coverage"

[run]
# Default environment file
env = ".env"
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM oven/bun:1 as builder

WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun build ./src/index.ts --outdir ./dist --target bun

# Production image
FROM oven/bun:1-slim

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER bun
EXPOSE 3000
CMD ["bun", "run", "dist/index.js"]
```

---

## Examples

### WebSocket Server

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (server.upgrade(req)) {
      return; // Upgrade to WebSocket
    }
    return new Response('Expected WebSocket', { status: 400 });
  },
  websocket: {
    open(ws) {
      console.log('Client connected');
      ws.send('Welcome!');
    },
    message(ws, message) {
      console.log('Received:', message);
      ws.send(`Echo: ${message}`);
    },
    close(ws) {
      console.log('Client disconnected');
    },
  },
});
```

### Worker Threads

```typescript
// main.ts
const worker = new Worker('./worker.ts');

worker.postMessage({ task: 'heavy-computation', data: [1, 2, 3] });

worker.onmessage = (event) => {
  console.log('Result:', event.data);
};

// worker.ts
self.onmessage = (event) => {
  const { task, data } = event.data;

  if (task === 'heavy-computation') {
    const result = data.reduce((a, b) => a + b, 0);
    self.postMessage(result);
  }
};
```

### Shell Commands

```typescript
import { $ } from 'bun';

// Run shell command
const output = await $`ls -la`.text();
console.log(output);

// With variables (automatically escaped)
const filename = 'my file.txt';
await $`cat ${filename}`;

// Piping
const result = await $`echo "hello" | tr 'a-z' 'A-Z'`.text();
console.log(result); // HELLO

// Check exit code
const proc = await $`false`.nothrow();
console.log(proc.exitCode); // 1
```

---

## Common Mistakes

1. **Assuming 100% Node.js compatibility** - Some Node.js APIs are missing or different
2. **Not using native Bun APIs** - They are faster than Node.js equivalents
3. **Mixing npm/pnpm with Bun** - Use Bun consistently for package management
4. **Ignoring bun.lockb** - Commit it for reproducible installs
5. **Not testing in Node.js** - If shipping to Node.js, test there too

---

## Checklist

- [ ] Bun installed and configured
- [ ] bun.lockb committed to git
- [ ] TypeScript types installed (@types/bun)
- [ ] Development scripts use --watch
- [ ] Tests running with bun test
- [ ] Docker image uses oven/bun base
- [ ] CI/CD installs with --frozen-lockfile

---

## Next Steps

- M-JS-003: Node.js Patterns (for comparison)
- M-JS-005: Testing with Jest/Vitest
- M-DO-003: Docker Basics

---

*Methodology M-JS-006 v1.0*
