# Go Testing Checklist

## Pre-Test Setup

- [ ] Create `*_test.go` file alongside source file
- [ ] Import `testing` package
- [ ] Set up test fixtures in `testdata/` directory if needed
- [ ] Define interfaces for external dependencies
- [ ] Create mock implementations for dependencies

## Unit Test Checklist

### Test Structure

- [ ] Function name starts with `Test` prefix
- [ ] Function accepts `*testing.T` parameter
- [ ] Test follows AAA pattern (Arrange, Act, Assert)
- [ ] Test name describes scenario and expected outcome

### Table-Driven Tests

- [ ] Define test cases as slice of structs
- [ ] Include `name` field for test identification
- [ ] Include input fields and expected output fields
- [ ] Use `t.Run(tt.name, func(t *testing.T) {...})` for subtests
- [ ] Cover happy path, edge cases, and error conditions

### Test Cases Coverage

- [ ] Valid input (happy path)
- [ ] Empty input (empty string, nil, zero values)
- [ ] Invalid input (malformed data)
- [ ] Boundary values (min, max, edge cases)
- [ ] Error conditions (expected errors)
- [ ] Concurrent access (if applicable)

## Assertion Checklist

### Standard Library

- [ ] Use `t.Errorf` for non-fatal failures (test continues)
- [ ] Use `t.Fatalf` only for precondition failures (test stops)
- [ ] Use `t.Helper()` in helper functions for correct line reporting
- [ ] Include expected vs got in error messages

### With testify/assert

- [ ] Import `github.com/stretchr/testify/assert`
- [ ] Use `assert.Equal(t, expected, actual)` for equality
- [ ] Use `assert.NoError(t, err)` for error checks
- [ ] Use `assert.Error(t, err)` when error is expected
- [ ] Use `require.*` when test cannot continue on failure

### With go-cmp

- [ ] Import `github.com/google/go-cmp/cmp`
- [ ] Use `cmp.Diff(want, got)` for detailed diff output
- [ ] Use `cmpopts.IgnoreUnexported()` for unexported fields
- [ ] Use `cmpopts.SortSlices()` for unordered comparisons
- [ ] Use `cmpopts.EquateApprox()` for floating point

## HTTP Handler Testing

### Setup

- [ ] Import `net/http/httptest`
- [ ] Create request with `httptest.NewRequest(method, path, body)`
- [ ] Create recorder with `httptest.NewRecorder()`
- [ ] Inject mock dependencies into handler

### Verification

- [ ] Check response status code
- [ ] Check response headers
- [ ] Parse and verify response body
- [ ] Verify mock method calls (if applicable)

### Test Server (for client testing)

- [ ] Create server with `httptest.NewServer(handler)`
- [ ] Use `server.URL` for client requests
- [ ] Defer `server.Close()`

## Mocking Checklist

### Interface Design

- [ ] Define interface in consuming package
- [ ] Keep interface small (1-3 methods)
- [ ] Use dependency injection for testability

### Manual Mocks

- [ ] Create mock struct with function fields
- [ ] Implement interface methods calling function fields
- [ ] Set up function fields in test setup

### With testify/mock

- [ ] Define mock type embedding `mock.Mock`
- [ ] Implement interface methods with `m.Called(...)`
- [ ] Use `m.On("Method", args).Return(...)` for expectations
- [ ] Use `m.AssertExpectations(t)` to verify calls

### With mockery (code generation)

- [ ] Add `//go:generate mockery --name=InterfaceName`
- [ ] Run `go generate ./...`
- [ ] Import generated mock from `mocks/` package

## Integration Test Checklist

### Build Tags

- [ ] Add `//go:build integration` at file top
- [ ] Create separate `*_integration_test.go` files
- [ ] Run with `go test -tags=integration ./...`

### With testcontainers-go

- [ ] Import `github.com/testcontainers/testcontainers-go`
- [ ] Create container in `TestMain` or test setup
- [ ] Use `container.Terminate(ctx)` in cleanup
- [ ] Get dynamic port with `container.MappedPort(ctx, port)`
- [ ] Do NOT hardcode ports (use dynamic mapping)

