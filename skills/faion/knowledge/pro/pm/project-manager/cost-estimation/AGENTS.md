# Cost Estimation

## Summary

Structured approach to producing a defensible project cost baseline: bottom-up estimation from a WBS, three-point (PERT) uncertainty modelling, risk-driven contingency reserve, and a separate management reserve. Output is a Cost Baseline plus Budget at Completion (BAC), versioned through every change-control event.

## Why

Projects fail financially because estimates omit indirect costs, ignore scope growth, and use flat contingency percentages instead of risk-driven reserves. Three-point estimation makes uncertainty explicit; separating contingency (PM-controlled) from management reserve (sponsor-controlled) prevents double-spending and provides a clear audit trail when the budget is challenged.

## When To Use

- Producing an initial budget for a feature, project, or RFP response.
- Bottom-up estimation from a WBS (each work package gets labor + tools + infra cost).
- Build-vs-buy / build-vs-SaaS decisions where opportunity cost must be quantified.
- Updating the cost baseline after a change-control event.
- Solopreneur "true cost" analysis — own time at market rate vs. out-of-pocket spend.

## When NOT To Use

- Agile teams estimating via story points + capacity-based run-rate — cost is derived from team-month spend, not bottom-up sums.
- Pre-discovery exploration where requirements are less than 30% defined — use ROM (rough order of magnitude, ±50%) instead; bottom-up output will be a fantasy.
- Fixed-fee contracts already signed — internal re-estimation has no contractual force and creates confusion.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Cost categories, five-step estimation process, PERT formula, contingency vs management reserve rules. |
| `content/02-examples.xml` | SaaS MVP phased estimate, solopreneur build-vs-buy analysis, common anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-worksheet.md` | Full cost breakdown with direct, indirect, reserves, and BAC sections. |
| `templates/quick-estimate.md` | Rapid labor + overhead + contingency formula for early-stage scoping. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/pert_estimate.py` | PERT mean, std-dev, P80, P95 from a WBS JSON with per-work-package 3-point hours + rate. |
