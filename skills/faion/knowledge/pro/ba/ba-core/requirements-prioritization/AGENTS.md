---
slug: requirements-prioritization
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: All-Must MoSCoW, Confidence=100% RICE, and conference-room Kano produce false confidence in priority decisions.
content_id: "f45b9ffe6a9978ae"
tags: [prioritization, moscow, rice, kano, wsjf, requirements, backlog-management]
---
# Requirements Prioritization

## Summary

**One-sentence:** All-Must MoSCoW, Confidence=100% RICE, and conference-room Kano produce false confidence in priority decisions.

**One-paragraph:** All-Must MoSCoW, Confidence=100% RICE, and conference-room Kano produce false confidence in priority decisions. A selector that refuses to recommend a method when prerequisites are missing — and that flags data-quality problems per scored row — forces the team to surface gaps before committing resources. Six methods available: MoSCoW (release scope with 60/20/20 effort budget), RICE (reach * impact * confidence / effort, default Confidence to 0.8), Kano (survey-driven, ≥30 respondents required), WSJF (SAFe Cost-of-Delay / Job Size with floor at 1), weighted-sum (regulated contexts, cap at 7 criteria), and Value-Effort (quick triage for small backlogs). Always require a REQ-XXX ID and effort estimate before scoring; include a status-quo "do nothing" baseline row; run sensitivity analysis (±20% perturbation on most-leverage factor) to identify fragile rankings.

## Applies If (ALL must hold)

- New release scope decision with ≥30 candidate items and only ~30-40% can ship in the window — explicit method beats stack-rank-by-vibe
- An "everything is Must" MoSCoW already exists and you need a forcing function (RICE, weighted-sum, or WSJF) to break the tie with numbers
- Mid-sized backlog (50-200 items) where ordinal stack-rank no longer survives one round of input from a new stakeholder — switch to a scored method that re-ranks deterministically
- SAFe or PI planning context with a 100+ feature pool where Cost-of-Delay matters more than feature count — WSJF is the explicit fit
- Customer-satisfaction-driven products (consumer apps, hospitality) where survey data is available and the question is "which features delight vs which are baseline expectations" — Kano with real survey input
- Quick triage of a <30-item set where the BA needs a 1-hour Value-Effort matrix to separate quick wins from thankless work before more rigorous scoring
- Regulated or audited contexts where the priority decision must cite criteria and weights — weighted-sum with documented weights is the only defensible answer

## Skip If (ANY kills it)

- Pre-PMF discovery — locking priorities on speculative requirements creates false rigor; use opportunity-solution-trees instead
- Internal engineering work (refactors, tech debt, infra upgrades) — RICE and Kano measure user-facing value; technical-debt scoring (SQALE, DORA-aligned) is the right toolset
- Hard regulatory deadlines — those are constraints, not priorities; mechanically force them into Must/top-N, do not score against business value
- Items with no effort estimate from delivery — every method here divides or trades against effort; without it, the score is "value vs imagination"
- Fewer than 10 items, single decision-maker — a stack rank by the PO is faster than any of these methods and just as defensible
- Cash-flow or capex decisions with a real model — go to NPV, payback, or option value; do not collapse to a 0.25-3 impact scale that throws away precision

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

- parent skill: `pro/ba/ba-core/`
