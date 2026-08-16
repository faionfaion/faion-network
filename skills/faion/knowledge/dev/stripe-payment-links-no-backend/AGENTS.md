# Stripe Payment Links No Backend

## Summary

**One-sentence:** Ships a versioned monetization-spec for accepting Stripe payments without a backend, using Payment Links plus Zapier or Make for webhook fanout.

**One-paragraph:** Indie hackers and solopreneurs need to charge customers before they own server infrastructure. Stripe Payment Links provide a hosted checkout URL; Stripe webhooks deliver the post-payment event; Zapier or Make routes the event to email / Sheets / CRM. This methodology turns that pattern into a deterministic spec — which products, which webhook events, which signature-verification path, which idempotency strategy, which fulfillment fanout. Output is a `payment-links-spec.md` plus a runnable Zapier-blueprint JSON.

**Ефективно для:** solopreneur charging customers for digital downloads, lifetime deals, or one-off coaching before any backend exists.

## Applies If (ALL must hold)

- Product is digital (download, course access, license key) or one-off service — no inventory, no shipping integration needed.
- Total catalog ≤20 SKUs (Payment Links scale poorly past that).
- Fulfillment can be expressed as 1-3 Zapier steps (email, Sheets row, Discord message, license-key issuance).
- Customer support volume tolerates manual refunds (no programmatic billing portal exposed).
- Operator already has a Stripe account in good standing and can verify identity.

## Skip If (ANY kills it)

