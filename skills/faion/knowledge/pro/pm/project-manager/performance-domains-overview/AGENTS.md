---
slug: performance-domains-overview
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: PMBoK 7/8 eight performance domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) used as a project-health rubric.
content_id: "7e8f9a0b1c2d3e4f"
complexity: light
produces: rubric
est_tokens: 3500
tags: [pmbok, performance-domains, project-assessment, governance, framework]
---
# PMBoK Performance Domains Overview

## Summary

**One-sentence:** PMBoK 7/8 eight performance domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) used as a project-health rubric.

**One-paragraph:** PMBoK 7/8 eight performance domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) used as a project-health rubric.

**Ефективно для:**

- PMO health checks, де project health має бути порівняний across portfolio.
- Onboarding PM-ів, які потребують спільної vocabulary.
- Audit reviews, де assessor питає 'як ви покриваєте PMBoK 7 domains?'.
- Self-assessment по quarter end для project leads.

## Applies If (ALL must hold)

- Project lead willing to score domains qualitatively (red/amber/green).
- Project &gt;4 weeks duration — domains have time to manifest.
- PMO accepts qualitative scoring over quantitative metrics.
- Audit or governance requires PMBoK alignment.

## Skip If (ANY kills it)

- Project &lt;4 weeks — domains have no chance to manifest.
- Engineering-only solopreneur — overhead exceeds benefit.
- Org explicitly uses an alternative framework (e.g. PRINCE2-only).
- Team rejects framework-based assessment as bureaucratic.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-framework-focus-areas]] | Focus areas complement performance domains. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `domain-scorer` | sonnet | Score each domain red/amber/green with evidence. |
| `rubric-renderer` | haiku | Emit final rubric report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/domain-rubric.md` | 8-row rubric: domain, score, evidence, recommended action. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-performance-domains-overview.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[pm-framework-focus-areas]]
- [[hybrid-delivery]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (project_duration_weeks, pmo_requires_assessment, framework_alignment) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
