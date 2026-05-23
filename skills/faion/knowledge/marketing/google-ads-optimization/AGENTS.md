# Google Ads Optimization Cycle

## Summary

**One-sentence:** Produces a Google Ads weekly + monthly optimization plan: bidding-strategy gate, negative-keyword rhythm, quality-score remediation, budget reallocation by ROAS bucket.

**One-paragraph:** Disciplined optimization loop: pick bidding strategy by conversion-history bucket (<30 conv → manual CPC, 30-100 → maximize-conversions, ≥100 → target-CPA / target-ROAS), run weekly negative-keyword sweep + quality-score remediation, monthly bid + budget rebalance across campaigns by ROAS bucket. Every change is logged + tested against learning-phase rule.

**Ефективно для:**

- Account з ≥30 days history + ≥30 conversions/month.
- Стабільний баланс daily change ≤25% + monthly major lift.
- Negative-keyword sweep weekly + QS remediation cycle.
- Budget rebalance по ROAS buckets monthly.

## Applies If (ALL must hold)

- Existing account with ≥30 days history and stable conversion volume.
- Cycle planning: weekly + monthly optimization rhythm.
- Quality Score remediation for keywords stuck below 5.
- Budget rebalance across campaigns by ROAS bucket.

## Skip If (ANY kills it)

- Accounts under 30 days — variance dominates; wait.
- <10 conv / month — manual CPC only; no smart bidding strategy works.
- Active learning-phase changes within the past 14 days — let signal settle first.
- Awareness-only campaigns — different KPI bucket.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Account audit + history | report | google-ads-basics |
| KPI target table | JSON | stakeholder |
| Conversion event taxonomy | schema | ads-conversion-tracking |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/google-ads-basics` | Foundation must be in place. |
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion signal feeds smart bidding. |
| `pro/marketing/ppc-manager/google-ads-reporting` | Reporting feeds the diagnosis loop. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for google-ads-optimization | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bidding-decision` | sonnet | Bucket choice + ROAS target. |
| `negative-sweep` | haiku | Mechanical cost-descending triage. |
| `budget-rebalance` | sonnet | Quartile-based reallocation with overrides. |

## Templates

| File | Purpose |
|------|---------|
| `templates/optimization-plan.md` | Monthly optimization plan Markdown skeleton. |
| `templates/change-log.csv` | Change-log CSV header. |
| `templates/optimization-plan.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-google-ads-optimization.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[google-ads-basics]]
- [[google-ads-reporting]]
- [[ads-conversion-tracking]]
- [[ads-budget-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
