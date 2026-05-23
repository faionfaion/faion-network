# Node.js Service Layer

## Summary

**One-sentence:** Layer a Node.js TypeScript service into controller / service / repository with HTTP types confined to controller and persistence to repository.

**One-paragraph:** Controller-Service-Repository pattern for Node.js TypeScript services: controllers decode requests + encode responses; services hold business logic and orchestration; repositories own ORM/SQL. Controller never imports Prisma/Drizzle/Knex; service never imports Express/Fastify. Dependency injection via constructor + interfaces declared at the consumer side. Output is the layered package set + dependency graph + tests at each layer.

**Ефективно для:**

- Replacing fat-controller Node.js services with reviewable layers.
- Greenfield TypeScript backends adopting layered architecture.
- Onboarding engineers to consistent per-feature layout.
- Adding interface seams to enable unit testing service logic.

## Applies If (ALL must hold)

- Node.js >=20 + TypeScript project.
- Service has multi-step business logic (>=2 operations per feature).
- Persistence (Prisma, Drizzle, Knex, raw pg) exists.
- Tests target service logic directly, not only via HTTP integration.

## Skip If (ANY kills it)

- Thin CRUD service where layering adds overhead without payoff.
- Project follows a different architecture (CQRS, NestJS module conventions).
- Serverless functions where each function is the layer.
- Single-file experiment where one module holds everything intentionally.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature inventory: which aggregates need controller/service/repo | table | tech-lead |
| ORM choice (Prisma / Drizzle / Knex / pg) | ADR | tech-lead |
| HTTP framework (Express / Fastify / Hono / Koa) | config | platform |
| Test stack (vitest, jest, supertest) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[monorepo-turborepo]] | Layered packages may live in workspaces. |
| [[logging-patterns]] | Each layer emits structured logs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (controller decodes/encodes, service has business logic, repo owns ORM, no HTTP in service, no ORM in controller) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for layered module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold → interfaces → repo → service → controller | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interface_design` | opus | Interface seams between layers. |
| `controller_authoring` | sonnet | Decode + call service + encode. |
| `repo_authoring` | sonnet | ORM/SQL + domain-type mapping. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-controller.ts` | Controller with decode + service call + encode |
| `templates/user-service.ts` | Service with business logic + interfaces |
| `templates/user-repository.ts` | Repository with ORM + domain-type mapping |
| `templates/errors.ts` | Domain error classes shared across layers |
| `templates/layer-check.sh` | Static check: no Prisma in controller, no Express in service |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nodejs-service-layer.py` | Validate layered module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-standard-layout]]
- [[monorepo-turborepo]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps service complexity, persistence presence, and existing architecture to a rule from `01-core-rules.xml`, telling the agent whether to layer or skip for thin/CQRS cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
