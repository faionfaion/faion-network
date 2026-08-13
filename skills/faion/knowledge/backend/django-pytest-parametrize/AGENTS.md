# Django pytest Parametrize

## Summary

**One-sentence:** Produces a parametrize spec naming the validation matrices, permission grids, and error-code tables — each with descriptive IDs, valid-payload base, and split-by-category to keep parameter lists below ~20 rows.

**Ефективно для:** Test suites where 12 near-identical tests differ only in (field, bad_value, expected_error), where pytest output reads `[0] [1] [2]` instead of `[email-invalid] [password-short]`.

**One-paragraph:** Codifies "when do we parametrize and how?" into one spec. Output names each parametrize block (test function + argnames + cases + IDs). Forbids: parameter lists &gt; 20 rows (split by category), model-instance parameters (use IDs + factories), generic auto-numeric IDs, mixed control-flow variations under one parametrize.

## Applies If (ALL must hold)

- Django ≥ 5.0 + pytest-django.
- The test under consideration has ≥ 3 near-identical bodies that differ only in data.
- Parameter cases are independent (no shared mutable state).
- Cases share setup, teardown, and assertion logic.
- Output drives test refactor or codegen.

## Skip If (ANY kills it)

- Cases need substantially different setup/teardown — separate test functions.
- &gt; 20 cases — split into category-named test functions.
- Cases differ in control flow, not just data.
- One-off test that isn't repeated anywhere — don't parametrize.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Group of near-identical tests | code refs | grep |
| Per-case (input, expected) data | bullets | spec / domain rules |
| Valid baseline payload (for matrix tests) | YAML | API contract |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-integration]]` | Endpoint matrix consumed by validation parametrize. |
| `[[django-pytest-fixtures]]` | api_client / authenticated_client used inside parametrize. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 4 testable rules: parametrize semantics, three-tuple matrix, refactor threshold, fixture switching via getfixturevalue | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the parametrize spec | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: huge parameter lists, model-instance params, generic IDs | ~700 |
| `content/06-decision-tree.xml` | essential | Per group of tests: refactor or keep? matrix shape? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `find_redundant_tests` | haiku | Mechanical grep. |
| `emit_parametrize_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/parametrize-spec.json` | Reference output. |
| `templates/test_validation_matrix.py` | Reference (field, value, error) matrix test. |
| `templates/test_role_grid.py` | Reference role/permission grid test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-parametrize.py` | Validate the parametrize spec JSON. | After spec emission. |

## Related

- [[django-pytest-integration]] — endpoint matrix consumed here.
- [[django-pytest-fixtures]] — client fixtures used inside parametrize.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per redundant test group: ≥ 3 bodies, same shape, only data differs → parametrize. &gt; 20 cases → split by category. Parameters include model instances → replace with IDs + factory lookup inside the test.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/parametrize-spec.json`

```json
{
  "_purpose": "Reference parametrize spec output.",
  "_consumes": "Group of redundant tests + per-case data.",
  "_produces": "JSON for test-refactor codegen.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~180 tokens.",
  "artefact_id": "billing-parametrize",
  "owner": "ruslan@faion.net",
  "parametrizations": [
    {
      "test_function": "test_create_invoice_validation",
      "argnames": "field, value, expected_error",
      "cases": [
        {
          "id": "amount-negative",
          "args": [
            "amount",
            "-5",
            "must be positive"
          ]
        },
        {
          "id": "amount-non-numeric",
          "args": [
            "amount",
            "abc",
            "must be a number"
          ]
        },
        {
          "id": "due-date-past",
          "args": [
            "due_date",
            "2020-01-01",
            "must be in the future"
          ]
        },
        {
          "id": "missing-customer",
          "args": [
            "customer_uid",
            null,
            "this field is required"
          ]
        }
      ],
      "ids_descriptive": true,
      "uses_indirect": false
    },
    {
      "test_function": "test_invoice_detail_by_role",
      "argnames": "client_fixture, expected_status",
      "cases": [
        {
          "id": "anonymous-401",
          "args": [
            "api_client",
            401
          ]
        },
        {
          "id": "user-owns-200",
          "args": [
            "authenticated_client",
            200
          ]
        },
        {
          "id": "user-cross-403",
          "args": [
            "other_authenticated_client",
            403
          ]
        },
        {
          "id": "admin-200",
          "args": [
            "admin_client",
            200
          ]
        }
      ],
      "ids_descriptive": true,
      "uses_indirect": false
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/test_validation_matrix.py`

```python
"""

from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def _valid_payload(customer_uid: str) -> dict[str, object]:
    return {
        "customer_uid": customer_uid,
        "amount": "10.00",
        "due_date": "2026-12-31",
    }


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        pytest.param("amount", "-5",          "must be positive",            id="amount-negative"),
        pytest.param("amount", "abc",         "must be a number",            id="amount-non-numeric"),
        pytest.param("due_date", "2020-01-01","must be in the future",       id="due-date-past"),
        pytest.param("customer_uid", None,    "this field is required",      id="missing-customer"),
    ],
)
def test_create_invoice_validation(
    authenticated_client: APIClient,
    customer,
    field: str,
    value: object,
    expected_error: str,
) -> None:
    payload = _valid_payload(str(customer.uid))
    payload[field] = value

    response = authenticated_client.post("/api/v1/invoices/", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected_error in str(response.data.get(field, ""))
```

### `templates/test_role_grid.py`

```python
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        pytest.param("api_client",                    401, id="anonymous-401"),
        pytest.param("authenticated_client",          200, id="user-owns-200"),
        pytest.param("other_authenticated_client",    403, id="user-cross-403"),
        pytest.param("admin_client",                  200, id="admin-200"),
    ],
)
def test_invoice_detail_by_role(request, invoice, client_fixture: str, expected_status: int) -> None:
    # getfixturevalue selects the API client per parametrized row.
    client = request.getfixturevalue(client_fixture)
    response = client.get(f"/api/v1/invoices/{invoice.uid}/", format="json")
    assert response.status_code == expected_status
```
