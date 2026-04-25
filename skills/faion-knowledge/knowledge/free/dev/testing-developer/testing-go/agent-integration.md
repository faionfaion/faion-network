# Agent Integration — Go Testing

## When to use
- Generating table-driven tests for any Go function with branching, error paths, or input variations.
- HTTP handler tests using `httptest.NewServer` / `httptest.NewRecorder`.
- Concurrency-heavy code: enable `-race` always; tests are the primary tool catching data races.
- Performance-sensitive code: write `BenchmarkXxx` functions; track regressions with `benchstat`.
- Security-sensitive parsers/decoders: add `FuzzXxx` functions; Go fuzzing is built-in since 1.18.
- Integration tests with real Postgres / Redis / Kafka via `testcontainers-go`.

## When NOT to use
- Pure CGo wrappers (`os/exec`, hardware) where the OS layer is the contract — skip unit tests, ship integration only.
- Code that's just a thin wrapper around `database/sql` execution — test at integration layer with real DB.
- Generated code (protoc, sqlc) — test consumers, not generated artifacts.
- Internal helpers ≤3 lines — coverage noise.
- Mocking standard library types (`*sql.DB`, `*http.Client`) directly — use the round-tripper / httptest substitution patterns instead.

## Where it fails / limitations
- README emphasizes table-driven tests but doesn't address subtest naming with special chars — agents emit names with spaces and slashes that break `go test -run`.
- `t.Parallel()` placement inside `t.Run` closures with shared `tt` loop var is a classic data-race trap; the README's example may not show the variable-shadow fix needed pre-Go-1.22.
- testify's `assert` vs `require` distinction underplayed — agents use `assert.Equal` for setup checks and tests continue running after fatal errors.
- gomock vs testify/mock vs hand-rolled fakes — README lists all three but no decision rubric; agents pick gomock for trivial interfaces.
- Fuzzing section likely has corpus seeds but no guidance on `-fuzztime` budgets in CI; agents wire fuzzing into PR pipelines and timeouts blow up.
- Build tags for integration tests (`//go:build integration`) often missing in examples; agents run `go test ./...` and integration tests fire in unit pipeline.
- `t.Cleanup` is the modern replacement for `defer` chains in fixtures — agents still write deeply nested defers.

## Agentic workflow
Default to table-driven + subtests with `t.Parallel()`. For each function: (1) read signature; identify error returns and branch points; (2) emit a `tests := []struct{...}{...}` slice covering happy + each error branch + boundary; (3) `t.Run(tt.name, func(t *testing.T) { t.Parallel(); ... })`; (4) use `require.NoError` for setup and `assert.Equal` for results; (5) `go test ./... -race -count=1 -shuffle=on`. For HTTP, use `httptest.NewServer` with the real `http.Handler`. Generate mocks with `mockery` or `go:generate mockgen` only for interfaces with > 1 method that have multiple real implementations.

### Recommended subagents
- `faion-test-agent` (custom) — emit Go test files restricted to `*_test.go`.
- `faion-go-agent` — refactor to interfaces at consumer side for testability.
- Reviewer subagent — scan diffs for race-prone `t.Parallel()` + closure-loop-var patterns and missing `t.Cleanup`.
- `faion-sdd-executor-agent` — TDD loop with `go test -run ^TestX$` between phases.

### Prompt pattern
```
Function: pkg/billing/calculate.go:CalculateTotal.
Read it; list every error path and branch. Emit pkg/billing/calculate_test.go:
- One TestCalculateTotal_TableDriven function.
- tt struct with name, in, want, wantErr.
- Cases: happy path, each error path, boundary (zero, negative, max int).
- Use t.Run + t.Parallel.
- Use github.com/stretchr/testify/require for setup, /assert for results.
- Use go-cmp's cmp.Diff for struct comparisons.
Run: go test ./pkg/billing -race -count=1 -v
```

```
Add a fuzz test for Parse(input string) (Foo, error).
File: pkg/foo/foo_fuzz_test.go.
- Seed corpus with 5 known-good and 3 known-malformed inputs.
- Invariant: Parse must not panic and must not return nil Foo with nil error.
Run: go test ./pkg/foo -run=^$ -fuzz=FuzzParse -fuzztime=30s
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test` | Built-in test runner | https://pkg.go.dev/testing |
| `go test -race` | Data-race detector | https://go.dev/doc/articles/race_detector |
| `go test -fuzz` | Built-in fuzzing | https://go.dev/security/fuzz/ |
| `go test -cover` / `-coverprofile` | Coverage; pair with `go tool cover -html` | https://go.dev/blog/cover |
| `gotestsum` | Pretty + JUnit XML output for CI | https://github.com/gotestyourself/gotestsum |
| `go test -shuffle=on` | Randomize test order | https://go.dev/doc/go1.17 |
| `mockery` | Generate testify-style mocks from interfaces | https://github.com/vektra/mockery |
| `mockgen` (uber-go/mock) | Generate gomock mocks | https://github.com/uber-go/mock |
| `testify` | Assertions, mocking, suites | https://github.com/stretchr/testify |
| `go-cmp` | Deep struct comparison with diff | https://github.com/google/go-cmp |
| `testcontainers-go` | Docker containers for integration | https://golang.testcontainers.org |
| `benchstat` | Compare benchmark results across runs | https://pkg.go.dev/golang.org/x/perf/cmd/benchstat |
| `gofakeit` | Fake data generator | https://github.com/brianvoe/gofakeit |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes | Use `actions/setup-go` + cache `~/go/pkg/mod` |
| GitLab CI | CI | Yes | `golang:` image; cache `GOPATH` |
| Codecov / Coveralls | SaaS | Yes — coverage upload | Combine `coverprofile` from multiple `go test` runs |
| Drone CI | OSS | Yes | Native Go support |
| Buildkite | CI | Yes — agent self-hosted | `gotestsum --junitfile` for test analytics |
| WireMock / Mockoon | OSS | Yes | When you need a stand-alone HTTP mock vs `httptest.NewServer` |

