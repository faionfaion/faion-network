# Freelance Insurance Buyers Guide

## Summary

**One-sentence:** Coverage-scoping artefact for E&O / professional liability / cyber: per-work-type recommended limits, named exclusions to watch, claims-made vs occurrence default, annual review trigger.

**One-paragraph:** Freelance Insurance Buyers Guide delivers a defensible report artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo фрілансер у US/EU, що бере проекти з material client-loss potential.
- Micro-agency (2-3 чол.) на пороги CAD/UK/EU compliance-grade engagements.
- Freelancer, що отримує клієнт-side вимогу 'show your E&O certificate' уперше.
- Bootstrapper, що оцінює risk-loaded pricing і потребує премію в overhead breakdown.

## Applies If (ALL must hold)

- the operator is a freelancer or micro-agency selling work that can cause material client loss
- operator is in a jurisdiction where professional liability insurance is purchasable as a sole trader / micro-entity
- annual revenue is large enough that policy premium is justifiable against the risk
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- operator works exclusively as an employee — employer policy covers liability
- the jurisdiction has no E&O market accessible to solo operators — defer to legal
- client mandates a specific named policy and broker — follow the mandate, do not re-scope

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelance_insurance_buyers_guide` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelance-insurance-buyers-guide.md` | report skeleton with required fields + 5-line header |
| `templates/freelance-insurance-buyers-guide.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-insurance-buyers-guide.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelance-msa-sow-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
