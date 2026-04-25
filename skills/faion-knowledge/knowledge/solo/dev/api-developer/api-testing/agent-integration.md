# Agent Integration — API Testing

## When to use
- Any HTTP/gRPC/GraphQL service heading toward production. The pyramid (unit → integration → contract → e2e) applies.
- Cross-team interfaces where consumer + provider deploy independently — contract tests (Pact / Spring Cloud Contract / pact-broker) catch drift.
- API published with an OpenAPI / GraphQL / Protobuf spec — automatic spec-conformance tests close the spec/code gap.
- Public SaaS API where SLA includes correctness + behavior (rate limit, idempotency, error shape).
- Refactor / version bump — regression suite is the safety net.

## When NOT to use
- Throwaway prototype. Smoke test with curl, ship.
- When the test costs more to maintain than the bug it would catch (low-traffic admin endpoint with no consumers).
- Replacing static type checks with runtime tests — let TypeScript / mypy / pydantic catch what they can.
- 100%-coverage cargo cult — coverage is a leading indicator, not a goal.

## Where it fails / limitations
- Slow integration suites (real DB, real external APIs) become the thing nobody runs locally → tests rot.
- Flaky tests caused by time, randomness, network, or shared state poison the signal. One flake destroys trust in 100 green runs.
- Mocks drift from reality: tests pass, prod breaks. Contract tests + spec validation guard against this.
- E2E suites against staging are quickly invalidated by data resets / shared environments.
- Test data setup is often longer than the assertion → people copy-paste and tests diverge. Use factories/fixtures.
- Auth + rate-limit + idempotency interactions are easy to forget — most bug reports are in this combinatorial gap.
- LLM-generated tests often assert what the code does, not what the spec requires — they "pass" while hiding bugs.

## Agentic workflow
Drive tests from the spec, not from the implementation. The agent reads the OpenAPI / GraphQL schema, generates positive + negative cases per operation (auth, validation, rate-limit, idempotency), runs them, then proposes contract pacts for downstream consumers. SDD gate enforces spec-conformance + at least one negative test per endpoint. For external APIs, agents record HTTP cassettes (VCR / pytest-recording) so re-runs are deterministic offline.

### Recommended subagents
- `faion-feature-executor` — sequence: read spec → generate cases → run → record cassettes → commit.
- `faion-sdd-execution` — quality gate enforcing happy + 401 + 403 + 422 + 429 cases per endpoint.
- A `contract-tester` agent (Sonnet) — wires Pact consumer + provider verification into CI.
- A `flake-detective` agent (Sonnet) — runs the suite N times, classifies failures, proposes deterministic fixes.

### Prompt pattern
```
Read openapi.yaml. For each operation in tags=[users, orders], generate a
pytest function in tests/contract/test_<resource>.py that asserts:
  - 200/201 happy path with example payload from spec
  - 401 when Authorization missing
  - 403 when role lacks scope (use fixture `low_priv_token`)
  - 422 with malformed body (drop one required field)
  - 429 after 11 calls in 1s (rate limit)
Use openapi-core for response-schema validation. Do not invent endpoints.
Output: unified diff only.
```

