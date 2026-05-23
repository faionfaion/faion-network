---
slug: go-standard-layout
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Layer a Go service into handler / service / repository packages with HTTP types confined to handler and ORM types confined to repository.
content_id: "c5198cd547e903b3"
complexity: medium
produces: code
est_tokens: 3800
tags: [go, architecture, layering, best-practices, package-design]
---
# Go Standard Layout

## Summary

**One-sentence:** Layer a Go service into handler / service / repository packages with HTTP types confined to handler and ORM types confined to repository.

**One-paragraph:** Within internal/, a Go service follows handler → service → repository layering. Handler decodes HTTP/gRPC, calls service with primitive args, encodes response; service holds business logic and orchestration; repository owns SQL/ORM and returns domain types. HTTP types live only in handler; DB types only in repository; services pass plain domain structs both ways. Output is the layered package set + interfaces at consumer sites + tests at each layer.

**Ефективно для:**

- Backend services in Go with non-trivial business logic per feature.
- Replacing single-file handlers with reviewable layered packages.
- Adding interface seams to enable unit testing service logic.
- Onboarding engineers to consistent per-feature layout.

## Applies If (ALL must hold)

- Go module follows go-project-structure (cmd/ + internal/).
- Service has multi-step business logic (>=2 operations per feature).
- Persistence exists (SQL or NoSQL through a repository).
- Tests target service logic directly, not only via HTTP integration.

## Skip If (ANY kills it)

- Service is a thin CRUD wrapper where layering adds overhead without payoff.
- Project follows a different architecture (CQRS, hexagonal with ports/adapters).
- Generated CRUD scaffolds where the layering decisions are made by the generator.
- Tiny experiment where one file holds everything intentionally.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature inventory: which aggregates need handler/service/repo | table | tech-lead |
| Persistence choice (sqlx / sqlc / GORM / ent) | ADR | tech-lead |
| HTTP framework choice (net/http, chi, gin, echo) | config | platform |
| Test stack (testify, mockery, dockertest) selected | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-project-structure]] | Layered packages live under internal/. |
| [[go-error-handling-patterns]] | Error chain flows from repository → service → handler. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (handler decodes/encodes only, service has business logic, repo owns SQL, no HTTP types in service, interfaces at consumer) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for layered package spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scaffold dirs → write interfaces → implement repo → implement service → wire handler | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interface_design` | opus | Interface seams between layers need careful design. |
| `handler_authoring` | sonnet | Mechanical: decode + call service + encode. |
| `repo_authoring` | sonnet | SQL/ORM CRUD + domain-type mapping. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler.go` | HTTP handler: decode request, call service, encode response |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-standard-layout.py` | Validate layered package spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-project-structure]]
- [[go-error-handling-patterns]]
- [[go-concurrency-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps service complexity, persistence presence, and architecture choice to a rule from `01-core-rules.xml`, telling the agent whether to layer or skip when the pattern doesn't fit. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
