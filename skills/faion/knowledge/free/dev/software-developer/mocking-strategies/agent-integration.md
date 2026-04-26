# Agent Integration — Mocking Strategies

## When to use
- Writing unit tests that need to isolate code from databases, HTTP services, time, randomness, or filesystem.
- Generating fixture-style fakes (`FakeUserRepository`) for fast in-memory tests of service layers.
- Mocking third-party SDK calls (Stripe, Twilio, S3) where real calls are expensive or non-deterministic.
- Adding `freeze_time` / fake-clock decorators to fix flaky time-dependent tests.
- Composing `AsyncMock` and `pytest-httpx` / `responses` for async HTTP clients.
- Writing characterization tests around legacy code by stubbing its dependencies.

## When NOT to use
- Integration tests that should hit a real DB / queue / cache. Mocking here defeats the purpose; use Testcontainers instead.
- Pure functions — they need no mocks; mocking constants reveals a design smell.
- Tests of the boundary itself (the HTTP client, the SQL query). Mock the layer **below**, test the boundary against a real (or VCR-recorded) backend.
- End-to-end tests — should exercise real services in a controlled environment.
- Cases where a fake is cheaper to maintain than a mock — prefer fakes for repository/cache abstractions.

## Where it fails / limitations
- README mixes Python and TypeScript; agents tend to copy idioms across languages incorrectly (e.g., `jest.spyOn` in pytest, `@patch` in Jest).
- `patch('mymodule.datetime')` example is a classic foot-gun — `datetime.now()` works, but `datetime(...)` constructor breaks unless `side_effect` is set; agents reproduce only the first half.
- The decorator-stack ordering note ("decorators are applied bottom-up") is buried; agents flip the argument order on multi-`@patch` and silently mis-mock.
- `MagicMock()` for `__enter__` / `__exit__` is shown but the `with patch('builtins.open', mock_open(...))` idiom (more idiomatic) is missing.
- `Mock(wraps=real_obj)` example claims spy-on-real, but if the real method itself calls another method on `self`, the wrapper bypasses it. Agents miss this.
- No mention of `pytest-mock`'s `mocker` fixture (cleaner than raw `patch`); agents stick to verbose decorator forms.
- HTTP examples use `responses` (sync) and `pytest-httpx` (async) but never `respx` (httpx-native, very popular).

## Agentic workflow
Make the agent choose the right test double **first**, write the test second. Use a two-step prompt: (1) given the production code, classify each external collaborator as `pure | stub | fake | mock | integration`; (2) generate the test using the chosen double. This prevents the default LLM behavior of mocking everything. Run mutation tests (`mutmut`, `cosmic-ray`) periodically to catch over-mocked tests that pass even when production code is broken.

### Recommended subagents
- `faion-sdd-executor-agent` — when test generation is part of an SDD task with explicit AC.
- General-purpose subagent restricted to `tests/` paths only — prevents accidental edits to production code under the guise of "making it more testable".
- Reviewer subagent that scans new tests for anti-patterns (`assert_called_once` chains > 3, mocks of internal classes).

### Prompt pattern
```
Goal: write tests for <module>.<function>.
Step 1: list collaborators of <function> and classify each as pure/stub/fake/mock/integration.
Step 2: for each non-pure collaborator, propose the smallest double (prefer fake > stub > mock).
Step 3: emit pytest test file. Use pytest-mock `mocker` fixture, not raw @patch.
Forbidden: mocking the function under test; mocking dataclasses; verifying internal helper calls.
```

