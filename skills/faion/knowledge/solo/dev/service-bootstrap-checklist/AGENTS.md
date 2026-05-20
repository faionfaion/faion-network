---
slug: service-bootstrap-checklist
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Day-0 greenfield service bootstrap checklist consolidating layout, CI, AGENTS.md, container, observability stubs, secrets, and release into a single ship-ready artefact."
content_id: "e22544a7079db040"
tags: [service-bootstrap-checklist, dev, solo]
---
# Service Bootstrap Checklist

## Summary

**One-sentence:** A day-0 consolidated checklist that turns an empty repo into a deployable, observable, AGENTS.md-documented service in a single sitting.

**One-paragraph:** Greenfield repo bootstrap touches a dozen topics — layout, CI, AGENTS.md, containerisation, observability stubs, secrets, release notes, deploy pattern — and only `github-repo-bootstrap` covers it at the free tier, in a way that misses the production-readiness floor. Solo builders need a single checklist that produces a service which can ship to production on day 1, not just compile. This methodology bundles the canonical floor into eight gates, each with a binary pass criterion, and emits a `BOOTSTRAP.md` record signed by the operator. Greenfield velocity is bottlenecked by forgetting one of these gates and discovering it during the first incident.

## Applies If (ALL must hold)

- you are creating a new repo / service from scratch (not extending an existing service)
- the service will ship to production (not a throwaway spike)
- you are the operator AND the future on-call (solo or small-team context)
- tier == solo or higher

## Skip If (ANY kills it)

- the service is a private spike with no production target (use a lighter scaffold)
- the org has an enterprise scaffold tool that already enforces these gates
- the repo is a library / package (not a runnable service) — different bootstrap concerns

## Prerequisites

- a name for the service and target deployment surface (Vercel / Fly / Railway / k8s / VPS)
- a chosen language / framework
- credentials access to the deploy provider
- a chosen secrets store (even Vercel env or `.env.local` for solo)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/github-repo-bootstrap` | parent — covers the empty-repo step this checklist extends |
| `solo/dev/automation-tooling` | sibling — CI patterns |
| `solo/dev/deploy-notes-template-with-rollback` | downstream — release notes template |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable bootstrap gates + 1 worked BOOTSTRAP.md example | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_repo_layout` | haiku | template instantiation |
| `generate_ci_pipeline` | sonnet | per-framework CI yaml |
| `wire_observability` | sonnet | per-deploy-surface Sentry/OTel stub |
| `produce_bootstrap_record` | sonnet | summary doc with sign-off |

## Related

- parent skill: `solo/dev/`
- `free/dev/github-repo-bootstrap`
- `solo/dev/automation-tooling`
- upstream playbook: `role-software-developer/Greenfield service from scaffold to first production deploy (8 weeks, P6 product team)`
