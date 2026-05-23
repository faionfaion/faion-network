# Fixed-Price vs T&M Decision Framework

## Summary

**One-sentence:** Decision-record selecting Fixed-Price, T&M-capped, or Retainer for a specific engagement: trigger checklist + margin model + risk-buffer logic + recommended structure.

**One-paragraph:** Fixed-Price vs T&M Decision Framework delivers a defensible decision-record artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- P4 outsource lead, що приймає 'fixed чи T&M' рішення кілька раз на квартал.
- Solo фрілансер, що вибирає між firm-bid і capped T&M для одного клієнта.
- Founder-PM на cusp між project-work і retainer-model, потрібен audit-trail рішення.
- Sales engineer на pre-sales stage, що тренує win-rate проти конкурентів з різними pricing.

## Applies If (ALL must hold)

- a new engagement is being scoped and pricing structure is not contractually predetermined
- the buyer is open to discussion on Fixed-Price vs T&M vs hybrid arrangements
- scope volatility, change-request exposure, and AI productivity factor can be estimated
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- buyer mandates one structure as a hard procurement rule — defer
- engagement is a one-shot small consultation — pricing-model complexity unjustified
- the framework's input parameters cannot be filled without manufacturing numbers

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
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-fixed_price_vs_tnm_decision_framework` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixed-price-vs-tnm-decision-framework.md` | decision-record skeleton with required fields + 5-line header |
| `templates/fixed-price-vs-tnm-decision-framework.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-price-vs-tnm-decision-framework.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[fixed-price-three-point-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
