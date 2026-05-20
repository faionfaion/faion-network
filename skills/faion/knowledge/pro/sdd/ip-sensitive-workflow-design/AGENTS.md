---
slug: ip-sensitive-workflow-design
tier: pro
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Clean separation (repos, credentials, time-fenced work, IP-attribution log) for outsource specialists building side-SaaS without IP-conflict with day-job clients.
content_id: "ec10154c11309970"
tags: [ip-sensitive-workflow-design, sdd, pro]
---

# IP-Sensitive Workflow Design

## Summary

**One-sentence:** Clean separation (repos, credentials, time-fenced work, IP-attribution log) for outsource specialists building side-SaaS without IP-conflict with day-job clients.

**One-paragraph:** IP assignment clauses vs side-SaaS create a hazard: code 'on hours' may belong to client. Methodology that enforces clean separation is missing. Output: workflow plan + repo policy + credential vault + IP-attribution log.

## Applies If (ALL must hold)

- developer with day-job IP-assignment contract AND active side-SaaS
- side project uses any tools, accounts, or time that could be claimed by employer
- developer wants legal defensibility

## Skip If (ANY kills it)

- day-job has no IP-assignment clause (rare in 2026)
- developer is a contractor with separate IP per project (different design)
- side project is open-source under company-approved policy

## Prerequisites

- read of day-job employment + IP clauses
- list of all tools/accounts used by both day-job + side
- calendar visible to verify time-fencing

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd` | parent skill — provides operating context for this methodology |
| `pro/marketing/freelance-saas-billing-decision` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/worker-misclassification-self-audit` | peer methodology — produces inputs or consumes outputs |

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

- parent skill: `solo/sdd/sdd/`
- peer methodology: `pro/marketing/freelance-saas-billing-decision`
- peer methodology: `pro/marketing/worker-misclassification-self-audit`
- external: https://github.com/jamiehannaford/what-happens-when-employee-leaves; https://www.eff.org/issues/employee-tech-rights
