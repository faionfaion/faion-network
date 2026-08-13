# Bun Runtime

## Summary

**One-sentence:** Produces a Bun-based JS/TS service scaffold (Bun runtime + bunfig + drizzle + Hono + Bun.test) pinned to a specific Bun version and gated in CI.

**One-paragraph:** Produces a Bun-based JS/TS service scaffold (Bun runtime + bunfig + drizzle + Hono + Bun.test) pinned to a specific Bun version and gated in CI. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- JS/TS project on Node-style runtime where Bun is a viable replacement.
- Single-binary toolchain (bundler + package manager + test runner) is a goal.
- CI runner supports Bun (oven-sh/setup-bun@v2 available).
- Team is willing to pin and freeze the Bun version.

## Skip If (ANY kills it)

- Production target needs npm-only ecosystem (some enterprise registries are not Bun-compatible).
- Project uses Node-specific native modules without Bun shims.
- Team has no capacity to maintain a second toolchain (Bun + Node) during migration.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | TS5 strict baseline this scaffold inherits. |
| `free/dev/software-developer/documentation` | Documents the file table + AGENTS.md pair this methodology depends on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to bun-runtime | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold the output skeleton | sonnet | Mechanical, deterministic. |
| Refine domain-specific content | opus | Needs judgement. |
| Validate against output contract | sonnet | Schema check, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bunfig.toml` | Bun runtime config with frozen-lockfile and coverage enabled. |
| `templates/dockerfile` | Bun production Dockerfile (multi-stage, distroless). |
| `templates/drizzle-schema.ts` | Drizzle ORM schema template wired to Bun. |
| `templates/hono-server.ts` | Hono HTTP server template on Bun.serve. |
| `templates/package.json` | Pinned Bun version + dev/start/test/build scripts. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bun-runtime.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-coverage]] — see methodology AGENTS.md for context.
- [[code-review]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/bunfig.toml`

```toml
[install]
# Frozen lockfile in CI — equivalent to npm ci
frozen-lockfile = true

[test]
coverage = true
coverageDir = "./coverage"
timeout = 5000

[build]
minify = true
sourcemap = "external"
```

### `templates/dockerfile`

```text
# syntax=docker/dockerfile:1.7
# Multi-stage Bun Dockerfile — pin version to match package.json packageManager field.

FROM oven/bun:1.1.34-alpine AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN --mount=type=cache,target=/root/.bun/install/cache \
    bun install --frozen-lockfile --production

FROM oven/bun:1.1.34-alpine AS build
WORKDIR /app
COPY package.json bun.lockb ./
RUN --mount=type=cache,target=/root/.bun/install/cache \
    bun install --frozen-lockfile
COPY . .
RUN bun run typecheck && bun test && \
    bun build src/index.ts --target=bun --outdir dist --minify

FROM oven/bun:1.1.34-alpine AS run
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER bun
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD bun -e "fetch('http://localhost:3000/health').then(r=>r.ok?process.exit(0):process.exit(1))"
ENTRYPOINT ["bun", "run", "dist/index.js"]
```

### `templates/drizzle-schema.ts`

```typescript
// src/db/schema.ts — Drizzle ORM schema with bun:sqlite
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core"
import { sql } from "drizzle-orm"

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" })
    .notNull()
    .default(sql`CURRENT_TIMESTAMP`),
})

// src/db/index.ts — Drizzle instance with bun:sqlite
import { drizzle } from "drizzle-orm/bun-sqlite"
import { Database } from "bun:sqlite"
import * as schema from "./schema"

const sqlite = new Database("app.db")
export const db = drizzle(sqlite, { schema })
```

### `templates/hono-server.ts`

```typescript
// src/index.ts — Hono server with middleware, Zod validation, JWT-protected routes
import { Hono } from "hono"
import { cors } from "hono/cors"
import { logger } from "hono/logger"
import { jwt } from "hono/jwt"
import { zValidator } from "@hono/zod-validator"
import { z } from "zod"

const app = new Hono()

// Middleware
app.use("*", logger())
app.use("/api/*", cors())

// Public routes
app.get("/health", (c) => c.json({ status: "ok" }))

// Auth routes
app.post(
  "/api/auth/login",
  zValidator(
    "json",
    z.object({
      email: z.string().email(),
      password: z.string().min(8),
    })
  ),
  async (c) => {
    const { email, password } = c.req.valid("json")
    // Replace with real auth logic
    const token = "jwt-token"
    return c.json({ token })
  }
)

// Protected routes
const api = new Hono()
api.use("*", jwt({ secret: Bun.env.JWT_SECRET! }))

api.get("/users", async (c) => {
  return c.json({ data: [] })
})

api.post(
  "/users",
  zValidator(
    "json",
    z.object({
      email: z.string().email(),
      name: z.string().min(1),
    })
  ),
  async (c) => {
    const data = c.req.valid("json")
    return c.json({ data }, 201)
  }
)

app.route("/api", api)

// Start server — Hono adapter for Bun.serve
export default {
  port: Bun.env.PORT || 3000,
  fetch: app.fetch,
}
```

### `templates/package.json`

```json
{
  "name": "my-bun-app",
  "type": "module",
  "packageManager": "bun@1.1.34",
  "scripts": {
    "dev": "bun --watch run src/index.ts",
    "start": "bun run src/index.ts",
    "test": "bun test",
    "typecheck": "tsc --noEmit",
    "build": "bun build ./src/index.ts --outdir ./dist --target bun --minify --sourcemap=external"
  },
  "dependencies": {
    "hono": "^4.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/bun": "^1.0.0",
    "@hono/zod-validator": "^0.2.0",
    "hono": "^4.0.0",
    "typescript": "^5.4.0"
  }
}
```
