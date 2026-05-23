---
slug: onboarding-30-day
tier: pro
group: comms
domain: hr
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: First-30-day phase: Week 1 orientation, Week 2 foundation, Weeks 3-4 deep-dive with first deliverable — milestone is contribution, not training completion.
content_id: "490671add71bfa02"
complexity: medium
produces: spec
est_tokens: 5000
tags: [onboarding, new-hire, 30-day-plan, milestones, hr]
---
# 30-Day Onboarding Phase

## Summary

**One-sentence:** First-30-day phase: Week 1 orientation, Week 2 foundation, Weeks 3-4 deep-dive with first deliverable — milestone is contribution, not training completion.

**One-paragraph:** First-30-day phase: Week 1 orientation, Week 2 foundation, Weeks 3-4 deep-dive with first deliverable — milestone is contribution, not training completion. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- генерація role-specific 30-day plans з universal template + team runbook.
- preboarding + Day 1 packet: welcome, equipment, week-1 calendar, doc links.
- tracking onboarding completion через HRIS/LMS APIs з 'behind plan' alerts.
- personalized check-in agendas (Day 7, 14, 30) based on progress.
- synthesizing 30-day survey across cohorts → systemic issue detection.

## Applies If (ALL must hold)

- generating role-specific 30-day plans (engineer, sales, support) from a universal template plus team runbook.
- producing pre-boarding and Day 1 packets: welcome email, equipment checklist, week 1 calendar invites, required doc links.
- tracking onboarding completion across new hires via HRIS/LMS APIs and surfacing 'behind plan' cases.
- drafting personalized check-in agendas (Day 7, 14, 30) based on hire progress.

## Skip If (ANY kills it)

- companies under 20 employees where each onboarding is bespoke.
- senior executives (VP/CXO) — bespoke high-touch work.
- contract or contingent workers with engagements shorter than 30 days.
- active reorg or RIF — build the plan after stabilization.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-30-day.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-onboarding-30-day.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[onboarding]]
- [[30-60-90-day-plan]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
