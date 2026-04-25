# Agent Integration — Unit Testing

## When to use
- New code with branching logic, parsing, validation, calculations, or state transitions — pure functions and small classes.
- Refactor of legacy code where you need a safety net before changing internals (characterization tests).
- Bug fixes — write a failing test that reproduces the bug FIRST, then fix.
- Boundary cases (empty inputs, max/min, off-by-one, time-zones, locale, unicode edge cases).
- Self-documenting executable specs co-located with code.
- Per-language: pytest (Python), Vitest/Jest (JS/TS), `go test` (Go), `cargo test`/`nextest` (Rust).

## When NOT to use
- Pure plumbing (controller → service → repo with no logic) — integration test is more honest with fewer mocks.
- UI rendering — visual regression / snapshot tests catch more than brittle assertions on JSX/HTML.
- Network protocols, DB-specific queries, cache eviction — needs a real dependency, integration territory.
- Trivially correct ≤5-line code (`def add(a, b): return a + b`) — coverage noise.
- High-churn experimental code (spike, prototype) — tests rot faster than the code; defer until shape stabilizes.
- Framework boilerplate (Django admin registration, FastAPI route registration without logic).

## Where it fails / limitations
- README's FIRST principles + AAA list is solid but never shows mocking patterns — agents reach for `MagicMock` even when a fake would be clearer.
- No section on test doubles taxonomy (dummy / stub / spy / mock / fake) — agents conflate them.
- No flaky-test triage hierarchy (timing → I/O → state → env); agents add `pytest.mark.flaky(reruns=3)` instead of fixing root cause.
- No mention of property-based testing (`hypothesis`, `fast-check`, Go fuzzing) — entire bug classes missed.
- No anti-pattern catalog (testing private methods, asserting log messages, global state mutation, `time.sleep`).
- Coverage section says "80%+" without distinguishing line vs branch vs mutation — agents game line coverage.
- Doesn't address parametrized tests — naming patterns shown use one assert per test, missing the leverage.

## Agentic workflow
For each unit under test: (1) read the unit; identify inputs (args, config, env), outputs (return, exceptions, side effects), and collaborators; (2) draft test names from the behavior matrix (one row per behavior, one column per relevant context); (3) AAA scaffold per row; (4) collaborator strategy: prefer fakes/stubs over mocks; only mock at process boundary (network/disk/clock); (5) run `pytest -x --tb=short` (or framework equivalent); (6) on red, fix the test or the code — never disable. CI gate: ban `pytest.mark.skip` / `it.skip` without an issue link in the reason string.

### Recommended subagents
- `faion-test-agent` (custom) — emit unit tests + fixtures for a target module, restricted to `tests/`.
- `faion-code-agent` — refactors untestable code into testable seams (DI, pure functions, command/query split).
- `faion-software-architect` — decides where the unit/integration boundary sits per layer.
- `faion-sdd-execution` — TDD loop: spec → failing test → impl → green → refactor.
- `faion-devtools-developer` — owns test infra (parallelization, sharding, flake detection).

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
  - Fixtures for shared setup. No mocks unless the call hits network/clock.
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
| `pytest-xdist` | Parallel test execution (`-n auto`) | https://pytest-xdist.readthedocs.io |
| `pytest-randomly` | Randomize test order; flushes state leaks | https://github.com/pytest-dev/pytest-randomly |
| `pytest-rerunfailures` | Quarantine flake detection (last resort) | https://github.com/pytest-dev/pytest-rerunfailures |
| `pytest-cov` | Coverage with branch tracking | https://pytest-cov.readthedocs.io |
| `freezegun` / `time-machine` | Pin `datetime.now()` deterministically | https://github.com/spulec/freezegun |
| `hypothesis` | Property-based testing for Python | https://hypothesis.readthedocs.io |
| `vitest` / `jest` | JS/TS unit test runners | https://vitest.dev, https://jestjs.io |
| `fast-check` | Property-based testing for JS/TS | https://fast-check.dev |
| `go test ./... -race -count=1` | Go runner with race detector, no cache | bundled |
| `cargo nextest` | Rust runner — faster than `cargo test` | https://nexte.st |
| `mutmut` / `cosmic-ray` / `stryker` | Mutation testing — kill "fake" tests | https://mutmut.readthedocs.io |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions / GitLab CI | CI | Yes | Matrix on Python/Node versions; cache deps |
| CircleCI | CI | Yes — `circleci tests split` for sharding | Test-splitting by timing |
| Buildkite | CI | Yes — agent self-hosted | Good for monorepos |
| ReportPortal | OSS / SaaS | Yes — JUnit XML ingest | Aggregate flake stats across runs |
| pytest-html | Local | Yes — HTML report | Useful for sharing failures |
| Codecov / Coveralls | SaaS | Yes — REST API + tokens | Coverage trend tracking; PR comment integration |
| Trunk Flaky Tests | SaaS | Yes — JUnit ingest | Auto-quarantine flaky tests |

