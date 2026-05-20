---
slug: senior-promotion-case-template-outsource-shop
tier: pro
group: comms
domain: comms
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Promotion case template tailored to outsource shops (SoftServe/EPAM/Globant/Andela) — combines technical scope, revenue impact, and utilization on the same rubric."
content_id: "f2f75d776e746000"
tags: [senior-promotion-case-template-outsource-shop, comms, pro]
---
# Senior Promotion Case Template (Outsource Shop)

## Summary

**One-sentence:** A promotion-case template tuned for outsource-services companies, where promotion rubrics weight technical scope, revenue-to-account, and billable utilization together.

**One-paragraph:** STAR works for interviews; outsource shops (SoftServe, EPAM, Globant, Andela, GlobalLogic, Infopulse, N-iX, …) run internal promotion reviews on a tri-axis rubric that pure STAR doesn't address — promoters need to show technical contribution AND revenue/account expansion AND utilization rate. This methodology gives the candidate a structured artefact: scope evidence (commits, design docs, client-visible deliverables), revenue evidence (account growth, scope-creep won, salvage stories), and utilization evidence (billable %, bench avoidance). Output is a 4-6 page case PDF the promotion committee can score line-by-line.

## Applies If (ALL must hold)

- you work at a services / outsource / consulting firm with formal promotion windows
- the firm uses a multi-axis rubric (technical + business + utilization) for senior+ promotions
- you have ≥ 6 months of measurable client work to cite
- tier == pro or higher

## Skip If (ANY kills it)

- you work at a product company (use a standard performance-review template instead)
- the promotion is mandatory / automatic by tenure (no case needed)
- your firm explicitly bans self-promotion cases (must follow internal alternative)

## Prerequisites

- access to your billing/utilization dashboard
- list of accounts/projects you've contributed to in the window
- manager pre-alignment on which rubric axes matter most for your role

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter` | parent role/operating context |
| `pro/comms/executive-stakeholder-demo-narrative-frame` | sibling narrative-framing methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + 1 worked rubric example | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_evidence` | sonnet | structured pull from candidate's notes / dashboards |
| `draft_case_narrative` | sonnet | bounded narrative around rubric axes |
| `committee_devil_review` | opus | adversarial pre-review against rubric |

## Related

- parent skill: `pro/comms/`
- `pro/comms/hr-recruiter`
- upstream playbook: `p4-outsource-specialist/Senior promotion case prep (every 6 months)`