- Recurring billing with metered usage or proration → needs the Stripe Billing API, not Payment Links.
- Multi-tenant SaaS that issues per-user accounts on payment → run `stripe-checkout-session-backend` instead.
- Marketplace flows (Stripe Connect, application_fee) → Payment Links don't support `transfer_data`.
- Compliance burden requires audit-grade webhook idempotency, replay protection, and IP allowlisting → backend needed.
- Regulator forces local data residency (EU-only / India-only storage) → Zapier US routing is disqualifying.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `catalog.yaml` | list of {sku, price_cents, currency, name, fulfill_action} | operator |
| `stripe-account-id` | string (acct_*) | Stripe dashboard |
| `fulfillment-channels` | list of {channel, address} | operator |
| `webhook-events-needed` | list (checkout.session.completed, charge.refunded, ...) | operator |
| `idempotency-store` | sheet URL or table name | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[github-repo-bootstrap]] | Spec artefact lives in a repo with a CHANGELOG and owner. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: signature verification, idempotency key, raw-body preservation, named owner, 5-min replay window. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for `payment-links-spec` + valid/invalid examples. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skipped signature check, missing idempotency, mutated body, expired URL reuse, plural owner. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate SKUs → create links → wire Zapier → verify signature → publish spec. | ~700 |
| `content/05-examples.xml` | recommended | One worked spec for a $29 lifetime-deal indie product. | ~600 |
| `content/06-decision-tree.xml` | essential | Decides Payment Link vs Checkout-Session vs Billing API, by recurring? + custom-amount? + connect? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_catalog` | haiku | Mechanical YAML→typed dict. |
| `draft_spec` | sonnet | Tradeoffs (signature library, idempotency key shape) require sound reasoning. |
| `verify_webhook_security` | opus | Subtle cross-cutting failures (replay, raw-body mutation) — high stakes for live money. |
| `emit_zapier_blueprint` | sonnet | Mechanical but must validate. |

## Templates

| File | Purpose |
|---|---|
| `templates/catalog.yaml` | Input catalog skeleton. |
| `templates/payment-links-spec.md.j2` | Markdown spec template — sections per SKU + webhook policy. |
| `templates/payment-links-spec.md` | Markdown spec template — sections per SKU + webhook policy. Generated from `templates/payment-links-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/zapier-blueprint.json` | Zapier-importable trigger+action JSON. |
| `templates/webhook-handler.py` | Reference signature-verification snippet (Stripe SDK, optional). |
| `templates/_smoke-test.yaml` | Minimum viable filled-in catalog (1 SKU, 1 channel). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-stripe-payment-links-no-backend.py` | Validates emitted spec against the JSON schema. | Pre-commit; in CI before publishing the spec. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[github-repo-bootstrap]]
- [[one-command-dev-env-template]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `billing_model` (one-off → Payment Link branch; recurring → Checkout Session or Billing API), then on `connect_required` (yes → reject, escalate; no → continue), then on `custom_amount_per_buyer` (yes → Checkout Session; no → Payment Link). Each leaf cites a rule id in 01-core-rules.xml so the spec always records which rule drove the branch — auditable replay.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/catalog.yaml`

```yaml
catalog:
  - sku: TODO              # short stable id, kebab-case
    price_cents: 0         # integer, cents (USD/EUR/etc.)
    currency: usd          # ISO 4217 lowercase
    name: TODO
    fulfill_action: TODO   # email-license-key | sheet-row | discord-ping | ...

drivers:
  billing_model: one-off            # one-off | recurring
  custom_amount_per_buyer: false    # true forces Checkout Session
  connect_required: false           # true forces backend escalation

fulfillment_channels:
  - {channel: email, address: TODO}

webhook_events_needed:
  - checkout.session.completed
  - charge.refunded

idempotency_store: TODO   # Sheets URL / KV bucket / DB table
owner: TODO               # single human (handle / email / role with rotation)
```

### `templates/zapier-blueprint.json`

```json
{
  "_header": {
    "purpose": "Zapier scenario blueprint for the no-backend Stripe webhook fanout",
    "consumes": "spec.json + STRIPE_WEBHOOK_SECRET (Zapier env)",
    "produces": "running Zap on import \u2014 triggers on checkout.session.completed",
    "depends-on": "Stripe app connection in Zapier; signing-secret env var",
    "token-budget-impact": "~200 tokens"
  },
  "trigger": {
    "app": "stripe",
    "event": "checkout.session.completed",
    "auth_account": "<stripe-account-handle>"
  },
  "steps": [
    {
      "step": "code-by-zapier",
      "name": "verify-signature",
      "language": "python",
      "inputs": {
        "raw_body": "{{trigger.raw_body}}",
        "sig_header": "{{trigger.headers.Stripe-Signature}}",
        "secret": "{{env.STRIPE_WEBHOOK_SECRET}}"
      },
      "purpose": "HMAC-SHA256 verification per r1/r2 in core-rules"
    },
    {
      "step": "google-sheets",
      "name": "idempotency-guard",
      "action": "lookup-row-or-create",
      "inputs": {
        "event_id": "{{trigger.id}}",
        "sheet": "<idempotency_store URL>"
      },
      "purpose": "Guards fulfillment against retry duplication per r3"
    },
    {
      "step": "gmail",
      "name": "fulfill-email",
      "action": "send-email",
      "inputs": {
        "to": "{{trigger.customer_details.email}}",
        "subject": "Your purchase",
        "body": "License key: {{license_key}}"
      }
    }
  ]
}
```

### `templates/webhook-handler.py`

```python
"""Reference snippet — copy into Zapier Code (Python) step or serverless handler."""
from __future__ import annotations

import hashlib
import hmac
import json
import time


class SignatureVerificationError(Exception):
    """Raised when Stripe-Signature header fails HMAC verification."""


def verify_stripe_signature(raw_body: bytes, sig_header: str, secret: str, tolerance_seconds: int = 300) -> dict:
    """Verify Stripe webhook payload and return the parsed event.

    raw_body must be the exact bytes Stripe sent — no framework re-serialisation.
    """
    if not isinstance(raw_body, (bytes, bytearray)):
        raise SignatureVerificationError("raw_body must be bytes — preserve raw request body")
    parts = dict(p.split("=", 1) for p in sig_header.split(","))
    ts = int(parts["t"])
    sig = parts["v1"]
    if abs(time.time() - ts) > tolerance_seconds:
        raise SignatureVerificationError("timestamp outside tolerance — possible replay")
    signed_payload = f"{ts}.".encode() + raw_body
    expected = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise SignatureVerificationError("HMAC mismatch — payload forged or secret wrong")
    return json.loads(raw_body)


if __name__ == "__main__":
    import sys
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
catalog:
  - sku: smoke-29
    price_cents: 2900
    currency: usd
    name: "Smoke Test Lifetime Deal"
    fulfill_action: email-license-key

drivers:
  billing_model: one-off
  custom_amount_per_buyer: false
  connect_required: false

fulfillment_channels:
  - {channel: email, address: smoke@faion.net}

webhook_events_needed:
  - checkout.session.completed

idempotency_store: "https://docs.google.com/spreadsheets/d/SMOKE/edit"
owner: smoke-test@faion.net
```
