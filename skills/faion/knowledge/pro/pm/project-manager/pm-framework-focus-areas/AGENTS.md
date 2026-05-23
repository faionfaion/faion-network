---
slug: pm-framework-focus-areas
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: PMBoK 8 replaces rigid five Process Groups with five Focus Areas (Initiating, Planning, Executing, Monitoring and Controlling, Closing) distributed across seven Performance Domains.
content_id: "9c8d7e6f5a4b3c2d"
complexity: light
produces: rubric
est_tokens: 3400
tags: [pmbok-8, focus-areas, process-groups, lifecycle, framework]
---
# PMBoK 8 Focus Areas

## Summary

**One-sentence:** PMBoK 8 replaces rigid five Process Groups with five Focus Areas (Initiating, Planning, Executing, Monitoring and Controlling, Closing) distributed across seven Performance Domains.

**One-paragraph:** PMBoK 8 replaces rigid five Process Groups with five Focus Areas (Initiating, Planning, Executing, Monitoring and Controlling, Closing) distributed across seven Performance Domains.

**Ефективно для:**

- PM-ів, що мігрують ментальну модель з PMBoK 6/7 на PMBoK 8.
- PMO governance, що оновлює internal templates під нову structure.
- L&D teams, що переписують курси під 2026 ECO.
- Audit reviewers, що оцінюють project artefacts проти PMBoK 8.

## Applies If (ALL must hold)

- Org uses PMI / PMBoK as its primary framework.
- PM is updating templates / governance to PMBoK 8.
- Audit or certification regime expects PMBoK 8 alignment.
- Team is willing to re-map artefacts from Process Groups to Focus Areas.

## Skip If (ANY kills it)

- Org uses PRINCE2 or IPMA as primary framework.
- Pure agile org — Focus Areas don't translate cleanly.
- No upcoming audit / certification refresh.
- Team rejects PMBoK as bureaucratic.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[performance-domains-overview]] | Companion: Focus Areas spread across the 7 domains. |

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
| `artefact-mapper` | sonnet | Map each artefact to focus area × domain cell. |
| `rubric-renderer` | haiku | Emit the rubric report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/focus-area-rubric.md` | 5×7 matrix: Focus Area × Domain, populated with artefact references. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-framework-focus-areas.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[performance-domains-overview]]
- [[pm-certification-alignment-2026]]
- [[hybrid-delivery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (framework_primary, refresh_planned, audit_pressure) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
