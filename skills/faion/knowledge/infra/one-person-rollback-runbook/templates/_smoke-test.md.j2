<!-- purpose: Minimum viable filled-in runbook for one release. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Rollback Runbook — v1.5.0 → v1.4.3

## Release context

- From: v1.4.3 (last known good)
- To:   v1.5.0 (broken: Sentry alert 18:12 UTC)

## Layer 1 — Code

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| c1 | `vercel rollback v1.4.3 --prod` | `vercel ls --prod` | v1.4.3 |

## Layer 2 — Database

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| d1 | `alembic downgrade 0013` | `alembic current` | 0013 |

## Layer 3 — Feature flags

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| f1 | `flag set checkout_v2 off` | `flag get checkout_v2` | off |

## Smoke check

| step | command | expected |
|------|---------|----------|
| s1 | `npx playwright test smoke/` | 10 passed |

## Sign-off

**Runtime owner:** @ruslan (founder)  •  **Last dry-run:** 2026-05-22  •  **Escalation:** @backup-oncall