```
Audit-only: scan <test_file> for over-mocking.
Output: list of mocks with severity {ok | suspicious | wrong-layer}, and a one-sentence justification.
Do not edit.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest-mock` | `mocker` fixture wrapping `unittest.mock` | https://pytest-mock.readthedocs.io/ |
| `freezegun` | Freeze time for deterministic tests | https://github.com/spulec/freezegun |
| `time-machine` | Faster `freezegun` alternative | https://github.com/adamchainz/time-machine |
| `responses` | Stub `requests` calls | https://github.com/getsentry/responses |
| `pytest-httpx` | Stub `httpx` calls | https://github.com/Colin-b/pytest_httpx |
| `respx` | httpx mocking, route-based | https://lundberg.github.io/respx/ |
| `vcrpy` | Record/replay real HTTP traffic | https://vcrpy.readthedocs.io/ |
| `wiremock` | Standalone HTTP mock server | https://wiremock.org/ |
| `msw` (Mock Service Worker) | TS/JS network mocking, browser+node | https://mswjs.io/ |
| `nock` | Node HTTP interceptor | https://github.com/nock/nock |
| `sinon` | JS spies/stubs/mocks | https://sinonjs.org/ |
| `mutmut` / `cosmic-ray` | Mutation testing — catches over-mocked suites | https://mutmut.readthedocs.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| WireMock Cloud | SaaS | Yes | Hosted mock server; useful for shared contract mocks. |
| Mockoon | OSS | Yes | Local mock server with CLI; good for E2E test fixtures. |
| Testcontainers | OSS | Yes | Pair with mocking — real services for integration, mocks for unit. |
| LocalStack | OSS | Yes | Local AWS mock — use instead of mocking boto3 calls. |
| MSW (Mock Service Worker) | OSS | Yes | Same handler reused in tests + Storybook. |
| Pact | SaaS+OSS | Yes | Consumer-driven contract testing — replaces brittle mocks at API boundaries. |
| Hoverfly | OSS | Yes | Service virtualization, replay HAR/captured traffic. |

## Templates & scripts
Inline anti-pattern detector — flags tests with too many `assert_called` per function (over-mocking proxy):

```python
#!/usr/bin/env python3
# scripts/over-mock-lint.py
import ast, sys, pathlib
THRESHOLD = 4
issues = 0
for path in pathlib.Path("tests").rglob("test_*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            asserts = sum(
                1 for c in ast.walk(node)
                if isinstance(c, ast.Attribute)
                and c.attr.startswith("assert_called")
            )
            if asserts > THRESHOLD:
                print(f"{path}:{node.lineno} {node.name} has {asserts} call assertions")
                issues += 1
sys.exit(1 if issues else 0)
```

## Best practices
- Mock at architectural seams (repositories, gateways, clients), not internal helpers.
- Prefer fakes over mocks for repositories — a 30-line `FakeUserRepository` is reusable across the suite and survives refactors.
- Use `assert_called_with(...)` only for behavior that is part of the contract (e.g., "an email is sent on order placement"); not for incidental calls.
- For HTTP mocks, prefer route-based matchers (URL + method + body shape) over exact-string matches; resilient to harmless changes.
- Reset mocks between tests (`pytest-mock` does this automatically; raw `unittest.mock` does not unless using context managers or `autouse` fixtures).
- For time, prefer injecting a `Clock` interface and providing a `FakeClock` fake over `freeze_time`; cleaner and faster.
- Keep mock setup in fixtures, assertions in tests — long inline mock setup is a smell.

## AI-agent gotchas
- Agents instinctively mock the function under test rather than its dependencies. Add an explicit "do not mock the system under test" rule.
- `@patch('foo.bar.baz')` patches the **import location**, not the source. Agents patch the source (`baz`'s defining module), which doesn't take effect. Always patch where it's looked up.
- `Mock()` returns a `Mock` for any attribute access — typos in attribute names silently pass. Use `spec=RealClass` or `autospec=True` to get errors instead.
- `AsyncMock` vs `Mock` confusion: agent mocks an async function with `Mock` and `await` returns a coroutine wrapping a Mock. Use `AsyncMock` always for `async def`.
- Agents over-use `side_effect` lists; if the production code calls the dependency more times than expected, you get `StopIteration` instead of a clear error.
- Mocking dataclasses or pydantic models almost always means the design needs adjustment, not the test. Reject these.
- `freeze_time` on a function decorator does NOT propagate to subprocesses or threads; agents misuse this in concurrency tests.
- Human-in-loop checkpoint: review any test that mocks more than two collaborators per test function — this is the over-mocking smell threshold.

## References
- https://docs.python.org/3/library/unittest.mock.html
- https://martinfowler.com/articles/mocksArentStubs.html
- https://martinfowler.com/bliki/TestDouble.html
- https://pytest-mock.readthedocs.io/
- https://jestjs.io/docs/mock-functions
- https://lundberg.github.io/respx/
- https://docs.pact.io/
- https://testcontainers.com/
