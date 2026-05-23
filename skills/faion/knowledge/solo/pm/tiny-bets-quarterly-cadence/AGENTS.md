---
slug: tiny-bets-quarterly-cadence
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Quarterly tiny-bets operating rhythm for indie portfolio operators: select \u22644 bets, commit, cull losers within 90 days \u2014 produces a versioned bet-record artefact per quarter."
content_id: "06b6aba45a349993"
complexity: medium
produces: checklist
est_tokens: 4000
tags: [tiny-bets-quarterly-cadence, pm, solo, indie-hacker, portfolio]
---
# Tiny Bets Quarterly Cadence

## Summary

**One-sentence:** Quarterly tiny-bets operating rhythm for indie portfolio operators: select ≤4 bets, commit, cull losers within 90 days — produces a versioned bet-record artefact per quarter.

**One-paragraph:** Indie / tiny-seed operators run their portfolio on a quarter-by-quarter bet cadence: pick ≤4 bets, commit at quarter start, cull the worst by mid-quarter, keep only winners into next quarter. Existing pm methodologies in faion target enterprise sprint/quarter cadences; the tiny-bets pattern is missing. This methodology produces a versioned bet-record (one row per bet: name, hypothesis, kill-criterion, time-box, owner, status) and an end-of-quarter rollup. ≤4 bets is the hard ceiling; ≥5 means the operator is hedging instead of betting.

**Ефективно для:**

- Indie hacker running ≥2 small SaaS products in a portfolio.
- Tiny-seed founder past Year-1 with predictable but stagnant revenue.
- Solo consultant productising 1-2 offers per quarter.
- Maker running newsletter + course + tool combinations.

## Applies If (ALL must hold)

- Operator has 1-3 live revenue streams plus capacity for new bets.
- Operator owns the calendar and can hard-cut a losing bet without team friction.
- A quarterly review window (≥30 min) is on the calendar.
- Operator can write a kill-criterion before starting a bet.

## Skip If (ANY kills it)

- Operator has only one product and no extra capacity — focus, do not bet.
- Revenue is below ramen profitability — survival, not bets.
- Operator's last 2 quarters had ≥5 bets and zero kills — discipline gap, not methodology gap.
- Bets are contractually committed (paid retainer) and cannot be killed mid-quarter.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Previous quarter bet record | yaml / md | last quarter file |
| Capacity estimate (hours/week) | int | operator self-report |
| Revenue baseline by product | csv / dashboard | billing system |
| Named owner for each candidate bet | handle | operator notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent solo-PM operating rhythm |
| `solo/product/multi-product-portfolio-management` | portfolio scoring inputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-tiny-bets-quarterly-cadence` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tiny-bets-quarterly-cadence.md` | Markdown skeleton for the checklist artefact, matching content/02-output-contract.xml |
| `templates/tiny-bets-quarterly-cadence.schema.json` | JSON Schema seed + filled fixture for the checklist artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tiny-bets-quarterly-cadence.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[anti-roadmap-template]]`
- `[[indie-portfolio-scorecard]]`
- `[[kill-or-keep-criteria]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
