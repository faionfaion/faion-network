# Unit Testing Checklist

Pre-commit checklist for unit tests. Use before merging any code.

## Test Quality Checklist

### Structure

- [ ] Each test has clear Arrange-Act-Assert sections
- [ ] Test names follow naming convention (method_scenario_expected)
- [ ] One assertion concept per test
- [ ] No test interdependencies

### Coverage

- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases covered (null, empty, boundary values)
- [ ] All public methods have tests

### Isolation

- [ ] No external dependencies (DB, API, filesystem)
- [ ] No shared mutable state
- [ ] Tests can run in any order
- [ ] Tests can run in parallel

### Assertions

- [ ] Assertions verify behavior, not implementation
- [ ] Error messages are descriptive
- [ ] No empty assertions (`assert True`)
- [ ] Expected values are explicit, not computed

### Performance

- [ ] Each test runs in < 100ms
- [ ] No unnecessary setup/teardown
- [ ] Efficient fixtures (reuse where safe)

## Pre-Commit Checks

```bash
# Python (pytest)
pytest --cov=src --cov-fail-under=80 -x

# JavaScript (Jest)
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# Go
go test -cover -race ./...
```

## LLM-Generated Test Review

When reviewing AI-generated tests:

- [ ] All tests actually run (no syntax errors)
- [ ] Assertions are meaningful (not trivial)
- [ ] Edge cases are realistic
- [ ] Mocking is appropriate (not over-mocked)
- [ ] Test names match behavior tested
- [ ] No hallucinated methods or classes
- [ ] Matches codebase style conventions

## Code Review Checklist

For reviewers examining test code:

### Completeness

- [ ] Tests cover new functionality
- [ ] Tests cover bug fix scenario
- [ ] Negative test cases included
- [ ] Boundary conditions tested

### Maintainability

- [ ] DRY violations minimized (but not at cost of clarity)
- [ ] Fixtures are reusable
- [ ] Test data is representative
- [ ] Comments explain non-obvious setup

### Robustness

- [ ] No flaky tests (time, randomness, order)
- [ ] Deterministic assertions
- [ ] Proper cleanup in teardown
- [ ] Timeout handling for async

## Quick Reference

### Minimum Coverage Targets

| Project Type | Line Coverage | Branch Coverage |
|--------------|---------------|-----------------|
| Library | 90% | 80% |
| API Service | 80% | 70% |
| CLI Tool | 75% | 65% |
| Internal Tool | 70% | 60% |

### Test-to-Code Ratio

| Complexity | Ratio |
|------------|-------|
| Simple CRUD | 1:1 |
| Business Logic | 2:1 |
| Financial/Critical | 3:1+ |

## Common Issues

| Issue | Fix |
|-------|-----|
| Flaky test | Mock time/randomness |
| Slow test | Replace I/O with fakes |
| Brittle test | Test behavior not implementation |
| Missing assertion | Add explicit verify |
| Shared state | Reset in setup/teardown |
