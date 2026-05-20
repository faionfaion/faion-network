---
slug: go-error-handling-patterns
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Wrap errors once per layer with fmt.
content_id: "62abd60a22cf38be"
tags: [go, errors, patterns, wrapping, sentinels]
---
# Go Error Handling Patterns

## Summary

**One-sentence:** Wrap errors once per layer with fmt.

**One-paragraph:** Wrap errors once per layer with fmt.Errorf("verb context: %w", err) to preserve the errors.Is/errors.As chain. Translate storage-layer sentinels (sql.ErrNoRows) into domain sentinels (ErrNotFound) at the repository boundary. Define one apperror package with sentinel vars and a typed AppError struct; never scatter errors.New("not found") per call site. Log errors at exactly one place per request — the outermost handler.

## Applies If (ALL must hold)

- New Go service or package where error contracts must be stable for callers.
- Refactoring a codebase using errors.New(fmt.Sprintf(...)) instead of fmt.Errorf("...: %w", err).
- Wiring errors.Is/errors.As checks at HTTP/gRPC boundaries to map domain errors to status codes.
- Adding retry-with-backoff and panic-recovery middleware for production handlers.
- Aggregating validation errors via errors.Join (Go 1.20+) or a MultiError type.

## Skip If (ANY kills it)

- Quick scripts or main packages where log.Fatalf on first error is acceptable.
- Test helpers — t.Fatal(err) is preferred over wrapping.
- Code that interacts only with the standard library and never returns an error to a caller.
- Legacy packages with stable public sentinel errors — changing them is a breaking change.

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

- parent skill: `pro/dev/backend-systems/`
