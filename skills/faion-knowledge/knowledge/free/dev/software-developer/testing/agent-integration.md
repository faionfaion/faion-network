# Agent Integration — Testing (cross-language)

## When to use
- A task whose acceptance criteria include "tests pass" — the agent must write or update tests as part of the implementation, not as an afterthought.
- Cross-language repos (Python services + JS frontend + Go workers) where one orchestrating agent needs language-specific testing patterns.
- Establishing a coverage floor (`fail_under = 80`) and wiring it into CI so PRs from agents block on regressions.
- Bootstrapping a new repo with the canonical pytest/jest/vitest/playwright config in one shot.

## When NOT to use
- One-off scripts and notebooks that are inherently exploratory (a few asserts in the script itself are enough).
- Pure infra-as-code (terraform/k8s manifests) where the test signal is `plan`/`apply` outcome, not unit testing.
- When the codebase has no testable seams (god objects, no DI, untyped globals) — fix that first; tests bolted on top become brittle and an agent will spend tokens chasing them.
- Visual regression flows — defer to Playwright screenshot diffs / Percy / Chromatic, not unit-test frameworks.

## Where it fails / limitations
- pytest fixtures with `@pytest.fixture(scope="session")` + `db` fixture from pytest-django frequently leak state across tests when an agent autogenerates them; one bad fixture corrupts an entire test session.
- pytest-asyncio with `asyncio_mode = "auto"` + sync fixtures cause hangs that look like infinite test runs to an agent watching stdout.
- Coverage tools miss code reachable only via subprocesses or Celery workers; agents over-trust 100% coverage badges.
- Mocking the wrong layer (mocking `requests.get` when the code uses `httpx.AsyncClient`) is the #1 LLM mistake — tests "pass" but exercise nothing.
- Flaky tests get re-run by the agent, which masks real concurrency/race bugs.