## Templates & scripts
See `templates.md` for AAA scaffolds. Smoke runner for the fast-feedback loop:

```bash
#!/usr/bin/env bash
# scripts/test-unit.sh — fast feedback for unit tests only.
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
- **Inject collaborators**, don't construct them inside the SUT. Hard-to-test == bad design signal; refactor instead of mocking deep.
- **Mock at process boundary, fake elsewhere.** `requests.get` mock OK; `OrderRepository` should be a fake, not `MagicMock(spec=OrderRepository)` lying about the contract.
- **Pin time and randomness.** `freezegun.freeze_time(...)`, `random.seed(0)`. A test that fails twice a year at midnight UTC is the worst kind.
- **Ban `time.sleep` in tests.** Use `await asyncio.sleep(0)` in async, `freezegun.tick`, or refactor to await an event.
- **Run `pytest-randomly` from day 1.** Flushes order dependencies before they entrench.
- **Parametrize boundary cases.** One row per case, error message asserted per row.
- **Fast unit suite < 30s.** If slower, you're including integration; mark and split.
- **Tests live next to code.** `apps/users/tests/test_services.py`, not a top-level `tests/` mirror — easier to keep in sync on refactor.
- **No production logic in test helpers.** A bug in `make_user_with_address` masks bugs in `User.create`.

## AI-agent gotchas
- **`MagicMock` accepts everything**: `mock.foo.bar.baz()` returns a Mock. Tests pass while production calls a method that doesn't exist. Use `spec=` or `autospec=True`.
- **`@patch` decorator order is reversed** vs argument order (bottom-up). `@patch("a") @patch("b") def test(self, mock_b, mock_a)`. Off-by-one bugs galore.
- **Patching the wrong path**: `@patch("foo.bar")` works only if `bar` was imported as `from foo import bar`. If the SUT did `from foo import bar`, you must patch the SUT module's `bar`.
- **Async tests need `pytest-asyncio`** + `@pytest.mark.asyncio` (or `asyncio_mode = "auto"` in config). Forgetting it makes the coroutine return without running.
- **`assert mock.called`** is True even after one call; use `mock.assert_called_once_with(...)` for stricter contracts.
- **Frozen time + DB**: `freezegun` doesn't freeze the DB server's clock. `created_at` set by `auto_now_add` may use server time.
- **`pytest.raises(Exception)`** catches everything including `KeyboardInterrupt`. Use the specific exception class.
- **Test order coupling**: a test that mutates `os.environ` without restoring poisons later tests. `monkeypatch` fixture restores automatically.
- **Class-level state** (`class Foo: items = []`) shared across tests if SUT uses class attributes. `setUp` doesn't reset it.
- **Reading from `__pycache__`** can mask file-edit changes when running `pytest` repeatedly without `-p no:cacheprovider`.
- **Flaky test detection**: `pytest --count=10 -p pytest-repeat` runs same test 10x; cheap way to surface ordering / timing flakes.
- **Async + freezegun**: `time-machine` works, freezegun has known issues. Pick one.
- **Parametrize with mutable defaults**: shared list mutated across runs — use factories.

## References
- README: `./README.md`
- Sibling: `../mocking-strategies/`, `../tdd-workflow/`, `../test-fixtures/`, `../testing-patterns/`, `../testing-pytest/`
- pytest: https://docs.pytest.org
- pytest-mock: https://pytest-mock.readthedocs.io
- hypothesis: https://hypothesis.readthedocs.io
- xUnit Test Patterns (Meszaros): http://xunitpatterns.com
- Working Effectively with Legacy Code (Feathers) — for legacy testability
- "FIRST" principles: https://agileinaflash.blogspot.com/2009/02/first.html
