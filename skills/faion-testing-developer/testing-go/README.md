# Go Testing

## Overview

Go has a built-in testing framework via the `testing` package requiring no external dependencies. The framework supports unit tests, table-driven tests, subtests, benchmarks, fuzzing, and examples.

**Key Principles:**
- Tests live alongside code in `*_test.go` files
- Test functions start with `Test` prefix
- Table-driven tests are idiomatic Go
- Interfaces enable easy mocking without frameworks

## Quick Reference

| Topic | Description |
|-------|-------------|
| Table-driven tests | Data-driven test pattern using slices of structs |
| Subtests (t.Run) | Nested tests for organization and selective execution |
| httptest | Standard library HTTP testing utilities |
| testify | Popular assertion and mocking library |
| go-cmp | Google's comparison library for complex types |
| testcontainers-go | Container-based integration testing |
| Benchmarks | Performance measurement with `Benchmark*` functions |
| Fuzzing | Automated input generation for vulnerability discovery |
| Coverage | Built-in code coverage with `go test -cover` |

## Project Structure

```
project/
├── pkg/
│   └── user/
│       ├── user.go
│       ├── user_test.go         # Unit tests
│       └── user_integration_test.go  # Integration tests (build tag)
├── internal/
│   └── service/
│       ├── service.go
│       ├── service_test.go
│       └── mocks/               # Mock implementations
│           └── repository.go
├── testdata/                    # Test fixtures
│   └── fixtures.json
└── go.mod
```

## Testing Libraries Ecosystem

### Standard Library

| Package | Purpose |
|---------|---------|
| `testing` | Core testing framework |
| `net/http/httptest` | HTTP handler/client testing |
| `io/ioutil.TempDir` | Temporary directories for tests |

### Third-Party Libraries

