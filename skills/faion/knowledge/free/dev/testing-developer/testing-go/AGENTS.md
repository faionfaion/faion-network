---
slug: testing-go
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers Go's standard `testing` package patterns: table-driven tests with `t.
content_id: "bba9dec29e6ab564"
tags: [go, testing, table-driven, benchmarks, fuzzing]
---
# Testing in Go

## Summary

**One-sentence:** Covers Go's standard `testing` package patterns: table-driven tests with `t.

**One-paragraph:** Covers Go's standard `testing` package patterns: table-driven tests with `t.Run`, interface-based mocking (manual + mockery), `httptest.Server` / `httptest.Recorder`, benchmarks with `b.N` and Go 1.24 `b.Loop()`, fuzzing with `f.Fuzz`, build tags for integration tests, and toolchain helpers (gotestsum, benchstat).

## Applies If (ALL must hold)

- Writing any Go unit or integration test
- Setting up table-driven tests with subtests for a new function
- Choosing between manual interface mocks and mockery-generated ones
- Writing HTTP handler tests with `httptest`
- Adding benchmarks or fuzz targets
- Debugging loop-variable capture bugs (pre-Go-1.22 patterns)

## Skip If (ANY kills it)

- Python tests — use testing-pytest
- JavaScript tests — use testing-javascript
- E2E browser tests — use e2e-testing

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

- parent skill: `free/dev/testing-developer/`
