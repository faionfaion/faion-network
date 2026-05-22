<!--
purpose: Fair-use cap policy skeleton.
consumes: heavy-user distribution + competitive norms.
produces: Customer-facing cap policy + internal enforcement rules.
depends-on: ../scripts/validate-agent-pricing-and-unit-economics.py.
token-budget-impact: ~200 tokens.
-->

# Fair-use cap policy — <tier>

## Threshold

- Monthly cap: <n tasks>
- Burst window: <n tasks in 24h>

## What happens at the cap

- Soft throttle: <text>
- Hard overage charge: $<x>/task above cap
- Notification: <when + where>

## Why we have a cap

- A few customers consuming 50-100× the median would exhaust the gross-margin floor for the whole tier. The cap protects the tier so it can keep its public price.

## Appeal / override

- Contact <support-channel>; we will quote a custom plan for sustained heavy use.
