# Portfolio Evm Rollup Method

## Summary

**One-sentence:** Portfolio-level EVM rollup (PV/EV/AC + SPI/CPI per project, weighted aggregate) ready for executive monthly review — pins method, owner, evidence, outcome.

**One-paragraph:** Portfolio-level EVM rollup (PV/EV/AC + SPI/CPI per project, weighted aggregate) ready for executive monthly review — pins method, owner, evidence, outcome. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Director-level PM/portfolio manager-у — щоб щомісячна executive review показувала реальний margin, не вибіркову частину.

## Applies If (ALL must hold)

- Portfolio contains ≥3 projects each running ≥6 weeks.
- Each project tracks its own EVM (PV/EV/AC) at week-grain.
- An executive monthly review is scheduled.
- A named portfolio owner exists.

## Skip If (ANY kills it)

- Portfolio < 3 projects — single-project EVM is enough.
- Projects do not run EVM individually — rollup has nothing to aggregate.
- Org runs OKRs only (no EVM tradition) — rollup is wrong shape for the audience.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-project EVM ledgers | CSV/JSON | project PMs |
| Portfolio weighting policy | doc | portfolio owner |
| Executive review schedule | calendar | leadership office |
| Outcome-review template | Markdown | portfolio runbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/ev-for-fixed-bid-outsource` | Source of the dual-ledger inputs for fixed-bid projects. |
| `geek/pm/project-manager/ai-earned-value-management` | Sensor-driven AC feed that lowers per-project EVM cost. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
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
| `templates/skeleton.json` | JSON Schema for the portfolio rollup artefact: per-project metrics + weighted aggregate + outcome-review block. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-portfolio-evm-rollup-method.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ev-for-fixed-bid-outsource]]
- [[ai-earned-value-management]]
- [[delivery-maturity-rubric]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run the rollup (≥3 projects + per-project EVM + owner + scheduled review), block (no per-project EVM), or skip (single project). Run before the first monthly review slot.
