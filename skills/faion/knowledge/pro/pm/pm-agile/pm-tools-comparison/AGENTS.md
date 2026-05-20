---
slug: pm-tools-comparison
tier: pro
group: pm
domain: pm-agile
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured framework for evaluating and selecting project management tools through a weighted scoring matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%), a two-week proof-of-concept protocol, total cost of ownership (TCO) analysis, and an ADR template for recording the decision.
content_id: "16634738c92634c0"
tags: [tool-evaluation, pm-tools, decision-making, adr, weighted-scoring]
---
# PM Tools Comparison

## Summary

**One-sentence:** A structured framework for evaluating and selecting project management tools through a weighted scoring matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%), a two-week proof-of-concept protocol, total cost of ownership (TCO) analysis, and an ADR template for recording the decision.

**One-paragraph:** A structured framework for evaluating and selecting project management tools through a weighted scoring matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%), a two-week proof-of-concept protocol, total cost of ownership (TCO) analysis, and an ADR template for recording the decision. Covers Jira, Linear, ClickUp, GitHub Projects, GitLab Boards, Azure DevOps, Notion, Trello, and Asana.

## Applies If (ALL must hold)

- Selecting an initial PM tool for a new team or product.
- Re-evaluating an existing tool when pain points (speed, cost, integrations) accumulate.
- Building an ADR for a board or leadership review with quantitative scoring.
- Mid-migration sanity check: confirm the chosen tool actually scores higher on what mattered.

## Skip If (ANY kills it)

- Single-person projects — overhead exceeds gain; use whatever is already available.
- When the org has a mandated tool (e.g., Jira via enterprise contract) and switching is not on the table.
- Hotfix or firefighting periods — tool selection should not be the response to delivery problems.

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

- parent skill: `pro/pm/pm-agile/`
