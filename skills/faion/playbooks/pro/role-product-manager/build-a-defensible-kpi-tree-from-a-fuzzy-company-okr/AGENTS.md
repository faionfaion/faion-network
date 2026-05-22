---
slug: build-a-defensible-kpi-tree-from-a-fuzzy-company-okr
tier: pro
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: PM receives a vague top-level OKR (e.g.
content_id: 437e3267b8e2e222
methodology_refs:
  - product-analytics
  - okr-setting
---

# Build a defensible KPI tree from a fuzzy company OKR

## Context

PM receives a vague top-level OKR (e.g. 'improve user activation') and produces a leaf-level metric tree the team can move weekly, with vanity metrics flagged and ejected. Faion has solo OKR-setting but nothing on cascade mechanics, north-star design, or vanity-vs-actionable distinction.

Tier: **pro**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Restated OKR with one verb, population, time window.
- North-star metric defined and not vanity.
- Driver layer mathematically composes the north-star.
- Every leaf has owner + data source.

## Steps

### 1. Restate the fuzzy OKR

Convert the prose objective into a single measurable outcome.

Tasks:
- Write the OKR as a single sentence with a verb + outcome.
- Identify the population it applies to.
- Set the time window for measurement.

Outputs:
- Restated OKR doc.

Decision gate: Advance when the OKR has one verb, one population, and one time window.

### 2. Pick a north-star

Anchor on the one metric that proxies the outcome.

Tasks:
- Brainstorm 5 candidate metrics.
- Score each on actionability, proxying power, and gameability.
- Pick the one north-star metric.

Outputs:
- North-star metric definition.

Decision gate: Advance when the chosen metric beats vanity-metric tests (not gameable, moves with effort).

### 3. Decompose to drivers

Cascade the north-star into driver metrics.

Tasks:
- Decompose the north-star into 3-5 driver metrics.
- Tie each driver to a team or owner.
- Confirm drivers sum or multiply to the north-star.

Outputs:
- Driver-metric layer.

Decision gate: Advance when drivers mathematically compose the north-star.

### 4. Drop to leaves

Cascade drivers into weekly-actionable leaf metrics.

Tasks:
- For each driver, list 2-4 leaf metrics teams can move weekly.
- Tag each leaf with the team that owns it.
- Confirm each leaf has a data source.

Outputs:
- Leaf-metric layer.

Decision gate: Advance when every leaf is weekly-actionable and has a data source.

### 5. Vanity audit

Eject metrics that look good but do not move the business.

Tasks:
- Flag any leaf that moves without business outcome.
- Demote vanity metrics to 'monitor-only'.
- Document the demotion rationale.

Outputs:
- Vanity audit log.

Decision gate: Required: a written vanity audit log with at least one demotion or explicit 'none found' verdict.

## Decision points

- Sum vs multiplicative cascade — sum when drivers are additive (revenue components); multiplicative for funnels.
- Demote vs delete vanity metrics — demote (monitor-only) preserves history; delete only when the metric misleads.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/product-analytics`
- `solo/product/product-manager/okr-setting`
