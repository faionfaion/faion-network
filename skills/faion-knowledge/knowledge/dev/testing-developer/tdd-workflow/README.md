# TDD Workflow for LLM-Assisted Development

Test-Driven Development (TDD) is exceptionally effective with LLMs because **tests serve as executable specifications**. When you write tests first, you give the LLM a clear, verifiable target that eliminates ambiguity and prevents scope creep.

## Why TDD Works Better with LLMs

### Tests as Specification

Traditional development: requirements → code → tests (hopes they match)
TDD with LLM: tests (specification) → code (constrained by tests)

The LLM cannot claim completion until assertions pass. This creates a forcing function that:

- **Prevents over-engineering**: Code only does what tests require
- **Eliminates ambiguity**: Tests define exact expected behavior
- **Enables self-correction**: LLM can iterate until tests pass
- **Maintains focus**: Each test is a micro-goal

### The Human-LLM TDD Loop

```
Human writes test    →  LLM implements code    →  Tests run
      ↑                                              ↓
      └──── Human reviews, writes next test ←──────┘
```

The human controls **what** to build (via tests), the LLM handles **how** to build it.

## Red-Green-Refactor for LLM Workflows

### Phase 1: RED (Write Failing Test)

**Human responsibility**: Define expected behavior

```
Prompt: "Write a failing test for a function that validates email addresses.
The test should cover: valid email, missing @, empty domain."
```

Key practices:
- Be specific about edge cases
- One behavior per test
- Use Given-When-Then format for clarity

### Phase 2: GREEN (Make Test Pass)

**LLM responsibility**: Implement minimal code

```
Prompt: "Implement the validateEmail function to make all tests pass.
Write only the code needed to pass these specific tests."
```

Key practices:
- Explicitly state "minimal implementation"
- Run tests after each change
- Commit passing code immediately

### Phase 3: REFACTOR (Improve Code)

**Shared responsibility**: Human reviews, LLM executes

```
Prompt: "Refactor the validateEmail function to improve readability.
Keep all tests passing. Extract validation rules into separate methods."
```

Key practices:
- Run tests after each refactoring step
- Focus on one improvement at a time
- Tests are the safety net

## When TDD Saves Tokens

| Scenario | TDD Approach | Token Impact |
|----------|--------------|--------------|
| Clear requirements | Write tests first | Saves 30-50% (fewer iterations) |
| Bug fix | Failing test → fix | Saves 40% (focused fix) |
| API design | Tests define interface | Saves 50% (less rework) |
| Complex logic | Incremental tests | Saves 60% (early error detection) |

## When TDD Costs More

| Scenario | Alternative | Reason |
|----------|-------------|--------|
| Exploratory coding | Spike first, then test | Requirements unclear |
| UI prototyping | Visual-first | Tests hard to specify |
| One-off scripts | Minimal testing | ROI too low |
| Existing untested code | Add tests incrementally | Full TDD not practical |

## Configuration for Claude Code

### CLAUDE.md Settings

```markdown
## Testing Standards

- Follow TDD: Write failing tests before implementation
- Run tests after every file edit
- Commit failing tests before implementation
- Use pytest for Python, Jest for TypeScript, go test for Go
```

### PostToolUse Hooks

Configure automatic test runs after edits:

```json
{
  "hooks": {
    "PostToolUse": {
      "Edit": "npm test -- --watchAll=false",
      "Write": "pytest -x"
    }
  }
}
```

## Directory Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Red-Green-Refactor checklist with LLM integration |
| [examples.md](examples.md) | TDD examples for Python, TypeScript, Go |
| [templates.md](templates.md) | Test templates for pytest, Jest, go test |
| [llm-prompts.md](llm-prompts.md) | Prompts for test-first development with LLMs |


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Sources

### Foundational TDD

- [Test-Driven Development by Example - Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Refactoring - Martin Fowler](https://martinfowler.com/books/refactoring.html)
- [The Three Laws of TDD - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
- [Is TDD Dead? - Martin Fowler, Kent Beck, DHH](https://martinfowler.com/articles/is-tdd-dead/)

### Framework Documentation

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Go Testing Package](https://pkg.go.dev/testing)
- [Go Wiki: TableDrivenTests](https://go.dev/wiki/TableDrivenTests)

### LLM-Assisted TDD

- [Claude Code and the Art of TDD](https://thenewstack.io/claude-code-and-the-art-of-test-driven-development/)
- [TDD with Claude Code - Steve Kinney](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)
- [My LLM Coding Workflow - Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)
- [Taming GenAI Agents with TDD](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code)
- [ClaudeCode101 TDD Tutorial](https://www.claudecode101.com/en/tutorial/workflows/test-driven)

## Related Methodologies

- [unit-testing.md](../unit-testing.md) - Unit testing patterns
- [integration-testing.md](../integration-testing.md) - Integration test strategies
- [mocking-strategies.md](../mocking-strategies.md) - Test doubles and mocks
- [test-fixtures.md](../test-fixtures.md) - Fixture management
