# Statistical Significance: Basics

## Summary

**One-sentence:** Foundational stats checklist for A/B testing: null hypothesis, p-value, alpha, statistical power, confidence intervals, and Type I/II errors — pre-test commitments only.

**One-paragraph:** Foundational stats checklist for A/B testing: null hypothesis, p-value, alpha, statistical power, confidence intervals, and Type I/II errors — pre-test commitments only. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Onboarding нового PM / growth analyst — спершу basics, потім application.
- Pre-test checklist щоб локнути alpha + sample size + MDE.
- Перед running першого A/B test у проєкті — basics як guardrail.
- Як reference під час test design review.

## Applies If (ALL must hold)

- Team що готує перший або відновлений A/B testing практикум.
- Доступ до даних для baseline rate (для power analysis).
- Stakeholder buy-in що тест має фіксовану horizon (no early-stop).

## Skip If (ANY kills it)

- Multi-arm bandit context — інша математика, інша methodology.
- Pre-revenue / pre-launch без conversion baseline — power analysis impossible.
- Already a stats-expert team — skip basics, go statistics-application.

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
| `templates/checklist-skeleton.md` | Statistical Significance: Basics skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Statistical Significance: Basics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-statistics-basics.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[statistics-application]]
- [[ab-testing-basics]]
- [[ab-testing-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
