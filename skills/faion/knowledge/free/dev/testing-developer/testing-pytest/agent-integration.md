# Agent Integration — pytest Testing Framework

## When to use

- Adding pytest to a Python repo with no test framework, or migrating off `unittest`.
- Bootstrapping the canonical plugin set: `pytest-cov`, `pytest-xdist`, `pytest-mock`, `pytest-asyncio`, `pytest-randomly`, `pytest-timeout`.
- Configuring pytest in `pyproject.toml` with strict markers, strict config, `filterwarnings = ["error"]`, and explicit `testpaths`.
- Generating new tests from a spec/AC: parametrized tests for happy/edge cases, fixtures for setup/teardown, mocks for external boundaries.
- Speeding up an existing suite: parallelism (`-n auto`), session-scoped fixtures, cheaper test setup (in-memory DB, monkeypatching slow deps).
- Diagnosing flake: `pytest-randomly` to surface order coupling, `pytest-rerunfailures` for confirmation, `pytest -p no:cacheprovider --lf` for narrowing.
- Upgrading from pytest 7.x → 8.x and dealing with the removed warnings, async-fail behaviour, and TOML config changes.

## When NOT to use

- Trivial scripts where adding `pytest` is overkill — a few `assert ... else SystemExit(1)` checks suffice.
- Test code that *must* run inside another runner (Django's `manage.py test`, Tox+legacy unittest) until that constraint is removed.
- Performance benchmarks on production paths — use `pytest-benchmark` only as a dev tool, not as gating.
- E2E browser tests — Playwright/Cypress have richer fixtures; `pytest-playwright` exists but it's a different methodology (see `e2e-testing`).
- TDD coaching for absolute beginners — too many concepts at once. Start with `unittest` then graduate.

## Where it fails / limitations

- **Implicit fixture dependencies**. Cross-file conftest discovery makes the dependency graph hard to read; agents that reorganise `tests/` break fixture resolution silently.
- **Fixture scope misuse**. A `session`-scoped fixture that mutates state turns the suite into one giant test.
- **`autouse=True`** is convenient and dangerous; tests run with hidden side effects. Hard to debug across hundreds of tests.
- **Plugin interaction order** is non-deterministic across pytest versions (`pytest-asyncio` + `pytest-django` + `pytest-xdist`) — pinning matters.
- **`--lf` / `--ff` cache** can lie when tests are renamed or parametrized differently — agents trust it and miss real failures.
- **Async tests without proper config** — pytest 8.4 hard-fails them (was warn+skip on 8.0). Agents copying old configs see breakage.
- **Tests returning non-None** is now a hard error in 8.4. Old `unittest`-converted tests with `return self.assertX(...)` silently break.
- **`monkeypatch`** scope is function-only; agents that `monkeypatch.setattr(module, "var", value)` and expect persistence across the session are confused.
- **`pytest --collect-only` ambiguities**: same name in two files yields collection errors with poor diagnostics.
- **Coverage gaming.** `pytest-cov` % rewards line touches, not assertions.
- **Parallelism + DB**. Without per-worker DB isolation, `-n auto` creates phantom failures.

## Agentic workflow

Run pytest as a deterministic gate: discover tests (`pytest --collect-only`), run them with strict markers/strict config in CI (`pytest -ra --strict-markers --strict-config`), capture coverage with a per-file threshold, and surface flake via `pytest-randomly`. Agents generate tests from acceptance criteria using the AAA pattern, parametrize edge cases, scope fixtures correctly, and never use `autouse=True` without explicit justification. The agent updates `pyproject.toml` only as a separate step with diff review.

### Recommended subagents

- `faion-testing-developer` (`testing-pytest`, `test-fixtures`, `mocking-strategies`) — Owns the methodology and patterns.
- `faion-python-developer` — Pairs to write fixtures aligned with the codebase (Django/FastAPI/SQLAlchemy idioms).
- `faion-sdd-executor-agent` — Treats AC → pytest tests as the gate; fails task `done` until tests for the AC pass.
- `faion-code-quality` — Wires `pytest -q --cov --cov-fail-under=…` into CI and PR review; rejects coverage drops.
- `faion-improver` — Periodic flake hunt (`pytest-randomly`), slowest-test tracking (`--durations=20`), unused-fixture audit.
- General-purpose `Task` subagent for `unittest → pytest` migration: mechanical and scoped per file.

### Prompt pattern

Generate tests for a function:

```
Function: <module>.<func>(<sig>) → <return>.
Generate tests/<module>/test_<func>.py:
- AAA pattern, one logical assert focus per test.
- Parametrize edge cases (boundary, empty, None, invalid type).
- Mock <external> via mocker.patch('<module>.<external>').
- No autouse fixtures unless setup is universal across the file.
Run: pytest -q tests/<module>/test_<func>.py --cov=<module>.
Stop on first failure with full traceback. No retries.
```

Plugin bootstrap on a fresh repo:

```
Add to pyproject.toml [tool.pytest.ini_options]:
- testpaths = ["tests"]
- addopts = ["-ra", "--strict-markers", "--strict-config", "--cov", "--cov-report=term-missing"]
- filterwarnings = ["error"]
- markers = [...]  # explicit
Pin: pytest, pytest-cov, pytest-xdist, pytest-mock, pytest-randomly, pytest-timeout, pytest-asyncio.
Add tests/conftest.py with shared fixtures only (no autouse).
Show diff first; apply only after approval.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Core runner | https://docs.pytest.org |
| `pytest-cov` | Coverage reporting | https://pytest-cov.readthedocs.io |
| `pytest-xdist` | Parallel + distributed | https://pytest-xdist.readthedocs.io |
| `pytest-mock` | `mocker` fixture (unittest.mock wrapper) | https://github.com/pytest-dev/pytest-mock |
| `pytest-asyncio` | `async def` test support | https://pytest-asyncio.readthedocs.io |
| `pytest-anyio` | Trio + asyncio | https://anyio.readthedocs.io |
| `pytest-timeout` | Hard test timeouts | https://github.com/pytest-dev/pytest-timeout |
| `pytest-randomly` | Randomise test order | https://github.com/pytest-dev/pytest-randomly |
| `pytest-rerunfailures` | Retry transient failures (use sparingly) | https://github.com/pytest-dev/pytest-rerunfailures |
| `pytest-instafail` / `pytest-sugar` | Better progress UX | https://github.com/Teemu/pytest-sugar |
| `pytest-benchmark` | Microbenchmarks | https://pytest-benchmark.readthedocs.io |
| `pytest-bdd` | Gherkin-style BDD | https://pytest-bdd.readthedocs.io |
| `pytest-django` | Django integration | https://pytest-django.readthedocs.io |
| `pytest-flask` | Flask integration | https://pytest-flask.readthedocs.io |
| `pytest-httpx` | `httpx` async mocking | https://github.com/Colin-b/pytest_httpx |
| `pytest-playwright` | Playwright integration | https://playwright.dev/python/docs/test-runners |
| `coverage` | Lower-level coverage tool | https://coverage.readthedocs.io |
| `tox` | Multi-env runner | https://tox.wiki |
| `nox` | Pythonic alt to tox | https://nox.thea.codes |
| `mutmut` | Mutation testing | https://mutmut.readthedocs.io |
| `hypothesis` | Property-based testing | https://hypothesis.readthedocs.io |
| `freezegun` / `time-machine` | Mock `datetime` | https://github.com/spulec/freezegun / https://github.com/adamchainz/time-machine |
| `responses` / `respx` | HTTP mocking (sync/async) | https://github.com/getsentry/responses / https://lundberg.github.io/respx/ |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — matrix Python versions, sharding, `actions/cache` | Standard CI |
| GitLab CI | SaaS/self-host | Yes | Same patterns |
| CircleCI | SaaS | Yes — orbs for pytest + xdist | Smaller share but solid |
| Codecov | SaaS | Yes — `codecov-action` | PR coverage diff |
| Coveralls | SaaS | Yes — `coveralls` CLI | Alt to Codecov |
| Sonar / SonarCloud | SaaS | Yes — reads `coverage.xml` + ruff/mypy reports | Quality gate aggregator |
| pre-commit.ci | SaaS | Yes — autorun pre-commit | Free for OSS |
| Datadog CI Visibility | SaaS | Yes — agent | Flaky test surface area + duration trends |
| Sentry CI Capture | SaaS | Yes — agent | Capture exceptions per test |
| Allure | OSS | Yes — `allure-pytest` | Rich HTML reports |
| ReportPortal | OSS | Yes — REST | AI-driven flake analytics |
| Testcontainers | OSS | Yes — Python API | Real Postgres/Redis/Kafka in tests |
| LocalStack | OSS | Yes — REST/CLI | AWS mocks for boto3 tests |
| WireMock / MockServer | OSS | Yes — REST | External HTTP mocks |
| Renovate / Dependabot | SaaS | Yes — `pyproject.toml` aware | Auto-PR plugin upgrades |

## Templates & scripts

See methodology `templates.md` for full `pyproject.toml`, `conftest.py`, GH Actions. Inline minimal `pyproject.toml` block (≤25 lines):

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
  "-ra", "--strict-markers", "--strict-config",
  "--cov", "--cov-report=term-missing", "--cov-fail-under=80",
  "--durations=15",
]
markers = [
  "slow: tests >1s; run with -m slow",
  "integration: hits real services; not in default run",
  "smoke: must run on every commit",
]
filterwarnings = ["error", "ignore::DeprecationWarning:botocore.*"]
```

Inline `tests/conftest.py` skeleton (≤30 lines):

```python
import pytest

@pytest.fixture(scope="session")
def app_settings():
    """Resolved settings for the test session."""
    from myapp.config import Settings
    return Settings(env="test")

@pytest.fixture
def freeze_time():
    """Function-scoped time freeze; opt-in via fixture name."""
    from time_machine import travel
    with travel("2026-01-01T00:00:00Z", tick=False) as t:
        yield t

@pytest.fixture
def http_responses():
    """Context manager seam for `responses`-style HTTP mocks."""
    import responses as _r
    with _r.RequestsMock(assert_all_requests_are_fired=True) as rm:
        yield rm
```

Diff-scoped CI runner (≤20 lines):

```bash
#!/usr/bin/env bash
# pytest-diff.sh — run only tests for files changed vs main.
set -euo pipefail
mapfile -t files < <(git diff --name-only --diff-filter=ACMR origin/main...HEAD -- '*.py')
[[ ${#files[@]} -eq 0 ]] && { echo "no python diff"; exit 0; }
mapfile -t mods < <(printf '%s\n' "${files[@]}" | sed -nE 's#^src/(.+)\.py$#\1#p' | tr / .)
ARGS=()
for m in "${mods[@]}"; do ARGS+=("--cov=$m"); done
pytest "${ARGS[@]}" --cov-report=term-missing -q
```

## Best practices

- **`--strict-markers --strict-config`** in CI. Typos in marker names or config keys must fail.
- **`filterwarnings = ["error"]`** so deprecations become test failures; whitelist narrowly.
- **Function scope by default**; broaden only when setup is expensive *and* immutable.
- **No `autouse=True`** unless universally applicable to the entire file/dir; document each instance in conftest.
- **Parametrize, don't loop**: `@pytest.mark.parametrize("a,b,exp", [...])` — each parameter set is a separate test ID.
- **Pin pytest and plugin versions** in `pyproject.toml`. Plugin minor releases (`pytest-asyncio`) regularly break suites.
- **Run `pytest-randomly`** in CI; only suppress with explicit cause comment when ordering is required.
- **Use `pytest -p no:cacheprovider`** for one-off debugging when `--lf` lies.
- **`--durations=15`** routinely; act on the top 15 every release.
- **Coverage threshold per file**, not global; prevents gaming.
- **Mock at the boundary**, not deep inside (`mocker.patch('mypkg.http_client.get')`, not `socket.socket`).
- **Use `monkeypatch` for env vars / attributes**, `mocker.patch` for callables; don't mix.
- **`tmp_path` over `/tmp`**; auto-clean, parallel-safe.
- **Tag external/integration tests** with markers and exclude from default run; CI has explicit jobs for them.
- **Migrate `unittest` to pytest gradually**: stop adding new `TestCase` subclasses; convert leaf tests first.

## AI-agent gotchas

- **Agents add `autouse=True`** to "make a mock global" — silently breaks isolation. Reject in review.
- **Mocking too deep.** Agents patch `socket.socket` instead of `requests.get`; tests pass but are meaningless. Patch the boundary.
- **Returning from tests**. Agents converting from unittest leave `return self.assertEqual(...)`; pytest 8.4 fails. Strip returns.
- **`pytest-asyncio` mode mismatch.** `asyncio_mode = "auto"` vs explicit `@pytest.mark.asyncio` collide; pick one and document.
- **Test IDs from parametrize collide**. Agents use a Faker-generated value as a parametrize argument; IDs differ each run, breaking `--lf`. Use static IDs.
- **`mocker.patch.object`** scope is the test function; agents that try to make it module-scoped fail. Use a fixture with `with` block.
- **`tmp_path` shared across xdist workers** if escalated to session scope. Always keep at function scope or use `tmp_path_factory` properly.
- **`assert mock_x.called`** without `assert_called_with(...)` lets wrong-arg bugs slip. Force argument assertions in review.
- **`@pytest.mark.skip`** sneaking in for "broken later" tests with no ticket. Prefer `xfail(reason=...)` and a TODO link.
- **Coverage cliffs.** Agents add tests that touch a 50-line function once; coverage rises but assertions are weak. Combine with mutation testing.
- **Plugin install but not enabled.** Agents `pip install pytest-cov` and forget to add `--cov` to addopts; coverage stays at 0%.
- **Strict markers off**. Agents typo `@pytest.mark.intergation`; without strict markers it silently registers as a no-op. Strict mode catches it.
- **`monkeypatch.setenv` vs `os.environ`** — direct `os.environ` writes leak across tests. Force `monkeypatch.setenv`.
- **`pytest --pdb` leaks credentials** when CI logs are public; agents add it for "easier debugging". Reject in CI configs.
- **Long async tests without `pytest-timeout`** hang CI when an `await` deadlocks. Set a default timeout.

## References

- Methodology README: `./README.md`
- pytest docs: https://docs.pytest.org
- pytest fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
- pytest markers: https://docs.pytest.org/en/stable/example/markers.html
- pytest 8.0 release: https://docs.pytest.org/en/stable/announce/release-8.0.0.html
- pytest 8.4 release: https://docs.pytest.org/en/stable/announce/release-8.4.0.html
- pytest-cov: https://pytest-cov.readthedocs.io
- pytest-xdist: https://pytest-xdist.readthedocs.io
- pytest-asyncio: https://pytest-asyncio.readthedocs.io
- pytest-mock: https://github.com/pytest-dev/pytest-mock
- pytest-randomly: https://github.com/pytest-dev/pytest-randomly
- pytest-django: https://pytest-django.readthedocs.io
- Hypothesis (property-based testing): https://hypothesis.readthedocs.io
- mutmut: https://mutmut.readthedocs.io
- Real Python pytest guide: https://realpython.com/pytest-python-testing/
- pytest-with-eric: https://pytest-with-eric.com/
- Codecov: https://about.codecov.io
- Allure: https://docs.qameta.io/allure/
- ReportPortal: https://reportportal.io/
