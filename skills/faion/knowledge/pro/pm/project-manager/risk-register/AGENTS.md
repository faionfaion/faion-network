---
slug: risk-register
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured log of identified threats and opportunities, each scored by probability x impact (1-25 scale), assigned a response strategy (Avoid/Transfer/Mitigate/Accept for threats; Exploit/Share/Enhance/Accept for opportunities), and owned by a named individual.
content_id: "370a99709358c1da"
tags: [risk-register, scoring, contingency, monitoring, opportunities]
---
# Risk Register

## Summary

**One-sentence:** A structured log of identified threats and opportunities, each scored by probability x impact (1-25 scale), assigned a response strategy (Avoid/Transfer/Mitigate/Accept for threats; Exploit/Share/Enhance/Accept for opportunities), and owned by a named individual.

**One-paragraph:** A structured log of identified threats and opportunities, each scored by probability x impact (1-25 scale), assigned a response strategy (Avoid/Transfer/Mitigate/Accept for threats; Exploit/Share/Enhance/Accept for opportunities), and owned by a named individual. Every Accept entry requires a contingency plan or amount. The register is a living artefact: reviewed weekly, updated on new signals, closed when risks pass or materialise.

## Applies If (ALL must hold)

- Standing up the uncertainty domain at project kickoff
- Weekly risk review cycles (diffing register against issue tracker and schedule)
- Pre-gate and steering-committee snapshots (top-N risks with response status)
- Vendor/supplier onboarding (category=External, contract clauses as triggers)
- Any milestone where "what could kill this?" deserves a written answer

## Skip If (ANY kills it)

- Pure-Scrum teams already tracking risks as backlog impediments — duplicate tracking splits attention
- Tasks under 1 week with a single owner — a standup question suffices
- Pre-discovery R&D where uncertainty is the work — use a learning log instead
- Risks already covered by a separate risk system (GDPR, security) — avoid reinventing

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/pm/project-manager/`
