# Bun Runtime: Code Templates

Ready-to-use templates for Bun projects.

## Project Configuration

### bunfig.toml

```toml
# Bun configuration file
[install]
# Lock dependencies
frozen-lockfile = true
# Production mode
production = false
# Registry
registry = "https://registry.npmjs.org/"

[test]
# Enable coverage
coverage = true
# Coverage directory
coverageDir = "./coverage"
# Test timeout (ms)
timeout = 5000
# Test reporter
reporter = "default"

[build]
# Minify output
minify = true
# Source maps
sourcemap = "external"
# Target runtime
target = "bun"
# Output directory
outdir = "./dist"

[run]
# Watch mode
hot = true
# Clear console on reload
clearScreen = true
```

### package.json

```json
{
  "name": "bun-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "bun --watch run src/index.ts",
    "build": "bun build ./src/index.ts --outdir ./dist --target bun",
    "build:node": "bun build ./src/index.ts --outdir ./dist --target node",
    "start": "bun run dist/index.js",
    "test": "bun test",
    "test:watch": "bun test --watch",
    "test:coverage": "bun test --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx}\""
  },
  "dependencies": {
    "hono": "^4.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/bun": "latest",
    "bun-types": "latest"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "types": ["bun-types"],
    "jsx": "react-jsx",
    "jsxImportSource": "react",

    "allowImportingTsExtensions": true,
    "noEmit": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true,

    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## HTTP Server Templates

### Native Bun.serve (Simple)

```typescript
// src/index.ts
const server = Bun.serve({
  port: Bun.env.PORT || 3000,

  fetch(request: Request): Response | Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return new Response('OK', { status: 200 });
    }

    // JSON response
    if (url.pathname === '/api/users' && request.method === 'GET') {
      return Response.json({ users: [] });
    }

    // POST with body
    if (url.pathname === '/api/users' && request.method === 'POST') {
      return handleCreateUser(request);
    }

    return new Response('Not Found', { status: 404 });
  },

  error(error: Error): Response {
    console.error('Server error:', error);
    return new Response('Internal Server Error', {
      status: 500,
      headers: { 'Content-Type': 'text/plain' }
    });
  },
});

console.log(`Server running on http://localhost:${server.port}`);

async function handleCreateUser(request: Request): Promise<Response> {
  try {
    const body = await request.json();

    // Validate
    if (!body.email || !body.name) {
      return Response.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Create user (mock)
    const user = {
      id: crypto.randomUUID(),
      ...body,
      createdAt: new Date().toISOString(),
    };

    return Response.json({ data: user }, { status: 201 });
  } catch (error) {
    return Response.json(
      { error: 'Invalid JSON' },
      { status: 400 }
    );
  }
}
```

### Hono Framework (Recommended)

```typescript
// src/index.ts
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { cors } from 'hono/cors';
import { jwt } from 'hono/jwt';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const app = new Hono();

// Global middleware
app.use('*', logger());
app.use('/api/*', cors());

// Health check
app.get('/health', (c) => c.text('OK'));

// Public routes
app.post(
  '/api/auth/login',
  zValidator('json', z.object({
    email: z.string().email(),
    password: z.string().min(8),
  })),
  async (c) => {
    const { email, password } = c.req.valid('json');

    // Authenticate (mock)
    const user = await authenticateUser(email, password);
    if (!user) {
      return c.json({ error: 'Invalid credentials' }, 401);
    }

    // Generate JWT
    const token = await generateToken(user);

    return c.json({ token, user });
  }
);

// Protected routes
const api = new Hono();
api.use('*', jwt({ secret: Bun.env.JWT_SECRET! }));

api.get('/users', async (c) => {
  const users = await getUsers();
  return c.json({ data: users });
});

api.post(
  '/users',
  zValidator('json', z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(['admin', 'user']).default('user'),
  })),
  async (c) => {
    const data = c.req.valid('json');
    const user = await createUser(data);
    return c.json({ data: user }, 201);
  }
);

api.put(
  '/users/:id',
  zValidator('json', z.object({
    name: z.string().min(1).max(100).optional(),
    role: z.enum(['admin', 'user']).optional(),
  })),
  async (c) => {
    const id = c.req.param('id');
    const data = c.req.valid('json');
    const user = await updateUser(id, data);

    if (!user) {
      return c.json({ error: 'User not found' }, 404);
    }

    return c.json({ data: user });
  }
);

api.delete('/users/:id', async (c) => {
  const id = c.req.param('id');
  await deleteUser(id);
  return c.json({ message: 'User deleted' });
});

app.route('/api', api);

// Error handler
app.onError((err, c) => {
  console.error('Error:', err);
  return c.json({ error: 'Internal Server Error' }, 500);
});

export default {
  port: Bun.env.PORT || 3000,
  fetch: app.fetch,
};

// Service functions (mock)
async function authenticateUser(email: string, password: string) {
  return { id: '1', email, name: 'John Doe' };
}

async function generateToken(user: any) {
  return 'mock-jwt-token';
}

async function getUsers() {
  return [{ id: '1', email: 'john@example.com', name: 'John Doe' }];
}

async function createUser(data: any) {
  return { id: crypto.randomUUID(), ...data };
}

async function updateUser(id: string, data: any) {
  return { id, ...data };
}

