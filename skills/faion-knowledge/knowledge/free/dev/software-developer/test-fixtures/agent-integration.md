# Agent Integration — Test Fixtures

## When to use
- Test suites where setup boilerplate has crept past 30% of test code — fixtures consolidate it without sacrificing isolation.
- Multi-language repos where shared test data shape (User, Order, Product) recurs across dozens of test files.
- Integration / E2E tests that need a seeded DB, an authenticated session, or a third-party stub server.
- Property-based testing (`hypothesis`, `proptest`, `fast-check`) where you wrap arbitrary instances in factories with sensible defaults.
- Agent-written tests — fixtures + factories prevent LLMs from inventing inconsistent test data on every spec.

## When NOT to use
- One-off test files where two literal objects are clearer than a factory abstraction.
- When a fixture would hide the actual scenario under test (the "magic constant" anti-pattern). Inline if specificity matters.
- Production-style mocks pretending to be fixtures — keep the mocking layer separate (use `mocking-strategies` methodology).
- Snapshot tests where the "fixture" is the snapshot file — different concern.

## Where it fails / limitations
- **Scope leakage.** `scope="module"` fixtures with mutable state cause cross-test pollution. Symptom: tests pass alone, fail in suite. Default to `function` scope until perf forces wider.
- **Yield + cleanup race.** A `yield`-style fixture's cleanup runs in `finally`; if the test panics during teardown, cleanup raises a second exception that masks the original.
- **Factory drift.** `make_user()` defaults change → 200 tests' implicit assumptions silently change. Pin defaults in a single source of truth and force keyword-only overrides.
- **Fixture coupling to ORM.** `db_session` fixture tied to SQLAlchemy → moving to async breaks every fixture transitively.
- **Lazy fixture loading mismatch.** pytest's autouse fixtures evaluated per-test; fixture cost balloons. Mark expensive fixtures `scope="session"` only when truly read-only.
- **Faker non-determinism.** `faker.email()` produces different values each run → snapshot tests flake. Seed faker once per run (`Faker.seed(42)`).
- **Cleanup order.** Pytest reverses fixture finalizers; cross-fixture dependencies that share resources need explicit ordering or `request.addfinalizer`.
- **Parallel test runners (pytest-xdist).** Module-scope fixtures rebuild per worker; agents assume "session" means cross-process.

## Agentic workflow
Drive fixture work in 3 stages: (1) a **fixture-extractor** subagent reads test files and identifies setup repeated >2 times → proposes a `conftest.py` fixture or factory; (2) a **factory-author** subagent writes a builder/factory function with keyword-only overrides and explicit defaults; (3) a **scope-tuner** subagent profiles test runtime (`pytest --durations=20`) and proposes scope upgrades only when fixture state is provably immutable. Always run the full suite after fixture changes (cross-test pollution is the dominant failure mode); compare `--collect-only` before/after to ensure no test silently dropped.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate ensures `pytest -p no:cacheprovider --maxfail=1 -q` passes after fixture refactor.
- A purpose-built **fixture-extractor-agent** (worth creating): given a test file, lists candidate fixtures + scope recommendation + impact analysis (which other tests benefit).
- A **factory-bot-agent** (worth creating): converts ad-hoc test object literals into factory_boy/factory-bot/Faker-based factories with traits.
- A **flaky-fixture-agent** (worth creating): runs test in random order (`pytest-randomly`) to detect fixture state leakage; reports the offending fixture + read/write log.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub seed data files (JSON/YAML/SQL) committed alongside fixtures.

### Prompt pattern
Pytest fixture extraction:
```
Read tests/test_orders.py. Identify setup repeated in ≥2 tests.
For each, propose a pytest fixture in tests/conftest.py with:
- name (snake_case)
- scope (function/module/session) + justification
- yield-based cleanup if any resource is acquired
- factory variant if N tests need overrides
Output as a single conftest.py diff. Do NOT change test bodies
yet — separate task.
```

