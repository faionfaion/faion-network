<!--
purpose: step-by-step Stripe Dashboard + API checklist for a pricing experiment
consumes: experiment-plan.md
produces: stripe_preflight section of the bundle
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when loaded as context
-->
# Stripe Config Checklist — REPLACE-EXPERIMENT-ID

- [ ] New Price object created per currency in plan.currencies_in_test
- [ ] Old Price object kept active (NOT archived, NOT deleted)
- [ ] tax_behavior set on each Price object matching plan.tax_behavior
- [ ] Stripe Tax enabled (or manual VAT/GST verified) for affected regions
- [ ] Grandfather coupon created (templates/grandfather-coupon.json) and attached to ALL eligible customer IDs
- [ ] Pricing-page A/B router live (random hash, geo, or cohort flag) — passes through to new Price for selected variant only
- [ ] No orphan subscriptions (subs referencing deleted Plan or unrelated Price)
- [ ] No test-mode artefacts present in live (Stripe Dashboard → Test Mode toggled off; sanity check via API)
- [ ] Webhook handlers updated to recognise new Price IDs in subscription.created / invoice.paid
- [ ] Idempotency key strategy documented for coupon re-attachment if a customer churns/returns
