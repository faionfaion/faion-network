# Django pytest Integration Tests

## Summary

**One-sentence:** Produces an integration-tests spec naming per-endpoint the security matrix (401/403/200/400/404), per-service the happy/error/edge cases, the transactional_db-scoped tests, the CI Postgres config, and the ≥ 80% coverage gate.

**Ефективно для:** Django/DRF projects where regressions slip through because tests assert only on status code, where SQLite-passing tests fail on Postgres in production, where permission combinations get missed for half the endpoints.

**One-paragraph:** Codifies the integration-test surface into one spec. Output names every endpoint with its 5 required test cases, every service-layer test class (one logical concept per test), every transactional_db case (on_commit, signals, atomic rollback), and the CI configuration (Postgres engine, coverage gate). Forbids: 200-only asserts, testing service logic via the view, missing permission combinations, running CI on SQLite when production is Postgres.

## Applies If (ALL must hold)

- Django ≥ 5.0 + DRF/Ninja + pytest-django installed.
- Service has ≥ 1 DRF endpoint and ≥ 1 service-layer function.
- CI runs against the production DB engine (PostgreSQL preferred).
- Team commits to coverage ≥ 80% gate.
- Output drives test codegen + CI config.

## Skip If (ANY kills it)

- Pure business logic with no HTTP — unit tests against services directly.
- E2E browser tests — Playwright/Cypress not pytest-django.
- Performance load tests — locust/k6 against a real env.
- Endpoint already integration-tested elsewhere — don't duplicate.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Endpoint list | YAML | [[django-api]] output |
| Service-layer function list | bullets | [[django-project-structure]] |
| CI runner config | YAML | .github/workflows/*.yml |
| Coverage current baseline | percentage | last pytest --cov run |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-fixtures]]` | api_client / authenticated_client / admin_client fixtures. |
| `[[django-pytest-factories]]` | factories used inside the integration tests. |
| `[[django-api]]` | endpoint matrix consumed here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: per-endpoint security matrix, service-layer direct tests, permission combinations, transactional_db cases, Postgres in CI, one concept per test | ~1300 |
| `content/02-output-contract.xml` | essential | JSON schema for the integration tests spec | ~1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: 200-only assert, view-tested service logic, missing permission combo, SQLite CI | ~800 |
| `content/04-procedure.xml` | deep | 6 steps: matrix → service tests → permission combos → transactional_db → CI → coverage | ~700 |
| `content/06-decision-tree.xml` | essential | Per endpoint: which fixture + which test cases? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_test_cases` | haiku | Mechanical fanout: endpoint × {401,403,200,400,404}. |
| `emit_integration_spec` | sonnet | Bounded transformation. |
| `audit_for_security` | opus | Permission combos + cross-user access checks. |

## Templates

| File | Purpose |
|---|---|
| `templates/integration-spec.json` | Reference output. |
| `templates/test_endpoint_skeleton.py` | Reference pytest module for one endpoint with all 5 cases. |
| `templates/ci-postgres.yml` | GitHub Actions snippet with Postgres service. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-integration.py` | Validate the integration spec JSON. | After spec emission. |

## Related

- [[django-pytest-fixtures]] — fixtures consumed by integration tests.
- [[django-pytest-mocking]] — boundary mocks (Celery, external API).
- [[django-api]] — endpoint contract under test.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per endpoint: write permission? → require force_authenticate per role; assert body. Per service: side effects (Celery, signals)? → transactional_db + mock at boundary. Per CI: production engine Postgres? → CI runs Postgres.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/integration-spec.json`

```json
{
  "_purpose": "Reference integration tests spec output.",
  "_consumes": "Endpoint list + service-layer list + CI runner.",
  "_produces": "JSON for test-module codegen + CI config update.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~220 tokens.",
  "artefact_id": "billing-integration-tests",
  "owner": "ruslan@faion.net",
  "django_version": "5.2.1",
  "endpoints": [
    {
      "path": "/api/v1/invoices/",
      "method": "POST",
      "test_cases": [
        "anonymous-401",
        "wrong-perm-403",
        "happy-201",
        "validation-400"
      ],
      "asserts_body": true
    },
    {
      "path": "/api/v1/invoices/{id}/",
      "method": "GET",
      "test_cases": [
        "anonymous-401",
        "happy-200",
        "not-found-404",
        "cross-user-403"
      ],
      "asserts_body": true
    }
  ],
  "service_tests": [
    {
      "class_name": "TestInvoiceCreate",
      "scenarios": [
        "happy_path",
        "duplicate_number",
        "negative_amount",
        "celery_enqueue"
      ],
      "uses_transactional_db": false,
      "boundary_mocks": [
        "apps.billing.services.send_invoice_email"
      ]
    },
    {
      "class_name": "TestInvoiceVoid",
      "scenarios": [
        "happy_path",
        "void_after_paid_raises",
        "rollback_on_payment_provider_failure"
      ],
      "uses_transactional_db": true,
      "boundary_mocks": [
        "apps.billing.services.payment_provider"
      ]
    }
  ],
  "ci": {
    "db_engine": "postgresql",
    "parallel": true,
    "coverage_command": "pytest -n auto --cov=apps --cov-report=xml --cov-fail-under=80"
  },
  "coverage_threshold": 80,
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/test_endpoint_skeleton.py`

```python
"""

from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.billing.models import Invoice  # adapt to the resource under test

pytestmark = pytest.mark.django_db


class TestInvoiceCreate:
    url = "/api/v1/invoices/"

    def test_anonymous_returns_401(self, api_client: APIClient) -> None:
        response = api_client.post(self.url, data={"amount": "10.00"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_wrong_permission_returns_403(self, api_client: APIClient, other_user) -> None:
        api_client.force_authenticate(user=other_user)
        response = api_client.post(self.url, data={"amount": "10.00"}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_happy_path_returns_201_and_body(self, authenticated_client: APIClient, customer) -> None:
        payload = {"customer_uid": str(customer.uid), "amount": "10.00", "due_date": "2026-06-01"}
        response = authenticated_client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        # Always assert at least one body field — never status-code-only.
        assert response.data["amount"] == "10.00"
        assert "uid" in response.data
        assert Invoice.objects.filter(uid=response.data["uid"]).exists()

    def test_validation_failure_returns_400(self, authenticated_client: APIClient, customer) -> None:
        bad_payload = {"customer_uid": str(customer.uid), "amount": "-5.00"}
        response = authenticated_client.post(self.url, data=bad_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data
```

### `templates/ci-postgres.yml`

```yaml
name: test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: faion
          POSTGRES_PASSWORD: faion
          POSTGRES_DB: faion_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U faion"
          --health-interval=5s
          --health-retries=10

    env:
      DATABASE_URL: postgres://faion:faion@localhost:5432/faion_test
      DJANGO_SETTINGS_MODULE: config.settings.test_postgres

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: pytest -n auto --cov=apps --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```
