---
slug: validation-methods
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Reference combining three pre-PMF validation lenses (Problem Validation, Pain Mining, Niche Viability Scoring) into one artefact; produces a triangulated discovery decision per opportunity covering whether the problem is real, painful, and in a market worth serving."
content_id: "777cac9b1c3eeadf"
complexity: medium
produces: spec
est_tokens: 4800
tags: ["validation", "pain-mining", "niche-scoring", "discovery", "user-research"]
---
# Validation Methods

## Summary

**One-sentence:** Reference combining three pre-PMF validation lenses (Problem Validation, Pain Mining, Niche Viability Scoring) into one artefact; produces a triangulated discovery decision per opportunity covering whether the problem is real, painful, and in a market worth serving.

**One-paragraph:** Early-stage discovery needs three simultaneous lenses: a problem may be real (validation) and painful (pain mining) but in a market too small or crowded to sustain a business (niche viability). This methodology stacks all three: Problem Validation (evidence hierarchy + 5-step process + PROCEED/PIVOT/KILL), Pain Mining (tiered sources + Pain Intensity Matrix), and Niche Viability (5-criteria weighted model: market size 25%, competition 20%, barriers 20%, profitability 20%, founder fit 15%). Output: a triangulated discovery decision artefact carrying all three lens results and a combined GO / NO-GO with rationale.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-MVP idea screening across multiple candidate opportunities.
- Founder due diligence — independent triangulation before committing engineering budget.
- Niche pivots — when the current niche is failing and the team is choosing the next one.

## Skip If (ANY kills it)

- Post-PMF — these lenses are pre-build instruments, not post-launch optimisation tools.
- A single lens already gave an unambiguous KILL (no need to triangulate).
- The team has zero customer access — start with cold pain mining only and defer the other lenses.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Opportunity list | one row per candidate | discovery brief |
| Access to all three lenses | capability audit | team capacity matrix |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/problem-validation` | lens 1 supplying evidence hierarchy + decision |
| `solo/ux/user-researcher/pain-point-research` | lens 2 supplying Pain Intensity Matrix scores |

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
| `templates/validation-methods.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-validation-methods.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-validation-methods.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[problem-validation]]
- [[pain-point-research]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
