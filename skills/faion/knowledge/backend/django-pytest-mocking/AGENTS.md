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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-mocking.py` | Validate the mocking spec JSON. | After spec emission. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-pytest-fixtures]] — eager Celery setting consumed here.
- [[django-pytest-integration]] — integration tests consuming these mocks.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per boundary: HTTP via requests → `responses` library. Local function call → unittest.mock.patch at import site. Time → freezegun/time-machine. Celery → eager + assert side effects OR patch .delay() + assert task triggered. ORM / sleep → never mock.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/mocking-spec.json`

```json
{
  "_purpose": "Reference mocking spec output.",
  "_consumes": "Boundary inventory + per-boundary contract.",
  "_produces": "JSON for test conventions + mocks/ codegen.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~180 tokens.",
  "artefact_id": "billing-mocks",
  "owner": "ruslan@faion.net",
  "boundaries": [
    {
      "name": "stripe-charge-create",
      "technique": "unittest-mock-patch",
      "patch_target": "apps.billing.services.stripe.Charge.create",
      "asserts": [
        "assert_called_once_with(amount=1000, currency='usd')"
      ]
    },
    {
      "name": "partner-webhook-post",
      "technique": "responses",
      "patch_target": "https://partner.example.com/webhook",
      "asserts": [
        "responses.calls[0].request.url == 'https://partner.example.com/webhook'",
        "len(responses.calls) == 1"
      ]
    },
    {
      "name": "coupon-expiry-clock",
      "technique": "freezegun",
      "patch_target": "2026-05-22T00:00:00Z",
      "asserts": [
        "coupon.is_valid() is False"
      ]
    },
    {
      "name": "invoice-send-task",
      "technique": "celery-delay-patch",
      "patch_target": "apps.billing.services.send_invoice_task.delay",
      "asserts": [
        "assert_called_once_with(invoice.id)"
      ]
    }
  ],
  "anti_mocks": [
    "django-orm",
    "time-sleep",
    "module-level-datetime-now"
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/test_stripe_mock.py`

```python
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from apps.billing import services

pytestmark = pytest.mark.django_db


class TestChargeCustomer:
    # Patch at the CONSUMER's import path: apps.billing.services.stripe.
    @patch("apps.billing.services.stripe.Charge.create")
    def test_creates_charge_with_correct_args(self, mock_create, customer) -> None:
        mock_create.return_value = {"id": "ch_123", "status": "succeeded"}

        services.charge_customer(customer=customer, amount_cents=1000)

        # Verifies BOTH that the call happened and that the arguments are right.
        mock_create.assert_called_once_with(
            amount=1000,
            currency="usd",
            customer=customer.stripe_id,
        )
```

### `templates/test_freezegun_expiry.py`

```python
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from apps.billing.services import coupon_is_valid

pytestmark = pytest.mark.django_db


class TestCouponExpiry:
    @freeze_time("2026-05-22T00:00:00Z")
    def test_coupon_valid_inside_window(self, coupon) -> None:
        # Coupon issued today, valid for 7 days.
        assert coupon_is_valid(coupon) is True

    def test_coupon_invalid_after_expiry(self, coupon) -> None:
        with freeze_time("2026-06-30T00:00:00Z"):
            assert coupon_is_valid(coupon) is False

    @freeze_time("2026-05-22T00:00:00Z")
    def test_now_is_frozen(self) -> None:
        # Reference: confirm the clock is actually frozen.
        assert datetime.now(timezone.utc).isoformat() == "2026-05-22T00:00:00+00:00"
```