## Templates & scripts
See `templates.md` for table-driven, httptest, and testcontainers templates. Inline race-safe parallel subtest pattern (Go < 1.22):

```go
//go:build !go1.22
// +build !go1.22

func TestCalculate(t *testing.T) {
    tests := []struct {
        name string
        in   int
        want int
    }{
        {"zero", 0, 0},
        {"positive", 5, 25},
        {"negative", -3, 9},
    }
    for _, tt := range tests {
        tt := tt // capture loop variable; Go 1.22+ can drop this line
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got := Square(tt.in)
            if got != tt.want {
                t.Errorf("Square(%d) = %d, want %d", tt.in, got, tt.want)
            }
        })
    }
}
```

## Best practices
- Default `go test` invocation: `-race -count=1 -shuffle=on`. Three flags catch most regressions.
- Use `t.Cleanup(fn)` instead of `defer` for setup teardown — runs even if subtests skip.
- Keep `*_test.go` files in the same package for white-box tests; use `package foo_test` for black-box (consumer view) tests.
- Prefer `httptest.NewServer` over mocking `http.Client`; lets you exercise real handler code.
- Use `go-cmp` for struct comparisons — produces a diff; `reflect.DeepEqual` only returns bool.
- For fuzzing in CI, use short `-fuzztime=30s` per package; long fuzzing in nightly job.
- Tag integration tests with `//go:build integration` and run separately: `go test -tags=integration ./...`.
- Use `t.TempDir()` for filesystem fixtures — auto-cleaned.
- Benchmarks: always run with `-benchmem` and use `b.ReportAllocs()` to track allocation regressions.
- For interfaces, define them at the consumer side (Go idiom). Mocks live next to consumers, not next to implementations.

## AI-agent gotchas
- **Loop variable capture**: pre-Go-1.22 `for _, tt := range tests` requires `tt := tt` inside the loop before `t.Parallel()`, or all subtests see the last value.
- **`assert.Equal` doesn't stop the test**; subsequent code still runs and may panic. Use `require.Equal` or `require.NoError` for setup-critical asserts.
- **Race detector requires CGO** — `CGO_ENABLED=0` silently disables it. Agents bake `CGO_ENABLED=0` into Dockerfiles and lose race coverage.
- **Subtest names with `/` or spaces** become path-like in `-run` filters (`TestFoo/bar%20baz`); agents struggle to re-run.
- **Fuzz corpus directory**: `go test -fuzz` writes new failing seeds to `testdata/fuzz/<FuncName>/`; agents `git ignore` it and lose regression seeds.
- **`-count=1`** disables the test-result cache. Agents debug "why did my fix not take effect" when running without it.
- **`httptest.NewServer` doesn't close itself**; missing `defer ts.Close()` leaks goroutines and files in long test runs.
- **`*testing.T` is not safe for concurrent use** outside `t.Parallel`-managed scopes; agents call `t.Errorf` from inside spawned goroutines incorrectly.
- **Mocking the wrong layer**: agents mock `database/sql` interfaces directly; instead define a repository interface at the consumer and mock that.
- **Build tags typo**: `//go:build integration` vs the older `// +build integration` — both required for compatibility through Go 1.16; agents drop one and tags don't apply.
- **Goroutine leaks**: `goleak.VerifyNone(t)` (uber-go/goleak) catches leaked goroutines per test; agents skip this and CI flakes intermittently.
- **Time-based tests**: `time.Now()` in production code → inject a `Clock` interface or `clockwork`; do not use `time.Sleep` to "wait for" something.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../integration-testing/`, `../mocking-strategies/`, `../tdd-workflow/`
- Go testing package: https://pkg.go.dev/testing
- Race detector: https://go.dev/doc/articles/race_detector
- Fuzzing: https://go.dev/security/fuzz/
- testify: https://github.com/stretchr/testify
- go-cmp: https://github.com/google/go-cmp
- testcontainers-go: https://golang.testcontainers.org/
- Dave Cheney "Prefer table-driven tests": https://dave.cheney.net/2019/05/07/prefer-table-driven-tests
