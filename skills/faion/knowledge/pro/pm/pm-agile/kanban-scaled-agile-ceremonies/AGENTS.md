---
slug: kanban-scaled-agile-ceremonies
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Alternative agile cadences for continuous-flow teams (Kanban) and multi-team programs (SAFe).
content_id: "a161af1b8138677b"
tags: [kanban, safe, ceremonies, agile, continuous-flow]
---
# Kanban and Scaled Agile Ceremonies

## Summary

**One-sentence:** Alternative agile cadences for continuous-flow teams (Kanban) and multi-team programs (SAFe).

**One-paragraph:** Alternative agile cadences for continuous-flow teams (Kanban) and multi-team programs (SAFe). Kanban replaces fixed sprints with five cadences: daily standup (walk-the-board right-to-left), weekly replenishment, weekly service-delivery review, bi-weekly retrospective, and monthly strategy review. SAFe adds PI Planning (2-day, every 8-12 weeks), Scrum-of-Scrums (daily), PO Sync (weekly), and Inspect-and-Adapt (end of PI). The rule: throughput plus 85th-percentile cycle time beats velocity for forecasting; use Monte Carlo on these for date predictions.

## Applies If (ALL must hold)

- Continuous-flow teams (support, ops, data engineering) with no natural sprint boundary.
- Multi-team programs needing PI Planning and Scrum-of-Scrums coordination.
- Teams with high mid-sprint volatility (incident-heavy ops, content production).
- Platform teams serving many internal customers where replenishment fits better than sprint commitment.
- Hybrid ScrumBan setups: sprint planning kept for steering, WIP limits enforced for flow.

## Skip If (ANY kills it)

- A single team of fewer than 8 people with stable feature work — Scrum's ceremonies suffice.
- Pure project work with fixed end date and known scope — predictive cadences fit better.
- Organizations drowning in ceremonies; adding SAFe events without removing others causes revolt.
- Discovery-heavy product work where dual-track agile maps better than SAFe.
- Solopreneur or 2-person teams — overhead exceeds value; a personal Kanban board is enough.

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
