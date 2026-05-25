# Django pytest Mocking

## Summary

**One-sentence:** Produces a mocking spec naming each boundary mock (where to patch, what to assert on the call) — payment provider, HTTP via `responses`, datetime via freezegun/time-machine, Celery via .delay() patch — and the explicit anti-list (no ORM, no sleep).

**Ефективно для:** Test suites that drift toward mocking everything (including the ORM), tests that flake because datetime.now() shifts across runs, tests that "pass" because the mock returned a value but was never actually called.

**One-paragraph:** Codifies "what do we mock and where?" into one spec. Forbids: patching at definition site, mocking ORM internals, mocking time.sleep, computing datetime.now() at module load, asserting on return without verifying the call happened.

## Applies If (ALL must hold)

- Django ≥ 5.0 + pytest-django.
- Service has ≥ 1 external boundary (HTTP API, payment provider, S3, Celery, time).
- Tests use unittest.mock + responses + freezegun (or time-machine).
- Output drives the mocking conventions used across the test suite.

## Skip If (ANY kills it)

- Pure unit tests of helpers with zero external boundaries.
- Real-integration tests against staging — no mocks at all.
- Browser E2E tests where mocks don't apply.
- Logic that uses the real ORM and DB — mock-based testing isn't appropriate.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| External boundary inventory | bullets | architecture doc + grep imports |
| Per-boundary contract (what arguments, what returns) | docs | partner API docs |
| Time-sensitive logic list | bullets | grep `datetime.now\|timezone.now` |
| Celery task inventory | bullets | apps/*/tasks.py |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-fixtures]]` | Fixtures + CELERY_TASK_ALWAYS_EAGER setting. |
| `[[django-pytest-integration]]` | Integration tests consume the mocks declared here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 4 testable rules: import-site patch, responses for HTTP, freezegun for time, Celery .delay() vs eager | ~1000 |
| `content/02-output-contract.xml` | essential | JSON schema for the mocking spec | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: definition-site patch, ORM mock, sleep mock, module-level datetime.now, missing call assert | ~800 |
| `content/04-procedure.xml` | medium | 5 steps: enumerate boundaries → pick technique → assertion contract → no-mock list → validate | ~600 |
| `content/06-decision-tree.xml` | essential | Per boundary: technique routing | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_boundaries` | haiku | Mechanical from import graph. |
| `emit_mock_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/mocking-spec.json` | Reference output. |
| `templates/test_stripe_mock.py` | Reference test with import-site patch + assert_called_once_with. |
| `templates/test_freezegun_expiry.py` | Reference clock-frozen test. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-mocking.py` | Validate the mocking spec JSON. | After spec emission. |

## Related

- [[django-pytest-fixtures]] — eager Celery setting consumed here.
- [[django-pytest-integration]] — integration tests consuming these mocks.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per boundary: HTTP via requests → `responses` library. Local function call → unittest.mock.patch at import site. Time → freezegun/time-machine. Celery → eager + assert side effects OR patch .delay() + assert task triggered. ORM / sleep → never mock.
