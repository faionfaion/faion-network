<!-- purpose: Markdown rollback runbook with three-layer steps + verify commands. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Rollback Runbook — {release_tag}

## Release context

- From: vX.Y.Z (last known good)
- To:   vA.B.C (broken release)

## Layer 1 — Code

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| c1 | git revert / vercel rollback | `vercel ls --prod` | vX.Y.Z |

## Layer 2 — Database

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| d1 | alembic downgrade -1 | `alembic current` | <revision> |

## Layer 3 — Feature flags

| step | command | verify_cmd | expected |
|------|---------|------------|----------|
| f1 | flag flip via vendor CLI | `flag get checkout_v2` | off |

## Smoke check

| step | command | expected |
|------|---------|----------|
| s1 | `npx playwright test smoke/` | 10 passed |

## Sign-off

**Runtime owner:** @handle (role)  •  **Last dry-run:** YYYY-MM-DD  •  **Escalation:** @backup
