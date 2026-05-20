---
slug: multi-region-active-active-pattern
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Traffic policy, data residency, conflict resolution, failover testing — multi-region active-active as a single methodology, not five reference docs.
content_id: "92b0d714ffe0f44a"
tags: [multi-region-active-active-pattern, infra, geek]
---

# Multi-Region Active-Active Pattern

## Summary

**One-sentence:** Traffic policy, data residency, conflict resolution, failover testing — multi-region active-active as a single methodology, not five reference docs.

**One-paragraph:** ZERO methodologies on multi-region patterns (active-active, active-passive, RTO/RPO, replication topology, traffic steering). Backup methodologies exist; DR architecture does not. Output: pattern decision + topology + conflict rules + failover drill plan.

## Applies If (ALL must hold)

- product serving multiple regions with SLO requirements
- single-region outage causes business impact
- data architecture supports replication (SQL with logical replication, or NoSQL)

## Skip If (ANY kills it)

- single-region acceptable for the foreseeable future
- data residency forbids cross-region (sovereignty)
- team has no observability or runbook capacity (prerequisite)

## Prerequisites

- SLOs defined per region
- current topology diagram
- RTO + RPO target per service

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/infra/devops-engineer` | peer methodology — produces inputs or consumes outputs |
| `pro/infra/infrastructure-engineer` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `pro/infra/devops-engineer`
- peer methodology: `pro/infra/infrastructure-engineer`
- peer methodology: `pro/infra/incident-response-blameless-playbook`
- external: https://www.cockroachlabs.com/docs/v23.2/multiregion-overview; https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws/
