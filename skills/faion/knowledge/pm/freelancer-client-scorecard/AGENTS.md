# Freelancer Client Scorecard

## Summary

**One-sentence:** Quarterly 5-axis client scorecard: rate, payment behaviour, scope discipline, growth potential, energy cost — surfaces drop/keep/expand decisions per client.

**One-paragraph:** Freelancer Client Scorecard delivers a defensible rubric artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo фрілансер з 5-15 активними/недавніми клієнтами і energy-drain patterns.
- Boutique consultant, що рік-у-рік перевертає portfolio за принципом 80/20.
- Bootstrapper, що готується відмовити токсичному клієнту і потребує decision-record.
- Two-person practice, що калібрує client-acquisition discipline через scorecard, не лише revenue.

## Applies If (ALL must hold)

- the operator has 3+ active or recent (last 12 months) freelance clients
- the operator captures or can reconstruct factual data per client (rate, payment lag, scope changes, growth signals)
- quarterly portfolio rebalance is a recurring discipline the operator commits to
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- operator has only 1-2 clients — scorecard insight is below noise, qualitative review is faster
- operator is closing the practice — portfolio rebalance is moot
- operator already runs a competing CRM scorecard with the same axes — do not duplicate

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
| `content/02-output-contract.xml` | essential | JSON Schema for the rubric + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelancer_client_scorecard` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-client-scorecard.md` | rubric skeleton with required fields + 5-line header |
| `templates/freelancer-client-scorecard.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-client-scorecard.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelance-capacity-model]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
