---
slug: weekly-product-metrics-review
tier: solo
group: role-product-manager
persona: role-product-manager
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: North-star plus 3-5 leading indicators reviewed against target band; deviations have a hypothesis; one action item is filed per red metric.
content_id: 086061918f2b774f
methodology_refs:
  - reporting-basics
  - experimentation-at-scale
  - product-analytics
  - okr-setting
  - outcome-based-roadmaps-advanced
---

# Weekly product metrics review

## Context

North-star plus 3-5 leading indicators reviewed against target band; deviations have a hypothesis; one action item is filed per red metric.

Tier: **solo**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- Every metric has a documented RAG status.
- Every red metric has a written deviation hypothesis.
- Every red metric has exactly one owned action item.
- A calibration note exists for the next planning cycle.

## Steps

### 1. Refresh dashboard

Pull a clean snapshot before reading anything.

Tasks:
- Confirm data freshness for every panel.
- Note any panel with stale or broken data.
- Refresh derived calculations.

Outputs:
- Refreshed dashboard with freshness timestamps.

Decision gate: Advance when every panel is current or explicitly flagged stale.

### 2. Read against target band

Compare each metric to the target band, not to last week.

Tasks:
- For each metric, classify against band: green / amber / red.
- Avoid week-over-week framing for noisy metrics.
- Use rolling windows for low-volume metrics.

Outputs:
- RAG status per metric.

Decision gate: Advance when every tracked metric has a documented RAG status.

### 3. Hypothesise deviations

Every red gets a hypothesis before discussion.

Tasks:
- For each red metric, write a one-line cause hypothesis.
- Distinguish 'we know' from 'we suspect'.
- Tag external vs internal cause.

Outputs:
- Deviation hypothesis table.

Decision gate: Advance when every red metric has at least one hypothesis on paper.

### 4. File action items

Convert reds into single owned action items.

Tasks:
- File exactly one action item per red metric.
- Assign an owner and a check-back date.
- Tag the action against the originating bet.

Outputs:
- Action item list (one per red).

Decision gate: Advance when each red has exactly one filed action.

### 5. Calibration check

Sanity-check whether targets themselves are wrong.

Tasks:
- If 3+ greens hold for 4 weeks, ask if the target is too easy.
- If 3+ reds hold for 4 weeks, ask if the target is wrong.
- Log calibration findings for the next planning cycle.

Outputs:
- Target calibration note.

Decision gate: Required: a calibration note for the next planning cycle even if no change is proposed.

## Decision points

- WoW noise vs trend — use rolling windows; do not panic on a single week.
- Target-wrong vs metric-wrong — if the metric stops moving the business, the metric is wrong, not the team.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/reporting-basics`
- `pro/product/product-manager/experimentation-at-scale`
- `pro/product/product-manager/product-analytics`
- `solo/product/product-manager/okr-setting`
- `solo/product/product-manager/outcome-based-roadmaps-advanced`
- `solo/product/product-operations/product-analytics`
