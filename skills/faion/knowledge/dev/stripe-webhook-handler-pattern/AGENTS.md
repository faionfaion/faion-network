# Stripe Webhook Handler Pattern

## Summary

**One-sentence:** Canonical Stripe webhook handler recipe: signature verification, idempotency on event.id, fast 2xx with queued work, dead-letter queue on fail, replay-safe state mutations.

**One-paragraph:** High-frequency task for solo SaaS founders and e-commerce builders. Generic logging-or-API methodologies do not cover Stripe-specific failure modes: skipped signature verification (DoS / injection surface), missing idempotency (double-charging via Stripe retries), slow synchronous handlers (timeouts plus retry storms), and silent fail without DLQ. This methodology produces a handler spec: verification call, idempotency store + key, sync-or-queue path, dead-letter URL, replay-safety test, named owner.

**Ефективно для:**

- Перший Stripe webhook у SaaS - зафіксувати baseline (verify+idempotency+queue).
- Post-incident після double-charge - закрити gap idempotency.
- Stripe timeouts -> retry storms - перевести важку роботу в queue.
- Migration з custom-webhook на сanonical pattern - провести аудит за rubric.
- Audit перед launch - перевірити DLQ + replay-safety test.

## Applies If (ALL must hold)

- Stripe is the payment processor and webhook endpoint is exposed publicly.
- At least one webhook event is consumed (e.g. checkout.session.completed, invoice.paid).
- Handler runs in a deployable service with access to a persistent store (DB or Redis).
- Team can deploy code changes and configure environment variables / secrets.

## Skip If (ANY kills it)

- Non-Stripe payment processor (PayPal, Adyen, etc.) - use processor-specific guide.
- Polling-only integration without webhooks - different pattern.
- Fully managed Stripe-hosted Payment Links with no custom webhook.
- Test-only scaffold with no production traffic - delay hardening.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stripe account | API + webhook secret | Stripe dashboard |
| Persistent store | DB or Redis with row-level locking | platform |
| Dead-letter target | queue or table for failed events | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[stripe-webhook-hardening]] | deeper hardening (replay attacks, secret rotation, audit). |
| [[structured-logging-as-code]] | log shape that feeds the audit + observability for the handler. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: signature first, idempotency by event.id, 2xx fast, DLQ on fail, replay-safe, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: verify, idempotency, fast-2xx, DLQ, replay-test | ~800 |
| `content/05-examples.xml` | essential | Worked example: invoice.paid handler with Redis idempotency + SQS DLQ | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `verify-signature` | haiku | Mechanical call to Stripe SDK helper. |
| `design-idempotency` | sonnet | Choice of store + key semantics is per-system. |
| `scope-sync-vs-queue` | sonnet | Latency budget per event type requires judgement. |
| `replay-safety-review` | opus | Stakes high; wrong design causes financial regressions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler.py` | Python handler skeleton: verify-then-idempotent-then-enqueue. |
| `templates/idempotency-table.sql` | Postgres schema for event-id idempotency table. |
| `templates/_smoke-test.json` | Filled-in minimum viable handler spec for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stripe-webhook-handler-pattern.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[stripe-webhook-hardening]]
- [[structured-logging-as-code]]
- [[rest-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then verification, then idempotency store, then sync-vs-queue path, then DLQ presence. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/handler.py`

```python
from __future__ import annotations
import os
import stripe
from fastapi import APIRouter, Request, HTTPException, Header

router = APIRouter()
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]


@router.post("/webhooks/stripe")
async def stripe_webhook(req: Request, stripe_signature: str = Header(...)) -> dict:
    body = await req.body()
    # 1) verify signature
    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="bad signature")

    # 2) idempotency dedup on event.id
    if await _seen_event(event["id"]):
        return {"ok": True, "deduped": True}

    # 3) fast 2xx: enqueue heavy work
    await _enqueue(event)
    return {"ok": True}


async def _seen_event(event_id: str) -> bool:
    # INSERT INTO stripe_events(event_id) ON CONFLICT DO NOTHING RETURNING 1
    raise NotImplementedError


async def _enqueue(event: dict) -> None:
    # push to SQS / Celery / pg-boss
    raise NotImplementedError
```

### `templates/idempotency-table.sql`

```sql
CREATE TABLE IF NOT EXISTS stripe_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ,
    payload JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_stripe_events_type_received
    ON stripe_events (event_type, received_at DESC);
```

### `templates/_smoke-test.json`

```json
{
  "event_types": [
    "invoice.paid"
  ],
  "verification_method": "stripe-sdk",
  "idempotency_store": "postgres-unique-index",
  "processing_path": "queue",
  "dead_letter_url": "sqs://billing-dlq",
  "replay_safety_test": "tests/test_invoice_paid_replay.py::test_replay_idempotent",
  "owner": "ruslan@faion.net"
}
```
