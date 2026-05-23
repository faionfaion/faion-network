<!--
purpose: One-pager listing the 5 canonical MRR/churn/ARPU/LTV formulas
consumes: operator's plan list + Stripe data
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-400 tokens when loaded as context
-->
# Canonical Formulas — Solo MRR Dashboard

## MRR (Monthly Recurring Revenue)

```
MRR(month_M) = sum over active subscriptions of:
  if interval == "month":   unit_amount
  if interval == "year":    unit_amount / 12
  if interval == "quarter": unit_amount / 3
```

Annual payment is NOT booked as a single month spike. Spread across the term.

## Gross churn (% lost in month)

```
gross_churn_pct = (MRR_lost_from_cancels + MRR_lost_from_downgrades) / MRR_at_start_of_month
```

## Net churn

```
net_churn_pct = gross_churn - MRR_from_expansions / MRR_at_start_of_month
```

State whether the dashboard publishes gross or net (one definition, no swapping).

## ARPU (Average Revenue Per User)

```
arpu = MRR / customer_count
```

## LTV (Lifetime Value)

```
ltv = arpu / gross_churn_pct
```

## Customer definition

```
customer = one paid subscription
```

NOT one auth user. NOT one workspace. Per-seat plans count seats only in a separate "avg seats per customer" tile.

## Refunds

```
refund in month M subtracts from MRR(M) only
```

Refunds do NOT retroactively delete the subscription from earlier months. Voids (mistaken charges, $0 net) are excluded entirely.

## Frozen snapshot

```
on the 5th of month M+1, append MRR(M), gross_churn(M), arpu(M), ltv(M), customer_count(M)
to the closed-months tab
```

External reports cite the snapshot, not a live recompute.
