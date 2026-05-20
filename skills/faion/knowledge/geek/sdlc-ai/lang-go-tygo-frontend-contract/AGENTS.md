---
slug: lang-go-tygo-frontend-contract
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: In any Go-backend / TypeScript-frontend repo, treat the Go DTO struct definitions as the single source of truth and generate the TypeScript counterpart with tygo generate from a checked-in tygo.
content_id: "2ffaf5e8a60aeaea"
tags: [go, typescript, tygo, contract, codegen]
---
# Go → TypeScript DTO Contract via tygo

## Summary

**One-sentence:** In any Go-backend / TypeScript-frontend repo, treat the Go DTO struct definitions as the single source of truth and generate the TypeScript counterpart with tygo generate from a checked-in tygo.

**One-paragraph:** In any Go-backend / TypeScript-frontend repo, treat the Go DTO struct definitions as the single source of truth and generate the TypeScript counterpart with tygo generate from a checked-in tygo.yaml. The frontend never hand-writes API types; it imports the generated .d.ts/.ts file. CI runs tygo generate and fails the build with git diff --exit-code if the committed output diverges from the regenerated output.

## Applies If (ALL must hold)

- Go backend + TypeScript frontend in the same repo or coupled repos.
- Internal RPC endpoints where OpenAPI is overkill but type safety still matters.
- Monorepos where backend struct edits should propagate to frontend types in one PR.
- Any team that has shipped a "frontend used wrong field name" production incident.

## Skip If (ANY kills it)

- OpenAPI-first projects — the spec, not Go, is the source of truth; use oapi-codegen for Go and openapi-typescript for TS instead.
- gRPC services — protobuf already gives you typed bindings on both sides.
- Polyglot backends (Go + Python + Java) where a single language can't be the source — adopt OpenAPI or protobuf.
- Throwaway prototypes — drift cost is below the tooling overhead.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
