---
slug: nodejs-service-layer-architecture
tier: solo
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Architectural scaffold for layered Node.
content_id: "453b2b59c5408bb4"
tags: [nodejs, express, architecture, dependency-injection, error-handling]
---
# Node.js Service Layer Architecture

## Summary

**One-sentence:** Architectural scaffold for layered Node.

**One-paragraph:** Architectural scaffold for layered Node.js REST APIs: folder structure, error taxonomy, DI wiring, and layer boundary rules. The core rule: process.env access only in config/index.ts, never scattered across the codebase; error handler middleware must be registered last in app.ts after all routes.

## Applies If (ALL must hold)

- Designing the folder structure and layer boundaries for a new Node.js REST API before writing code
- Establishing dependency injection patterns and container wiring strategy for a team codebase
- Auditing an existing Express app for layer violations (business logic in controllers, Prisma in services)
- Defining error taxonomy and error handler middleware as a shared foundation before feature work

## Skip If (ANY kills it)

- Prototypes and throwaway scripts where architectural purity adds no return
- Serverless functions (Lambda/Edge) where a cold-start DI container is overhead
- GraphQL APIs with resolver-based patterns where resolvers replace controllers

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
