<!-- purpose: Versioned attribution-policy document used across the rollup -->
<!-- consumes: team agreement on attribution model + view-through window -->
<!-- produces: signed policy doc referenced by attribution_policy_version field -->
<!-- depends-on: content/01-core-rules.xml (rule single-attribution-model) -->
<!-- token-budget-impact: ~300 tokens when loaded -->

# Attribution Policy

**Version:** 1.2.0
**Effective from:** 2026-05-23
**Owner:** @growth-lead
**Reviewed by:** @finance-partner

## Default model

Last non-direct click within a **30-day click window**.

## View-through

1-day post-impression window. Captured in `view_through_count` column only — NEVER added to `attributed_conversions`.

## Customer ID

Hashed email (SHA-256) is the canonical join key. Fallback: anonymized user_id from product DB.

## Organic baseline

Computed as trailing 8-week median weekly organic conversions, adjusted for seasonal index.

## Change process

Quarterly review. Any change to model, windows, or baseline definition:

1. Open RFC.
2. Re-run last 90 days under both old + new model.
3. Document delta.
4. Brief growth + finance.
5. Bump policy version (semver).
6. Update `attribution_policy_version` in next week's rollup.
