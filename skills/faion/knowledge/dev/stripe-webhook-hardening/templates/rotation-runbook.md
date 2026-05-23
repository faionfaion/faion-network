<!-- purpose: Webhook-secret rotation runbook with rollback plan. -->
<!-- consumes: see content/02-output-contract.xml inputs for stripe-webhook-hardening -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Stripe Webhook Secret Rotation Runbook

## Pre-rotation
1. Stripe Dashboard -> Webhooks -> add a second secret to the same endpoint
2. Store the new secret in the secret manager under `stripe.webhook_secret_v2`
3. Roll the app config to read both: verify with v1, fall through to v2

## Rotation
1. Deploy app with dual-secret verify
2. Flip Stripe Dashboard primary secret -> v2
3. Watch audit log for 24h - should see zero failed verifies caused by rotation

## Cleanup
1. Remove v1 from the secret manager
2. Remove the v1 fall-through in app code
3. Update `rotation_cadence_days` clock
