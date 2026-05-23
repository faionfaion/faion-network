---
slug: feature-discovery
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Six-step process for identifying, validating, and prioritizing product features: four-source collection → Kano → opportunity score → effort → RICE → validate before build."
content_id: "1f1a6126cc40da6e"
complexity: deep
produces: spec
est_tokens: 4800
tags: ["feature-discovery", "product-prioritization", "user-research", "rice-framework", "kano-model"]
---
# Feature Discovery

## Summary

**One-sentence:** Six-step process for identifying, validating, and prioritizing product features: four-source collection → Kano → opportunity score → effort → RICE → validate before build.

**One-paragraph:** Feature decisions made on gut feeling or the loudest customer voice produce features nobody uses and miss features that drive adoption. This methodology separates discovery from prioritisation: collect from four source types (research, analytics, competitive, market), categorise via Kano, score Opportunity = Importance + max(Importance−Satisfaction, 0), estimate effort, prioritise via RICE = (Reach × Impact × Confidence)/Effort, then validate top-RICE candidates with fake-door / prototype / Wizard-of-Oz / limited beta before engineering commitment.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Quarterly roadmap planning when the backlog is full but priorities are unclear.
- Post-launch identification of next-build candidates based on usage data and support tickets.
- Competitive-gap analysis discovering features rivals have but the product lacks.
- Synthesising a large feature-request log (50+ items) into a prioritised shortlist.

## Skip If (ANY kills it)

- The core product is not yet working — feature discovery before PMF is premature optimisation.
- Only one vocal customer is requesting a feature — frequency matters; one voice is not signal.
- The team has already committed to a roadmap for the current quarter — discovery is for next cycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer interview notes | Markdown transcripts | research repository |
| Usage analytics export | CSV / dashboard | analytics tool (Amplitude / Mixpanel / GA) |
| Competitor feature matrix | spreadsheet | competitive-analysis output |
| Engineering effort estimates | XS/S/M/L/XL per candidate | engineering lead (NOT agent-generated) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/jobs-to-be-done` | separates "what users ask for" from "what job they need done" |
| `solo/ux/ux-researcher/competitive-analysis` | supplies the competitor feature matrix this consumes |

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
| `templates/feature-discovery.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-feature-discovery.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-discovery.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[jobs-to-be-done]]
- [[competitive-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
