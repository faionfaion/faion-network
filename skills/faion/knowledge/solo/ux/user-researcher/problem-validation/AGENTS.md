---
slug: problem-validation
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Validate a problem against an evidence hierarchy (paid > committed > engaged > stated > anecdote), apply Mom Test rewrites to avoid leading questions, output a PROCEED / PIVOT / KILL decision with a scored evidence log and a pre-declared kill threshold."
content_id: "bbd8dc64e2e0237f"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["problem-validation", "lean-startup", "mom-test", "evidence-hierarchy", "discovery"]
---
# Problem Validation

## Summary

**One-sentence:** Validate a problem against an evidence hierarchy (paid > committed > engaged > stated > anecdote), apply Mom Test rewrites to avoid leading questions, output a PROCEED / PIVOT / KILL decision with a scored evidence log and a pre-declared kill threshold.

**One-paragraph:** Pre-build problem validation prevents the most expensive bug: building the wrong thing right. This methodology stacks evidence against a hierarchy (paid > committed > engaged > stated > anecdote), forces Mom Test rewrites on every interview question to eliminate leading/hypothetical framing, requires a kill threshold declared BEFORE evidence is collected, and outputs a structured PROCEED / PIVOT / KILL decision with the evidence log attached. Downstream consumers (feature discovery, value-proposition design, MVP planning) read the decision without re-running interviews.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-MVP idea screening — is this problem worth building anything for?
- Pivot decisions when current product has weak retention and team suspects wrong problem.
- Founder due diligence — does the team have evidence the problem exists at the scale claimed?
- Customer-development sprints during the first 90 days of a new product.

## Skip If (ANY kills it)

- The problem has already been validated < 6 months old with the same segment.
- Engineering is already mid-build — validation now is theatre, not a gate.
- The decision in front of the team is solution-shape, not problem-existence — use prototype tests instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement draft | one paragraph | founder / PM notes |
| Target segment definition | segment doc | audience-segmentation output |
| Kill threshold declared | numeric criterion | written BEFORE evidence collection |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/pain-point-research` | sibling lens supplying pain evidence |
| `solo/ux/user-researcher/value-proposition-design` | downstream consumer of the validation decision |

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
| `templates/problem-validation.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-problem-validation.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-problem-validation.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[pain-point-research]]
- [[value-proposition-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
