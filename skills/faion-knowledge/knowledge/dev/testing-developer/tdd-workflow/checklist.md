# TDD Checklist with LLM Integration

A practical checklist for Red-Green-Refactor cycle when working with LLMs like Claude Code, Cursor, or Copilot.

## Pre-TDD Setup

- [ ] Identify the feature or behavior to implement
- [ ] Break down into small, testable units
- [ ] Choose testing framework (pytest, Jest, go test)
- [ ] Ensure test runner is configured and working
- [ ] Set up CLAUDE.md with TDD rules (if using Claude Code)

## RED Phase: Write Failing Test

### Human Tasks

- [ ] Define expected behavior in plain language
- [ ] Identify inputs and expected outputs
- [ ] Consider edge cases and error conditions
- [ ] Write test name that describes the behavior

### LLM Prompt Checklist

- [ ] Specify testing framework explicitly
- [ ] Use Given-When-Then format for clarity
- [ ] Request single-behavior tests
- [ ] Include edge cases in prompt
- [ ] State "test should fail initially"

### Verification

- [ ] Run test → confirms FAIL (not error, but assertion failure)
- [ ] Test fails for the right reason
- [ ] Test is readable and self-documenting
- [ ] Commit failing test with descriptive message

## GREEN Phase: Make Test Pass

### LLM Prompt Checklist

- [ ] Reference the specific failing test
- [ ] Request "minimal implementation"
- [ ] State "do not modify existing tests"
- [ ] Specify "only code needed to pass this test"
- [ ] Include relevant context (existing code, types)

### Verification

- [ ] Run test → confirms PASS
- [ ] No other tests broken (regression check)
- [ ] Implementation does only what test requires
- [ ] No premature optimization
- [ ] Commit passing implementation

## REFACTOR Phase: Improve Code

### Refactoring Targets

- [ ] Remove code duplication (DRY)
- [ ] Improve naming (variables, functions, classes)
- [ ] Extract methods for clarity
- [ ] Simplify complex conditionals
- [ ] Apply appropriate design patterns

### LLM Prompt Checklist

- [ ] Specify refactoring goal clearly
- [ ] State "keep all tests passing"
- [ ] Request small, incremental changes
- [ ] Ask for explanation of changes

### Verification

- [ ] Run tests after each refactoring step
- [ ] All tests still pass
- [ ] Code is more readable
- [ ] No behavior changes introduced
- [ ] Commit refactored code

## Iteration Checklist

### Adding More Tests

- [ ] Identify next behavior to test
- [ ] Write failing test (RED)
- [ ] Implement (GREEN)
- [ ] Refactor if needed
- [ ] Repeat until feature complete

### Test Quality Checks

- [ ] Each test verifies one behavior
- [ ] Tests are independent (no shared state)
- [ ] Tests run fast (< 100ms for unit tests)
- [ ] Test names describe the scenario
- [ ] Assertions have clear error messages

## LLM-Specific Best Practices

### Prompting for Tests

```
Good: "Write a pytest test for a function that calculates shipping cost.
      Test case: order over $100 gets free shipping."

Bad:  "Write tests for shipping."
```

### Prompting for Implementation

```
Good: "Implement calculate_shipping_cost to pass the failing test.
      Only handle the free shipping case for now."

Bad:  "Implement the shipping calculation function."
```

### Prompting for Refactoring

```
Good: "Refactor calculate_shipping_cost: extract the free shipping
      threshold to a constant. Keep all tests passing."

Bad:  "Make the code better."
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing after code | Tests influenced by implementation | Always write test first |
| Multiple behaviors per test | Hard to identify failures | One assertion concept per test |
| Modifying tests to pass | Defeats TDD purpose | Fix code, not tests |
| Skipping refactor phase | Technical debt accumulates | Always review and improve |
| Over-engineering | Gold plating | Only implement what tests require |
| Hardcoded test values | Brittle tests | Use meaningful constants |

## Session Completion Checklist

- [ ] All planned tests written and passing
- [ ] Code refactored and clean
- [ ] No commented-out tests
- [ ] Test coverage adequate for requirements
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] All commits have descriptive messages
- [ ] CI pipeline passes

## Quick Reference: TDD Cycle

```
1. RED    →  Write failing test        →  Human defines "what"
2. GREEN  →  Make test pass (minimal)  →  LLM implements "how"
3. REFACTOR →  Improve code quality    →  Human reviews, LLM executes
4. REPEAT →  Next test                 →  Continue until done
```
