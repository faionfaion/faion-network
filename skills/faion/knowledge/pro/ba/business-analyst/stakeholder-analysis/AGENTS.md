---
slug: stakeholder-analysis
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A six-step methodology that identifies all parties affected by or influencing a change initiative, maps them on a 2x2 influence-vs-impact matrix (Manage Closely / Keep Satisfied / Keep Informed / Monitor), documents individual needs, concerns, and communication preferences, plans engagement cadence per quadrant, and stores the register as a YAML file in git so diffs become the relationship history.
content_id: "42ba2d9d896f76bf"
tags: [stakeholder-management, engagement, requirements, change-management, risk-mitigation]
---
# Stakeholder Analysis

## Summary

**One-sentence:** A six-step methodology that identifies all parties affected by or influencing a change initiative, maps them on a 2x2 influence-vs-impact matrix (Manage Closely / Keep Satisfied / Keep Informed / Monitor), documents individual needs, concerns, and communication preferences, plans engagement cadence per quadrant, and stores the register as a YAML file in git so diffs become the relationship history.

**One-paragraph:** A six-step methodology that identifies all parties affected by or influencing a change initiative, maps them on a 2x2 influence-vs-impact matrix (Manage Closely / Keep Satisfied / Keep Informed / Monitor), documents individual needs, concerns, and communication preferences, plans engagement cadence per quadrant, and stores the register as a YAML file in git so diffs become the relationship history. The register is a living artifact refreshed at minimum quarterly.

## Applies If (ALL must hold)

- Kickoff of any cross-functional initiative with more than five named parties (sponsor, SMEs, end users, regulator, vendor)
- Migration/replacement projects where end-user resistance is the dominant risk
- Regulated programs (HIPAA, GDPR, SOX, MDR) — the regulator is a mandatory stakeholder
- M&A and reorg work where the political map is unstable; rerun the matrix every 2-4 weeks
- Pre-RFP/vendor-selection work where the buying committee has hidden influencers (security, procurement, legal)
- Triggered automatically when CHANGELOG or `stakeholders/register.yaml` has not been touched for 90 days on an active initiative

## Skip If (ANY kills it)

- Solo founder pre-PMF with fewer than three people involved — go directly to customer interviews
- Strictly internal engineering refactors with no business stakeholder change — RACI alone is sufficient
- Public open-source projects with anonymous community contributors — influence/impact axis is meaningless; use governance patterns
- One-off bug fixes or hotfixes — the stakeholder map will be stale before the deploy completes

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
