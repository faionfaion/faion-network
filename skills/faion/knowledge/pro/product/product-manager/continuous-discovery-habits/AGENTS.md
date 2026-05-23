---
slug: continuous-discovery-habits
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Weekly customer-discovery cadence where the Product Trio (PM, Design, Tech) maintains an Opportunity Solution Tree with verbatim-quote provenance and agent-assisted triage / coding / synthesis.
content_id: "ff40be6332b952b3"
complexity: deep
produces: playbook-step
est_tokens: 6100
tags: [product-discovery, continuous-discovery, opportunity-solution-tree, customer-research, product-trio]
---
# Continuous Discovery Habits

## Summary

**One-sentence:** Weekly customer-discovery cadence where the Product Trio (PM, Design, Tech) maintains an Opportunity Solution Tree with verbatim-quote provenance and agent-assisted triage / coding / synthesis.

**One-paragraph:** Weekly customer-discovery cadence (≥1 interview/week) where the Product Trio maintains an Opportunity Solution Tree (OST). Every roadmap item traces to a verbatim quote with participant-id + interview-date; opportunities are problem-shaped (never 'build X'); the tree is pruned monthly. Agents automate mechanical work — feedback triage, transcript coding, weekly tree-diff synthesis — under explicit token budgets. Output: tree-as-YAML + weekly discovery readout + roadmap-input delta.

**Ефективно для:**

- PM-owned продукт із потребою захищеного weekly cadence (≥1 інтерв'ю/тиждень).
- Roadmap, що дрейфує в feature-list — leadership не пояснює outcome за пунктами.
- Product Trio, який тільки формується і шукає shared artefact для синхронізації.
- Quarterly planning synthesis — агенти зводять 60-80 інтерв'ю в свіжий OST.

## Applies If (ALL must hold)

- PM owns one product area and needs a defensible weekly cadence (one interview/week minimum).
- Roadmaps drifting to feature-list mode — leadership cannot articulate what outcome each item serves.
- Product Trio is forming and needs a shared artifact to triangulate on.
- Quarterly planning prep — agents synthesize 60-80 interviews into a refreshed OST that becomes input to roadmap, OKRs, and discovery sprints.
- Solo PM at a startup wants an LLM to triage support tickets, NPS verbatims, sales-call recordings into the OST as candidate opportunities for trio review.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with founder-led customer development — use customer-development methodology.
- Regulated domains where weekly outside-customer interviews require legal review per touchpoint.
- B2B with fewer than 20 logo accounts and a 12-month sales cycle — weekly interviews are not sustainable.
- Mature growth-stage where experimentation-at-scale has displaced qualitative discovery as the primary loop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Outcome metric | string + movability check | PM / leadership |
| Customer roster | table {segment, recency, plan_tier, churn_status} | CRM / billing |
| Transcript store | text/audio per interview | Zoom / Otter / Granola |
| OST current state | YAML | previous week's commit |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Trio decision-rights + sponsor cadence inform the OST review meeting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology covering provenance, cadence, prune, trio-prep | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for OST node + weekly readout + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: outcome → interview → code → synthesize → trio decide | 800 |
| `content/06-decision-tree.xml` | essential | Apply / skip routing on observable signals → rule from 01-core-rules.xml | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feedback-triage` | haiku | High-volume taxonomy categorisation. |
| `interview-prep` | sonnet | Structured authoring with past-behaviour anchoring. |
| `ost-synthesizer` | opus | Cross-corpus reasoning over coded quotes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | OST-as-YAML skeleton with outcome → opportunity → solution → assumption-test fields. |
| `templates/weekly-discovery.md` | Weekly discovery readout template with shipped / coded / tree-diff / next-week sections. |
| `templates/ost-apply.py` | Apply a tree-diff (JSON-patch / YAML-diff) to the current OST file. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-discovery-habits.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[stakeholder-management]]
- [[product-analytics]]
- [[experimentation-at-scale]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
