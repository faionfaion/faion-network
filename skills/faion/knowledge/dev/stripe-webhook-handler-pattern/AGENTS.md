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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stripe-webhook-handler-pattern.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[stripe-webhook-hardening]]
- [[structured-logging-as-code]]
- [[rest-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then verification, then idempotency store, then sync-vs-queue path, then DLQ presence. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default.
