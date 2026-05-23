---
slug: heuristic-evaluation
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "3-5 expert evaluators independently audit a product against Nielsen's 10 usability heuristics; reconcile findings into a single severity-rated report identifying 60-75% of usability problems without user testing."
content_id: "432b0a5968c469ed"
complexity: deep
produces: report
est_tokens: 4800
tags: ["heuristic-evaluation", "usability-testing", "expert-review", "research-method", "nielsen-heuristics"]
---
# Heuristic Evaluation — Nielsen's 10 Usability Heuristics

## Summary

**One-sentence:** 3-5 expert evaluators independently audit a product against Nielsen's 10 usability heuristics; reconcile findings into a single severity-rated report identifying 60-75% of usability problems without user testing.

**One-paragraph:** Heuristic evaluation uses 3-5 expert evaluators to audit a product against Nielsen's 10 usability heuristics — visibility of system status, match with real world, user control, consistency, error prevention, recognition, flexibility, aesthetic and minimalist design, error recovery, help documentation. Evaluators audit independently, then reconcile findings with severity rating (cosmetic / minor / major / catastrophic). Output is a heuristic-evaluation report — typically catching 60-75% of usability problems for a fraction of the cost of moderated testing.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Mid-product quality pass when budget for moderated testing is constrained.
- Pre-release sanity check on a near-shipping flow.
- Onboarding a new designer or PM to the product's known usability state.
- Triage step before deciding whether full moderated testing is warranted.

## Skip If (ANY kills it)

- Fewer than 3 expert evaluators available — single-evaluator audits are biased and produce false confidence.
- A current heuristic evaluation < 6 months old already covers the same surface with no major changes since.
- The product is at sketch stage — heuristics are for implemented or prototyped flows, not paper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 3-5 expert evaluators | rostered with availability | research operations |
| Product surface to audit | staging URL or prototype | product team |
| Severity rubric | cosmetic / minor / major / catastrophic | pattern bank |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/error-prevention` | maps to Heuristic #5 |
| `solo/ux/ux-researcher/error-recovery` | maps to Heuristic #9 |
| `solo/ux/ux-researcher/consistency-standards` | maps to Heuristic #4 |

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
| `templates/heuristic-evaluation.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-heuristic-evaluation.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-heuristic-evaluation.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[error-prevention]]
- [[error-recovery]]
- [[consistency-standards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
