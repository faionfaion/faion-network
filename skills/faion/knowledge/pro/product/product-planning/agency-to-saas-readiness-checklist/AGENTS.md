---
slug: agency-to-saas-readiness-checklist
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "dd0b121e0b3981cf"
summary: Structured readiness audit for an agency planning a SaaS pivot — IP rights, repeatable assets, codebase ownership, retainer-base stability, founder bandwidth.
tags: [agency-to-saas, pivot, productization, readiness-checklist, ip-rights, codebase-ownership]
---
# Agency-to-SaaS Readiness Checklist

## Summary

**One-sentence:** Structured readiness audit for an agency planning a SaaS pivot — IP rights, repeatable assets, codebase ownership, retainer-base stability, founder bandwidth.

**One-paragraph:** Agencies chasing the SaaS exit underestimate the 5 pre-requisites that decide whether the pivot is viable: (1) IP rights — do your client SOWs grant the agency derivative rights or did the client own IP? (2) repeatable IP — have you shipped the same shape of solution ≥ 3 times? (3) codebase ownership — is the code yours to repackage or is it stuck inside client repos? (4) retainer-base stability — is the agency's cash flow stable enough to fund a 9-12 month SaaS build? (5) founder bandwidth — who runs the agency while the SaaS gets built? The checklist scores each on 0/1/2 with red-flag thresholds. Output: a readiness score + a decision (ready / pre-work needed / not viable).

## Applies If (ALL must hold)

- agency / consultancy with ≥ 12 months operating history
- founder actively considering a SaaS pivot or product spin-off
- there is a candidate SaaS idea informed by repeat agency work
- founder owns equity / control of the agency (decision rights to pivot)
- 9-12 months of operating runway available OR a clear path to it

## Skip If (ANY kills it)

- &lt; 12 months of agency history — too early to know what's repeatable
- founder hasn't validated SaaS demand at all — do JTBD / problem-validation first
- agency revenue declining quarter-over-quarter — fix the agency first
- founder is the sole revenue earner with no operational redundancy — pivot will collapse both businesses

## Prerequisites (must be true before starting)

- list of all SOWs from past 24 months with IP clauses readable
- repository inventory (client repos vs. agency-owned repos vs. shared)
- retainer client list with start dates + monthly value + concentration metrics
- founder time allocation map (hours/week on agency ops vs. sales vs. delivery)
- candidate SaaS idea + a 1-page hypothesis about target customer + price

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher/agency-revenue-mix-audit-template` | Source of retainer stability + productizable-deliverable data |
| `pro/pm/project-manager/agency-pnl-tracker-template` | Source of runway + cash-flow data |
| `solo/research/researcher/problem-validation` | Required preceding step (validate SaaS demand before pivot decision) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 5-dimension scoring, IP-clause audit mandatory, repeatable-evidence threshold, retainer-base buffer, founder-replacement plan | ~900 |
| `content/02-output-contract.xml` | essential | Score schema, decision schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (IP hubris, copyright underground, productize-once illusion, runway-fantasy, founder-irreplaceable, deferred-no decision) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sow_ip_clause_extraction` | sonnet | Per-SOW reading: who owns derivative work |
| `repeatable_asset_inventory` | opus | Cross-project synthesis: what shape repeats |
| `runway_stress_test` | sonnet | Compute survival under retainer churn scenarios |
| `decision_recommendation_synthesis` | opus | Cross-dimension judgment for ready/not |

## Templates

| File | Purpose |
|------|---------|
| `templates/readiness-scorecard.md` | 5-dimension score card with evidence |
| `templates/sow-ip-audit.md` | Per-SOW IP clause documentation |
| `templates/runway-stress-test.md` | Cash-flow model with 3 churn scenarios |
| `templates/founder-replacement-plan.md` | Who runs agency operations during the pivot |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/extract-ip-clauses.py` | Parse SOWs for IP-rights language | Audit setup |
| `scripts/compute-readiness-score.py` | Aggregate dimensions + map to decision | Audit close |
| `scripts/runway-stress-test.py` | 3-scenario cash flow simulation | Decision support |

## Related

- parent skill: `pro/product/product-planning/`
- peer methodologies: `agency-revenue-mix-audit-template`, `agency-pnl-tracker-template`, `competitive-positioning`
- external: [Built to Sell (Warrillow)](https://builttosell.com/) · [Pivot to Profit (Constantin Bjerke)](https://medium.com/@constantinbjerke) · [The Mom Test (Fitzpatrick)](https://www.momtestbook.com/)
