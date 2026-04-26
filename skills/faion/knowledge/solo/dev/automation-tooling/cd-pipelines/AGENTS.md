# CD Pipelines and Deployment Strategies

## Summary

CD pipelines automate the path from a passing test suite to a running production deployment. Structure as discrete jobs: build → integration → staging → E2E → production (manual approval). Choose a deployment strategy — rolling, blue/green, or canary — based on rollback speed and traffic-split requirements. Always emit DORA events (deploy_started, deploy_succeeded, deploy_failed) with version + sha + duration.

## Why

Ad-hoc `deploy.sh` scripts lack observability, rollback, and approval gates. A structured pipeline makes every stage independently retry-able, captures DORA metrics automatically, and enforces human sign-off before production. Automatic rollback on smoke-test failure cuts mean time to restore from hours to minutes.

## When To Use

- Authoring or refactoring `.github/workflows/cd.yml` (or GitLab CI / Buildkite equivalent) for a service.
- Adding deployment-strategy primitives: blue/green, canary, rolling with proper readiness/liveness probes.
- Wiring smoke tests, rollback triggers, deployment notifications, and DORA metric tracking.
- Replacing ad-hoc `deploy-gh.sh` scripts with observable, gated pipelines.

## When NOT To Use

- Pure CI (build + test only) — this is CD-specific; see `cd-basics` for CI principles.
- Full platform engineering (multi-cluster, cross-region, GitOps with Argo/Flux) — use `pro/infra/cicd-engineer`.
- Serverless deploys managed by the vendor (Vercel, Netlify, Cloud Run) — those only need build config.
- Monorepo selective deploys per package — requires Turborepo/Nx-aware pipelines not covered here.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-structure.xml` | Five-stage GitHub Actions pipeline (build/integ/staging/e2e/prod), environment approvals, concurrency group. |
| `content/02-strategies.xml` | Rolling (K8s), blue/green (label swap), canary (Istio weight), readiness/liveness probes. |
| `content/03-rollback-dora.xml` | Auto-rollback on smoke failure, DORA metric emission, health check endpoint pattern. |

## Templates

| File | Purpose |
|------|---------|
| `templates/deploy-with-rollback.sh` | Bash script: set image → rollout-status → smoke → rollback on failure. |
