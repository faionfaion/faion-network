# Churn Basics

## Summary

**One-sentence:** Computes a baseline churn-measurement report with customer churn rate, MRR churn rate, NRR, and segment breakdowns — gate for any retention intervention.

**One-paragraph:** Computes a baseline churn-measurement report with customer churn rate, MRR churn rate, NRR, and segment breakdowns — gate for any retention intervention. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- SaaS / subscription бізнеси що шукають baseline churn rate перед prevention work.
- Quarterly board prep що вимагає customer churn + MRR churn + NRR + segment breakdown.
- Діагностика чи pain — acquisition mix, нові-cohort onboarding, чи aging cohort decay.
- Перед запуском cohort-basics, ops-churn-prevention або health-score алертів.

## Applies If (ALL must hold)

- Subscription / usage-based бізнес що потребує baseline churn rate.
- Mature data: ≥ 3 повні місячні cohorts з ≥ 30 customers each.
- Ownership: визначений власник звіту з доступом до billing + product DB.

## Skip If (ANY kills it)

- Pre-revenue або < 3 повних місяців даних — sample too small.
- Один-time transactional бізнес без subscription — використовуй repeat-purchase rate.
- Annual-only contracts з < 2 renewal cycles.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source: three metrics together, voluntary vs involuntary split, compounded annualization, cohort × plan segmentation, leading-indicator health score, one written churn definition, customer churn alongside NRR, 90-day threshold backtest | 1550 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with symptom / root-cause / fix: lagging-only, linear annualization, aggregate hides cohort, untested thresholds, churn rate without leading indicators, annualize by twelve, alerts without backtest | 1050 |
| `content/04-procedure.xml` | essential | 7-step procedure plus the churn analysis process checklist: define churn, measure current churn, analyze patterns and root causes, segment, health score setup, dashboard and monitor; monthly-churn.sql and churn-report.md references | 1800 |
| `content/05-examples.xml` | medium | One worked end-to-end example plus metric formulas, benchmarks by segment, composite health score model, common churn reason distribution | 850 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml: preconditions, data maturity, three metrics, voluntary split, cohorts, leading indicators, written definition, backtested health score | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/report-skeleton.md.j2` | Churn Basics skeleton — fill per artefact, do not commit free-form output. |
| `templates/report-skeleton.md` | Churn Basics skeleton — fill per artefact, do not commit free-form output. Generated from `templates/report-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in Churn Basics. |
| `templates/_smoke-test.md` | Minimum viable filled-in Churn Basics. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/churn-report.md.j2` | ops-churn-basics — churn report |
| `templates/churn-report.md` | ops-churn-basics — churn report Generated from `templates/churn-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-churn-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ops-churn-prevention]]
- [[cohort-implementation]]
- [[retention-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
