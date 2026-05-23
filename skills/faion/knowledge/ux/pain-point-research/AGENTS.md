# Pain Point Research

## Summary

**One-sentence:** Five-step process producing a ranked pain log: define scope, mine four source tiers (complaints, questions, forums, job boards), categorise, score with Pain Intensity Matrix (frequency × severity × reach × spend × alternatives), extract root causes via 5 Whys.

**One-paragraph:** Discovering pain points without a source strategy produces confirmation bias — researchers look where they expect to find what they already believe. This methodology forces triangulation across four source tiers (direct complaints → questions/support → forum threads → job-board willingness-to-pay), categorises pains by type, scores each via Pain Intensity Matrix (frequency, severity, reach, spend, alternatives), and extracts root causes via 5 Whys before any solution work. Output: a ranked pain log spec, not an assumption list.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-build discovery for a product hypothesis with no prior pain inventory.
- Mid-product reset when retention drops and no one knows which pain caused the drop.
- Niche selection — finding which segment's pains are loud enough and high-spend enough to be worth solving.
- Quarterly refresh of the pain inventory after major market or feature changes.

## Skip If (ANY kills it)

- The product is post-PMF and the question is conversion-optimisation — use A/B testing, not pain mining.
- A < 90-day-old pain log already exists with PIM scoring for the same segment.
- The team has zero customer access (cold-start) — run problem-validation first to even get five interviews.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Defined research scope | segment + time-window | research plan |
| Access to all four source tiers | list of URLs / repositories | researcher prep |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/problem-validation` | sibling lens — pain mining feeds problem validation evidence |
| `solo/ux/user-researcher/user-validation-methods` | parent router covering the four lenses |

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
| `templates/pain-point-research.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-pain-point-research.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pain-point-research.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[problem-validation]]
- [[user-validation-methods]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
