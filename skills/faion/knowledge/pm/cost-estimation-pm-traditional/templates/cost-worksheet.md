<!-- purpose: Bottom-up cost worksheet with three-point PERT per package + contingency stack -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Cost Estimate — [Project Name]

**Date:** [Date]
**Currency:** [USD/EUR/UAH — declare per line if mixed]
**Estimator:** [Name]
**WBS version:** [ID]

## Direct Costs

| Category | Item | Qty | Unit | Rate | Source | Total |
|----------|------|-----|------|------|--------|-------|
| Labor | [Role] | [hours] | h | [$X/h] | [contract/survey] | [$X] |
| Software | [Tool] | [months] | mo | [$X/mo] | [vendor quote] | [$X] |
| Cloud/Infra | [Service] | [months] | mo | [$X/mo] | [infracost/pricing API] | [$X] |
| **Subtotal Direct** | | | | | | **[$X]** |

## Indirect Costs

| Item | Basis | Rate | Total |
|------|-------|------|-------|
| Office overhead | % of direct labor | [10%] | [$X] |
| Admin support | % of total direct | [5%] | [$X] |
| **Subtotal Indirect** | | | **[$X]** |

## Reserves

| Type | Method | Amount |
|------|--------|--------|
| Contingency (risk-driven) | Sum(P x impact) from risk register | [$X] |
| Management Reserve | [5-10%] of cost baseline | [$X] |

## Total Budget

| Component | Amount |
|-----------|--------|
| Direct Costs | [$X] |
| Indirect Costs | [$X] |
| Contingency Reserve | [$X] |
| **Cost Baseline (BAC - MR)** | **[$X]** |
| Management Reserve | [$X] |
| **Budget at Completion (BAC)** | **[$X]** |

## Monte Carlo Summary
- P50: [$X]
- P80: [$X] — **use this as baseline target**
- P95: [$X]

## Assumptions
- [Explicit assumption 1]
- [Explicit assumption 2]
