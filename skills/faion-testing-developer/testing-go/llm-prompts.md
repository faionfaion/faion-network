# LLM Prompts for Go Testing

Effective prompts for AI-assisted Go test generation and review.

## Unit Test Generation

### Basic Test Generation

```
Generate table-driven tests for this Go function:

[paste function code]

Requirements:
- Use t.Run for subtests
- Include happy path, edge cases, and error conditions
- Follow AAA pattern (Arrange, Act, Assert)
- Use descriptive test case names
```

### With Specific Library

```
Write tests for this function using testify/assert:

[paste function code]

Requirements:
- Table-driven tests with t.Run
- Use assert for non-fatal checks
- Use require for preconditions
- Cover: valid input, empty input, nil values, error cases
```

### For Complex Types

```
Generate tests for this function using go-cmp for comparisons:

[paste function code and related types]

Requirements:
- Use cmp.Diff for detailed comparison output
- Handle unexported fields with cmpopts
- Include test cases for struct equality
```

## Mock Generation

### Manual Mock

```
Create a manual mock implementation for this interface:

type UserRepository interface {
    Create(user User) (User, error)
    FindByID(id int) (User, error)
    Update(user User) error
    Delete(id int) error
}

Requirements:
- Function fields for each method
- Call tracking for verification
- Default behavior when function not set
```

### testify/mock

```
Generate a testify/mock implementation for this interface:

[paste interface]

Include:
- Mock struct with mock.Mock embedding
- All interface methods using m.Called()
- Example test showing mock setup with On().Return()
```

## HTTP Handler Testing

### Handler Test

```
Write tests for this HTTP handler:

[paste handler code]

Requirements:
- Use httptest.NewRequest and httptest.NewRecorder
- Test different HTTP methods
- Test valid and invalid inputs
- Test authentication/authorization if applicable
- Check status codes and response bodies
```

### API Client Test

```
Generate tests for this HTTP client function:

[paste client code]

Requirements:
- Use httptest.NewServer to mock external API
- Test successful responses
- Test error responses (4xx, 5xx)
- Test network errors
- Test response parsing
```

### Middleware Test

```
Write tests for this middleware:

[paste middleware code]

Requirements:
- Test pass-through to next handler
- Test blocking conditions
- Test request/response modification
- Test with various header combinations
```

## Integration Testing

### Database Integration

```
Generate integration tests for this repository:

[paste repository code]

Requirements:
- Use testcontainers-go for PostgreSQL
- Setup in TestMain with container lifecycle
- Test CRUD operations
- Test error cases (not found, duplicate)
- Use transactions for test isolation
```

### Cache Integration

```
Write integration tests for this cache implementation:

[paste cache code]

Requirements:
- Use testcontainers-go for Redis
- Test Set/Get operations
- Test TTL expiration
- Test cache miss scenarios
```

## Benchmark Generation

### Basic Benchmark

```
Generate benchmarks for this function:

[paste function code]

Requirements:
- Standard b.N loop style
- Go 1.24+ b.Loop() style alternative
- Use b.ResetTimer() after setup
- Include memory allocation reporting
```

### Comparative Benchmark

```
Create comparative benchmarks for these two implementations:

[paste implementation 1]
[paste implementation 2]

Requirements:
- Sub-benchmarks for each implementation
- Test with different input sizes
- Include memory allocation stats
- Format for easy benchstat comparison
```

### Parallel Benchmark

```
Generate parallel benchmarks for this concurrent-safe function:

[paste function code]

Requirements:
- Use b.RunParallel
- Test with different CPU counts
- Measure contention impact
```

## Fuzzing

### Basic Fuzz Test

```
Generate a fuzz test for this parsing function:

[paste function code]

Requirements:
- Add meaningful seed corpus
- Check for panics
- Verify invariants
- Handle both valid and invalid inputs gracefully
```

### Complex Fuzz Test

```
Create a fuzz test for this function with multiple inputs:

[paste function code]

Requirements:
- Multiple input types in fuzz function
- Seed corpus with edge cases
- Round-trip verification if applicable
- Property-based invariant checks
```

## Test Review

### Review Existing Tests

```
Review these tests for completeness and best practices:

[paste test code]

Check:
- Missing edge cases
- Proper use of t.Helper()
- Correct use of t.Errorf vs t.Fatalf
- Table-driven test opportunities
- Parallel test safety
- Mock verification
```

### Improve Test Coverage

```
These tests have low coverage. Suggest additional test cases:

Source code:
[paste source code]

Existing tests:
[paste test code]

Coverage report shows these lines uncovered:
[paste uncovered lines]

Requirements:
- Suggest specific test cases to cover uncovered code
- Focus on meaningful scenarios, not just line coverage
```

## Specific Scenarios

### Error Handling Tests

```
Generate tests focusing on error handling for:

[paste function code]

Requirements:
- Test all error return paths
- Use errors.Is for error type checking
- Test wrapped errors
- Verify error messages contain useful info
```

### Concurrent Code Testing

```
Write tests for this concurrent function:

[paste function code]

Requirements:
- Test with -race flag considerations
- Test concurrent access patterns
- Use sync.WaitGroup for coordination
- Test edge cases: empty input, single item, many items
```

### Time-Dependent Tests

```
Generate tests for this function that uses time:

[paste function code]

Requirements:
- Use interface for time dependency injection
- Create mock time provider
- Test timeout scenarios
- Test time-based conditions
```

## Test Refactoring

### Convert to Table-Driven

```
Refactor these repetitive tests to table-driven style:

[paste repetitive tests]

Requirements:
- Extract common test structure to struct
- Use t.Run for each case
- Preserve test coverage
- Improve readability
```

### Extract Test Helpers

```
Identify opportunities to extract test helpers from:

[paste test file]

Requirements:
- Common setup/teardown patterns
- Repeated assertions
- Mock creation patterns
- Use t.Helper() for correct line reporting
```

## Documentation Generation

### Generate Test Documentation

```
Generate documentation comments for these tests:

[paste test code]

Requirements:
- Describe what each test verifies
- Document test setup requirements
- Note any special configurations needed
```

## Prompt Templates Summary

| Task | Key Elements to Include |
|------|------------------------|
| Unit test | Function code, expected patterns, edge cases |
| Mock | Interface definition, verification needs |
| HTTP test | Handler/client code, expected responses |
| Integration | Repository/service code, database type |
| Benchmark | Function code, input sizes, comparison needs |
| Fuzz | Parser/validator code, input format |
| Review | Test code, source code, coverage data |

## Best Practices for Prompts

1. **Include full context**: Function code, types, interfaces
2. **Specify library preferences**: testify, go-cmp, standard library
3. **Define coverage expectations**: happy path, errors, edge cases
4. **Request specific patterns**: table-driven, parallel, AAA
5. **Mention constraints**: Go version, build tags, performance

## Common LLM Mistakes to Watch

1. **Missing `t.Helper()`** in helper functions
2. **Not capturing loop variable** (`tt := tt`) in parallel tests
3. **Using wrong assertion library** (mixing testify/assert and require)
4. **Forgetting `defer server.Close()`** in httptest
5. **Missing `b.ResetTimer()`** in benchmarks with setup
6. **Not checking `err` before using result**
7. **Hardcoding ports** in testcontainers (use dynamic mapping)
8. **Missing build tags** for integration tests