```
Run `pytest -p no:randomly --reruns 3 -q tests/integration` 5 times.
Identify any test that failed at least once. Output a table:
test_id | failure_count | suspected_cause | proposed_fix.
Do NOT modify tests, only diagnose.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `schemathesis` | Property-based testing of OpenAPI/GraphQL APIs | `pip install schemathesis` |
| `dredd` | OpenAPI conformance | `npm i -g dredd` |
| `pact-broker` / `pact-cli` | Contract test broker + verifier | docs.pact.io |
| `newman` | Postman collection runner for CI | `npm i -g newman` |
| `hurl` | Plain-text HTTP test files, fast in CI | `brew install hurl` |
| `bruno` | Open-source Postman alternative, file-based | usebruno.com |
| `k6` | Load + functional checks | k6.io |
| `mockoon-cli` | Mock servers from JSON config | `npm i -g @mockoon/cli` |
| `prism` | OpenAPI mock + proxy with validation | `npm i -g @stoplight/prism-cli` |
| `httpx` (CLI) | Async test client | `pip install httpx[cli]` |
| `vcrpy` / `pytest-recording` | Record/replay HTTP cassettes | `pip install pytest-recording` |
| `restqa` | YAML-driven API tests | `npm i -g @restqa/restqa` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| PactFlow | SaaS | Yes — REST API | Hosted Pact broker + can-i-deploy |
| Postman / Newman | SaaS + CLI | Yes — collection JSON | Best for partner-shareable suites |
| ReadyAPI / SoapUI | Commercial | Partial | Legacy SOAP + REST |
| 42Crunch | SaaS | Yes — CI plugin | OpenAPI security audit + conformance |
| Assertible | SaaS | Yes — REST API | Scheduled + post-deploy API checks |
| Checkly | SaaS | Yes — `checkly` CLI, IaC | Synthetic monitoring + Playwright |
| RunScope (BlazeMeter API) | SaaS | Yes — REST | Multi-region API tests |
| WireMock Cloud | SaaS + OSS | Yes — JSON config | Mock external APIs |
| Stoplight Prism | OSS | Yes | OpenAPI mock + validating proxy |

## Templates & scripts
See `templates.md` for pytest fixtures (auth, db, factories) and `examples.md` for Pact + OpenAPI conformance.

Schemathesis fuzz against a running app (CI gate):

```bash
#!/usr/bin/env bash
set -euo pipefail
APP=${1:?usage: $0 http://localhost:8000}
schemathesis run "$APP/openapi.json" \
  --checks all \
  --hypothesis-max-examples=50 \
  --workers 4 \
  --header "Authorization: Bearer $TEST_TOKEN" \
  --junit-xml=reports/schemathesis.xml
```

## Best practices
- Pyramid: many unit tests (pure logic), some integration (DB + service), few contract (consumer-driven), fewest e2e.
- Negative cases are required, not nice-to-have. Per endpoint: missing auth, wrong role, malformed body, missing required field, rate limit, idempotency.
- Validate every response against the OpenAPI / GraphQL schema with a generic assertion — it catches drift agents introduce.
- Test data via factories (`factory_boy`, `polyfactory`, `fishery`) — never inline literals in 50 tests.
- Reset DB between tests with transactions or per-test schemas; never with `truncate` (slow + masks order bugs).
- Tag tests by tier; CI runs unit on every push, integration on PR, e2e nightly + pre-deploy.
- Record + replay cassettes for tests that hit third-party APIs. Re-record on schedule, diff for surprises.
- Idempotency: every POST that allows retries must be tested with two identical calls + Idempotency-Key.
- Rate limit tests use a knob to lower the limit in test config; do not actually hit prod limits.
- Property-based tests (Hypothesis, Schemathesis) find inputs you didn't think of — run on the spec.

## AI-agent gotchas
- Agents write tests that mirror current behavior, not the spec. Result: refactors look safe, regressions slip. Force prompt: "assert against openapi.yaml, not implementation".
- Generated tests pile up `time.sleep(1)` waits → slow + flaky. Replace with explicit polling + timeout helpers.
- LLMs love `assert response.status_code == 200`. Require also `validate_response(spec, response)` and at least one body field assertion.
- Contract tests get out of date because nobody re-runs verification. Wire `pact verify --provider` into the provider's CI; broken contract = build red.
- Mocks invented by an agent often disagree with the real API. Prefer cassette-replay over hand-coded mocks for third-party APIs.
- An agent fixing a flake by retrying hides root cause. Quality gate: any test marked `@flaky` or with `--reruns` >0 needs a JIRA/issue link.
- Test data with hardcoded `user_id="1"` collides across test runs. Lint for hardcoded primary keys, force fixtures.
- Agents copy production secrets into test config. Run secret-scan on test files too — they often skip linting in `tests/`.
- E2E suites driven by an agent over staging will mutate shared data. Insist on per-run namespacing (org_id derived from PR number) or ephemeral envs.

## References
- https://martinfowler.com/articles/practical-test-pyramid.html
- https://docs.pact.io/
- https://schemathesis.readthedocs.io/
- https://hypothesis.readthedocs.io/
- https://owasp.org/www-project-api-security/
- https://stoplight.io/api-types/openapi/conformance-testing
- https://openapi-core.readthedocs.io/
- https://docs.pytest.org/en/stable/how-to/fixtures.html