Factory authoring:
```
Generate factory_boy factories for User, Order, OrderItem in
tests/factories.py.
- Use SubFactory for relations
- Use FuzzyChoice / Faker for fields
- Seed Faker(42) at module scope
- Provide traits: PaidOrder, RefundedOrder
- Default email: f"user{n}@example.com" (sequence) — NOT random
  (snapshot stability)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` | Fixture-aware Python runner | https://docs.pytest.org |
| `pytest-randomly` | Detect order-dependent fixtures | `pip install pytest-randomly` |
| `pytest-xdist` | Parallel runs; surfaces fixture scope bugs | `pip install pytest-xdist` |
| `factory_boy` | Python factories | https://factoryboy.readthedocs.io |
| `Faker` | Fake data generator (Python, JS) | https://faker.readthedocs.io |
| `factory-bot` | Ruby factories | https://github.com/thoughtbot/factory_bot |
| `fishery` | TypeScript factories | https://github.com/thoughtbot/fishery |
| `@faker-js/faker` | TS/JS fake data | https://fakerjs.dev |
| `freezegun` | Freeze time inside fixtures | https://github.com/spulec/freezegun |
| `responses` / `respx` / `nock` / `wiremock` | HTTP fixture servers | https://github.com/getsentry/responses |
| `pytest-postgresql` / `testcontainers` | DB fixtures with real Postgres | https://github.com/ClearcodeHQ/pytest-postgresql |
| `vcr.py` / `polly.js` | Record/replay HTTP for fixture replay | https://vcrpy.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mockaroo | SaaS | yes (REST API) | Generate large fixture datasets in CSV/JSON; agent can post schema and pull file. |
| Mockoon | OSS | yes (CLI) | Local fixture API server; spec via JSON, no UI required. |
| Beeceptor / RequestBin | SaaS | yes | Capture real third-party responses for fixture replay. |
| WireMock Cloud | SaaS | yes | Hosted fixture server with API for stub mgmt. |
| Localstack | OSS | yes | AWS-compatible fixtures for S3/SQS/DynamoDB tests. |
| Stripe / Twilio test modes | SaaS | yes | Sandbox tenants with fixture cards/numbers; deterministic. |
| Mirage JS / MSW | OSS | yes | In-process fixture servers for browser/Node tests. |

## Templates & scripts
See `templates.md` and `examples.md` for pytest fixtures, factory_boy patterns, fishery setup. Add a fixture-pollution detector (≤50 lines):

```bash
#!/usr/bin/env bash
# fixture-pollution-check.sh — detect order-dependent tests.
# Usage: fixture-pollution-check.sh [PYTEST_ARGS...]
set -euo pipefail
RUNS="${RUNS:-3}"
SEEDS=()
PASS_FIRST=true
for i in $(seq 1 "$RUNS"); do
  S=$RANDOM
  SEEDS+=("$S")
  echo "=== run $i seed=$S ==="
  if pytest -p randomly --randomly-seed="$S" -q "$@" >".pytest-pollution-$i.log" 2>&1; then
    echo "  OK"
  else
    echo "  FAIL"
    PASS_FIRST=false
    grep -E "FAILED|ERROR" ".pytest-pollution-$i.log" | head -20
  fi
done
if ! $PASS_FIRST; then
  echo "Order-dependent failures detected. Seeds: ${SEEDS[*]}"
  echo "Reproduce locally: pytest -p randomly --randomly-seed=<seed>"
  exit 1
fi
echo "OK — no order dependency in $RUNS runs"
```

Run before merging fixture changes.

