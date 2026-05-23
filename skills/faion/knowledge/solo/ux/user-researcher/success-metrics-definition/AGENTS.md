---
slug: success-metrics-definition
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Before sprint planning or launch, define one North Star Metric and 3-5 Primary KPIs via AARRR (Acquisition / Activation / Retention / Revenue / Referral) with quantified baseline + target, exact measurement definitions, and vanity-vs-actionable classification."
content_id: "b6b9eab8b31c2f3d"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["success-metrics", "kpis", "aarrr", "north-star", "product-metrics"]
---
# Success Metrics Definition

## Summary

**One-sentence:** Before sprint planning or launch, define one North Star Metric and 3-5 Primary KPIs via AARRR (Acquisition / Activation / Retention / Revenue / Referral) with quantified baseline + target, exact measurement definitions, and vanity-vs-actionable classification.

**One-paragraph:** Teams that measure the wrong things, or too many things, waste energy on features that do not move the business. This methodology pins one North Star Metric (the single number the team agrees represents long-term value), 3-5 Primary KPIs partitioned by AARRR stage, exact measurement definitions (event name, filter rules, time window, exclusions), baseline data, target with deadline, and a vanity-vs-actionable classification per metric. Output: a metrics spec artefact consumed by dashboarding, OKR planning, and post-launch analysis.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-launch metric setup before any tracking event is implemented.
- Quarterly OKR planning when last quarter's metrics did not predict outcomes.
- Post-pivot reset when the previous metric set no longer matches the new product hypothesis.
- Onboarding a new growth or product hire who needs the canonical metric set.

## Skip If (ANY kills it)

- A current metrics spec < 90 days old exists and the product hypothesis has not changed.
- The team has no baseline data at all (cold-start) — run a 4-week instrumentation sprint first.
- The change in front of the team is a single experiment, not the strategic metric set — use the experiment design template instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product hypothesis | one-paragraph statement | PM / founder |
| Baseline analytics export | 4-week window | analytics tool |
| Stakeholder list | who reads which dashboard | engagement charter |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/use-case-mapping` | supplies the user-flow events the metric set measures |
| `solo/ux/user-researcher/feature-discovery` | consumes the metric set to score feature impact |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/success-metrics-definition.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-success-metrics-definition.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-success-metrics-definition.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[use-case-mapping]]
- [[feature-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
