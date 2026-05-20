---
slug: scheduled-job-decommission-checklist
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Scheduled-Job Decommission Checklist: a structured cron / scheduled-task retirement procedure that prevents orphan-job sprawl found during monthly cron audits.
content_id: "1ccecef97937fcd3"
tags: [scheduled-job-decommission-checklist, infra, pro]
---
# Scheduled-Job Decommission Checklist

## Summary

**One-sentence:** A typed checklist that retires a cron / scheduled job in a verifiable order — disable in scheduler, archive code, verify no consumer reads its output, drop downstream tables / queues, remove monitoring — so the audit trail proves the job is actually gone, not "probably gone".

**One-paragraph:** Dead-job cleanup during the monthly cron audit is usually informal: someone comments out the schedule and moves on. Months later the job is still present in the code, still has a dashboard panel, still writes to an empty table that costs storage, and may still be re-enabled by accident. This methodology defines the five-stage decommission (disable, observe, archive code, drop dependencies, remove signals) with checkpoint evidence at each stage, plus the 30-day observation window that proves no caller noticed. Output is a typed decommission record per job that can be cited if anything depending on the job surfaces later.

## Applies If (ALL must hold)

- a scheduled job has been identified for retirement (during monthly audit, or post-replacement)
- there is at least one writable scheduler interface (cron file, k8s CronJob, GitHub Actions schedule, etc.)
- the team has observability covering the job's prior outputs (logs, downstream tables, queues)
- tier == pro or higher

## Skip If (ANY kills it)

- the job is a one-off scaffolded script never wired into a scheduler (just delete the file)
- the job is part of a packaged third-party app whose update path replaces it — defer to the upgrade
- a deletion freeze is active (audit window, ongoing incident) — schedule for after the freeze

## Prerequisites

- the job's identifier (scheduler name + code path)
- list of downstream consumers (tables, files, queues, dashboards, alerts)
- access to disable the schedule and archive the code
- a named owner who attests the job is no longer needed

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cronjob-overrun-monitoring` | observability assumed for the observation window |
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: five-stage-order, owner-attestation, 30-day-observation, downstream-removal, archive-not-delete | ~1100 |

## Related

- parent skill: `pro/infra/devops-engineer`
- upstream playbook: `role-devops-engineer/Cron / scheduled-job audit (monthly)`
- companion methodology: `pro/infra/deprecated-api-sweeper-recipe`