## Best practices
- **`conftest.py` per test directory layer.** Project-wide in `tests/conftest.py`; module-specific in `tests/users/conftest.py`. Don't dump everything in root.
- **Fixtures yield, factories return.** Resources that need cleanup → `yield` + cleanup. Pure data → factory function.
- **Keyword-only overrides** in factories. `def make_user(*, email=None, role="user")` prevents positional drift over time.
- **Sequenced determinism by default.** `factory.Sequence(lambda n: f"user{n}@example.com")` over `Faker('email')` for snapshot stability; opt into Faker per-field.
- **`scope="function"` is the safe default.** Move to broader scope only with profiling proof + immutability check.
- **Tear down in reverse acquisition order.** pytest does this automatically; in JS land (`beforeAll`/`afterAll`) wire it manually.
- **Truncate, don't drop, between integration tests.** `TRUNCATE` is 10x faster than `DROP/CREATE`; preserve schema cache.
- **Real DB > in-memory** for integration. SQLite-in-place-of-Postgres lies about types; use `testcontainers` for the real thing.
- **Freeze time when asserting timestamps.** `freezegun` (Py), `@sinonjs/fake-timers` (JS), `testing-time` (Go) — never assert `now()` ranges.
- **Fixtures are public API.** Document them like real code; agents copy patterns.

## AI-agent gotchas
- **Inventing fixture data inline.** LLM writes `User(id="abc", email="a@b.com")` instead of using `user_factory()`. Force prompt: "Use existing factories from tests/factories.py only."
- **Wrong scope.** Agent marks `scope="session"` because it "looks like setup", forgets the fixture mutates DB. Fixture pollution surfaces 50 tests later.
- **Yield-based fixture without `try/finally`.** Test exception during use → resource leaked. Always wrap.
- **`autouse=True` cascade.** Adding one autouse fixture forces every test to pay for it; agents underestimate cost on large suites.
- **Faker without seed.** Snapshot tests flake on next run. Seed once in `conftest.py` `pytest_configure(config)`.
- **Reusing fixture across processes.** With `pytest-xdist`, `scope="session"` runs once per worker, not once globally. Cross-worker shared state must be process-safe.
- **Mock-as-fixture confusion.** Agent puts `Mock(spec=Service)` in `conftest.py` and reuses it across tests; `assert_called_with` accumulates calls → false positives next test.
- **Deepcopy missing.** Returning shared mutable list from a factory; one test mutates it; next test sees mutation. Either return a fresh list or deep-copy on call.
- **DB cleanup via SQLAlchemy `session.rollback()` only.** Connection-level uncommitted writes leak across tests under `expire_on_commit=False`. Use `TRUNCATE` after rollback for surety.
- **Path-style fixtures (`tmp_path` vs `tmp_path_factory`).** Agent uses `tmp_path` at session scope → unsupported, opaque error. Force `tmp_path_factory.mktemp(...)`.
- **Re-using HTTP responses recordings (`vcr.py`)** that captured auth tokens; tokens leak in fixtures committed to repo. Scrub before commit.
- **Dependency injection for clocks.** Agent forgets to wire the test clock into the SUT; `datetime.now()` still real. Always inject `Clock` or freeze globally.
- **factory_boy `lazy_attribute` evaluated once.** Agent expects `lazy_attribute(lambda o: now())` to refresh per build — no, only once per declaration. Use `LazyFunction(now)`.

## References
- pytest fixtures reference: https://docs.pytest.org/en/stable/fixture.html
- factory_boy docs: https://factoryboy.readthedocs.io
- Faker docs: https://faker.readthedocs.io
- factory-bot (Ruby): https://github.com/thoughtbot/factory_bot
- fishery (TS): https://github.com/thoughtbot/fishery
- pytest-randomly: https://github.com/pytest-dev/pytest-randomly
- testcontainers-python: https://testcontainers-python.readthedocs.io
- Martin Fowler — Object Mother / Test Data Builder: https://martinfowler.com/bliki/ObjectMother.html
- Sibling methodologies: `free/dev/software-developer/mocking-strategies/`, `free/dev/software-developer/integration-testing/`, `free/dev/software-developer/unit-testing/`.