### Database Testing

- [ ] Start with clean database state
- [ ] Use transactions with rollback for isolation
- [ ] Clean up test data after tests
- [ ] Consider using test fixtures

## Benchmark Checklist

### Setup

- [ ] Function name starts with `Benchmark` prefix
- [ ] Function accepts `*testing.B` parameter
- [ ] Run setup code before timer starts
- [ ] Call `b.ResetTimer()` after setup (pre-Go 1.24)
- [ ] Use `b.Loop()` for Go 1.24+ benchmarks

### Execution

- [ ] Use `for i := 0; i < b.N; i++` loop (pre-Go 1.24)
- [ ] Or use `for b.Loop()` (Go 1.24+)
- [ ] Avoid compiler optimization of results
- [ ] Run with `-benchmem` for memory stats

### Parallel Benchmarks

- [ ] Use `b.RunParallel(func(pb *testing.PB) {...})`
- [ ] Use `for pb.Next()` inside parallel function
- [ ] Run with `-cpu` flag to vary GOMAXPROCS

## Fuzzing Checklist

### Setup

- [ ] Function name starts with `Fuzz` prefix
- [ ] Function accepts `*testing.F` parameter
- [ ] Add seed corpus with `f.Add(...)`
- [ ] Include valid and edge case seeds

### Implementation

- [ ] Use `f.Fuzz(func(t *testing.T, args...) {...})`
- [ ] Check for panics (implicit)
- [ ] Verify invariants in fuzz function
- [ ] Don't check for specific outputs

### Execution

- [ ] Run with `go test -fuzz=FuzzName`
- [ ] Set time limit with `-fuzztime=30s`
- [ ] Check `testdata/fuzz/` for failing inputs
- [ ] Add failing inputs to regression tests

## Coverage Checklist

### Measurement

- [ ] Run `go test -cover ./...` for summary
- [ ] Run `go test -coverprofile=coverage.out ./...` for detailed
- [ ] Generate HTML report with `go tool cover -html=coverage.out`

### Analysis

- [ ] Check coverage percentage (aim for 70-80%+)
- [ ] Review uncovered lines in HTML report
- [ ] Add tests for critical uncovered paths
- [ ] Don't chase 100% (focus on quality)

## Test Quality Checklist

### Code Quality

- [ ] Tests are deterministic (no random failures)
- [ ] Tests are independent (no shared state)
- [ ] Tests are fast (< 1s for unit tests)
- [ ] Tests are readable (clear intent)

### Error Messages

- [ ] Include expected value in error message
- [ ] Include actual value in error message
- [ ] Include context (input that caused failure)
- [ ] Use diff output for complex comparisons

### Maintenance

- [ ] Tests document expected behavior
- [ ] Tests break when behavior changes
- [ ] Tests don't break on refactoring
- [ ] Tests are colocated with source code

## CI/CD Integration

### Configuration

- [ ] Run tests in CI pipeline
- [ ] Enable race detector (`-race`)
- [ ] Set coverage threshold
- [ ] Run integration tests separately

### Performance

- [ ] Cache Go modules
- [ ] Use test parallelization
- [ ] Skip slow tests in PR builds (`-short`)
- [ ] Run full suite on merge

## Quick Commands Reference

```bash
# Unit tests
go test ./...
go test -v ./...
go test -run TestName ./...
go test -short ./...

# Coverage
go test -cover ./...
go test -coverprofile=c.out ./... && go tool cover -html=c.out

# Race detection
go test -race ./...

# Benchmarks
go test -bench=. ./...
go test -bench=. -benchmem ./...
go test -bench=BenchmarkName -count=5 ./...

# Fuzzing
go test -fuzz=FuzzName -fuzztime=30s ./...

# Integration tests
go test -tags=integration ./...

# All quality checks
go test -v -race -cover ./...
```
