---
slug: freelancer-proposal-template-fixed-vs-tm
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Side-by-side proposal artefact for a single engagement: fixed-scope vs T&M-cap vs retainer table, tradeoffs, recommended structure, the buyer's decision in one column.
content_id: "7c1d15e721e874cd"
complexity: medium
produces: spec
est_tokens: 5200
tags: [pm, pro, freelance, proposal, pricing, fixed-price, tnm]
---
# Freelancer Proposal Template Fixed-vs-T&M

## Summary

**One-sentence:** Side-by-side proposal artefact for a single engagement: fixed-scope vs T&M-cap vs retainer table, tradeoffs, recommended structure, the buyer's decision in one column.

**One-paragraph:** Freelancer Proposal Template Fixed-vs-T&M delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo фрілансер з inbound lead і вибором між firm-bid, capped T&M, retainer.
- Boutique consultant, що тестує retainer pivot на існуючому клієнті.
- Bootstrapper в pre-sales call: 3-option proposal as anchor для discovery + commitment.
- Founder-PM, що калібрує win-rate проти конкурентів з різними pricing structures.

## Applies If (ALL must hold)

- an inbound lead has accepted a proposal request and pricing structure is open for discussion
- the operator can credibly support all three structures (fixed, T&M-cap, retainer)
- the buyer is sophisticated enough to choose between pricing models with tradeoffs surfaced
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- buyer mandates one pricing model in the RFP — do not waste capacity proposing alternatives
- engagement value is below the proposal-overhead threshold (e.g. < €5k) — short SOW suffices
- the operator cannot honestly support one of the three structures — drop it from the template

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
| `content/02-output-contract.xml` | essential | JSON Schema for the spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelancer_proposal_template_fixed_vs_tm` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-proposal-template-fixed-vs-tm.md` | spec skeleton with required fields + 5-line header |
| `templates/freelancer-proposal-template-fixed-vs-tm.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-proposal-template-fixed-vs-tm.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[fixed-price-vs-tnm-decision-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
