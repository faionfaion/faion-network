# Continuous Delivery Basics

## Summary

Continuous Delivery (CD) is the practice of keeping every commit in a deployable state so that production releases require only a manual trigger — not a manual testing campaign. Prerequisites: CI in place, comprehensive automated tests, feature flags, backward-compatible migrations, and IaC. Every change ships through an automated pipeline; the only human gate is the final production deploy button.

## Why

Manual deployments batch risk: the larger the batch, the harder the rollback. CD forces small batches (&lt;200 LOC per PR), which reduces lead time, lowers change failure rate, and makes rollback trivial. DORA research (Accelerate) shows elite teams deploy on-demand with p95 lead time &lt;1 hour and MTTR &lt;1 hour — achieved through CD, not heroics.

## When To Use

- Team currently does manual deployments and wants a phased CD roadmap.
- Auditing an existing pipeline against the CI / CD (Delivery) / CD (Deployment) matrix.
- Designing backward-compatible schema migrations (expand-contract pattern) to decouple deploy from data changes.
- Introducing feature flags as the bridge between "code shipped" and "feature released."
- Diagnosing CD blockers: large batches, slow tests, manual gates, non-backward-compatible migrations.

## When NOT To Use

- Pipeline YAML and deployment strategy mechanics — read `cd-pipelines/` instead.
- Full GitOps (Argo/Flux) — `pro/infra/cicd-engineer` territory.
- Mobile app store releases — review/policy gates dominate; CD principles apply but tooling diverges.
- Environments with mandatory regulatory release boards — CD is achievable but heavier; this methodology does not cover evidence-capture automation.
- When CI is not yet in place — fix prerequisites first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core CD rules: releasable commits, pipeline stages, automation scope, feature-flag / deploy-release decoupling. |
| `content/02-migrations-and-challenges.xml` | Expand-contract migration pattern, common CD blockers (batch size, test speed, DB changes) and solutions. |
| `content/03-dora-and-roadmap.xml` | DORA elite targets, five-phase adoption roadmap (Foundation → Continuous Deployment), CD vs CI vs CDeployment matrix. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cd-readiness.yaml` | Per-service scorecard: CI, tests, IaC, release, DORA metrics, gaps, next phase. |
| `templates/feature-flag-service.py` | Minimal Python FeatureFlagService with cache, httpx evaluation, and usage example. |
