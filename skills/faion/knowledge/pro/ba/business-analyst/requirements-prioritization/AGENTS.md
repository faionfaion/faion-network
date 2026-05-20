---
slug: requirements-prioritization
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: BABOK-aligned methodology for BA-as-facilitator of multi-stakeholder prioritization.
content_id: "f45b9ffe6a9978ae"
tags: [requirements-prioritization, moscow, rice, kano, babok, business-analysis]
---
# Requirements Prioritization

## Summary

**One-sentence:** BABOK-aligned methodology for BA-as-facilitator of multi-stakeholder prioritization.

**One-paragraph:** BABOK-aligned methodology for BA-as-facilitator of multi-stakeholder prioritization. Picks the right method (MoSCoW / RICE / Kano / Value-Effort / WSJF / weighted-sum), runs elicitation and reconciliation, and ties the output back to the requirements catalog and delivery (backlog rank or release scope). Includes templates for release scope decisions where the BA must shrink a 200-item requirement set to a 30-item MVP/MMR with defensible rationale.

## Applies If (ALL must hold)

- Release scope decisions where the BA must shrink a 200-item requirement set to a 30-item MVP/MMR with a defensible rationale (regulated industries especially: auditors will ask "why this scope?").
- Cross-team backlog where Sales, Support, Engineering and Compliance each lobby for "their" items and the Product Owner needs an explicit method to break ties without drama.
- Vendor-RFP / RFI scoring where requirements are scored against multiple proposals — same matrix machinery, requirement IDs become rows.
- Pre-PI / pre-quarter prioritization in scaled agile (SAFe ART, LeSS) — WSJF over a 50–150 feature backlog where sequencing matters more than hard categories.
- After every elicitation wave when fresh requirements need to be slotted into the existing rank without reshuffling everything.
- When the team already produced a "everything is Must" MoSCoW and the BA needs a forcing function (RICE or weighted scoring) to break the tie.
- Whenever a stakeholder asks "why isn't my requirement in this release?" — the priority record is the answer.

## Skip If (ANY kills it)

- Discovery phase before product-market fit — locking priorities on speculative requirements creates false rigor; use opportunity-solution-trees and continuous-discovery instead.
- Single-team, single-PO, < 10 stories — a 1-D stack rank by the PO is faster than RICE.
- Pure cost optimization with quantified cash flows — go to NPV / payback, not 1-5 scoring which discards precision.
- Engineering-internal items (refactors, infra) — those need technical-debt-management criteria, not business-value scoring; BA does not own these.
- Hard regulatory deadlines — those are constraints, not priorities; route to the Won't/Must boundary mechanically and stop debating.
- When "the answer is already chosen" — a retrofitted prioritization to justify a decided scope damages BA credibility.

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
