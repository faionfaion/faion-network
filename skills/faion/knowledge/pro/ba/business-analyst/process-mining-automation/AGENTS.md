---
slug: process-mining-automation
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A data-driven methodology for discovering actual process execution from IT event logs and identifying automation candidates using objective scoring criteria.
content_id: "63c361296bd7dd91"
tags: [process-mining, automation-assessment, rpa, event-logs, data-driven]
---
# Process Mining and Intelligent Automation Analysis

## Summary

**One-sentence:** A data-driven methodology for discovering actual process execution from IT event logs and identifying automation candidates using objective scoring criteria.

**One-paragraph:** A data-driven methodology for discovering actual process execution from IT event logs and identifying automation candidates using objective scoring criteria. Combines process mining tools (Celonis, Disco, ProM) to reconstruct real process flows, conformance checking against documented processes, and an automation readiness matrix that scores candidates on volume, standardization, stability, digital input, error rate, and ROI potential. Produces an automation assessment report with full/partial/no-go recommendations.

## Applies If (ALL must hold)

- Pre-RPA or intelligent automation initiative where automation candidates must be ranked objectively
- Process variance analysis where conformance checking reveals deviations between documented and actual flows
- Cost reduction initiative where high-volume, rule-based processes need to be identified from system data
- Audit or compliance context where process evidence must come from system logs, not interviews
- Digital transformation assessment needing a portfolio of automation opportunities with ROI estimates

## Skip If (ANY kills it)

- Processes with no digital event trail (fully manual, paper-based) — mining requires event logs
- Highly creative or judgment-intensive processes (strategy, design) — automation readiness score will be below threshold
- Processes changing faster than the mining cycle — the discovered model is stale before recommendations land
- Organizations without access to process mining tooling or data engineering capability to extract event logs
- When the goal is process improvement rather than automation — use BPMN and business process analysis instead

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

- parent skill: `pro/ba/business-analyst/`
