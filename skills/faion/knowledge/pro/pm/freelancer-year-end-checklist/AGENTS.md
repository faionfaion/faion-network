---
slug: freelancer-year-end-checklist
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Annual end-of-year SOP: books reconciled, taxes prepped, legal (renewals, insurance, MSA review), portfolio scorecard, next-year revenue model — single-page run-list.
content_id: "5bdcb724d4a89b4f"
complexity: medium
produces: checklist
est_tokens: 5200
tags: [pm, pro, freelance, year-end, checklist, annual]
---
# Freelancer Year-End Checklist

## Summary

**One-sentence:** Annual end-of-year SOP: books reconciled, taxes prepped, legal (renewals, insurance, MSA review), portfolio scorecard, next-year revenue model — single-page run-list.

**One-paragraph:** Freelancer Year-End Checklist delivers a defensible checklist artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Solo P3 фрілансер з простою бухгалтерією і потребою в annual checkpoint.
- Boutique consultant з кількома jurisdictions і нагадуваннями про renewals.
- Bootstrapper, що готує річну ревю до tax-preparer-а без surprises.
- Founder-CEO мікро-агенції, що замикає рік без bookkeeper-а але хоче audit-trail.

## Applies If (ALL must hold)

- the operator runs a freelance practice with year-end obligations (books, taxes, renewals)
- the practice has been active long enough to need formal reconciliation (≥ 6 months)
- the operator commits to running the checklist within 30 days of fiscal year-end
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- operator hires an external bookkeeper / lawyer that produces the equivalent run-list — do not duplicate
- the practice is mid-pivot and most line items are moot (closing entity, switching country) — defer until structure stable
- operator already runs a competing SOP that covers all line items — use the existing one

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
| `content/02-output-contract.xml` | essential | JSON Schema for the checklist + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-freelancer_year_end_checklist` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-year-end-checklist.md` | checklist skeleton with required fields + 5-line header |
| `templates/freelancer-year-end-checklist.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-year-end-checklist.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[freelance-capacity-model]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
