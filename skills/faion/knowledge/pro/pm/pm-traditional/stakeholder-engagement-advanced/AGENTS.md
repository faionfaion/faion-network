---
slug: stakeholder-engagement-advanced
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Differentiate engagement strategy per stakeholder by current vs desired level, attaching measurable behavioural indicators and tracking week-over-week deltas.
content_id: "2e053b505b30b5a5"
complexity: medium
produces: spec
est_tokens: 4000
tags: [stakeholder-management, engagement, change-management, pmi]
---
# Stakeholder Engagement Advanced

## Summary

**One-sentence:** Differentiate engagement strategy per stakeholder by current vs desired level, attaching measurable behavioural indicators and tracking week-over-week deltas.

**One-paragraph:** Builds on `stakeholder-engagement`: each entry in the register gains an explicit strategy section, measurable behavioural indicators (baseline + target + evidence source), and a diff cycle that surfaces engagement-level changes between cycles. Used in transformations where moving stakeholders from `resistant` to `supportive` is itself a milestone with measurable signals.

**Ефективно для:**

- Transformations where moving stakeholders to supportive is a milestone.
- Programmes with resistant high-power stakeholders needing structured plans.
- Distressed-project rescue where engagement is the leading lever.
- Multi-org work needing behavioural-indicator measurement.

## Applies If (ALL must hold)

- Programme has at least one stakeholder at resistant or neutral level.
- Engagement movement is itself part of success criteria.
- Programme has bandwidth for per-stakeholder strategy work.
- Engagement diff cycle is run between weekly status reviews.

## Skip If (ANY kills it)

- Simple delivery where keep-informed monthly is enough.
- Stakeholder set is small and already supportive.
- No behavioural indicators are observable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| stakeholder-engagement register | YAML / JSON | stakeholder-engagement |
| Behavioural signal catalogue | doc | comms |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Provides the base register + cadence. |
| `communications-management` | Channels and templates for engagement actions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — strategy per stakeholder, measurable indicators, current-vs-desired delta, weekly diff, escalation thresholds | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for engagement plan + indicators | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: assess delta → choose strategy → set indicators → execute → diff | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `delta-analysis` | sonnet | Cross-stakeholder pattern reasoning. |
| `indicator-design` | opus | Designing measurable behavioural indicators is high-leverage. |
| `weekly-diff` | haiku | Mechanical diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-plan.md` | Per-stakeholder plan with strategy + indicators. |
| `templates/meeting-prep.md` | Per-meeting prep template with asks + signals. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-engagement-advanced.py` | Schema-validate engagement plan JSON. | Pre-commit + before review. |
| `scripts/engagement_diff.py` | Diff prior vs current register; surface NEW/CHANGED/CLOSED. | Weekly diff cycle. |

## Related

- [[stakeholder-engagement]]
- [[stakeholder-register]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the stakeholder-engagement-advanced input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
