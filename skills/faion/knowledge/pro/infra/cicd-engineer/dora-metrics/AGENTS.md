# DORA Metrics

## Summary

DORA (DevOps Research and Assessment) metrics are four research-validated KPIs that measure software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore. Elite teams deploy 208x more often and recover 2,604x faster than low performers. A fifth metric — Reliability (SLO achievement) — was added in 2025. AI-generated code reduces delivery stability by ~7%, so batch size must be monitored when using AI tools.

## Why

The four metrics are the only empirically-proven predictors of both technical and organizational performance (from the "Accelerate" book, 2018). They give a complete picture: throughput (DF + LT) and stability (CFR + MTTR). Without them, teams optimize locally and miss systemic bottlenecks.

## When To Use

- Setting up engineering metrics for a team or service for the first time
- Evaluating CI/CD pipeline health before a refactoring sprint
- Connecting engineering output to business outcomes (revenue, churn, team wellbeing)
- Running quarterly DevOps performance reviews
- Designing a metrics collection system backed by CI/CD + incident tools

## When NOT To Use

- Comparing individual developers — metrics are team-level, not individual
- Early-stage prototype projects with no production — no deployment signal to measure
- As a performance review tool — misuse drives gaming; use for improvement only
- When incident tooling (PagerDuty, Opsgenie) is not yet integrated — MTTR will be inaccurate

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Four metrics definitions, elite/high/medium/low thresholds, 2025 AI impact findings |
| `content/02-implementation.xml` | Data collection rules, tool integrations, implementation checklist steps |
| `content/03-examples.xml` | GitHub Actions and GitLab CI deployment event examples, PromQL queries, Python lead time calculator |

## Templates

| File | Purpose |
|------|---------|
| `templates/deploy-event.yml` | GitHub Actions workflow step emitting deployment events to a metrics endpoint |
| `templates/prometheus-rules.yml` | Prometheus recording rules and alerts for all four DORA metrics |
| `templates/schema.sql` | PostgreSQL schema for deployments + incidents tables with DORA materialized view |
