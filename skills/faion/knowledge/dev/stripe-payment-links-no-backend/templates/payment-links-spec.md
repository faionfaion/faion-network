<!--
purpose: human-readable wrapper around the payment-links-spec JSON
consumes: validated spec.json from the output contract
produces: rendered markdown for code review and owner sign-off
depends-on: 02-output-contract.xml schema
token-budget-impact: ~400 tokens
-->

# Payment Links Spec — `<product-name>`

## Owner

`<owner>` — paged on webhook failure.

## Drivers

- `billing_model`: `<value>`
- `custom_amount_per_buyer`: `<value>`
- `connect_required`: `<value>`
- `catalog_size`: `<value>`

## Decision

- `mode`: `<payment-link | checkout-session | reject-connect>`
- `signature_strategy`: `<hmac-sha256-stripe-sdk | hmac-sha256-manual>`
- `idempotency_store`: `<URL>`
- `webhook_endpoint`: `<URL>`

## Links

| SKU | URL | Price | Currency |
|---|---|---|---|
| `<sku>` | `<url>` | `<cents>` | `<iso>` |

## Fulfillment channels

| Channel | Address |
|---|---|
| email | `<addr>` |
| sheet | `<URL>` |

## Audit

Rules consulted: `<r-list>` — see content/01-core-rules.xml.
