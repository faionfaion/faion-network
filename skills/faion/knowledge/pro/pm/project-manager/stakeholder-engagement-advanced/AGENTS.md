---
slug: stakeholder-engagement-advanced
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Move stakeholders one level at a time (Unaware → Resistant → Neutral → Supportive → Leading) via evidence-backed activities; classify by behaviour not assumed intent; detect drift via cadence-vs-last-touch.
content_id: "2e053b505b30b5a5"
complexity: deep
produces: spec
est_tokens: 4700
tags: [engagement-levels, stakeholder-movement, evidence-based, change-management, drift-detection]
---
# Stakeholder Engagement (Advanced)

## Summary

**One-sentence:** Move stakeholders one level at a time (Unaware → Resistant → Neutral → Supportive → Leading) via evidence-backed activities; classify by behaviour not assumed intent; detect drift via cadence-vs-last-touch.

**One-paragraph:** Structured process for moving stakeholders from current to desired engagement level (Unaware / Resistant / Neutral / Supportive / Leading) through targeted, evidence-based activities. Each level change requires a quoted behavioural signal — not a vibe. Move one level at a time; never plan a jump from Resistant directly to Leading. Build an Engagement Assessment Matrix with Power × Interest × Current × Desired × Gap × Next-Activity. Detect drift when last-touch exceeds cadence threshold with no blocker reason.

**Ефективно для:**

- Stakeholder Register exists but project lacks champions, has dormant supporters, or active resisters
- Pre-launch / change-management where adoption depends on department heads
- Long projects (>6 months) where engagement levels drift
- Coalition-building for portfolio shifts (M&A, reorg, platform migration)

## Applies If (ALL must hold)

- Stakeholder Register exists but the project lacks champions or has active resisters
- Pre-launch and change-management work where adoption depends on department heads
- Long projects (over 6 months) where engagement levels drift — quarterly re-assessment needed
- Coalition-building for portfolio shifts (M&A, reorg, platform migration)
- Public-facing launches where end users are Unaware and need to reach Supportive

## Skip If (ANY kills it)

- One-off small tasks with no organisational politics
- Adversarial negotiations (procurement, legal disputes) — engagement implies collaboration
- Crisis communications — different discipline, different cadence and tone
- Projects under 4 weeks with a single decision-maker

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder register | YAML | stakeholder-register methodology |
| Communications log | JSON / CSV | Slack / email metadata |
| Meeting minutes | Markdown | PM / facilitator |
| Cadence thresholds | config | team consensus |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-engagement]] | Quadrant strategies + base cadence |
| [[stakeholder-register]] | Register schema this methodology mutates |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: classify-from-behaviour-only, one-level-at-a-time, assessment-matrix-required, cadence-driven-engagement, drift-flag-on-cadence-breach | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-level-from-behaviour` | sonnet | Per-stakeholder evidence quote → level assignment |
| `draft-transition-plan` | sonnet | One-level-at-a-time activity sequence |
| `meeting-prep` | sonnet | Concerns + motivations + last interaction + desired outcome |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-plan.md` | Full engagement plan: assessment matrix + per-stakeholder strategy + activity table |
| `templates/meeting-prep.md` | Pre/post meeting brief for a single stakeholder interaction |
| `templates/assessment-matrix.csv` | Power × Interest × Current × Desired × Gap × Next-Activity schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-engagement-advanced.py` | Lint assessment matrix + one-level-at-a-time rule + evidence-required check | Pre-commit |
| `scripts/drift-detector.py` | Flag stakeholders past their cadence threshold with no recorded blocker | Weekly cron |

## Related

- parent skill: `pro/pm/project-manager/`
- [[stakeholder-engagement]]
- [[stakeholder-register]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
