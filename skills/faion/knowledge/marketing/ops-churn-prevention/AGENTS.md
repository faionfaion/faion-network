# Churn Prevention

## Summary

**One-sentence:** Three-phase churn-prevention playbook (early intervention / save offer / win-back) with reason-segmented actions and a stop-loss review trigger.

**One-paragraph:** Three-phase churn-prevention playbook (early intervention / save offer / win-back) with reason-segmented actions and a stop-loss review trigger. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- SaaS з визначеним baseline churn rate що готова інвестувати в reduction.
- Team має lifecycle-marketing tooling (Customer.io, Iterable, Braze, або equivalent).
- CS / Support data доступна для root-cause кодування cancellation reasons.
- Перед запуском великих save offers або win-back кампаній.

## Applies If (ALL must hold)

- ops-churn-basics уже виконано — baseline measured + cohort/plan segmented.
- Cancellation reason codes збираються (>= 5 codes, >= 100 cancels coded).
- Lifecycle-marketing tool здатний на segmented sends + drip cycles.

## Skip If (ANY kills it)

- Baseline churn не виміряний — спершу run ops-churn-basics.
- Cancellation reasons не кодуються — спершу запровадь reason capture.
- Discount-only страtegy без segment differentiation — це продаж знижок, не prevention.

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
| `templates/playbook-step-skeleton.md` | Churn Prevention skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Churn Prevention. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-churn-prevention.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[ops-churn-basics]]
- [[retention-strategies]]
- [[retention-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
