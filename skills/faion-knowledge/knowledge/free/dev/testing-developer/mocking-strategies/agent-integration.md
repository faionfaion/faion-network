# Agent Integration — Mocking Strategies

## When to use
- Unit tests where the SUT collaborates with external systems (HTTP APIs, databases, S3, message queues, third-party SDKs).
- Time-sensitive code: replace `datetime.now()`, `time.time()`, `Date.now()` with frozen/fake clocks for determinism.
- Randomness: seed PRNGs or stub random sources to make property-style tests reproducible.
- Replacing slow or paid services in CI (Stripe, Twilio, OpenAI) with fakes/recordings.
- Characterization tests over legacy code where dependencies cannot be easily injected.
- Async code: use `AsyncMock` (Python), `vi.fn().mockResolvedValue` (Vitest), `jest.fn().mockResolvedValue` (Jest).

## When NOT to use
- Integration tests — mocking the integration target defeats the purpose; use Testcontainers / real local services.
- Pure functions, dataclasses, value objects — they have no dependencies; mocking is noise.
- The class/function under test itself — agents commonly mock the SUT to make tests "pass".
- E2E flows — must exercise real services in a controlled environment.
- Cases where a 30-line in-memory fake is cheaper to maintain than a chain of `MagicMock` calls.
- DB-specific behavior (constraints, isolation levels) — mocks cannot validate that.

## Where it fails / limitations
- README mixes Python and JS/TS — agents cross-pollinate idioms (`jest.spyOn` in pytest, `@patch` in Jest).
- The "patch where used, not where defined" rule appears once and gets ignored — most failures trace back to `@patch("source_module.dep")` instead of `@patch("consumer_module.dep")`.
- `MagicMock()` swallows attribute typos — `mock.fetech_user()` returns a Mock and the test passes; agents skip `spec=`/`autospec=True`.
- No coverage of `respx` (httpx-native), `responses` is shown but not `httpx` async equivalents.
- No mention of `pytest-mock`'s `mocker` fixture — agents stick with verbose decorator stacks.
- `Mock(wraps=real)` example claims spy-on-real, but if the real method calls `self.other()`, the wrapper bypasses it.
- Decorator stack ordering (bottom-up vs argument order) is buried; agents flip arg order on multi-`@patch`.
- `freeze_time` doesn't propagate to subprocess / DB-server clock — invisible footgun.

## Agentic workflow
Force the agent to **classify each collaborator first, mock second**. Two-step prompt: (1) read SUT, list collaborators, classify each as `pure | stub | fake | mock | integration`; (2) write tests using the chosen double, prefer fake > stub > mock. Run mutation tests (`mutmut`, `cosmic-ray`, `stryker`) after the suite is green to catch over-mocked tests that pass against any implementation. A reviewer subagent restricted to `tests/` paths scans diffs for mocks of internal classes / dataclasses and rejects them.

### Recommended subagents
- `faion-sdd-executor-agent` — when test generation is a quality gate inside an SDD task.
- `faion-test-agent` (custom) — single-purpose: emit pytest/vitest tests for a given module, restricted to `tests/`.
- Reviewer subagent — audits diffs for over-mocking smells (`assert_called_once` chains > 3, mocks of internal types).
- General-purpose subagent restricted to `tests/` paths only — prevents the "make it more testable" production-code edits sneaking in.

### Prompt pattern
```
Goal: write tests for <module>.<function>.
Step 1: list collaborators of <function>; classify each as pure/stub/fake/mock/integration.
Step 2: for each non-pure collaborator pick the smallest double (fake > stub > mock).
Step 3: emit pytest test file. Use pytest-mock `mocker` fixture, autospec=True for mocks.
Forbidden: mocking the SUT; mocking dataclasses; >3 `assert_called_*` per test.
```

