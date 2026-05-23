<!-- purpose: minimum viable staging-smoke checklist for validator smoke-test. -->
<!-- consumes: see content/02-output-contract.xml inputs for staging-smoke-checklist-by-surface -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Staging Smoke - top 3 surfaces

## Surface 1: Login (web)
- click Login in nav -> expect login form renders
- click Sign in with valid creds -> expect redirect to /dashboard within 2s

## Surface 2: Create order (API)
- POST /api/orders with valid payload -> expect 201 + order_id

## Surface 3: Payment webhook
- trigger Stripe test event payment_succeeded -> expect order status flips to paid

Signed: RM 2026-05-20T14:12:00Z build:a3f9c1d
