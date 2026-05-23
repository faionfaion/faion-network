---
slug: statistics-application
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Applied significance-testing toolkit: raw-count templates, power analysis, 3 worked examples (significant / insufficient / underpowered), and Python helpers.
content_id: "1e8df61f60556d88"
complexity: deep
produces: report
est_tokens: 4200
tags: [statistics, significance, ab-testing, power-analysis, experiments]
---
# Statistical Significance: Application

## Summary

**One-sentence:** Applied significance-testing toolkit: raw-count templates, power analysis, 3 worked examples (significant / insufficient / underpowered), and Python helpers.

**One-paragraph:** Applied significance-testing toolkit: raw-count templates, power analysis, 3 worked examples (significant / insufficient / underpowered), and Python helpers. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Growth team що running регулярні A/B tests і потребує analysis discipline.
- Перед закриттям running test — щоб вирішити stop / continue / reject.
- Для квартальних experiment retrospectives — sanity check past calls.
- При onboarding нового PM / growth analyst — practical companion до statistics-basics.

## Applies If (ALL must hold)

- statistics-basics уже виконано — N hypothesis / alpha / power вкорінені.
- Доступ до raw counts (n1, x1, n2, x2) — НЕ percentages alone.
- Power analysis виконано pre-test (sample size locked).

## Skip If (ANY kills it)

- Only headline percentages, no raw counts — не запускай тест аналіз.
- Sample size not pre-committed — це не A/B test, це fishing expedition.
- Multi-arm bandit running, не fixed-horizon test — інша математика.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/report-skeleton.md` | Statistical Significance: Application skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Statistical Significance: Application. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-statistics-application.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[statistics-basics]]
- [[ab-testing-basics]]
- [[growth-experiment-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
