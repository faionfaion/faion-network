---
slug: hybrid-delivery
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Program-level framework that mixes predictive (waterfall) and agile delivery modes per workstream, with explicit handoff contracts between modes.
content_id: "c2b1a0f9e8d7c6b5"
complexity: medium
produces: spec
est_tokens: 4300
tags: [hybrid, agile, waterfall, program-management, governance]
---
# Hybrid Delivery

## Summary

**One-sentence:** Program-level framework that mixes predictive (waterfall) and agile delivery modes per workstream, with explicit handoff contracts between modes.

**One-paragraph:** Program-level framework that mixes predictive (waterfall) and agile delivery modes per workstream, with explicit handoff contracts between modes.

**Ефективно для:**

- Програм із regulated workstream (waterfall) + R&D workstream (agile).
- Корпорацій, що мігрують з повного waterfall до agile поступово.
- Великих vendors зі змішаним customer base (enterprise vs SMB).
- Проектів, де hardware (waterfall) + firmware/software (agile) переплітаються.

## Applies If (ALL must hold)

- Program has ≥2 workstreams with materially different delivery cadence.
- Workstream interfaces are stable enough to specify in advance.
- Governance accepts mode-per-workstream rather than mode-per-org.
- Each workstream lead can defend mode choice.

## Skip If (ANY kills it)

- Single workstream — pick one mode, not hybrid.
- Org politics force one mode despite mismatch — fix governance first.
- Workstream interfaces unstable — handoff contracts will churn.
- Project &lt;3 months — hybrid overhead dominates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-framework-focus-areas]] | PMBoK 8 framework backbone. |
| [[performance-domains-overview]] | Performance-domain vocabulary for both modes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workstream-classifier` | sonnet | Assign each workstream to predictive/agile. |
| `interface-contract-author` | opus | Author handoff contract between modes. |
| `governance-overlay-designer` | sonnet | Single governance layer over both modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hybrid-plan.md` | Program plan: workstream table with mode + handoff contracts. |
| `templates/interface-contract.md` | Handoff contract template: inputs, outputs, SLA, escalation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hybrid-delivery.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[pm-framework-focus-areas]]
- [[performance-domains-overview]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (workstream_count, interface_stability, governance_flexibility) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
