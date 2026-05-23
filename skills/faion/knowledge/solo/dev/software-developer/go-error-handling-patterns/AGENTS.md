---
slug: go-error-handling-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Define sentinel errors in one apperror package, wrap with fmt.Errorf %w, classify with errors.Is/As, and never panic for control flow.
content_id: "62abd60a22cf38be"
complexity: medium
produces: code
est_tokens: 3800
tags: [go, error-handling, best-practices, testing]
---
# Go Error Handling Patterns

## Summary

**One-sentence:** Define sentinel errors in one apperror package, wrap with fmt.Errorf %w, classify with errors.Is/As, and never panic for control flow.

**One-paragraph:** Go services define sentinel errors in one apperror package (ErrNotFound, ErrConflict, ErrUnauthorized); call sites wrap with fmt.Errorf("context: %w", err) to preserve the chain; switching on error class uses errors.Is/As, never type assertion. Panics are reserved for unrecoverable programmer error (invariant violation), never for control flow. The HTTP/gRPC edge translates errors.Is(err, apperror.ErrNotFound) to status codes in one place.

**Ефективно для:**

- Go services with multi-layer call chains (handler → service → repo).
- API edge that must translate domain errors to HTTP/gRPC status codes.
- Refactoring inconsistent error handling across packages.
- Onboarding engineers to a uniform error convention.

## Applies If (ALL must hold)

- Go 1.21+ project (errors.Is/As mature in standard library).
- Service has >=3 layers (handler / service / repository / external clients).
- Multiple error classes exist (not-found, conflict, validation, auth, system).
- Edge translates errors to status codes or RPC errors.

## Skip If (ANY kills it)

- Tiny CLI with one layer — `errors.New` everywhere is fine.
- Project uses an alternate convention (pkg/errors stack traces, github.com/cockroachdb/errors) — adapt the rule set.
- External-only library code that must not impose a specific convention on callers.
- Generated code (protobuf service stubs) that has its own error model.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Error class inventory: domain errors that the API surfaces | list | tech-lead |
| apperror package location (single canonical path) | path | tech-lead |
| Edge translator implementation (HTTP middleware or gRPC interceptor) | code | platform |
| golangci-lint with `errorlint` + `wrapcheck` enabled | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-project-structure]] | apperror package placement follows the layout. |
| [[logging-patterns]] | Error logs carry the wrapped chain context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (sentinels in apperror, wrap with %w, errors.Is/As at boundary, no panic for control flow, edge translates once) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for error module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory → declare sentinels → wrap at boundaries → translate at edge → lint enforce | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sentinel_declaration` | sonnet | Mechanical: declare ErrXxx vars in apperror. |
| `wrap_chain_review` | sonnet | Walk call sites; ensure %w wrapping at layer boundaries. |
| `edge_translator` | sonnet | Single middleware/interceptor that maps to status codes. |
| `lint_config` | sonnet | Enable errorlint + wrapcheck in golangci.yml. |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | Sentinel error declarations + helper constructors |
| `templates/golangci.yml` | golangci-lint config with errorlint + wrapcheck |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling-patterns.py` | Validate error module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-project-structure]]
- [[logging-patterns]]
- [[go-concurrency-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps language version, layering depth, and edge-translator presence to a rule from `01-core-rules.xml`, telling the agent whether to enforce the convention or skip when the project already follows an incompatible model. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
