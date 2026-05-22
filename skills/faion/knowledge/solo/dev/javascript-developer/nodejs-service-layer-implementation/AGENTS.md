---
slug: nodejs-service-layer-implementation
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Practical TypeScript implementation of the Controller-Service-Repository pattern for Express APIs: controllers handle HTTP only, services own business logic, repositories own all database access.
content_id: "7f82b47e6611a40e"
tags: [nodejs, typescript, express, architecture, prisma]
---
# Node.js Service Layer Implementation

## Summary

**One-sentence:** Practical TypeScript implementation of the Controller-Service-Repository pattern for Express APIs: controllers handle HTTP only, services own business logic, repositories own all database access.

**One-paragraph:** Practical TypeScript implementation of the Controller-Service-Repository pattern for Express APIs: controllers handle HTTP only, services own business logic, repositories own all database access. The core rule: hash passwords in the service layer, never in the controller or repository; Prisma stays inside repositories only.

## Applies If (ALL must hold)

- Scaffolding Controller-Service-Repository layers for a new Express/Fastify REST API
- Generating typed DTO interfaces and Zod validation schemas for a route handler
- Converting fat controller functions that mix HTTP and business logic into the 3-layer pattern
- Writing unit tests for service classes with injected repository mocks

## Skip If (ANY kills it)

- Simple one-file scripts or CLI tools without persistent state
- Lambda functions where request → DB → response fits inline with no shared business logic
- Read-only proxy services that forward requests to another API without transformation

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/javascript-developer/`
