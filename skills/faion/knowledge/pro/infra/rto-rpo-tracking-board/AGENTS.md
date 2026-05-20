---
slug: rto-rpo-tracking-board
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: RTO/RPO Tracking Board: defines the standing surface that keeps observed vs. contractual RTO/RPO visible per system across drills and incidents.
content_id: "cf54231a8102ef5c"
tags: [rto-rpo-tracking-board, infra, pro]
---
# RTO/RPO Tracking Board

## Summary

**One-sentence:** A standing visualisation surface (board, dashboard, or wiki page) that keeps observed RTO/RPO per system visible against the contractual target across drills and real incidents, so drift is detected before the next audit.

**One-paragraph:** Without a standing surface, observed RTO/RPO numbers from drills and real incidents live in scattered reports nobody re-opens. Six months later the team cannot tell whether the contractual 1-hour RTO is being met. This methodology defines the row schema (per-system × per-period), the data sources it must pull from (rto-rpo-measurement-template records, incident postmortems, backup-verification logs), the staleness rules, and the visualisation defaults (target band as horizontal line; observed dots above/below; trend arrow per system). Output is a continuously-refreshed board referenced from the SLO doc and reviewed each quarter.

## Applies If (ALL must hold)

- the org has committed RTO/RPO targets per system (via rpo-rto-negotiation-guide or contract)
- at least one drill or real incident measurement record exists per tracked system
- the team has weekly backup-verification or DR drill cadence
- tier == pro or higher

## Skip If (ANY kills it)

- only one system is in scope and one record exists — a board is overhead, use a single linked record
- existing observability platform already renders target-vs-actual SLO bands and ingests drill records — extend it, do not build a parallel board
- there is no contractual or stakeholder-signed target to compare against (build that first via rpo-rto-negotiation-guide)

## Prerequisites

- list of systems with contractual RTO/RPO targets
- record links: drill measurements (rto-rpo-measurement-template), incident postmortems, backup verifications
- a hosting surface (Grafana, Notion, wiki, Linear board, etc.) that supports updates
- named board-owner who is accountable for staleness

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/rto-rpo-measurement-template` | source records this board aggregates |
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: standing-surface, row-schema, source-record-link, staleness-policy, breach-flag | ~1100 |

## Related

- parent skill: `pro/infra/devops-engineer`
- upstream playbook: `role-devops-engineer/Backup verification (weekly)`
- companion methodology: `pro/infra/rto-rpo-measurement-template`
