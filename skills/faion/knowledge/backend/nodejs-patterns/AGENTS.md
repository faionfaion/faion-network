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
