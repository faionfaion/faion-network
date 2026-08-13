# Node.js Patterns

## Summary

**One-sentence:** Produces a layered TypeScript Express scaffold spec with controllers/services/middleware/errors and Pino request logging, with mandatory middleware ordering.

**Ефективно для:** Bootstrapping or refactoring a Node HTTP service into a testable layered structure where each layer can be unit-tested independently and the error handler is guaranteed to catch every thrown exception.

**One-paragraph:** This methodology turns the "how should we structure a new TS Express service?" question into a single auditable spec artefact. The output names the feature folders, the middleware order, the createApp factory boundary, the error class hierarchy, and the Pino logger wiring. Downstream tasks (codegen, code review, refactor PRs) consume the spec without re-deriving the rationale. Misordered middleware (error handler before routes), inline app.listen() inside createApp(), and scattered process.env reads are the three failures this methodology forbids by contract.

## Applies If (ALL must hold)

- Target runtime is Node ≥ 20 with Express 4.x or 5.x — not edge runtimes (Workers, Vercel Edge, Deno Deploy).
- The service exposes an HTTP layer (REST/JSON) — not a CLI script, websocket-first daemon, or worker process.
- The codebase uses TypeScript with strict mode (or migrates to it as part of the work).
- The team commits to a layered separation (routes → controllers → services → models) instead of all-in-one route files.
- Downstream readers (codegen agents, reviewers) will consume the spec as the source of truth for module layout.

## Skip If (ANY kills it)

- Service runs on an edge runtime (Cloudflare Workers, Vercel Edge, Deno Deploy) — Express is Node-only; use Hono / Itty Router instead.
- High-throughput WebSocket-first service — Express's middleware chain is slow; use uWebSockets.js or Fastify.
- Single-file script or CLI tool with no HTTP layer — layering scaffold is pure overhead.
- Frontend-only React/Next.js project — no Node HTTP server owned.
- Team has already committed to NestJS / AdonisJS — those frameworks own structure decisions; this methodology conflicts with their conventions.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Target Node version | semver string | `package.json` engines field |
| List of resources (users, products, …) | bulleted text | product brief or existing routes file |
| Auth model (JWT / session / API key) | one-word choice | architecture decision record |
| Existing tsconfig.json (if migrating) | JSON | repo root |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[typescript-strict-mode]]` | Strict tsconfig is the baseline for type-safe layer boundaries. |
| `[[typescript-patterns]]` | Discriminated unions for the error class hierarchy + Result types. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: middleware order, createApp factory, env config, error classes, async handlers, structured logging, transport flush | ~1100 |
| `content/02-output-contract.xml` | essential | JSON schema for the scaffold spec output (folders, middleware order list, error classes, logger config) + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: error handler before routes, listen() inside factory, scattered process.env, missing async cleanup, console.log in production | ~800 |
| `content/04-procedure.xml` | medium | 6 steps: collect resources → decide auth → emit folder tree → emit middleware order → emit error classes → emit logger config | ~700 |
| `content/05-examples.xml` | medium | One worked example: ProductService with createApp factory, three middlewares, two error classes, Pino logger | ~500 |
| `content/06-decision-tree.xml` | essential | Root question: HTTP service + Node + Express? → yes path runs scaffold, no path skips with rationale | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `collect_resources` | haiku | Template fill — list resources, auth mode. |
| `emit_scaffold_spec` | sonnet | Bounded transformation; folder tree + middleware list. |
| `review_for_security` | opus | Cross-checks error handling + secrets + middleware order. |

## Templates

| File | Purpose |
|---|---|
| `templates/create-app.ts` | Reference `createApp()` factory: helmet → cors → json → compression → requestLogger → routes → errorHandler. |
| `templates/error-classes.ts` | AppError / NotFoundError / UnauthorizedError / ValidationError with isOperational flag. |
| `templates/scaffold-spec.json` | Example output document satisfying the methodology contract. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-nodejs-patterns.py` | Validate a scaffold-spec JSON file against the output contract. | After the agent emits the spec, before downstream codegen reads it. |

