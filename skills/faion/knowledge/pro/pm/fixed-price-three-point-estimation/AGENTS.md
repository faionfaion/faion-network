---
slug: fixed-price-three-point-estimation
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defensible fixed-price bid: per-leaf O/M/P in senior-dev hours, AI productivity factor, separate risk reserve, 10k Monte Carlo, P85 bid, disjoint pricing breakdown.
content_id: "a0320dca79d276ac"
complexity: deep
produces: spec
est_tokens: 5200
tags: [pm, pro, estimation, fixed-price, monte-carlo, outsource, bid]
---
# Fixed-Price Three-Point Estimation

## Summary

**One-sentence:** Defensible fixed-price bid: per-leaf O/M/P in senior-dev hours, AI productivity factor, separate risk reserve, 10k Monte Carlo, P85 bid, disjoint pricing breakdown.

**One-paragraph:** Fixed-Price Three-Point Estimation delivers a defensible spec artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Outsource P4 vendor, що бідає firm-price на 6-26 тиж integration project.
- Agency-side bid team з power-user spreadsheet або numpy/Excel.
- Founder-консультант, що проходить процедуру buyer procurement з audit-trail запитом.
- PMO, що навчає junior estimators дисципліні anchoring + reserve disclosure.

## Applies If (ALL must hold)

- the engagement is a fixed-price (firm-price) bid, not Time & Materials
- a WBS exists or can be drafted with leaf tasks at 1-5 dev-day granularity
- the team's senior developer hourly rate (loaded) is known
- a spreadsheet or scripting environment is available to run 10k Monte Carlo iterations

## Skip If (ANY kills it)

- the contract is Time & Materials — three-point estimation overhead is not justified
- the WBS is too coarse to estimate at leaf level (no leaves <1 week)
- scope is so volatile that no most-likely estimate is honest — bid no-bid or restructure as discovery + delivery

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
| `synthesize-fixed_price_three_point_estimation` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixed-price-three-point-estimation.md` | spec skeleton with required fields + 5-line header |
| `templates/fixed-price-three-point-estimation.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fixed-price-three-point-estimation.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[fixed-price-vs-tnm-decision-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
