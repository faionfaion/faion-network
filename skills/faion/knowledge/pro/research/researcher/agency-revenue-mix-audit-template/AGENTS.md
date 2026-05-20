---
slug: agency-revenue-mix-audit-template
tier: pro
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6868a356fc8b23df"
summary: Quarterly research audit that decomposes agency revenue into project / retainer / productized lines with gross margin per line and trend analysis.
tags: [research, agency, revenue-mix, margin, productization, business-model-research]
---
# Agency Revenue Mix Audit Template

## Summary

**One-sentence:** Quarterly research audit that decomposes agency revenue into project / retainer / productized lines with gross margin per line and trend analysis.

**One-paragraph:** Generic business-model research treats agency revenue as a single number; this audit decomposes it into the three operationally distinct lines and tracks margin per line + line-mix trend over 4-6 quarters. Mechanism: pull 6 quarters of revenue data, classify every invoice into project / retainer / productized / misc, compute gross margin per line (revenue - direct costs of delivery), compute concentration (top-3 client share within line + across all), compute line-mix trend (is retainer growing as % of total?). Output: a quarterly research report with 5 decision questions for the founder (raise rates, drop low-margin clients, productize, hire vs. contract, exit?).

## Applies If (ALL must hold)

- agency / consultancy with ≥ 6 quarters of revenue history
- founder makes strategic revenue-mix decisions quarterly (productize? raise rates? exit a line?)
- you have line-classified invoicing data OR can reconstruct from invoices + SOWs
- accounting software has gross-margin tracking OR direct costs are reconstructable per line

## Skip If (ANY kills it)

- &lt; 4 quarters of history — trend analysis is noise, not signal
- pure-project agency with no retainer aspiration — analysis still helps but lower ROI
- enterprise / 50+ person firm — different reporting framework needed (FP&amp;A team)
- accounting in shambles (uncategorized expenses, missing invoices) — fix bookkeeping first

## Prerequisites (must be true before starting)

- 6 quarters of invoiced revenue with client + SOW reference
- direct costs per invoice (contractor pay, tooling, third-party services)
- list of active retainers with monthly value and start/end dates
- list of productized offerings (if any) with unit count + price
- top-line P&L per quarter (revenue, COGS, opex, net)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/agency-pnl-tracker-template` | Weekly / monthly data source the audit consumes |
| `pro/research/researcher/business-model-research` | Broader business-model framing this audit slots into |
| `pro/product/product-operations/account-health-scoring-model` | Account health weights into top-3-client analysis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: line classification rigor, margin per line not just revenue, 6-quarter trend window, concentration cross-cut, 5-decision-question close | ~900 |
| `content/02-output-contract.xml` | essential | Audit report schema, line-mix trend schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (line drift, hidden direct costs, vanity revenue, productization theater, missing exit analysis, decision deferral) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `invoice_classification_per_line` | sonnet | Per-invoice judgment: project / retainer / productized / misc |
| `direct_cost_pull` | haiku | Lookup from accounting export |
| `trend_synthesis` | opus | Cross-quarter pattern detection (line growing, margin shrinking) |
| `decision_questions_synthesis` | opus | Translate findings into 5 founder-actionable questions |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-report.md` | Full audit report skeleton |
| `templates/line-mix-trend-chart.md` | 6-quarter stacked bar of revenue by line |
| `templates/margin-per-line-table.md` | Per-line gross margin trend |
| `templates/decision-question-set.md` | 5 founder-decision prompts based on findings |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/classify-invoices.py` | Map invoices to line based on SOW + contract pattern | Audit setup |
| `scripts/compute-margin-per-line.py` | Revenue - direct costs per line per quarter | Audit core |
| `scripts/detect-concentration-risk.py` | Cross-cut concentration by line + global | Audit close |

## Related

- parent skill: `pro/research/researcher/`
- peer methodologies: `business-model-research`, `agency-pnl-tracker-template`, `agency-to-saas-readiness-checklist`
- external: [Profit First (Michalowicz)](https://mikemichalowicz.com/profit-first/) · [Built to Sell (Warrillow)](https://builttosell.com/) · [Agency Profit Toolkit (Parakeeto)](https://parakeeto.com/blog/)
