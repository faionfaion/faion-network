---
slug: incident-response-blameless-playbook
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Severity matrix, IC roles, comms templates, blameless retro structure — the operational practice geek/sdlc-ai/postmortem-auto-draft is missing at pro tier.
content_id: "1d5b87f93344b154"
tags: [incident-response-blameless-playbook, infra, pro]
---

# Incident Response Blameless Playbook

## Summary

**One-sentence:** Severity matrix, IC roles, comms templates, blameless retro structure — the operational practice geek/sdlc-ai/postmortem-auto-draft is missing at pro tier.

**One-paragraph:** Current incident content lives in geek/sdlc-ai (postmortem-auto-draft, runbook-as-markdown) — AI-tool wrappers, not operational practice. A DevOps engineer at pro tier needs severity matrix, IC roles, comms templates, blameless retro. Output: severity matrix + IC RACI + comms templates + retro template.

## Applies If (ALL must hold)

- production system with paying users
- team ≥3 with on-call rotation
- manager authority to standardize incident response

## Skip If (ANY kills it)

- single-customer or pre-revenue product — over-engineering
- no on-call rotation — set up rotation first
- team already runs Google SRE-style incident management — augment, don't duplicate

## Prerequisites

- service catalogue with SLOs
- on-call rotation tool (PagerDuty, Opsgenie, Grafana OnCall)
- comms channels (Slack #incidents, status page, customer comms list)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/infra/devops-engineer` | peer methodology — produces inputs or consumes outputs |
| `geek/sdlc-ai/postmortem-auto-draft` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/sdlc-ai/postmortem-auto-draft`
- peer methodology: `pro/infra/regulated-incident-response-protocol`
- external: https://sre.google/sre-book/managing-incidents/ (Google SRE); https://response.pagerduty.com/; https://www.atlassian.com/incident-management
