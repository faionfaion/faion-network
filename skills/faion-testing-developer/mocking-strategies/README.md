# Mocking Strategies

## Overview

Test doubles (mocks, stubs, fakes, spies, dummies) isolate code under test from dependencies. Proper mocking enables fast, reliable, and deterministic tests while avoiding the complexity of real external systems.

**Key principle:** Mock at boundaries, not internals. Mock external dependencies (APIs, databases, time), never internal implementation details.

## When to Use Mocking

| Scenario | Mock? | Reason |
|----------|-------|--------|
| External API calls | Yes | Avoid network latency, flakiness, costs |
| Database operations | Sometimes | Use fakes/Testcontainers for integration tests |
| Time/date functions | Yes | Ensure deterministic test results |
| File system operations | Sometimes | Use temp directories when possible |
| Random number generation | Yes | Enable reproducible tests |
| Internal business logic | No | Test real behavior, not mocked behavior |
| Data structures | No | Use real data structures |
| Pure functions | No | No dependencies to mock |

## When NOT to Mock

Mocking has significant downsides when overused:

1. **Internal classes** - Mocking internal implementation couples tests to code structure
2. **Data structures** - Structs, dataclasses, and POJOs should be real
3. **Pure functions** - No external dependencies means no need to mock
4. **Simple value objects** - Creating real instances is simpler
5. **Everything** - If you mock everything, you test nothing

**Signs of over-mocking:**
- Complex mock setup taking more lines than test logic
- Tests break on refactoring without behavior change
- High coverage but bugs slip through
- Mocks returning mocks returning mocks

## Test Doubles Taxonomy

| Type | Purpose | Verification | Example |
|------|---------|--------------|---------|
| **Dummy** | Fill parameter lists | None | Unused config object |
| **Stub** | Provide canned responses | State | Fixed return values |
| **Spy** | Record calls while executing | State + Behavior | Call counter |
| **Mock** | Verify expected interactions | Behavior | Assert method called |
| **Fake** | Simplified working implementation | State | In-memory database |

**State verification:** Assert on the result/output
**Behavior verification:** Assert on interactions/calls

## Language-Specific Tooling

### Python

| Library | Use Case |
|---------|----------|
| `unittest.mock` | Standard library, full-featured |
| `pytest-mock` | pytest plugin, cleaner fixtures |
| `freezegun` | Time mocking (simple, mature) |
| `time-machine` | Time mocking (faster, C extension) |
| `responses` | HTTP mocking for `requests` |
| `pytest-httpx` | HTTP mocking for `httpx` |
| `factory_boy` | Test data factories |

**pytest-mock vs unittest.mock:**
- pytest-mock provides `mocker` fixture with auto-cleanup
- Less boilerplate, cleaner syntax
- Use pytest-mock for pytest projects
- Use unittest.mock for unittest projects or when you need full control

### JavaScript/TypeScript

| Library | Use Case |
|---------|----------|
| Jest mocks | Built-in mocking for Jest |
| Sinon.js | Standalone mocking library |
| nock | HTTP request mocking |
| msw | Mock Service Worker (intercepts fetch/XHR) |
| jest-mock-extended | Type-safe mocks for TypeScript |

### Go

| Tool | Use Case |
|------|----------|
| Interfaces | Native mocking via interface satisfaction |
| gomock | Code generation for mock interfaces |
| testify/mock | Popular mocking library |
| httptest | HTTP handler testing |

**Go pattern:** Define small interfaces at the consumer, implement mocks manually or with gomock.

## Key Concepts

### Mock at Boundaries

```
┌─────────────────────────────────────────┐
│           Your Application               │
│  ┌─────────────────────────────────┐    │
│  │   Business Logic (don't mock)   │    │
│  │                                  │    │
│  │   ┌──────────┐ ┌──────────┐    │    │
│  │   │ Service  │ │ Service  │    │    │
│  │   │    A     │ │    B     │    │    │
│  │   └────┬─────┘ └────┬─────┘    │    │
│  └────────┼────────────┼──────────┘    │
│           │            │                 │
└───────────┼────────────┼─────────────────┘
            │            │
    ┌───────▼───┐   ┌────▼────┐
    │ External  │   │Database │  ← Mock these boundaries
    │   API     │   │         │
    └───────────┘   └─────────┘
```

### Partial Mocking vs Full Replacement

