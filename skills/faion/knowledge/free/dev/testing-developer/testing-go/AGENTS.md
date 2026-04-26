# Testing in Go

Go testing idioms: table-driven tests, subtests, interface mocking, httptest, benchmarks, fuzzing, and parallel execution.

## Summary

Covers Go's standard `testing` package patterns: table-driven tests with `t.Run`, interface-based mocking (manual + mockery), `httptest.Server` / `httptest.Recorder`, benchmarks with `b.N` and Go 1.24 `b.Loop()`, fuzzing with `f.Fuzz`, build tags for integration tests, and toolchain helpers (gotestsum, benchstat).

## Why

Go's test idioms differ from other languages: no test classes, subtests via closures, mocking by interface substitution (not monkey-patching), and benchmarks as first-class citizens. Misapplying patterns from other ecosystems (e.g., asserting inside goroutines, using `assert` instead of `require` for fatal checks) causes subtle failures. This methodology enforces idiomatic Go test style.

## When To Use

- Writing any Go unit or integration test
- Setting up table-driven tests with subtests for a new function
- Choosing between manual interface mocks and mockery-generated ones
- Writing HTTP handler tests with `httptest`
- Adding benchmarks or fuzz targets
- Debugging loop-variable capture bugs (pre-Go-1.22 patterns)

## When NOT To Use

- Python tests → use `testing-pytest`
- JavaScript tests → use `testing-javascript`
- E2E browser tests → use `e2e-testing`

## Content

| File | What it covers |
|------|---------------|
| `content/01-table-driven.xml` | Table-driven pattern, subtest naming, `t.Parallel()`, loop-variable capture fix, `t.Helper()` |
| `content/02-mocking-http.xml` | Interface-based mocking (manual vs mockery), httptest.Server, httptest.Recorder, gomock decision rubric |
| `content/03-benchmarks-fuzz.xml` | Benchmark structure, b.N vs b.Loop() (Go 1.24), benchstat workflow, fuzzing with f.Fuzz, build tags for integration tests |
