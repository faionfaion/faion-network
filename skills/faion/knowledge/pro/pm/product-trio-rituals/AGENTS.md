---
slug: product-trio-rituals
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pinned weekly ritual for the product trio (PM + design + eng) with mixed-method prioritisation scoring, named owners per discovery item, decision log, and outcome review.
content_id: "6e6819ab1e82eedf"
complexity: medium
produces: playbook-step
est_tokens: 3800
tags: [product-trio, rituals, discovery, pm-design-eng, decision-cadence]
---
# Product Trio Rituals

## Summary

**One-sentence:** Pinned weekly ritual for the product trio (PM + design + eng) with mixed-method prioritisation scoring, named owners per discovery item, decision log, and outcome review.

**One-paragraph:** Product Trio Rituals pin the weekly discovery + prioritisation session for the PM, design, and engineering triad. The artefact fixes attendance, agenda template, time-box per topic, and decision-log shape. Each item names an owner and an explicit desired outcome (decision needed). Decisions taken in the session feed forward into the discovery backlog; outcomes are reviewed at the next cycle. The methodology produces a versioned ritual artefact reviewed against outcomes weekly.

**Ефективно для:**

- Continuous-discovery teams with PM + design + eng cadence.
- Programmes that suffer prioritisation wars without ritual.
- Multi-team product orgs needing decision provenance.
- Distressed projects where misalignment between PM/design/eng is the leading lever.

## Applies If (ALL must hold)

- Trio (PM + design + eng) exists with named humans.
- Trio meets at least weekly with a published agenda.
- Decisions are logged in a version-controlled space.
- Discovery backlog is owned and groomed continuously.

## Skip If (ANY kills it)

- Solo-founder team (no trio yet).
- Trio members rotate per session — ritual never gels.
- Org runs a different ceremony covering the same purpose adequately.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Discovery backlog | MD / Notion / Linear | product |
| Prior decisions log | MD | trio |
| Trio member list | RACI / list | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Trio members are stakeholders themselves. |
| `communications-management` | Decision-log shape borrows comms-plan conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — fixed attendance, time-box per item, named outcome per item, decision-log per session, weekly review | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the session artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: prep → run → log → review → score | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping ritual state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prep-agenda` | haiku | Template fill from backlog priorities. |
| `synthesise-decisions` | sonnet | Capture decisions with rationale + owner. |
| `outcome-review` | opus | Cross-week synthesis of trio effectiveness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agenda.md` | Weekly trio agenda with time-box + outcomes. |
| `templates/scorecard.md` | Weekly scorecard tracking decisions + carryover. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-trio-rituals.py` | Schema-validate the session artefact. | Pre-commit + weekly. |

## Related

- [[product-planning]]
- [[communications-management]]
- [[stakeholder-engagement]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the product-trio-rituals input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
