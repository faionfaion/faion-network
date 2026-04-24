# Bun Runtime

**High-performance JavaScript runtime with built-in tooling**

## When to Use

| Use Bun | Use Node.js |
|---------|-------------|
| New projects | Legacy codebases |
| Maximum performance | Complex native deps |
| TypeScript-first | Enterprise constraints |
| Monorepos | AWS Lambda (limited support) |
| Dev tooling | Maximum compatibility |

## Project Setup

```bash
# Initialize
bun init

# Dependencies
bun add express zod
bun add -d @types/express

# Run
bun run src/index.ts

# Watch mode
bun --watch run src/index.ts

# Test
bun test
```

## Configuration

```toml
# bunfig.toml
[install]
frozen-lockfile = true

[test]
coverage = true
coverageDir = "./coverage"
timeout = 5000

[build]
minify = true
sourcemap = "external"
```

## HTTP Server (Native Bun)

```typescript
const server = Bun.serve({
  port: 3000,

  fetch(request: Request): Response | Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/api/users' && request.method === 'GET') {
      return Response.json({ users: [] });
    }

    if (url.pathname === '/api/users' && request.method === 'POST') {
      return handleCreateUser(request);
    }

    return new Response('Not Found', { status: 404 });
  },

  error(error: Error): Response {
    console.error(error);
    return new Response('Internal Server Error', { status: 500 });
  },
});

async function handleCreateUser(request: Request): Promise<Response> {
  const body = await request.json();
  const user = await db.users.create({ data: body });
  return Response.json({ data: user }, { status: 201 });
}
```

## Using Hono Framework

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { jwt } from 'hono/jwt';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const app = new Hono();

// Middleware
app.use('*', logger());
app.use('/api/*', cors());

// Auth routes
app.post(
  '/api/auth/login',
  zValidator('json', z.object({
    email: z.string().email(),
    password: z.string().min(8),
  })),
  async (c) => {
    const { email, password } = c.req.valid('json');
    const user = await authService.authenticate(email, password);
    const token = await authService.generateToken(user);
    return c.json({ token });
  }
);

// Protected routes
const api = new Hono();
api.use('*', jwt({ secret: Bun.env.JWT_SECRET! }));

api.get('/users', async (c) => {
  const users = await userService.getUsers();
  return c.json({ data: users });
});

api.post(
  '/users',
  zValidator('json', z.object({
    email: z.string().email(),
    name: z.string().min(1),
  })),
  async (c) => {
    const data = c.req.valid('json');
    const user = await userService.createUser(data);
    return c.json({ data: user }, 201);
  }
);

app.route('/api', api);

export default {
  port: Bun.env.PORT || 3000,
  fetch: app.fetch,
};
```

## File Operations

```typescript
// Read
const file = Bun.file('data.json');
const content = await file.text();
const json = await file.json();
const bytes = await file.arrayBuffer();

// Write
await Bun.write('output.txt', 'Hello World');
await Bun.write('data.json', JSON.stringify({ key: 'value' }));

// Stream large files
const stream = Bun.file('large.csv').stream();
for await (const chunk of stream) {
  // Process chunk
}

// Copy
await Bun.write('copy.txt', Bun.file('original.txt'));

// Check exists
const exists = await Bun.file('path.txt').exists();
```

## Environment Variables

```typescript
// Access
const dbUrl = Bun.env.DATABASE_URL;
const port = Bun.env.PORT || 3000;

// Type-safe
interface Env {
  DATABASE_URL: string;
  JWT_SECRET: string;
  PORT?: string;
}

function getEnv(): Env {
  const required = ['DATABASE_URL', 'JWT_SECRET'];

  for (const key of required) {
    if (!Bun.env[key]) {
      throw new Error(`Missing required env var: ${key}`);
    }
  }

  return Bun.env as unknown as Env;
}
```

## Testing

```typescript
import { describe, it, expect, beforeEach, mock } from 'bun:test';
import { createApp } from '../src/app';

describe('Users API', () => {
  let app: ReturnType<typeof createApp>;

  beforeEach(() => {
    app = createApp();
  });

  it('should return users list', async () => {
    const response = await app.request('/api/users');

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.users).toEqual([]);
  });

  it('should create user', async () => {
    const response = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@example.com',
        name: 'Test User',
      }),
    });

    expect(response.status).toBe(201);
    const data = await response.json();
    expect(data.data.email).toBe('test@example.com');
  });

  it('should validate input', async () => {
    const response = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'invalid', name: 'Test' }),
    });

    expect(response.status).toBe(400);
  });
});

// Mocking
describe('with mocks', () => {
  it('should mock function', async () => {
    const mockGetUser = mock(() =>
      Promise.resolve({ id: '1', name: 'Mock User' })
    );

    userService.getUser = mockGetUser;

    const result = await userService.getUser('1');
    expect(result.name).toBe('Mock User');
    expect(mockGetUser).toHaveBeenCalledWith('1');
  });
});
```

## Bundling

```bash
# Build for Bun
bun build ./src/index.ts --outdir ./dist --target bun --minify

# Build for Node.js
bun build ./src/index.ts --outdir ./dist --target node

# Build for browser
bun build ./src/client.ts --outdir ./dist --target browser

# Multiple entries
bun build ./src/index.ts ./src/worker.ts --outdir ./dist

# With source maps
bun build ./src/index.ts --outdir ./dist --sourcemap=external
```

## Native APIs

```typescript
// Password hashing (built-in)
const hash = await Bun.password.hash(password);
const valid = await Bun.password.verify(password, hash);

// Shell command
import { $ } from 'bun';
await $`ls -la`;

// Spawn process
const proc = Bun.spawn(['ls', '-la']);
const output = await new Response(proc.stdout).text();

// WebSocket (built-in)
const server = Bun.serve({
  websocket: {
    open(ws) {
      console.log('WebSocket connected');
    },
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    close(ws) {
      console.log('WebSocket disconnected');
    },
  },
  fetch(req, server) {
    if (server.upgrade(req)) {
      return; // WebSocket upgraded
    }
    return new Response('Expected WebSocket', { status: 400 });
  },
});
```

## Anti-patterns

```typescript
// Avoid: Third-party libs for built-in features
import fetch from 'node-fetch';  // BAD - use native fetch
import bcrypt from 'bcrypt';     // BAD - use Bun.password

// Good: Use native APIs
const response = await fetch(url);
const hash = await Bun.password.hash(password);

// Avoid: Ignoring Node.js incompatibilities
import { exec } from 'child_process';  // May differ from Node

// Good: Use Bun-specific APIs
import { $ } from 'bun';
await $`ls -la`;
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Bun project setup | haiku | Quick start automation |
| Bun vs Node performance | sonnet | Comparison analysis |

## Sources

- [Bun Documentation](https://bun.sh/docs) - Official docs and API reference
- [Hono Framework](https://hono.dev/) - Fast web framework for Bun
- [Bun GitHub](https://github.com/oven-sh/bun) - Source code and issues
- [Bun vs Node.js Performance](https://bun.sh/blog/bun-v1.0) - Official benchmarks
