---
slug: regulated-incident-response-protocol
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Incident comms under PCI/HIPAA/GDPR breach-notification clocks (72h GDPR, 60d HIPAA) — for outsource specialists in regulated client engagements.
content_id: "7d5b8ea867d7e2ea"
tags: [regulated-incident-response-protocol, infra, pro]
---

# Regulated Incident Response Protocol

## Summary

**One-sentence:** Incident comms under PCI/HIPAA/GDPR breach-notification clocks (72h GDPR, 60d HIPAA) — for outsource specialists in regulated client engagements.

**One-paragraph:** When a regulated system has a P1, the dev is in the loop with client SOC + compliance officer + sometimes regulator. faion has nothing on incident comms under regulated breach clocks. High-stakes gap. Output: regulated incident playbook + comm templates + clock tracker.

## Applies If (ALL must hold)

- system handling PCI / HIPAA / GDPR / SOC2-regulated data
- dev role includes incident response touching that data
- client expects external regulator notifications may be required

## Skip If (ANY kills it)

- non-regulated systems
- client handles all compliance internally (no dev role)
- system already has dedicated SOC team — defer to their playbook

## Prerequisites

- regulatory scope documented
- BAA / DPA / equivalent agreements in place
- client's compliance officer + outside counsel contact list

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/infra/incident-response-blameless-playbook` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/ai-governance-compliance` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/infra/incident-response-blameless-playbook`
- peer methodology: `geek/ai/ai-governance-compliance`
- peer methodology: `pro/sec/data-classification`
- external: https://gdpr.eu/article-33-data-breach-notification/; https://www.hhs.gov/hipaa/for-professionals/breach-notification/; https://www.pcisecuritystandards.org/document_library/
