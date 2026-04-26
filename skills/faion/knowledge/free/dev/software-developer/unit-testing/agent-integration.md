# Agent Integration — Unit Testing

Methodology covers AAA pattern, isolation, mocking, naming, deterministic test design. Use this file as the playbook for an LLM agent producing or auditing unit tests.

## When to use
- New code with branching logic, math, parsing, validation, or state transitions — pure functions and small classes.
- Refactor of legacy code where you need a safety net before changing internals.
- Bug fixes — write a failing test reproducing the bug FIRST, then fix.
- Boundary cases (empty inputs, max/min, off-by-one, time-zones, locale, unicode edge cases).
- Self-documenting executable specs alongside docs.

## When NOT to use
- Pure plumbing (controller calls service calls repo) — integration test is more honest, fewer mocks.
- UI rendering — visual regression / snapshot tests catch more, unit tests on JSX/HTML brittle.
- Network protocols, DB-specific queries, cache eviction — needs a real dependency, integration territory.
- Code that's ≤5 lines and trivially correct (`def add(a, b): return a + b`) — coverage noise.
- High-churn experimental code (spike, prototype) — tests rot faster than the code; defer.

## Where it fails / limitations
- README's AAA example (`PriceCalculator`) is decent but never shows mocking — agents need patterns for collaborator isolation.
- No section on test doubles (dummy / stub / spy / mock / fake distinction). Agents reach for `MagicMock` even when a fake would be clearer.
- No guidance on **flaky test triage**: detection, quarantine, root-cause hierarchy (timing → I/O → state → env).
- No mention of property-based testing (hypothesis / fast-check) — entire classes of bugs missed.
- Naming conventions implied (`test_<behavior>_when_<context>`) but not enforced; agents will mix `test_create_user`, `test_user_creation_works`, `test_should_create_user`.
- No anti-pattern catalog (testing private methods, asserting log messages, global state mutation, time.sleep).
- Doesn't address parametrized tests — given snippet uses one assert per test, missing the leverage.

## Agentic workflow
For each unit under test: (1) read the unit; identify inputs (args, config, env), outputs (return, exceptions, side effects), and collaborators, (2) draft test names from the behavior matrix (one row per behavior, one column per relevant context), (3) AAA scaffold per row, (4) collaborator strategy: prefer fakes/stubs over mocks; only mock at process boundary (network/disk/clock), (5) run `pytest -x --tb=short`, (6) on red, fix the test or the code — never disable. CI: ban `pytest.mark.skip` without an issue link.

### Recommended subagents
- `faion-test-agent` — Default for writing unit tests + fixtures.
- `faion-code-agent` — Refactors untestable code into testable seams (DI, pure functions, command/query split).
- `faion-software-architect` — Decides where the unit/integration boundary sits per layer.
- `faion-sdd-execution` — TDD loop: spec → failing test → impl → green → refactor.
- `faion-devtools-developer` — Owns test infra (parallelization, sharding, flake detection).

### Prompt pattern
Behavior-first scaffold:

```
Unit: src/billing/price_calculator.py:calculate_total.
Read it. List behaviors it must satisfy (one bullet per behavior with
inputs and expected output/exception). Then write pytest tests in
tests/billing/test_price_calculator.py:
  - One test class per behavior cluster.
  - AAA layout, blank lines between phases.
  - Names: test_<behavior>_when_<context>.
  - Use fixtures for shared setup. No mocks unless calling network/clock.
  - Cover edges: empty list, negative quantity, fractional tax rate
    (Decimal precision), zero subtotal.
Run: pytest tests/billing/test_price_calculator.py -v.
```

Bug repro:

```
Bug report: Issue #123 — calculate_total returns 0 for quantity=0.
1) Add a failing test in tests/billing/test_price_calculator.py named
   test_calculate_total_returns_zero_for_zero_quantity.
2) Run pytest, confirm it fails for the bug reason.
3) Fix code minimally to pass.
4) Re-run; commit test + fix together. Reference issue in commit body.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Python test runner | https://docs.pytest.org |
| `pytest-xdist` | Parallel test execution | https://pytest-xdist.readthedocs.io |
| `pytest-randomly` | Randomize test order to flush state leaks | https://github.com/pytest-dev/pytest-randomly |
| `pytest-rerunfailures` | Quarantine flake detection (last resort) | https://github.com/pytest-dev/pytest-rerunfailures |
| `freezegun` | Pin `datetime.now()` in tests | https://github.com/spulec/freezegun |
| `time-machine` | Faster freezegun alt | https://github.com/adamchainz/time-machine |
| `hypothesis` | Property-based testing | https://hypothesis.readthedocs.io |
| `vitest` / `jest` | JS/TS unit test runners | https://vitest.dev, https://jestjs.io |
| `ts-jest` | Jest + TypeScript | https://kulshekhar.github.io/ts-jest/ |
| `go test ./... -race -count=1` | Go runner with race detector, no cache | bundled |
| `cargo test` / `cargo nextest` | Rust runners (nextest faster) | https://nexte.st |
| `mocha` + `chai` | Node alt | https://mochajs.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI | CI | Yes | Matrix on Python/Node versions; cache deps |
| CircleCI | CI | Yes — orbs simplify pytest | Test-splitting by timing |
| Buildkite | CI | Yes — agent self-hosted | Good for mono-repos |
| Sauce Labs / BrowserStack | SaaS | No — for E2E, not unit | Skip for unit |
| pytest-html | Local | Yes — HTML report | Useful for sharing failures |
| ReportPortal | OSS / SaaS | Yes — JUnit XML ingest | Aggregate flake stats across runs |

## Templates & scripts
README has AAA. Add a behavior table generator + smoke runner (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/test-unit.sh — fast feedback loop for unit tests.
set -euo pipefail
SCOPE="${1:-tests/}"
pytest "$SCOPE" \
  -x \
  --tb=short \
  -p no:cacheprovider \
  -m "not integration and not e2e and not slow" \
  --maxfail=1 \
  --randomly-seed=last \
  --durations=10
```

