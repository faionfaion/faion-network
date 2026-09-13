# Portfolio Evm Rollup Method

## Summary

**One-sentence:** Portfolio-level EVM rollup (PV/EV/AC + SPI/CPI per project, weighted aggregate) ready for executive monthly review — pins method, owner, evidence, outcome.

**One-paragraph:** Portfolio-level EVM rollup (PV/EV/AC + SPI/CPI per project, weighted aggregate) ready for executive monthly review — pins method, owner, evidence, outcome. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Director-level PM/portfolio manager-у — щоб щомісячна executive review показувала реальний margin, не вибіркову частину.

## Applies If (ALL must hold)

- At least 3 projects can each hand over a week-grain PV / EV / AC ledger export (CSV or JSON) with an export timestamp, as of one shared data date.
- Every fixed-bid project earns EV on accepted milestones or deliverables at contract value (milestone weight, 0/100 or 50/50), and its contract value is known.
- A named portfolio owner will sign the rollup before a scheduled executive review, and has written numeric variance thresholds (SPI / CPI floor, CV as a percent of BAC).
- Ledgers or previous rollups exist for the two prior data dates, so a three-period SPI / CPI trend can be shown.

## Skip If (ANY kills it)

- Fewer than 3 projects with a current ledger after stale ones are excluded — single-project EVM is enough.
- Projects report progress as self-assessed percent complete with no PV / EV / AC ledger — there is nothing to sum.
- Ledgers are kept in different currencies with no agreed conversion rate at the data date — the currency sum cannot be formed.
- The audience runs OKRs or burn-up only and no executive review consumes EAC, VAC and margin — the rollup is the wrong shape.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-project week-grain ledger export with BAC, PV, EV, AC per data date, contract type, EV method and export timestamp | CSV or JSON, one file per project | project PMs, from the project EVM tool |
| Variance threshold policy: `spi_min`, `cpi_min`, `cv_pct_of_bac_max` | section of the portfolio runbook | portfolio owner |
| Weighting policy naming a weight per project, when anything other than the currency sum is reported | Markdown or PDF policy document | portfolio owner |
| Contract value per fixed-bid project | contract register row | account lead / finance |
| Previous two rollups or ledger reads at the two prior data dates | JSON rollups matching `templates/skeleton.json` | portfolio runbook archive |
| Executive review date | calendar entry | leadership office |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/pm/ev-for-fixed-bid-outsource` | Source of the dual-ledger inputs for fixed-bid projects. |
| `geek/pm/project-manager/ai-earned-value-management` | Sensor-driven AC feed that lowers per-project EVM cost. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the rollup: one data date and currency, per-project rows with BAC / PV / EV / AC / SV / CV / SPI / CPI / EAC / VAC, EV method and EAC formula, stale projects apart, currency-sum aggregate with LOE separate, weighting beside unweighted, three-period trend, thresholds with narrative only beyond them, money block, owner sign-off; valid and invalid rollups; 8 forbidden patterns | ~5500 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | recommended | 8 steps: fix the data date and stale-flag late ledgers, record contract type and EV method, compute the per-project table, sum currency into portfolio SPI / CPI, print weighting beside unweighted, pull the three-period trend, apply thresholds and write narratives, money block and owner sign-off | ~1700 |
| `content/05-examples.xml` | recommended | Complete August rollup of a four-project portfolio with a fifth stale (fixed-bid milestone EV, LOE apart, strategic weight printed beside the currency sum, one escalated project) with a note per value, plus the same month reported the usual way and what the validator prints | ~2900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric-aggregate` | haiku | Pure math rollup. |
| `variance-extract` | sonnet | Bounded judgement: which variance to flag for execs. |
| `outcome-narrative` | opus | Cross-project synthesis for leadership. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton of the rollup artefact matching `content/02-output-contract.xml`: per-project EVM rows, stale projects, currency-sum aggregate with LOE apart, weighting, thresholds, money block, owner sign-off. |
| `templates/header.yaml` | Header block of the rollup: portfolio, owner, data_date, currency, reporting_period, executive_review_date. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-portfolio-evm-rollup-method.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ev-for-fixed-bid-outsource]]
- [[ai-earned-value-management]]
- [[delivery-maturity-rubric]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the rollup (≥3 projects + per-project EVM + owner + scheduled review), block (no per-project EVM), or skip (single project). Run before the first monthly review slot.