async function deleteUser(id: string) {
  // Delete user
}
```

### WebSocket Server

```typescript
// src/websocket.ts
const server = Bun.serve({
  port: 3000,

  websocket: {
    open(ws) {
      console.log('Client connected');
      ws.send(JSON.stringify({ type: 'welcome', message: 'Connected' }));
    },

    message(ws, message) {
      const data = JSON.parse(message as string);
      console.log('Received:', data);

      // Echo back
      ws.send(JSON.stringify({
        type: 'echo',
        data: data,
        timestamp: Date.now(),
      }));

      // Broadcast to all clients
      server.publish('global', JSON.stringify({
        type: 'broadcast',
        data: data,
      }));
    },

    close(ws, code, reason) {
      console.log('Client disconnected:', code, reason);
    },

    error(ws, error) {
      console.error('WebSocket error:', error);
    },
  },

  fetch(req, server) {
    const url = new URL(req.url);

    // Upgrade to WebSocket
    if (url.pathname === '/ws') {
      const upgraded = server.upgrade(req);
      if (upgraded) {
        return; // Connection upgraded
      }
      return new Response('Expected WebSocket', { status: 400 });
    }

    return new Response('Not Found', { status: 404 });
  },
});

console.log(`WebSocket server on ws://localhost:${server.port}/ws`);
```

## File Operations

### Read Operations

```typescript
// Read as text
const file = Bun.file('data.txt');
const text = await file.text();

// Read as JSON
const jsonFile = Bun.file('config.json');
const config = await jsonFile.json();

// Read as ArrayBuffer
const binaryFile = Bun.file('image.png');
const buffer = await binaryFile.arrayBuffer();

// Stream large file
const largeFile = Bun.file('large.csv');
const stream = largeFile.stream();

for await (const chunk of stream) {
  // Process chunk
  console.log(chunk);
}

// Check if file exists
const exists = await Bun.file('maybe.txt').exists();
if (exists) {
  const content = await Bun.file('maybe.txt').text();
}
```

### Write Operations

```typescript
// Write text
await Bun.write('output.txt', 'Hello World');

// Write JSON
await Bun.write('data.json', JSON.stringify({ key: 'value' }, null, 2));

// Write ArrayBuffer
const buffer = new Uint8Array([1, 2, 3, 4]);
await Bun.write('binary.dat', buffer);

// Copy file
await Bun.write('copy.txt', Bun.file('original.txt'));

// Append to file (not directly supported, read then write)
const existing = await Bun.file('log.txt').text();
await Bun.write('log.txt', existing + '\nNew line');
```

## Environment Variables

```typescript
// src/config.ts
export interface Env {
  NODE_ENV: 'development' | 'production' | 'test';
  PORT: string;
  DATABASE_URL: string;
  JWT_SECRET: string;
  API_KEY: string;
}

export function getEnv(): Env {
  const required: (keyof Env)[] = [
    'DATABASE_URL',
    'JWT_SECRET',
    'API_KEY',
  ];

  for (const key of required) {
    if (!Bun.env[key]) {
      throw new Error(`Missing required environment variable: ${key}`);
    }
  }

  return {
    NODE_ENV: (Bun.env.NODE_ENV as Env['NODE_ENV']) || 'development',
    PORT: Bun.env.PORT || '3000',
    DATABASE_URL: Bun.env.DATABASE_URL!,
    JWT_SECRET: Bun.env.JWT_SECRET!,
    API_KEY: Bun.env.API_KEY!,
  };
}

// Usage
const env = getEnv();
console.log(`Running on port ${env.PORT}`);
```

## Testing

### Basic Test

```typescript
// tests/math.test.ts
import { describe, it, expect } from 'bun:test';
import { add, subtract } from '../src/math';

describe('Math functions', () => {
  describe('add', () => {
    it('should add two numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(add(-2, 3)).toBe(1);
    });
  });

  describe('subtract', () => {
    it('should subtract two numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });
  });
});
```

### Mock Functions

```typescript
// tests/service.test.ts
import { describe, it, expect, mock, beforeEach } from 'bun:test';
import { fetchUser, createUser } from '../src/service';

describe('User service', () => {
  beforeEach(() => {
    // Reset mocks before each test
  });

  it('should fetch user by ID', async () => {
    const mockFetch = mock(() =>
      Promise.resolve({ id: '1', name: 'John' })
    );

    const result = await mockFetch('1');

    expect(result.name).toBe('John');
    expect(mockFetch).toHaveBeenCalledTimes(1);
    expect(mockFetch).toHaveBeenCalledWith('1');
  });

  it('should create user', async () => {
    const mockCreate = mock((data) =>
      Promise.resolve({ id: crypto.randomUUID(), ...data })
    );

    const result = await mockCreate({ name: 'Jane', email: 'jane@example.com' });

    expect(result.name).toBe('Jane');
    expect(result.id).toBeDefined();
  });
});
```

## Docker

### Dockerfile (Production)

```dockerfile
FROM oven/bun:1-alpine AS base
WORKDIR /app

# Install dependencies
FROM base AS deps
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

# Build
FROM base AS builder
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun build ./src/index.ts --outdir ./dist --target bun --minify

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

EXPOSE 3000
CMD ["bun", "run", "dist/index.js"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - JWT_SECRET=your-secret-key
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Run linter
        run: bun run lint

      - name: Run tests
        run: bun test --coverage

      - name: Build
        run: bun build ./src/index.ts --outdir ./dist
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image: oven/bun:1-alpine

stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - bun install --frozen-lockfile
    - bun run lint
    - bun test --coverage
  coverage: '/All files\s+\|\s+([\d.]+)/'

build:
  stage: build
  script:
    - bun install --frozen-lockfile
    - bun build ./src/index.ts --outdir ./dist --minify
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

deploy:
  stage: deploy
  script:
    - echo "Deploy to production"
  only:
    - main
```