## Agentic workflow
A planning subagent reads the spec/test-plan, enumerates acceptance criteria, and emits a list of `test_*` IDs with one-line behaviors. An implementation subagent writes both code and tests. A test-runner subagent executes the suite, parses output (pytest's `--junitxml` is parser-friendly), and feeds failures back. Pre-commit hooks run a fast subset; full suite runs in CI. The orchestrator never marks a task done until red-green-refactor cycles complete and coverage ≥ floor.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the task lifecycle, gates on test pass.
- `faion-feature-executor` — sequential task runner with quality gates including test validation.
- A purpose-built `test-writer` subagent — given a function signature + docstring, produces parametrized pytest cases (or jest/vitest cases for JS).
- A `flaky-detector` subagent — re-runs the suite N times, identifies tests with non-deterministic outcomes.

### Prompt pattern
```
For each public function in <module>, list 3-7 test cases:
  - happy path
  - boundary values
  - invalid inputs / errors
  - empty / null / zero
  - one rare edge case
Format: test name, inputs, expected outcome.
```
```
Run `pytest --junitxml=/tmp/r.xml -q -p no:cacheprovider`. Parse failures.
For each failure, return: test name, assertion line, actual, expected,
likely root cause (code bug / test bug / fixture bug / flake).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Python test runner | `pip install pytest` · https://docs.pytest.org/ |
| `pytest-cov` | Coverage with branch tracking | `pip install pytest-cov` |
| `pytest-xdist` | Parallel runs (`-n auto`) | `pip install pytest-xdist` |
| `pytest-mock` | `mocker` fixture wrapping unittest.mock | `pip install pytest-mock` |
| `pytest-asyncio` | Async test support | `pip install pytest-asyncio` |
| `hypothesis` | Property-based fuzzing | `pip install hypothesis` |
| `jest` / `vitest` | JS unit runners | `npm i -D vitest` · https://vitest.dev/ |
| `playwright` / `cypress` | Browser E2E | `npm i -D @playwright/test` |
| `go test` | Go built-in | `go test ./...` |
| `cargo test` / `cargo nextest` | Rust runners | `cargo install cargo-nextest` |
| `mutmut` / `cosmic-ray` | Mutation testing for Python | `pip install mutmut` |
| `stryker` | Mutation testing for JS/TS | `npm i -D @stryker-mutator/core` |
| `coverage` | Standalone Python coverage | `pip install coverage` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Codecov | SaaS | Yes | Upload coverage XML; PR-comment integration. |
| Coveralls | SaaS | Yes | Same niche, simpler config. |
| GitHub Actions / GitLab CI | SaaS | Yes | Native test runners; matrix across versions. |
| BuildKite / CircleCI | SaaS | Yes | Parallelized test sharding via API. |
| Allure / ReportPortal | OSS | Partial | Rich test reports; agents can post results via REST. |
| Sentry | SaaS | Yes | Test-failure → issue mapping in production. |

## Templates & scripts
See `templates.md` for pytest/jest/Playwright configs. Minimal CI agent script:

```bash
#!/usr/bin/env bash
# run-tests.sh — language-agnostic dispatcher
set -euo pipefail
if [ -f pyproject.toml ]; then
  poetry run pytest --junitxml=test-results.xml \
    --cov=src --cov-report=xml --cov-fail-under=80 -q
elif [ -f package.json ]; then
  if grep -q '"vitest"' package.json; then npx vitest run --coverage
  else npx jest --ci --coverage --coverageThreshold='{"global":{"lines":80}}'
  fi
elif [ -f go.mod ]; then
  go test -race -coverprofile=cover.out ./... \
    && go tool cover -func=cover.out | tail -1
elif [ -f Cargo.toml ]; then
  cargo nextest run --no-fail-fast
else
  echo "no recognized stack" >&2; exit 2
fi
```

## Best practices
- Test naming: `test_<unit>_<condition>_<expected>` so an agent reading failure logs immediately understands intent.
- One logical assertion per test (multiple `assert` lines OK if they describe one outcome).
- Use factories (`factory_boy` / `pytest-factoryboy` / `@faker-js/faker`) over hand-built fixtures — agents can extend factories without re-reading the schema.
- Mark slow tests (`@pytest.mark.slow`) and split CI: fast suite on every push, full suite nightly.
- Always set `--strict-markers` and `--strict-config` so unknown markers fail loudly — prevents typo'd `@pytest.mark.skip` patterns.
- Coverage with branch (`branch = true` for Python, `--coverage --coverage-reporter=lcov` for JS); line coverage alone hides untested branches.
- For async code, always provide an event loop fixture; never let pytest-asyncio guess.
- For DB tests, use transactional rollback (`pytest-django`'s `db` fixture) instead of teardown queries — orders of magnitude faster.
- Fail-fast off in CI (`pytest --maxfail=0`) so the agent sees all failures in one pass; fail-fast on in pre-commit (one test = one fix iteration).

## AI-agent gotchas
- LLMs love testing implementation details (mock the function the code calls and assert it was called) instead of behavior. Prompt: "Test outcomes, not call sequences. Mock only at I/O boundaries."
- LLM-generated tests almost always re-import the function under test inside the test file, then mock the wrong path (`from foo.bar import baz` mocks `tests.test_foo.baz` not `foo.bar.baz`). Pin patch targets to the module under test, not the test file.
- An agent re-running a flaky test until it passes hides race conditions. Configure `pytest --reruns 0` in CI; only allow reruns in a separate "flake repair" agent loop.
- pytest's collection silently skips files that error during import. An agent looking at "0 failures" must also check "0 errors" and "X collected" — otherwise broken tests appear green.
- `--cov-fail-under` must be set per-module for large repos; a single global threshold lets new code drift down.
- LLM-generated parametrize lists frequently duplicate cases or omit the boundary the bug actually lives at. Prompt for boundary values explicitly (-1, 0, 1, max, max+1, None, "").
- Snapshot tests (jest `toMatchSnapshot`) accumulate stale snapshots when an agent re-runs with `-u`. Block `--ci -u` combinations in pre-commit.
- Mutation testing budget: an agent running `mutmut run` on a large repo can spend 10k+ tokens on output. Run mutation tests on changed files only.

## References
- https://docs.pytest.org/en/latest/ — pytest reference
- https://pytest-cov.readthedocs.io/ — coverage plugin
- https://hypothesis.readthedocs.io/ — property-based testing
- https://vitest.dev/ — vitest (Vite-native)
- https://playwright.dev/docs/test-intro — Playwright tests
- https://martinfowler.com/articles/practical-test-pyramid.html — Fowler on test pyramid
- https://testing.googleblog.com/ — Google testing blog (real-world failure patterns)