## Related

- [[typescript-strict-mode]] — strict tsconfig baseline this spec assumes.
- [[typescript-patterns]] — Result + discriminated unions consumed by the error classes section.
- [[django-api]] — analogous spec for Django REST APIs in Python.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (HTTP-serving Node + Express) and, once in, branches on auth-mode (JWT vs session vs none) and on greenfield-vs-refactor — each leaf maps to a rule id from `01-core-rules.xml`. Use it before emitting the spec to confirm the methodology is applicable.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/create-app.ts`

```typescript
import express, { type Express } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { config } from './config/env';
import { requestLogger } from './middleware/requestLogger';
import { authenticate } from './middleware/auth';
import { errorHandler } from './middleware/errorHandler';
import routes from './routes';

export function createApp(): Express {
  const app = express();

  // 1. Security headers
  app.use(helmet());
  app.use(cors({ origin: config.CORS_ORIGIN }));

  // 2. Parsers
  app.use(express.json({ limit: '10kb' }));
  app.use(express.urlencoded({ extended: true, limit: '10kb' }));

  // 3. Compression
  app.use(compression());

  // 4. Logging
  app.use(requestLogger);

  // 5. Auth (optional — remove the line when auth_mode == 'none')
  app.use('/api', authenticate);

  // 6. Routes
  app.use('/api/v1', routes);

  // 7. Health probe
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', ts: new Date().toISOString() });
  });

  // 8. Error handler — MUST be last.
  app.use(errorHandler);

  return app;
}
```

### `templates/error-classes.ts`

```typescript
export class AppError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number = 500,
    public readonly code: string = 'INTERNAL_ERROR',
    public readonly isOperational: boolean = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public readonly fields: Record<string, string[]> = {},
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}
```

### `templates/scaffold-spec.json`

```json
{
  "_purpose": "Example scaffold-spec output satisfying the nodejs-patterns output contract.",
  "_consumes": "Inputs from the Prerequisites table in AGENTS.md.",
  "_produces": "scaffold-spec.json consumed by a codegen agent or reviewer.",
  "_depends-on": "content/02-output-contract.xml schema.",
  "_token-budget-impact": "~150 tokens.",
  "artefact_id": "billing-api-scaffold",
  "owner": "ruslan@faion.net",
  "service_name": "billing-api",
  "node_version": ">=20.11.0",
  "folder_tree": [
    "src/app.ts",
    "src/server.ts",
    "src/config/env.ts",
    "src/routes/index.ts",
    "src/controllers/invoices.controller.ts",
    "src/services/invoices.service.ts",
    "src/middleware/auth.ts",
    "src/middleware/errorHandler.ts",
    "src/middleware/requestLogger.ts",
    "src/utils/errors.ts",
    "src/utils/logger.ts",
    "src/utils/asyncHandler.ts"
  ],
  "middleware_order": [
    "helmet",
    "cors",
    "json",
    "urlencoded",
    "compression",
    "requestLogger",
    "auth",
    "routes",
    "errorHandler"
  ],
  "error_classes": [
    {
      "name": "AppError",
      "statusCode": 500,
      "code": "INTERNAL_ERROR",
      "isOperational": true
    },
    {
      "name": "NotFoundError",
      "statusCode": 404,
      "code": "NOT_FOUND",
      "isOperational": true
    },
    {
      "name": "UnauthorizedError",
      "statusCode": 401,
      "code": "UNAUTHORIZED",
      "isOperational": true
    },
    {
      "name": "ValidationError",
      "statusCode": 400,
      "code": "VALIDATION_ERROR",
      "isOperational": true
    }
  ],
  "logger": {
    "library": "pino",
    "request_id_header": "x-request-id"
  },
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
