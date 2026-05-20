---
slug: vercel-deployment-discipline
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "64d4d750c86f72b0"
summary: Solo-tier discipline for Vercel deployments — preview branches, env-scoped variables, edge vs node runtime decisions, rollback, and the 6 gotchas (function timeouts, ISR cache, function-region pinning, secrets leakage, build-cache poisoning, ESM/CJS interop).
tags: [vercel, deployment, preview-branches, edge-runtime, rollback]
---

# Vercel Deployment Discipline

## Summary

**One-sentence:** Solo-tier discipline for Vercel deployments — preview branches, env-scoped variables, edge vs node runtime decisions, rollback, and the 6 gotchas (function timeouts, ISR cache, function-region pinning, secrets leakage, build-cache poisoning, ESM/CJS interop).

**One-paragraph:** `free/hosting-infra/deploy-to-vercel-free` shows how to deploy a hobby project. Real solo SaaS hits production gotchas: edge-runtime functions silently fail on Node-only APIs, ISR caches the wrong tenant data, secrets defined in preview leak to prod via "share across all environments", rollbacks via UI work but `vercel rollback` CLI is gated, build caches poison across PR branches. This methodology codifies the rules: per-environment env scoping (dev / preview / prod isolation), edge-runtime allow-list before adoption, ISR cache-key discipline, atomic rollback procedure, and a pre-prod gotcha checklist. Output: `DeploymentPlan` JSON + a per-env settings audit.

## Applies If (ALL must hold)

- production deployment on Vercel (Hobby or Pro plan)
- app uses Next.js, Astro, Nuxt, SvelteKit, or any meta-framework Vercel runs
- operator deploys ≥ 1× per week (otherwise the discipline overhead is wasted)
- there is at least one paying user OR PR / launch in the pipeline

## Skip If (ANY kills it)

- pre-production hobby project — vercel's defaults are fine
- self-hosted on docker / fly.io / railway — different methodology
- enterprise compliance forcing Vercel Enterprise plan — most rules already enforced
- single-environment setup with no preview branches (lol — fix that first)

## Prerequisites

- Vercel project linked to a GitHub repo
- branch protection on `main` (PR required)
- access to Vercel dashboard or `vercel` CLI
- ability to scope env vars per environment (Hobby+ plan supports this)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/hosting-infra/deploy-to-vercel-free` | Bootstrap upstream — this methodology takes over post-launch |
| `pro/infra/cicd-engineer/github-actions-pipelines` | Sister CI methodology for non-Vercel steps |
| `pro/infra/devops-engineer/data-residency-controls` | Function-region pinning ties into residency rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: env scoping, runtime allow-list, ISR cache key, rollback atomicity, secrets boundary | ~1000 |
| `content/02-output-contract.xml` | essential | `DeploymentPlan` + env-audit schemas | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: edge runtime API miss, ISR data leak, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `env_var_audit_scan` | haiku | API call + diff against rules |
| `runtime_compatibility_check` | sonnet | API-allow-list matching for Edge runtime |
| `isr_cache_key_review` | sonnet | Reviews `revalidate` + dynamic params |
| `rollback_plan_compose` | sonnet | Generates rollback playbook per deploy |

## Templates

| File | Purpose |
|------|---------|
| `templates/deployment-plan.json` | Output schema |
| `templates/env-audit.json` | Per-env variable audit schema |
| `templates/runtime-allow-list.yaml` | Edge-compatible API list |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/env-audit.sh` | Scans Vercel env vars, flags cross-scope leaks | Pre-deploy and weekly |
| `scripts/preview-rollback.sh` | Atomic rollback to previous deployment | Incident response |

## Related

- parent skill: `solo/infra/server-craft/`
- peer methodologies: `deploy-to-vercel-free` (free tier), `github-actions-pipelines`
- external: [Vercel — Environment Variables](https://vercel.com/docs/projects/environment-variables) · [Vercel — Edge Functions runtime](https://vercel.com/docs/functions/edge-functions) · [Next.js — ISR Caching](https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration) · [Vercel — Rollbacks](https://vercel.com/docs/rollback)
