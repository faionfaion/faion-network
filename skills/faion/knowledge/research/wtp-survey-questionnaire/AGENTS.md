# WTP Survey Questionnaire

## Summary

**One-sentence:** Van Westendorp + Gabor-Granger questionnaire ready to run, with sample-frame rules, anchoring-bias controls, and a scoring sheet that emits an acceptable-price-range plus optimal-price-point report.

**One-paragraph:** Survey design is generic; pricing surveys are not. PMs running their first willingness-to-pay study without this methodology produce numbers that justify whatever they already wanted to charge. This methodology ships a Van Westendorp (four-question price-sensitivity meter) + Gabor-Granger (purchase-intent at price ladder) questionnaire, defines the minimum sample (n >= 200 per segment), forbids anchoring (no 'our current price is X' in stimulus), and scores the responses into an acceptable price range, an indifference point, and an optimal price point with confidence interval.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «wtp survey questionnaire» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you are pricing a new product or repricing an existing one with material revenue exposure.
- you can recruit n >= 200 in-target respondents per segment via panel, customer base, or list.
- you have a working product description or prototype to show as stimulus (not just a name).

## Skip If (ANY kills it)

- panel access is unavailable AND customer base is < 200 -- sample too small to score.
- the product is enterprise B2B sold in <50 accounts/year -- WTP surveys mis-fit; interview pricing instead.
- regulatory pricing (utility, insurance) where WTP is bounded by law, not preference.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the WTP Survey Questionnaire task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role/operating context. |
| `pro/research/researcher/survey-design` | general survey-design rules this pricing variant extends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wtp-questionnaire.md` | Four Van Westendorp questions + five-point Gabor-Granger ladder + segment screener. |
| `templates/wtp-scoring.md` | Scoring sheet: acceptable range / indifference point / OPP / CI columns. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wtp-survey-questionnaire.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[win-loss-interview-program]]
- [[thematic-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