**Full replacement (Mock/Stub):**
- Replace entire dependency with mock
- Use when you need complete control
- Faster, more isolated

**Partial mocking (Spy):**
- Keep real behavior, track calls
- Use when you need real logic + verification
- More realistic but potentially slower

### Mocking Time

Time-dependent code is a common source of flaky tests. Use time mocking libraries:

**Python:** `freezegun` or `time-machine`
**JavaScript:** `jest.useFakeTimers()` or Sinon fake timers
**Go:** Inject a `Clock` interface

**Best practice:** Inject time as a dependency rather than calling `datetime.now()` directly.

### Mocking External APIs

Levels of mocking:

1. **Function-level mock** - Mock the client method (fastest, least realistic)
2. **HTTP-level mock** - Mock HTTP responses (catches marshaling errors)
3. **Container-level mock** - WireMock/MockServer in Docker (most realistic for integration)

**Recommendation:** Use HTTP-level mocking for unit tests, container-level for integration tests.

## LLM Usage Tips

When using LLMs to generate mocks:

### Effective Prompting

1. **Provide the interface/signature** - LLMs need the exact method signatures to mock correctly
2. **Specify the framework** - "using pytest-mock" vs "using unittest.mock"
3. **Include error cases** - Ask for both success and failure scenarios
4. **Request cleanup** - Ask for proper mock teardown

### Common LLM Mistakes to Watch For

- Wrong patch target (patches where defined, not where used)
- Missing `async` handling for async mocks
- Over-complicated mock setups
- Not resetting mocks between tests
- Missing `autospec=True` for signature validation

### Template for LLM Requests

```
Generate a mock for [function/class] that:
- Uses [pytest-mock/unittest.mock/Jest/etc.]
- Returns [expected data] for [scenario]
- Raises [exception] for [error scenario]
- Includes proper cleanup
- Uses autospec for type safety
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Over-mocking | Testing mocks, not code | Mock only external boundaries |
| Complex mock setup | Hard to maintain | Simplify code design |
| Mocking data structures | Unnecessary complexity | Use real data |
| Asserting every call | Brittle tests | Assert on outcomes |
| Not resetting mocks | State leakage | Use fixtures with cleanup |
| Patching wrong location | Mocks not applied | Patch where used, not defined |
| Ignoring signatures | Invalid mock calls pass | Use `autospec=True` |

## Decision Tree: Should I Mock This?

```
Is it external to your system? (API, DB, file system, time)
├── Yes → Consider mocking
│   ├── Is it slow/unreliable/costly?
│   │   ├── Yes → Mock it
│   │   └── No → Maybe use real (with cleanup)
│   └── Is it deterministic?
│       ├── No (time, random) → Mock it
│       └── Yes → Evaluate case by case
└── No (internal code)
    ├── Is it complex with many dependencies?
    │   ├── Yes → Refactor to be testable
    │   └── No → Don't mock, test directly
    └── Is it pure logic?
        └── Yes → Never mock
```

## External Resources

### Official Documentation

- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions)
- [Go Testing](https://pkg.go.dev/testing)
- [gomock](https://github.com/golang/mock)

### Articles and Guides

- [Mocks Aren't Stubs - Martin Fowler](https://martinfowler.com/articles/mocksArentStubs.html)
- [Test Double - Martin Fowler](https://martinfowler.com/bliki/TestDouble.html)
- [When to Mock - Enterprise Craftsmanship](https://enterprisecraftsmanship.com/posts/when-to-mock/)
- [Mocking is an Anti-Pattern](https://www.amazingcto.com/mocking-is-an-antipattern-how-to-test-without-mocking/)
- [Common Mocking Problems - Pytest with Eric](https://pytest-with-eric.com/mocking/pytest-common-mocking-problems/)

### Libraries

- [freezegun](https://github.com/spulec/freezegun) - Python time mocking
- [time-machine](https://github.com/adamchainz/time-machine) - Fast Python time mocking
- [responses](https://github.com/getsentry/responses) - HTTP mocking for requests
- [nock](https://github.com/nock/nock) - HTTP mocking for Node.js
- [msw](https://mswjs.io/) - Mock Service Worker
- [WireMock](https://wiremock.org/) - API mocking server
- [Testcontainers](https://testcontainers.com/) - Docker-based integration testing


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Files

- [checklist.md](checklist.md) - Step-by-step mocking checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - Prompts for LLM-assisted mock generation

---

*Last updated: 2025-01*
