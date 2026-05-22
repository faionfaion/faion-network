---
slug: testing-go
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces idiomatic Go test files: table-driven `t.Run` subtests, interface mocks, `httptest`, benchmarks with `b.Loop()`, fuzzing, integration build tags."
content_id: "bba9dec29e6ab564"
complexity: medium
produces: code
est_tokens: 4500
tags: [go, testing, table-driven, benchmarks, fuzzing, httptest]
---

# Testing in Go

## Summary

**One-sentence:** Produces idiomatic Go test files: table-driven `t.Run` subtests, interface mocks, `httptest`, benchmarks with `b.Loop()`, fuzzing, integration build tags.

**One-paragraph:** Covers Go's standard `testing` package patterns: table-driven tests with `t.Run`, interface-based mocking (manual + mockery), `httptest.Server` / `httptest.Recorder`, benchmarks with `b.N` and Go 1.24 `b.Loop()`, fuzzing with `f.Fuzz`, build tags for integration tests, and toolchain helpers (gotestsum, benchstat). Misapplying patterns from other ecosystems (asserting in goroutines, using `assert` instead of `require` for fatal checks) causes subtle failures.

**Ефективно для:** any new `*_test.go` file in a Go module; CI test suites that need parallel-safe subtests; HTTP handler test coverage; performance regression gates via benchstat; fuzz targets for parsers and validators.

## Applies If (ALL must hold)

- Writing any Go unit or integration test in a Go 1.22+ module
- Setting up table-driven tests with subtests for a new function
- Choosing between manual interface mocks and mockery-generated ones
- Writing HTTP handler tests with `httptest`
- Adding benchmarks or fuzz targets to existing code

## Skip If (ANY kills it)

- Python tests — use `[[testing-pytest]]`
- JavaScript/TypeScript tests — use `[[testing-javascript]]`
- Cross-browser E2E — use `[[e2e-testing]]`

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Function/handler under test | Go source file | package being tested |
| Go toolchain | `go version` >= 1.22 | developer workstation / CI image |
| testify (optional) | go.mod dep `github.com/stretchr/testify` | `go get` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[testing-patterns]]` | AAA / table-driven structure conventions |
| `[[unit-testing]]` | FIRST principles + naming |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate table-driven cases | sonnet | Pattern application; deterministic from function signature. |
| Pick mockery vs manual mock | sonnet | Rubric-based decision. |
| Diagnose flaky test trace | opus | Multi-step reasoning over logs + race detector output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/table-driven.go.tmpl` | Skeleton for a table-driven `_test.go` file with `t.Run` and `require/assert`. |
| `templates/httptest-handler.go.tmpl` | Skeleton for HTTP handler tests using `httptest.NewRecorder`. |
| `templates/benchmark.go.tmpl` | Benchmark skeleton using Go 1.24 `b.Loop()`. |
| `templates/fuzz.go.tmpl` | Fuzz test skeleton with `f.Add` seeds and `f.Fuzz` body. |
| `templates/_smoke-test.go` | Minimal compilable example combining the four templates above. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-go.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/dev/testing-developer/`
- `[[testing-pytest]]`
- `[[testing-javascript]]`
- `[[testing-patterns]]`
- `[[unit-testing]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether testing-go applies: root question — "Is the test target a pure Go function/method in this module?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