`pyproject.toml` markers (matches the script):

```toml
[tool.pytest.ini_options]
markers = [
  "slow: > 1s per test, excluded from -m 'not slow'",
  "integration: spans multiple units / hits real deps",
  "e2e: full stack",
]
addopts = "--strict-markers"
```

## Best practices
- **Behavior names, not function names.** `test_charges_zero_when_quantity_is_zero` beats `test_calculate_total_zero`.
- **One reason to fail per test.** Multiple asserts OK if checking aspects of one behavior; if asserting two different behaviors, split.
- **Fixtures over `setup_method`.** Composable, scope-aware (`function`, `module`, `session`), parametrizable.
- **Inject collaborators**, don't construct them inside the unit. Hard to test == bad design signal, refactor instead of mocking deep.
- **Mock at process boundary, fake elsewhere.** `requests.get` mock OK; `OrderRepository` should be a fake, not `MagicMock(spec=OrderRepository)` lying about the contract.
- **Pin time and randomness.** `freezegun.freeze_time(...)`, `random.seed(0)`. A test that fails twice a year at midnight UTC is the worst kind.
- **Ban `time.sleep` in tests.** Use `await asyncio.sleep(0)` in async, `freezegun.tick`, or refactor to await an event.
- **Run `pytest-randomly` from day 1.** Flushes order dependencies before they entrench.
- **Parametrize boundary cases.** README's password test is a model — error message asserted per row.
- **Fast unit suite < 30s.** If slower, you're including integration; mark and split.
- **Tests live next to code.** `apps/users/tests/test_services.py`, not a top-level `tests/` mirror — easier to keep in sync on refactor.
- **No production logic in test helpers.** A bug in `make_user_with_address` masks bugs in `User.create`.
- **Assertion messages**: `assert x == 5, f"got {x}, expected 5 because ..."` — saves debugging on rare failures.

## AI-agent gotchas
- **`MagicMock` accepts everything**: `mock.foo.bar.baz()` returns a Mock. Tests pass while production calls a method that doesn't exist. Use `spec=` or `autospec=True`.
- **`@patch` decorator order is reversed** vs argument order: bottom-up. `@patch("a") @patch("b") def test(self, mock_b, mock_a)`. Off-by-one bugs galore.
- **Patching the wrong path**: `@patch("foo.bar")` works only if `bar` was imported as `from foo import bar`. If the SUT does `import foo; foo.bar()`, you need `@patch("foo.bar")` AND it works; if SUT did `from foo import bar`, you must patch `sut_module.bar`.
- **Async tests need `pytest-asyncio`** + `@pytest.mark.asyncio` (or `asyncio_mode = "auto"` in config). Forgetting it makes the coroutine return without running.
- **`assert mock.called`** is True even after one call; use `mock.assert_called_once_with(...)` for stricter contracts.
- **Frozen time + DB**: `freezegun` doesn't freeze the DB server's clock. `created_at` set by `auto_now_add` may use server time, not client.
- **`pytest.raises(Exception)`** catches everything including `KeyboardInterrupt`. Use specific exception class.
- **Test order coupling**: a test that mutates `os.environ` without restoring poisons later tests. `monkeypatch` fixture restores automatically.
- **Class-level state** (`class Foo: items = []`) shared across tests if SUT uses class attributes. `setUp` doesn't reset it; explicit `Foo.items = []` per test.
- **Reading from `__pycache__`** can mask file-edit changes when running `pytest` repeatedly without `-p no:cacheprovider` — agents debug "why didn't my fix take effect".
- **Flaky test detection**: `pytest --count=10 -p pytest-repeat` runs same test 10x; cheap way to surface ordering / timing flakes.
- **Async + freezegun**: `time-machine` works, freezegun has known issues. Pick one.
- **Parametrize with mutable defaults**: `@pytest.mark.parametrize("x", [[]])` — if test mutates `x`, next run reuses same list. Use factories.

## References
- README: `./README.md`
- Sibling: `../code-coverage/`, `../tdd-workflow/`, `../mocking-strategies/`, `../test-fixtures/`, `../testing/`
- pytest: https://docs.pytest.org
- pytest-mock: https://pytest-mock.readthedocs.io
- hypothesis (property tests): https://hypothesis.readthedocs.io
- freezegun: https://github.com/spulec/freezegun
- time-machine: https://github.com/adamchainz/time-machine
- xUnit Test Patterns (Meszaros): http://xunitpatterns.com
- Working Effectively with Legacy Code (Feathers) — for legacy testability
- Testing Decorators in Python: https://realpython.com/python-mock-library/
