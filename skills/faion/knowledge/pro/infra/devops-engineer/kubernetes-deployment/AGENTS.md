# Kubernetes Deployment Strategies

## Summary

Kubernetes offers two built-in strategies (Recreate and Rolling Update) and three advanced strategies via Argo Rollouts (Blue-Green, Canary, A/B Testing). 80% of Kubernetes outages stem from deployment errors. The default Rolling Update is zero-downtime but has medium rollback speed; Blue-Green provides instant rollback at 2x resource cost; Canary is the most risk-averse — it shifts traffic incrementally while Prometheus/Datadog analysis gates each step.

## Why

Strategy choice directly maps to acceptable risk, resource cost, and rollback speed. Using Recreate in production causes downtime. Using only native Rolling Update for critical services misses the metric-driven auto-rollback that Argo Rollouts provides. Canary analysis with automated success/failure thresholds eliminates manual "watch dashboards during deploy" practice and catches regressions before they reach 100% of traffic.

## When To Use

- Any production Kubernetes deployment that requires zero downtime (Rolling Update minimum).
- Critical services needing instant rollback — use Blue-Green.
- High-traffic systems where a bad deploy must not reach all users — use Canary.
- GitOps workflows — Argo Rollouts integrates natively with Argo CD.

## When NOT To Use

- Applications that cannot run two versions simultaneously (DB schema breaking change) — use Recreate or migrate schema first.
- Dev/staging environments where downtime is acceptable — Recreate is simpler.
- Teams without Prometheus metrics or observability — Canary analysis gates require metrics; fall back to Rolling Update.

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Strategy comparison table, Recreate/Rolling/Blue-Green/Canary mechanics, Argo Rollouts vs native K8s, progressive delivery workflow |
| `content/02-checklists.xml` | Pre-deployment, Rolling Update, Blue-Green, Canary, Argo Rollouts setup, rollback, and production-readiness checklists with kubectl commands |

## Templates

none