```
Audit-only: scan <test_file> for over-mocking.
Output JSON list of mocks with severity {ok | suspicious | wrong-layer} and a one-sentence justification. Do not edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest-mock` | `mocker` fixture wrapping `unittest.mock` with auto-cleanup | https://pytest-mock.readthedocs.io |
| `freezegun` | Freeze `datetime.now()` for deterministic tests | https://github.com/spulec/freezegun |
| `time-machine` | Faster freezegun alternative (C extension) | https://github.com/adamchainz/time-machine |
| `responses` | Stub `requests` calls | https://github.com/getsentry/responses |
| `pytest-httpx` | Stub `httpx` calls | https://github.com/Colin-b/pytest_httpx |
| `respx` | httpx-native route-based mocking | https://lundberg.github.io/respx/ |
| `vcrpy` | Record/replay real HTTP traffic to YAML cassettes | https://vcrpy.readthedocs.io |
| `msw` | Mock Service Worker — TS/JS network mocks for browser+node | https://mswjs.io/ |
| `nock` | Node HTTP interceptor | https://github.com/nock/nock |
| `sinon` | JS spies/stubs/mocks | https://sinonjs.org/ |
| `mockery` (Go) | Auto-generate mocks from Go interfaces | https://github.com/vektra/mockery |
| `gomock` | Google's interface mocking framework for Go | https://github.com/uber-go/mock |
| `mutmut` / `cosmic-ray` | Mutation testing — surface tests that pass against any impl | https://mutmut.readthedocs.io |
| `stryker-mutator` | Mutation testing for JS/TS/C# | https://stryker-mutator.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| WireMock / WireMock Cloud | OSS + SaaS | Yes — REST admin API | Hosted mock server; record-and-replay supported |
| Mockoon | OSS | Yes — CLI + Docker image | Local mock server with admin API and openapi import |
| MSW | OSS | Yes — same handlers in Storybook + tests | Network-level interception; works in Node + browser |
| Pact (broker) | OSS + SaaS | Yes — CLI driveable | Consumer-driven contract testing replacing brittle E2E mocks |
| Hoverfly | OSS | Yes — CLI proxy mode | Service virtualization; replay HAR files |
| LocalStack | OSS + SaaS | Yes — `awslocal` CLI | Local AWS API mock — far better than mocking `boto3` calls |
| Testcontainers | OSS | Yes — programmatic API | Pair with mocking: real services for integration, mocks for unit |
| Beeceptor | SaaS | Yes — REST control | Quick public mock endpoints for webhooks |

## Templates & scripts
See `templates.md` for ready-made `mocker` / `responses` / `respx` patterns. Inline detector for the over-mocking smell:

```python
#!/usr/bin/env python3
# scripts/over-mock-lint.py — flag tests with too many call-assertions per function.
import ast, sys, pathlib
THRESHOLD = 4
issues = 0
for path in pathlib.Path("tests").rglob("test_*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            asserts = sum(
                1 for c in ast.walk(node)
                if isinstance(c, ast.Attribute) and c.attr.startswith("assert_called")
            )
            if asserts > THRESHOLD:
                print(f"{path}:{node.lineno} {node.name} has {asserts} call assertions")
                issues += 1
sys.exit(1 if issues else 0)
```

## Best practices
- Mock at architectural seams (gateways, repositories, clients), never internal helpers.
- Prefer fakes over mocks for repositories — `FakeUserRepo` (30 lines, in-memory dict) reuses across the suite, survives refactors.
- `assert_called_with(...)` only for contracts that matter ("an email is sent on order placement"), never for incidental calls.
- For HTTP, use route-based matchers (URL + method + body shape) not exact-string matches; resilient to harmless changes.
- Reset mocks between tests — `pytest-mock` does this automatically; raw `unittest.mock` does not unless wrapped.
- For time, prefer injecting a `Clock` interface and providing a `FakeClock` over `freeze_time`; cleaner, faster, async-safe.
- Long inline mock setup is a smell — move to fixtures, keep tests tight.
- Use `autospec=True` / `spec=Real` to validate mock signatures match the real callable.

## AI-agent gotchas
- Agents mock the SUT to make tests pass. Add an explicit "do not mock the function under test" rule.
- `@patch('foo.bar.baz')` patches the **import location**, not source. `from foo import bar` in SUT requires `@patch('sut_module.bar')`.
- `Mock()` returns Mock for any attribute — typos pass silently. Always use `spec=` or `autospec=True`.
- `AsyncMock` vs `Mock`: agent uses `Mock` for `async def` and `await` returns a coroutine wrapping a Mock. Always use `AsyncMock` for async callables.
- `side_effect=[a, b]` lists raise `StopIteration` if the SUT calls more times than expected — confusing test failure.
- `@patch` decorator order is reversed vs argument order (bottom-up); off-by-one bugs galore on multi-patch.
- Mocking dataclasses or pydantic models almost always means the design needs adjustment, not the test — reject these diffs.
- `freeze_time` does NOT propagate to subprocesses, threads, or DB-server clocks; agents miss this in concurrency tests.
- Human-in-loop checkpoint: review any test that mocks more than two collaborators per function — over-mocking smell threshold.
- Coverage % goes up with mocks while real bugs slip — pair with mutation testing.

## References
- README: `./README.md`
- Sibling: `../unit-testing/`, `../integration-testing/`, `../test-fixtures/`, `../tdd-workflow/`
- https://docs.python.org/3/library/unittest.mock.html
- https://martinfowler.com/articles/mocksArentStubs.html
- https://martinfowler.com/bliki/TestDouble.html
- https://pytest-mock.readthedocs.io/
- https://jestjs.io/docs/mock-functions
- https://lundberg.github.io/respx/
- https://docs.pact.io/
- https://testcontainers.com/
