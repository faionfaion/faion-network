# Agent Integration — Python Testing with pytest

Methodology covers core pytest features (fixtures, parametrize, markers), the 2025-2026 plugin ecosystem (pytest-cov, pytest-xdist, pytest-asyncio, pytest-mock, pytest-randomly), and conventions for integrating with Django, FastAPI, and async code. Use this file when an agent bootstraps a pytest suite, writes tests, or migrates from `unittest`.

## When to use
- New Python project — wire pytest as the only test runner; never use stdlib `unittest` for new code.
- Migrating `unittest.TestCase` classes — keep them running, add new tests in pytest style; mix is supported.
- Adding parametrized tests for input matrices, error paths, version sweeps.
- Async test coverage — `pytest-asyncio` for FastAPI, aiohttp, pure asyncio code.
- Parallel CI — `pytest-xdist -n auto` reduces run time on multi-core runners.
- Coverage gates in CI — `pytest --cov --cov-fail-under=80`.
- Snapshot/contract testing of API response shapes via `syrupy` or `pytest-snapshot`.

## When NOT to use
- Doctest-only libraries — pytest can run doctests but adds setup; pure stdlib `python -m doctest` is enough for tiny libs.
- Single-script tools where setup ratio dominates — assert + manual run is fine.
- Hard-real-time / hardware-in-loop tests — pytest's discovery and fixture model add latency; use a dedicated harness.
- BDD-style requirement docs — `pytest-bdd` exists but `behave` is more idiomatic for Gherkin shops.
- Performance benchmarks — `pytest-benchmark` works, but for serious perf use `asv` (airspeed velocity) or vendor-specific profilers.

## Where it fails / limitations
- README's "fixtures > setUp" framing is true but agents over-rely on session-scoped fixtures, hiding inter-test dependencies that pytest-randomly will then expose as flakes.
- `pytest.fixture` scope rules are subtle — `module` vs `package` vs `session` interact with `--reuse-db` (Django) and connection pools.
- `pytest-asyncio` mode (`auto` vs `strict`) is the most common config drift; flipping breaks marker expectations silently.
- Parametrize with complex objects in `params` produces opaque `test_x[arg0]` names — agents skip `ids=` and lose traceability.
- Plugin combos can conflict: `pytest-xdist` + `pytest-randomly` + `pytest-recording` requires explicit seed coordination.
- Coverage of fixture code itself is misleading — `# pragma: no cover` patterns not shown.
- No coverage of `pytest --collect-only` for static analysis or `--co --quiet` for CI tooling.
- Mocking strategy guidance is thin — agents reach for `monkeypatch` when `mocker.patch` is cleaner with autospec.

## Agentic workflow
Bootstrap: (1) `uv add --dev pytest pytest-cov pytest-asyncio pytest-mock pytest-randomly pytest-xdist`, (2) configure `[tool.pytest.ini_options]` in `pyproject.toml` (`testpaths = ["tests"]`, `asyncio_mode = "auto"`, `addopts = "-ra --strict-markers"`), (3) configure `[tool.coverage.run]` (branch + parallel + omit migrations), (4) write `conftest.py` with shared fixtures, (5) per module: `tests/test_<module>.py` mirroring source layout. Per-feature: write smallest failing test first, then implement, then expand parametrize for edge cases. CI: `pytest -n auto --cov --cov-report=xml --cov-fail-under=80`; upload to Codecov.

### Recommended subagents
- `faion-test-agent` — Default for writing tests, fixtures, parametrize matrices.
- `faion-code-agent` — Implements the code under test; toggles to test-agent for failing tests.
- `faion-devtools-developer` — Owns pytest config, plugin selection, CI matrix.
- `faion-feature-executor` — TDD loop: failing test → impl → green → next test.
- `faion-software-architect` — Decides snapshot vs assertion, integration vs unit boundaries.

### Prompt pattern

Add tests for a function:

