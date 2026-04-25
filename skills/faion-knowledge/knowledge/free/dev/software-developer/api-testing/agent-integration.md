# Agent Integration — API Testing

## When to use
- New REST/GraphQL service: agents draft happy-path + error tests from the OpenAPI/JSON schema before implementation.
- Frontend ↔ backend contract is unstable across teams or repos — drive Pact consumer tests from the FE side, verify on BE.
- After every spec change to `openapi.yaml` / `schema.graphql` — regenerate validation tests so the agent catches drift.
- Building integration tests on top of `TestClient` / `httpx.AsyncClient` for a FastAPI/Django app.
- Adding negative tests (auth failures, validation errors, rate-limiting, idempotency keys) that the dev forgot.

## When NOT to use
- Pure unit-level logic that has no transport, schema, or external contract — use plain pytest/jest and skip Pact, schemathesis, OpenAPI validation.
- Greenfield prototypes where the contract changes hourly — investing in Pact pacts will create churn faster than value.
- Single-team, single-repo monoliths where an integration test (`TestClient`) already covers the same surface — adding contract tests is redundant.
- Pure browser flows (form clicks, redirects) — that's E2E (Playwright/Cypress), not API testing.
- Internal binary RPC where the schema is enforced by code generation; contract drift is impossible.

## Where it fails / limitations
- README's testing pyramid puts "Contract Tests" above "Unit Tests" — agents take this literally and over-invest in Pact for solo/internal services. Restate that contract tests only pay off across team or service boundaries.
- The Pact snippet uses `pactman` on the provider side; `pactman` is unmaintained — modern stacks use `pact-python` v2 or the Pact JVM/.NET providers. Agents will install the wrong package.
- README mixes `OpenAPI.from_file_path` (`openapi-core`) with FastAPI's auto-generated spec — but doesn't say to dump the *served* spec to disk. Agents will let the file go stale.
- The Postman collection example is fine for manual runs but agents try to drive Postman from CLI — they should use Newman (`newman run collection.json`).
- No mention of authentication test setup, JWT refresh, idempotency keys, retry semantics, or pagination — agents will skip these.
- "Test rate limiting behavior" is a one-liner with no method; agents need explicit guidance (`X-RateLimit-Remaining` header assertion, fixed-window vs token-bucket semantics).
- No discussion of test data isolation — agents reuse a single fixture user and tests start interfering once parallelism is enabled.

## Agentic workflow
Two-pass loop: (1) generation — an agent reads `openapi.json` (served by the running app) and emits one test module per resource with happy + 4xx + 5xx cases; (2) verification — a second agent runs `pytest`, parses failures, opens or updates a corresponding test (never the production code unless explicitly authorized). For contract tests, run consumer tests in CI, publish pacts to a Pact Broker, and have the provider pipeline `verify` against the latest tag. Always require a fresh `openapi.json` snapshot diff per PR — that diff IS the contract.

### Recommended subagents
- `faion-sdd-executor-agent` — picks up "add tests for endpoint X" SDD tasks; matches naturally to one-resource-per-task scope.
- `faion-feature-executor` — sequential gate: generate tests → run them → fix failing assertions or report broken contract.
- General-purpose subagent restricted to `tests/api/**` + `tests/contracts/**` only; deny writes to `app/`/`src/`.
- `password-scrubber-agent` — sweep test fixtures and `.env.test` for accidentally hardcoded tokens before commit.

### Prompt pattern
```
Stack: FastAPI + pytest + httpx.AsyncClient. Spec: ./openapi.json (served by app).
Generate tests/api/test_<resource>.py covering: 200 happy, 400 validation, 401 unauth,
403 forbidden, 404 not-found, 409 conflict where applicable, 429 if rate-limited.
Use `client` and `auth_headers` fixtures from conftest.py. No new fixtures.
Validate every response against the OpenAPI schema via openapi-core.
```

