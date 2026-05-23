# Card Sorting

## Summary

**One-sentence:** Ask 15-20+ users to organise 30-60 content cards into groups and name them; produce a similarity-matrix-backed IA spec artefact identifying high-confidence groupings and ambiguous items before navigation is locked in.

**One-paragraph:** Navigation categories that make sense internally often fail users because they mirror org charts or product taxonomies rather than user mental models. This methodology runs card sorting (open for category generation, closed for validation), recruits 15-20 participants for open and 30+ for closed, uses 30-60 cards in user language, and analyses results via a similarity matrix and agreement scores. Output: an IA spec artefact naming high-confidence groupings, ambiguous items to re-test, and a recommended category structure with rationale per cluster.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Designing a new product's navigation when no precedent exists internally.
- Restructuring an existing IA when analytics show high search and low menu-click ratios.
- Renaming a confusing category that recurs in support tickets.
- Validating a proposed taxonomy before committing to nav implementation.

## Skip If (ANY kills it)

- The navigation is constrained by a third-party platform with fixed taxonomy.
- A < 12-month-old card-sort study exists with the same content set and target users.
- The product has fewer than ~15 content items — direct stakeholder review is cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Content inventory | 30-60 items | content audit |
| Target user definition | segment doc | audience-segmentation output |
| Recruiter capacity | 15-30 participants | research operations |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/content-audit-process` | supplies the content inventory cards are drawn from |
| `solo/ux/user-researcher/use-case-mapping` | supplies the user goals categories are tested against |

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
| `templates/card-sorting.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-card-sorting.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-card-sorting.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[content-audit-process]]
- [[use-case-mapping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