```
Write pytest tests for <module>.<function> per
free/dev/python-developer/python-testing-pytest/README.md.
Cover:
  - Happy path with realistic input.
  - Edge cases: empty, None, max-size, off-by-one.
  - Error paths: each exception class explicitly raised.
  - @pytest.mark.parametrize for input matrix; provide ids= for readable names.
  - Use `mocker.patch` (pytest-mock) over `monkeypatch` for object methods; autospec=True.
Aim for branch coverage ≥ 90% on the function. Run:
  pytest -v tests/test_<module>.py --cov=<module> --cov-branch --cov-report=term-missing
Show output. Fix any uncovered branches before stopping.
```

Async tests:

```
Add pytest-asyncio tests for <async_module>.<coroutine> per
free/dev/python-developer/python-testing-pytest/README.md.
Setup:
  - asyncio_mode = "auto" (already in pyproject); no @pytest.mark.asyncio needed.
  - Mock httpx with respx; mock asyncpg with the right fixtures.
  - Test concurrent paths: TaskGroup error propagation; ExceptionGroup handling with except*.
  - Timeout assertions: `with pytest.raises(asyncio.TimeoutError): await asyncio.wait_for(...)`.
Run pytest -v --asyncio-mode=auto.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Test runner | https://docs.pytest.org |
| `pytest-cov` | Coverage reporting | https://pytest-cov.readthedocs.io |
| `pytest-xdist -n auto` | Parallel execution | https://pytest-xdist.readthedocs.io |
| `pytest-asyncio` | Async test support | https://pytest-asyncio.readthedocs.io |
| `pytest-mock` | mocker fixture (unittest.mock wrapper) | https://pytest-mock.readthedocs.io |
| `pytest-randomly` | Randomize test order | https://github.com/pytest-dev/pytest-randomly |
| `pytest-django` | Django integration | https://pytest-django.readthedocs.io |
| `pytest-factoryboy` | Factory Boy fixture autoreg | https://pytest-factoryboy.readthedocs.io |
| `pytest-recording` / `vcrpy` | Record HTTP fixtures | https://github.com/kiwicom/pytest-recording |
| `respx` | httpx mocking | https://lundberg.github.io/respx |
| `freezegun` / `time-machine` | Time mocking | https://github.com/spulec/freezegun |
| `pytest-benchmark` | Microbenchmarks with regression detection | https://pytest-benchmark.readthedocs.io |
| `syrupy` / `pytest-snapshot` | Snapshot testing | https://github.com/tophat/syrupy |
| `pytest-watch` / `ptw` | Re-run on file changes | https://github.com/joeyespo/pytest-watch |
| `coverage erase / report / html` | Coverage CLI | https://coverage.readthedocs.io |
| `pytest --collect-only -q` | Static test list (CI gating, indexing) | bundled |
| `hypothesis` | Property-based testing | https://hypothesis.readthedocs.io |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GitHub Actions | CI | Yes — services: postgres/redis | Standard matrix runner |
| Codecov | SaaS coverage | Yes — `coverage xml` upload | PR comments |
| Coveralls | SaaS coverage | Yes | Lighter alt to Codecov |
| Allure | SaaS / OSS reporter | Yes — `allure-pytest` plugin | Rich test reports for stakeholders |
| Datadog CI Visibility | SaaS | Yes — `datadog-ci-pytest` | Per-test telemetry |
| BuildJet / depot.dev | Faster CI runners | Yes — drop-in for GH Actions | Cuts xdist time further |
| Hypothesis CI | OSS service | Yes | Shrinks failing examples |
| Testcontainers | OSS | Yes — postgres/redis containers per session | Replaces sqlite-for-tests |

## Templates & scripts

See `templates.md` for full configs. Add this minimal `pyproject.toml` block (≤45 lines):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-branch",
    "--cov-report=term-missing",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with -m 'not slow')",
    "integration: requires external services",
    "unit: pure unit test (default)",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning:pytest_asyncio.*",
]

[tool.coverage.run]
branch = true
parallel = true
source = ["src"]
omit = [
    "*/migrations/*",
    "*/__main__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_also = [
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@(abc\\.)?abstractmethod",
]
fail_under = 80
show_missing = true
```

