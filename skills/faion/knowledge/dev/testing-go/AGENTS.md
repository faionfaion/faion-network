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
| `templates/_smoke-test.go` | Minimal compilable example combining the four templates above. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.go`

```go
package testing_go_test

import "testing"

// Smoke test demonstrating the four shapes.
func TestPlaceholder(t *testing.T) {
  t.Skip("placeholder template; replace with real test per 04-procedure.xml")
}
```
