# Unit Testing Guide

Unit testing verifies individual components in isolation. This guide covers principles, patterns, and LLM-assisted test generation for maintainable, reliable tests.

## FIRST Principles

What makes a good unit test:

| Principle | Description | Example |
|-----------|-------------|---------|
| **F**ast | Milliseconds to run, no I/O | In-memory fakes instead of DB |
| **I**solated | No shared state between tests | Fresh fixtures per test |
| **R**epeatable | Same result every time | No random values, fixed time |
| **S**elf-validating | Pass/fail without manual check | Clear assertions |
| **T**imely | Written close to production code | TDD or immediate after |

## Test Structure (Arrange-Act-Assert)

Every test follows the AAA pattern:

```python
def test_calculate_discount_for_premium_user():
    # Arrange - Set up preconditions
    user = User(tier="premium")
    calculator = DiscountCalculator()

    # Act - Execute the behavior under test
    discount = calculator.calculate(user, amount=100)

    # Assert - Verify the expected outcome
    assert discount == 20  # 20% for premium
```

**Why AAA matters:**
- Clear separation of concerns
- Easy to identify what's being tested
- Consistent structure across codebase
- LLMs generate better tests with this pattern

## Test Naming Conventions

### Pattern 1: Method-Scenario-Expected

```
test_<method>_<scenario>_<expected_result>
```

Examples:
- `test_calculate_total_with_zero_quantity_returns_zero`
- `test_validate_email_with_invalid_format_raises_error`
- `test_get_user_when_not_found_returns_none`

### Pattern 2: Should-When (BDD-style)

```
test_should_<expected_behavior>_when_<condition>
```

Examples:
- `test_should_return_empty_list_when_no_orders_exist`
- `test_should_send_notification_when_order_placed`

### Pattern 3: Given-When-Then (Gherkin-style)

```
test_given_<precondition>_when_<action>_then_<result>
```

Examples:
- `test_given_expired_subscription_when_access_premium_then_denied`

## Coverage Strategies

### Coverage Types

| Type | Description | Target |
|------|-------------|--------|
| Line | % of lines executed | 80%+ |
| Branch | % of if/else paths | 75%+ |
| Function | % of functions called | 90%+ |
| Mutation | % of mutants killed | 70%+ |

### What to Cover

**Always test:**
- Public API methods
- Business logic / calculations
- Error handling paths
- Edge cases (null, empty, boundary)
- State transitions

**Skip testing:**
- Simple getters/setters
- Framework-generated code
- Third-party library internals
- Pure configuration

### Coverage Anti-patterns

- Chasing 100% (diminishing returns after 80%)
- Testing implementation details
- Ignoring mutation testing
- Coverage without assertions

## Test Categories

| Category | Scope | Speed | Dependencies |
|----------|-------|-------|--------------|
| Unit | Single function/class | < 10ms | None (mocked) |
| Integration | Multiple components | < 1s | Real dependencies |
| E2E | Full system | > 1s | All services |

## Mocking Strategies

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Pure functions |
| Databases | Domain logic |
| File system | Value objects |
| Time/randomness | Simple calculations |
| Slow services | In-memory structures |

### Test Double Types

| Type | Purpose | Example |
|------|---------|---------|
| **Stub** | Return canned values | `repo.find.return_value = user` |
| **Mock** | Verify interactions | `notifier.send.assert_called()` |
| **Spy** | Wrap real behavior | `Mock(wraps=real_service)` |
| **Fake** | Working alternative | `InMemoryRepository` |

## LLM-Assisted Testing

### Benefits

- Generate comprehensive edge cases
- Identify untested scenarios
- Consistent test structure
- Faster test creation (250x with proper prompts)

### Best Practices for LLM-Generated Tests

1. **Review all generated tests** before merging
2. **Verify assertions** are meaningful (not just `assert True`)
3. **Check edge cases** coverage
4. **Match codebase style** and naming conventions
5. **Run mutation testing** to validate quality

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Run tests
  run: pytest --cov=src --cov-fail-under=80

- name: Mutation testing
  run: mutmut run --paths-to-mutate=src/
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Testing implementation | Breaks on refactor | Test behavior, not internals |
| Over-mocking | Tests mocks, not code | Use fakes for complex deps |
| Shared state | Tests affect each other | Fresh setup per test |
| Testing private methods | Couples to internals | Test through public API |
| Flaky tests | Random failures | Control time, randomness |
| No assertions | Always passes | Verify expected outcomes |
| Giant tests | Hard to debug | One behavior per test |

## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Pre-commit testing checklist |
| [examples.md](examples.md) | Language-specific examples |
| [templates.md](templates.md) | Copy-paste test templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for test generation |

## External Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Go testing Package](https://pkg.go.dev/testing)
- [xUnit Test Patterns](http://xunitpatterns.com/)
- [Martin Fowler on Unit Tests](https://martinfowler.com/bliki/UnitTest.html)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

- [LLM Testing Best Practices](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies)
- [Automated Unit Testing Guide 2026](https://zencoder.ai/blog/automated-unit-testing)
- [AI Testing Frameworks 2026](https://www.accelq.com/blog/ai-testing-frameworks/)
- [Testing AI Systems](https://www.testmo.com/blog/10-essential-practices-for-testing-ai-systems-in-2025/)