## Best practices
- **Mirror source tree in `tests/`** — `src/foo/bar.py` ↔ `tests/foo/test_bar.py`. Auto-discoverable, easy to navigate.
- **Smallest scope first**: function-scope fixture is the default; only widen to module/session when measured cost demands it.
- **Parametrize with `ids=`** — `pytest.param(..., id="empty-list")` makes failures readable.
- **Mock at the boundary, not the call site.** Patch the dependency where it's used in the unit under test (`module.dependency`), not where it's defined.
- **`mocker.patch.object(cls, 'method', autospec=True)`** prevents drift when the real method's signature changes.
- **`pytest-randomly` always on** — exposes order-dependence early. Pin seed in CI for reproducibility on failure.
- **Strict markers + strict config** — typos fail the run, not silently mark as no-marker.
- **`filterwarnings = ["error"]`** turns warnings into failures — catches deprecations before upgrades break.
- **Snapshot DRF/JSON shapes with syrupy** — diff in PR review surfaces unintended response changes.
- **Hypothesis for invariants** (round-trip serializers, idempotent operations) — catches edge cases parametrize misses.
- **Coverage exclude_also** for `if TYPE_CHECKING:`, abstract methods, defensive `raise NotImplementedError` — clean signal.
- **Don't share state via module globals** — fixtures or `pytest-randomly` will burn you.

## AI-agent gotchas
- **Forgotten `await` in async tests** — assertion runs against a coroutine object, passes silently. Ruff `ASYNC` rules + `--strict` warning catch some.
- **`@pytest.fixture` returning vs yielding** — yielding allows teardown; agents return when teardown is needed and leak resources.
- **Fixture scope mismatch**: a `function`-scope fixture depending on a `session`-scope fixture works; the reverse raises at collection time.
- **`monkeypatch.setenv` doesn't reload modules** that read env at import time — agents see no change.
- **`mocker.patch('module.func')` patches the binding, not the def** — patch where the import landed, not where defined.
- **`@pytest.mark.parametrize` with mutable default** — the same list/dict is shared across runs; mutation contaminates.
- **`tmp_path` is per-test, `tmp_path_factory` is per-session** — agents pick wrong scope for cache fixtures.
- **`autouse=True` fixtures** apply to ALL tests in the directory — surprising when the fixture has DB or HTTP side effects.
- **`pytest.raises(Exception)`** catches everything including `KeyboardInterrupt`; use the most specific class.
- **`pytest.warns()` vs `filterwarnings = ["error"]`** — turning warnings to errors breaks `pytest.warns` blocks unless they're scoped via `filterwarnings("default::DeprecationWarning")` marker.
- **`pytest-xdist` and stdout capture** — `print` from one worker can interleave; use `caplog` for log assertions instead.
- **Import-time errors in conftest.py** abort discovery silently — agents debug for hours; run `pytest --collect-only` to surface.
- **`pytest-django` `db` fixture** must be requested by tests touching DB; `pytest-asyncio` async tests with sync DB ORM block the loop and look like timeouts.
- **`pytest-recording`** records and re-uses HTTP cassettes; agents commit cassettes with secrets baked in. Use `filter_headers`.
- **`hypothesis` with random-seeded CI** — agents see flaky failures; pin profile (`hypothesis.settings(profile="ci")`) and shrink locally with `--hypothesis-seed=...`.

## References
- README: `./README.md`
- Sibling: `../django-testing/`, `../django-pytest/`, `../python-async/`, `../python-code-quality/`
- pytest: https://docs.pytest.org
- pytest-cov: https://pytest-cov.readthedocs.io
- pytest-asyncio: https://pytest-asyncio.readthedocs.io
- pytest-xdist: https://pytest-xdist.readthedocs.io
- pytest-mock: https://pytest-mock.readthedocs.io
- coverage.py: https://coverage.readthedocs.io
- hypothesis: https://hypothesis.readthedocs.io
- syrupy: https://github.com/tophat/syrupy
- testcontainers-python: https://testcontainers-python.readthedocs.io
- ruff PT rules: https://docs.astral.sh/ruff/rules/#flake8-pytest-style-pt
