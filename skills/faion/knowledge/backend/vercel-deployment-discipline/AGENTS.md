# Vercel Deployment Discipline

## Summary

**One-sentence:** Generates a DeploymentPlan + per-env audit for Vercel — env scoping, edge-runtime allow-list, ISR tenant discriminator, atomic rollback — gated by go/no-go criteria.

**One-paragraph:** Real solo SaaS hits production gotchas on Vercel: edge-runtime silently fails on Node-only APIs, ISR caches the wrong tenant data, secrets defined 'All Environments' leak to prod, rollback CLI is gated, build cache poisons across branches. This methodology codifies per-environment env scoping, edge-runtime allow-list, ISR cache-key discipline, atomic rollback procedure, and a go/no-go gate. Output: a DeploymentPlan + per-env settings audit.

**Ефективно для:**

- Next.js / Astro / Nuxt apps on Vercel Pro shipping ≥1×/week.
- Multi-tenant SaaS where ISR cache-key discipline is non-negotiable.
- Solo on-call where rollback must be a sub-5-minute operation.
- Audit of an existing Vercel project before launch.

## Applies If (ALL must hold)

- Production deployment on Vercel (Hobby or Pro).
- App uses Next.js / Astro / Nuxt / SvelteKit / any meta-framework Vercel runs.
- Operator deploys ≥1×/week.
- At least one paying user OR a PR/launch in the pipeline.

## Skip If (ANY kills it)

- Pre-production hobby project — defaults are fine.
- Self-hosted on docker / fly.io / railway — different methodology.
- Vercel Enterprise plan — many rules already enforced upstream.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Vercel project ID + linked repo | string | Vercel dashboard |
| Branch protection on main | GitHub branch rule | GitHub repo settings |
| Env variable inventory | list of {name, scope} | Vercel env panel |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| secrets-management | Secrets-boundary rule consumes the secrets inventory. |
| monitoring-logging | Rollback verification step pings the monitoring surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-env-scoping, r2-runtime-allow-list, r3-isr-cache-key, r4-rollback-atomicity, r5-secrets-boundary | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Vercel Deployment Discipline artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: all-envs-secret-leak, edge-node-api-500, isr-tenant-leak, slow-rollback, build-cache-poison | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `env-var-audit-scan` | haiku | API call + diff against rules. |
| `runtime-compatibility-check` | sonnet | API-allow-list matching for Edge runtime. |
| `isr-cache-key-review` | sonnet | Reviews revalidate + dynamic params. |
| `rollback-plan-compose` | sonnet | Generates rollback playbook per deploy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vercel-deployment-discipline.json` | DeploymentPlan JSON skeleton. |
| `templates/vercel-deployment-discipline.md` | Human-readable audit trail + go/no-go report. |
| `templates/deployment-plan.json` | Per-release DeploymentPlan template. |
| `templates/env-audit.json` | Per-env variable audit template. |
| `templates/runtime-allow-list.yaml` | Edge-compatible API list. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vercel-deployment-discipline.py` | Validate DeploymentPlan JSON against the schema. | Pre-deploy gate + post-deploy audit. |
| `scripts/env-audit.sh` | Scans Vercel env vars, flags cross-scope leaks. | Pre-deploy + weekly. |
| `scripts/preview-rollback.sh` | Atomic rollback to previous deployment. | Incident response. |

## Related

- [[secrets-management]]
- [[monitoring-logging]]
- [[cloudflare-domain-dns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