| Library | Purpose | When to Use |
|---------|---------|-------------|
| [testify](https://github.com/stretchr/testify) | Assertions, mocking, suites | Most projects - expressive assertions |
| [go-cmp](https://github.com/google/go-cmp) | Deep equality comparison | Complex struct comparisons |
| [testcontainers-go](https://golang.testcontainers.org/) | Docker containers in tests | Integration tests with real DBs |
| [mockery](https://github.com/vektra/mockery) | Mock generation | Auto-generate mocks from interfaces |
| [gofakeit](https://github.com/brianvoe/gofakeit) | Fake data generation | Test data generation |
| [gomock](https://github.com/golang/mock) | Google's mocking framework | Interface mocking |

## Key Concepts

### 1. Table-Driven Tests

The idiomatic Go pattern for testing multiple scenarios.

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid", "user@example.com", false},
        {"missing @", "invalid", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("got error %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### 2. Subtests with t.Run

Organize tests hierarchically and run selectively.

```go
func TestUserService(t *testing.T) {
    t.Run("Create", func(t *testing.T) {
        t.Run("valid input", func(t *testing.T) { /* ... */ })
        t.Run("invalid email", func(t *testing.T) { /* ... */ })
    })
    t.Run("Update", func(t *testing.T) { /* ... */ })
}
```

Run specific subtests: `go test -run TestUserService/Create/valid`

### 3. Testing with Interfaces

Design code for testability using interfaces.

```go
// Define interface for dependency
type UserRepository interface {
    Create(user User) (User, error)
    FindByID(id int) (User, error)
}

// Production implementation
type PostgresUserRepository struct { db *sql.DB }

// Test implementation (mock)
type MockUserRepository struct {
    CreateFunc func(user User) (User, error)
}

func (m *MockUserRepository) Create(user User) (User, error) {
    return m.CreateFunc(user)
}
```

### 4. HTTP Handler Testing

Use `httptest` for testing HTTP handlers.

```go
func TestGetUserHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/users/1", nil)
    w := httptest.NewRecorder()

    handler := NewUserHandler(mockService)
    handler.GetUser(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Errorf("got status %d, want %d", resp.StatusCode, http.StatusOK)
    }
}
```

### 5. Benchmarking

Measure performance with benchmark functions.

```go
func BenchmarkProcessData(b *testing.B) {
    data := generateTestData(1000)
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        ProcessData(data)
    }
}

// Go 1.24+ preferred style
func BenchmarkProcessDataLoop(b *testing.B) {
    data := generateTestData(1000)
    for b.Loop() {
        ProcessData(data)
    }
}
```

### 6. Fuzzing

Automated input generation for discovering edge cases.

```go
func FuzzParseJSON(f *testing.F) {
    f.Add([]byte(`{"name": "test"}`))
    f.Add([]byte(`{}`))

    f.Fuzz(func(t *testing.T, data []byte) {
        var result map[string]any
        _ = json.Unmarshal(data, &result)
        // Check for panics and unexpected behavior
    })
}
```

## Running Tests

```bash
# Basic commands
go test ./...                    # Run all tests
go test -v ./...                 # Verbose output
go test -run TestCreate ./...    # Run matching tests
go test -short ./...             # Skip long-running tests

# Coverage
go test -cover ./...             # Show coverage percentage
go test -coverprofile=c.out ./... && go tool cover -html=c.out

# Race detection
go test -race ./...              # Detect race conditions

# Benchmarks
go test -bench=. ./...           # Run benchmarks
go test -bench=. -benchmem ./... # Include memory stats

# Fuzzing
go test -fuzz=FuzzParse -fuzztime=30s ./...
```

## Best Practices

### Test Organization

1. **One test file per source file**: `user.go` -> `user_test.go`
2. **Group related tests with subtests**: Use `t.Run()` for organization
3. **Separate integration tests**: Use build tags `//go:build integration`
4. **Keep test data in `testdata/`**: Go ignores this directory in builds

### Test Quality

1. **Test behavior, not implementation**: Focus on inputs/outputs
2. **Use meaningful test names**: Describe scenario and expected outcome
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Prefer `t.Errorf` over `t.Fatalf`**: Continue testing unless precondition fails
5. **Use `t.Helper()` in test helpers**: Better error line reporting

### Mocking Strategy

1. **Mock at boundaries**: External APIs, databases, file systems
2. **Don't mock value types**: Use real `bytes.Buffer`, `strings.Builder`
3. **Define interfaces where used**: Not where implemented
4. **Keep interfaces small**: Single responsibility

### Performance

1. **Run parallel when safe**: `t.Parallel()` for independent tests
2. **Use `testing.Short()`**: Skip slow tests in quick iterations
3. **Reset timer in benchmarks**: `b.ResetTimer()` after setup
4. **Profile with pprof**: Identify bottlenecks

## LLM Usage Tips

When working with LLMs for Go testing:

### Effective Prompts

1. **Provide context**: Include function signature, types, and dependencies
2. **Specify test style**: "table-driven tests with subtests"
3. **Request specific patterns**: "using testify/assert" or "using go-cmp"
4. **Include edge cases**: "test empty input, nil values, and error paths"

### Code Generation Tips

```
Good prompt:
"Generate table-driven tests for this function using testify/assert.
Include edge cases for nil input, empty slice, and large input.
Use t.Run for subtests."

Less effective:
"Write tests for this function"
```

### Common LLM Mistakes to Watch

1. **Missing `t.Helper()`** in test helper functions
2. **Not capturing loop variable** in parallel tests (`tt := tt`)
3. **Using `t.Fatal` instead of `t.Error`** when test should continue
4. **Forgetting `b.ResetTimer()`** in benchmarks with setup
5. **Mocking too much**: Real implementations are simpler for value types

## External Resources

### Official Documentation
- [Go Testing Package](https://pkg.go.dev/testing)
- [Table Driven Tests](https://go.dev/wiki/TableDrivenTests)
- [Go Fuzzing](https://go.dev/doc/security/fuzz/)
- [Go 1.24 testing.B.Loop](https://go.dev/blog/testing-b-loop)

### Libraries
- [testify](https://github.com/stretchr/testify) - Assertions and mocking
- [go-cmp](https://github.com/google/go-cmp) - Comparison library
- [testcontainers-go](https://golang.testcontainers.org/) - Container testing
- [mockery](https://github.com/vektra/mockery) - Mock generation

### Tutorials
- [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests/)
- [Testing HTTP Handlers](https://www.twilio.com/en-us/blog/developers/community/how-to-test-go-http-handlers)
- [Testcontainers Getting Started](https://testcontainers.com/guides/getting-started-with-testcontainers-for-go/)

### Videos
- [Advanced Testing with Go](https://www.youtube.com/watch?v=8hQG7QlcLBk) - Mitchell Hashimoto
