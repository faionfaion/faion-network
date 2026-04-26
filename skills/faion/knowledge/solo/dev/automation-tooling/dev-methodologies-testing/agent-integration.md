# Agent Integration — Dev Methodologies: Testing

## When to use
- Bootstrapping a test suite in a new service across Python/JS/Ruby/Java/C#/Rust — pick the matching framework template and let the agent scaffold.
- Filling coverage holes on an existing module — feed source + this reference and ask for unit/integration tests in the project's idiom.
- Standardising test style across a polyglot monorepo (one team, many stacks) where engineers keep reinventing layouts.
- Producing first-cut tests during SDD `in-progress/` so review focuses on logic, not boilerplate.

## When NOT to use
- Performance / load testing — see `perf-test-basics`, `perf-test-tools`.
- Browser E2E — see `playwright-automation` / `puppeteer-automation`.
- Specifying *what* to test (acceptance criteria) — that belongs in `test-plan.md` of an SDD feature, not in this reference.
- When the project already has a strong test convention (ARRANGE-ACT-ASSERT macros, custom factories) — agent will drift into the generic style here and create churn.

## Where it fails / limitations
- Each language section is a single canonical example, not a decision matrix — agents may pick `pytest` over `unittest` or `RSpec` over `Minitest` even when the project standard is the latter. Always pin the framework in the prompt.
- Generated tests look correct but assert on shape, not behaviour (`assert result.is_active is True` patterns) — humans must add edge/error cases.
- No flakiness guidance: timeouts, retries, isolation between tests are absent. Agents tend to write order-dependent suites unless told otherwise.
- Mocking strategy is implicit (Mock in C#, RSpec doubles in Ruby) — without explicit instruction, agents over-mock and tests stop catching regressions.
- Spring/.NET examples assume `@Autowired`/DI container exists; agents will scaffold that even when the codebase uses constructor injection only.

## Agentic workflow
Use this reference as a *style anchor*, not as a generator. Have the agent read the relevant language section + the project's existing test file as a few-shot, then produce one test class at a time. Run the resulting suite immediately (`pytest -x`, `vitest run`, `cargo test`) and feed failures back; do not let the agent move on until green. For multi-language repos, dispatch per-language subagents so each picks the correct idiom.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the spec→test→impl loop with quality gates; pair this reference with its `test-plan.md` step.
- Generic test-writer subagent (project-local) — instantiate per language with the README section pre-loaded.

### Prompt pattern
```
Project stack: Django 5 + pytest + factory_boy.
Existing style: see tests/test_orders.py.
Task: write tests for apps/billing/services/refund.py covering:
- happy path (full refund)
- partial refund with rounding
- idempotency on retry
- raises BillingError on closed period
Use @pytest.mark.django_db, parametrize where it removes duplication.
Run `pytest tests/billing -x` before returning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Python test runner | `pip install pytest pytest-django pytest-cov` · https://docs.pytest.org |
| `vitest` | Vite-native JS/TS runner | `npm i -D vitest` · https://vitest.dev |
| `jest` | JS/TS runner (legacy default) | `npm i -D jest @types/jest` |
| `@testing-library/react` | DOM-centric component tests | `npm i -D @testing-library/react @testing-library/jest-dom` |
| `rspec` | Ruby BDD runner | `bundle add rspec rspec-rails` |
| `phpunit` / `pest` | PHP runners (Laravel default Pest) | `composer require --dev pestphp/pest` |
| `mvn test` / `gradle test` + JUnit 5 | Java | `JUnit 5` + AssertJ |
| `dotnet test` + xUnit/Moq | .NET | `dotnet add package xunit Moq FluentAssertions` |
| `cargo test` + `tokio-test` | Rust sync/async | built-in; `cargo add --dev tokio-test` |
| `coverage.py` / `c8` / `tarpaulin` / `simplecov` | Coverage per language | language-specific |
| `mutmut` / `stryker-mutator` | Mutation testing | `pip install mutmut` / `npm i -D @stryker-mutator/core` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Codecov | SaaS | Yes — token + CI uploader | Coverage diff on PRs; agents can read the Codecov API to gate merges. |
| Coveralls | SaaS | Yes | Free tier for OSS; same niche as Codecov. |
| SonarQube / SonarCloud | SaaS + OSS | Yes — REST API | Quality gate on coverage + smells; pre-commit usable via `sonar-scanner`. |
| GitHub Actions | SaaS | Yes — first-class | Cache test runners (`actions/cache`), shard via matrices. |
| Buildkite / CircleCI | SaaS | Yes | Better for heavy parallel test matrices. |
| Testcontainers | OSS | Yes | Real DB/Redis/Kafka in tests; agents can spin them via `testcontainers-python`/`-node`. |
| Wiremock / MockServer | OSS | Yes | HTTP fakes for integration tests. |

## Templates & scripts
See `templates.md` for per-language scaffolds. Quick pytest fixture an agent can paste into `conftest.py` for Django + factories:

```python
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authed_client(db, api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user
```

## Best practices
- One assertion *concept* per test (not one `assert` statement) — name the test after the concept; agents naming `test_1`, `test_2` is a smell.
- Prefer pure functions + thin integration tests over deep mocks; mocks freeze refactors.
- Use factories (`factory_boy`, `factory-bot`, `bogus`) over fixtures for object graphs — fixtures rot, factories evolve with the model.
- Speed budget: unit < 50 ms, integration < 1 s, full unit suite < 60 s; if it grows, profile (`pytest --durations=20`).
- Fail loud on flaky tests: quarantine with a marker, don't `@pytest.mark.flaky` retry — that hides race conditions.
- Forbid network in unit tests via `pytest-socket` or equivalent; agents otherwise add live API calls.
- Snapshot tests are fine for serialisers but reviewable diffs only — never approve a 500-line snapshot blindly.

## AI-agent gotchas
- LLMs gravitate to `unittest.TestCase` even in pytest projects; explicitly say "use pytest function-style tests".
- Generated assertions often re-run the SUT in the assertion (`assert service.do() == service.do()`) — review for side-effect doubling.
- Agents reach for `Mock(spec=...)` after one failure and over-mock the whole call graph; cap mock depth in the prompt.
- TypeScript/Jest: agent forgets `import { describe, it, expect } from 'vitest'` when the project is on vitest, leading to silent global pollution.
- Spring tests: agent adds `@SpringBootTest` (full context) to everything, blowing test time. Force `@DataJpaTest` / `@WebMvcTest` slices.
- Rust async: agent mixes `#[test]` and `#[tokio::test]` — fails to compile silently when feature flags differ.
- Human-in-loop checkpoint: never let the agent edit production code to make a failing test pass without surfacing the diff — that's the core TDD failure mode for LLMs.
- Coverage as a goal, not a target: agents will write `assert True` tests to hit threshold; require mutation score, not just line coverage, on critical modules.

## References
- https://docs.pytest.org/en/stable/ — pytest
- https://testing-library.com/docs/ — Testing Library philosophy
- https://martinfowler.com/articles/practical-test-pyramid.html — test pyramid
- https://kentcdodds.com/blog/write-tests — "write fewer, longer tests"
- https://google.github.io/styleguide/pyguide.html#316-naming — test naming
- https://docs.rs/tokio-test — async testing in Rust
