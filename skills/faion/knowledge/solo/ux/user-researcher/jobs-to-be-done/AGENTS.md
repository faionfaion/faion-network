---
slug: jobs-to-be-done
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a job-statement artefact (functional + emotional + social dimensions, forces of progress, 8-stage job map) revealing why customers hire the product."
content_id: "8ec6f0d653b43606"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["jobs-to-be-done", "jtbd", "user-research", "product-positioning", "customer-motivation"]
---
# Jobs to Be Done (JTBD)

## Summary

**One-sentence:** Produces a job-statement artefact (functional + emotional + social dimensions, forces of progress, 8-stage job map) revealing why customers hire the product.

**One-paragraph:** Customers buy products to make progress in their lives — they 'hire' the product to do a 'job'. This methodology pins the job statement format ('When [situation], I want to [motivation], so I can [expected outcome]'), maps the four forces of progress (push, pull, anxiety, habit), and walks the 8-stage job map (define → locate → prepare → confirm → execute → monitor → modify → conclude) to reveal where the job breaks down. Output: a JTBD spec artefact downstream consumers (positioning, value-proposition design, switch interviews) read without re-doing the customer research.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Positioning a product against alternatives users currently 'hire' for the same job.
- Designing onboarding around the job, not the feature taxonomy.
- Diagnosing why a feature has high signup but low retention — the job context differs from the feature flow.
- Preparing the input for switch-interview / Mom Test sessions.

## Skip If (ANY kills it)

- The product has no live users yet — JTBD requires real switch evidence; use problem-validation first.
- A current JTBD artefact for the same primary user segment exists < 6 months old.
- The decision being made is a UI polish issue, not a product-strategy question — JTBD is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Switch interviews | transcripts (≥5 per segment) | recruited switchers from research repository |
| Primary user segment | segment definition | audience-segmentation output |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/problem-validation` | upstream evidence that the problem matters |
| `solo/ux/user-researcher/value-proposition-design` | downstream consumer of the JTBD output |

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
| `templates/jobs-to-be-done.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-jobs-to-be-done.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jobs-to-be-done.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[problem-validation]]
- [[value-proposition-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
