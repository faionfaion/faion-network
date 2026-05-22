---
slug: agile-hybrid-approaches
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A decision framework for selecting and tailoring a delivery mode — predictive (waterfall), agile (Scrum/Kanban), or a named hybrid pattern — based on six scored dimensions: requirement clarity, stakeholder engagement, risk tolerance, team agility, contract flexibility, and regulatory burden.
content_id: "033a37e36a311d7c"
tags: [hybrid, waterfall, scrum, kanban, delivery-mode]
---
# Agile and Hybrid Approaches

## Summary

**One-sentence:** A decision framework for selecting and tailoring a delivery mode — predictive (waterfall), agile (Scrum/Kanban), or a named hybrid pattern — based on six scored dimensions: requirement clarity, stakeholder engagement, risk tolerance, team agility, contract flexibility, and regulatory burden.

**One-paragraph:** A decision framework for selecting and tailoring a delivery mode — predictive (waterfall), agile (Scrum/Kanban), or a named hybrid pattern — based on six scored dimensions: requirement clarity, stakeholder engagement, risk tolerance, team agility, contract flexibility, and regulatory burden. "Hybrid" is never a hand-wave; the selected pattern must be named (Water-Scrum-Fall, agile-discovery-then-predictive, predictive-governance-over-agile-execution). LLMs default to "agile" for almost any prompt — force balanced scoring.

## Applies If (ALL must hold)

- Choosing a delivery mode at project kickoff given a known project context
- Re-evaluating mid-project when symptoms appear (waterfall slipping repeatedly, Scrum failing on fixed-price compliance)
- Designing a tailored hybrid for fixed-price clients
- Authoring the Development Approach section of a PMBoK 8 plan
- Coaching a team transitioning between approaches with explicit ceremony and artefact mappings

## Skip If (ANY kills it)

- Tiny projects under 4 weeks with a single well-scoped team — any methodology overhead beats the work itself; use a checklist
- Mandated-by-contract approaches (DoD waterfall, FDA validated software) — no degrees of freedom
- Pure operations / BAU work with no defined start/end — use Kanban + SLAs, not project methodology
- Research-heavy pre-PMF startups — approach selection is premature

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
