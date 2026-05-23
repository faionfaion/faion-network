---
slug: freelance-capacity-model
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo-operator weekly capacity artefact: delivery vs pipeline vs self vs R&D hour budget, overcommitment alarms, monthly review cadence, suggested rebalances.
content_id: "d240b1bb7e10b10f"
complexity: medium
produces: spec
est_tokens: 5200
tags: [pm, pro, freelance, capacity, allocation, solo]
---
# Freelance Capacity Model

## Summary

**One-sentence:** Solo-operator weekly capacity artefact: delivery vs pipeline vs self vs R&D hour budget, overcommitment alarms, monthly review cadence, suggested rebalances.

**One-paragraph:** Freelance Capacity Model delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo freelancer, що бачить over-commit pattern і не може його кількісно описати.
- Two-person практика, що балансує delivery / sales / self-investment.
- Bootstrapper-консультант з кварталом R&D activity (продукт, контент, кейс-стаді).
- Founder, що моделює власну available capacity перед прийняттям наступного engagement.

## Applies If (ALL must hold)

- the operator is a solo or two-person freelance practice with billable + non-billable work
- weekly hours are countable (calendar, time-tracker, or honest self-report)
- the operator has authority to refuse, defer, or rebalance new requests
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- operator is on a full-time retainer covering ~100% of capacity — capacity model collapses to one client
- no time-tracking and no intent to start — model inputs would be invented
- team has 4+ billable people — switch to a team-level capacity model instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelance_capacity_model` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelance-capacity-model.md` | spec skeleton with required fields + 5-line header |
| `templates/freelance-capacity-model.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-capacity-model.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelancer-client-scorecard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
