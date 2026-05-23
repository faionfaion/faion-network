# One Person Rollback Runbook

## Summary

**One-sentence:** Verified rollback runbook for solo SaaS: code revert, database migration down, feature-flag flip, smoke checks, and a single dry-run pass before the staging-to-prod gate opens.

**One-paragraph:** Solo SaaS deploys break in three places: app code, DB migrations, and feature flags. Without a rehearsed rollback runbook, a 30-second mistake becomes a multi-hour outage and a refund spiral. This methodology produces a versioned, dry-run-verified rollback artefact that the operator hits in two commands when prod breaks. Every step has a verify command, every command has an expected output, and the runbook is dry-run weekly so the muscle memory is real.

## Applies If (ALL must hold)

- App is deployed by a single person from a staging branch to prod.
- Stack has database migrations + feature flags + git-tagged releases.
- Operator can take staging down for 5 minutes weekly for dry-run.

## Skip If (ANY kills it)

- Multi-tenant DB where rollback would destroy other tenants' data — needs per-tenant procedure.
- Stateless edge function deploy where redeploy IS the rollback — use platform-native revert.
- Greenfield prototype with no paying customers — defer until first paid user.

**Ефективно для:**

- Соло-засновники SaaS на Vercel / Railway / Fly.io з активними платниками.
- Indie hackers що деплоять Friday-evening — щоб мати reversal-path до понеділка.
- Микро-команди (1-3 людини) без on-call ротації.
- Аудит-ready середовища де reversal-trail вимагається регулятором.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Last 3 release tags | git tags | ops repo |
| Migration log | Alembic / Prisma / Rails migrations table | app DB |
| Feature flag inventory | JSON / LaunchDarkly export | flag vendor |
| Smoke-check suite | Playwright / curl scripts | ops repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/deploy-scripts` | Rollback inverts the deploy script. |
| `solo/infra/server-craft/health-checks-autoheal` | Health checks decide whether rollback is needed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step rollback procedure with dry-run | 900 |
| `content/05-examples.xml` | essential | Worked example from incident detection to verified rollback | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-runbook` | haiku | Template fill from release tags + flag list. |
| `populate-verify-commands` | sonnet | Per-step verify + expected output. |
| `review-coverage` | opus | Cross-step coverage: code + DB + flags + smoke. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown rollback runbook with steps + verify commands. |
| `templates/_smoke-test.md` | Minimum viable filled-in runbook for one release. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-one-person-rollback-runbook.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On runbook commit; in CI before release tag. |

## Related

- [[deploy-scripts]]
- [[health-checks-autoheal]]
- [[sentry-supabase-vercel-wiring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