```
You are verifying contract drift. Run `pytest tests/contracts -q`.
On failure, do NOT modify production code. Print the consumer expectation,
the provider response, and the diff. Open a TODO note in tests/contracts/DRIFT.md.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytest` + `pytest-asyncio` | Test runner | https://docs.pytest.org/ |
| `httpx` (`AsyncClient`, `ASGITransport`) | In-process & out-of-process HTTP test client | https://www.python-httpx.org/ |
| `schemathesis` | Property-based API testing from OpenAPI/GraphQL | https://schemathesis.readthedocs.io/ |
| `openapi-core` | Validate request/response against OpenAPI 3 | https://openapi-core.readthedocs.io/ |
| `pact-python` v2 | Consumer-driven contract tests | https://docs.pact.io/implementation_guides/python |
| `pact-broker` CLI | Publish / can-i-deploy gates | https://docs.pact.io/pact_broker/client_cli |
| `newman` | Run Postman collections in CI | https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/ |
| `hurl` | Plain-text HTTP test files | https://hurl.dev/ |
| `dredd` | OpenAPI/Blueprint contract test runner | https://dredd.org/ |
| `oasdiff` | Diff two OpenAPI specs (breaking-change gate) | https://github.com/Tufin/oasdiff |
| `wiremock` / `mockoon-cli` | Stub external dependencies | https://wiremock.org/ , https://mockoon.com/cli/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Pact Broker / Pactflow | OSS / SaaS | Yes | Stores pacts, gates deploys via `can-i-deploy`. CLI is scriptable. |
| Postman / Postman API | SaaS | Yes | API + Newman make collections agent-driven. Use Postman Cloud only when humans collaborate. |
| Insomnia / Bruno | OSS | Yes | Bruno stores collections as plain files (git-friendly) — preferred for agents over Postman cloud. |
| ReadyAPI / SoapUI | SaaS / OSS | Limited | GUI-first; only useful when SOAP/legacy is involved. |
| Stoplight | SaaS | Yes | Hosts spec; trigger Spectral (linter) and prism (mock server) from CI. |
| Prism | OSS | Yes | Mock server from OpenAPI; great for FE agents to develop against unfinished BE. |
| Hoppscotch | OSS | Partial | UI tool; CLI exists but less mature than Newman. |
| Mockoon | OSS | Yes | CLI-first mocks, fits agent loops. |

## Templates & scripts
Inline runner: validate every served response against the snapshotted OpenAPI spec, fail CI on drift.

```bash
#!/usr/bin/env bash
# scripts/api-contract-check.sh
set -euo pipefail
SPEC=${1:-openapi.json}
BASE=${2:-http://localhost:8000}
python - <<PY
import json, sys, httpx
from openapi_core import OpenAPI
from openapi_core.contrib.requests import RequestsOpenAPIRequest, RequestsOpenAPIResponse

spec = OpenAPI.from_file_path("$SPEC")
endpoints = [
    ("GET", "/health", 200),
    ("GET", "/users", 200),
    ("GET", "/users/does-not-exist", 404),
]
errors = []
with httpx.Client(base_url="$BASE") as c:
    for method, path, expected in endpoints:
        r = c.request(method, path)
        if r.status_code != expected:
            errors.append((method, path, expected, r.status_code))
if errors:
    for e in errors: print("MISMATCH", *e)
    sys.exit(1)
print("OK")
PY
```

For contract testing, see `templates.md` for Pact consumer/provider scaffolds.

## Best practices
- Generate tests from the served `openapi.json`, not a hand-maintained spec — the served version is the source of truth.
- Snapshot `openapi.json` per PR; an unintentional diff is a breaking-change signal. Use `oasdiff` for "breaking" vs "non-breaking" classification.
- One auth fixture per role (`anon_client`, `user_client`, `admin_client`); never thread tokens through arguments.
- Run schemathesis in CI as a fuzz pass — it catches edge cases hand-written tests miss (huge integers, empty strings, unicode, nulls in unexpected fields).
- Never share state between contract tests; each consumer pact is independent. Reset Pact Broker tags per branch.
- Always assert on the response body schema, not just the status code — a 200 with a missing field is still a regression.
- For idempotent endpoints, run the test twice in the same module to catch hidden side-effects.
- Keep contract test fixtures dumb: a single `state` string on the provider; the provider implements `/_pact/states` to set up DB rows.

## AI-agent gotchas
- Agents copy README's `pactman` import; it's abandoned. Pin `pact-python>=2`.
- Agents conflate "integration test against TestClient" with "contract test"; only the latter publishes a pact. Be explicit which you want.
- Agents write tests that mutate shared fixtures, then parallelize with `pytest-xdist` — order-dependent failures appear non-deterministic. Force `--dist=loadgroup` or use `pytest.mark.serial`.
- Agents leak credentials into committed test fixtures (Authorization headers, refresh tokens). Run a scrubber pass before commit.
- Agents use `requests` instead of `httpx` in async test files, blocking the event loop and producing flaky timeouts.
- Agents call the live external service (Stripe, SendGrid) in tests because it "works locally"; require `respx`/WireMock and ban network egress in CI.
- When asked to "fix the failing test", agents weaken the assertion (`assert r.status_code in (200, 201, 204)`). Forbid loosening assertions in the prompt — failures must be fixed in production code or in the spec.
- Agents skip 5xx tests because "the server is supposed to work"; require an explicit failure-injection test for at least one dependent (DB down, third-party 503).
- Human-in-loop checkpoint: any change to `openapi.json` snapshot or a removed Pact pact must be reviewed by a human — agents will silently delete drifting tests.

## References
- https://martinfowler.com/articles/practical-test-pyramid.html
- https://docs.pact.io/
- https://schemathesis.readthedocs.io/
- https://openapi-core.readthedocs.io/
- https://learning.postman.com/docs/writing-scripts/test-scripts/
- https://github.com/Tufin/oasdiff
- https://stoplight.io/open-source/spectral
- https://hurl.dev/
