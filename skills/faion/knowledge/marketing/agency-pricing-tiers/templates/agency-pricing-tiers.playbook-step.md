<!-- purpose: good / better / best rate-sheet skeleton — three costed tiers with margin, nested deliverables, 3 / 5 / 8 prices, the fence, scope-up and concession rules, best-first presentation, rollout steps -->
<!-- consumes: deliverable list with hours per deliverable, loaded hourly cost, pass-through costs, the ICP outcome, the target price of the middle tier -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/06-decision-tree.xml -->
<!-- token-budget-impact: ~800 tokens when loaded -->
# Agency Pricing Tiers — Rate sheet and playbook step for <company_name>

## Tiers (exactly three, in this order; prices in <currency> per month; better about 1.67 x good, best about 1.6 x better, within 15 percent)

| name | price | hours | loaded_hourly_cost | pass_through | gross_margin_abs (price - (hours x rate + pass_through)) | gross_margin_pct (abs / price) |
|---|---|---|---|---|---|---|
| good | <good_price> | <h> | <loaded_hourly_cost> | <cost> | <computed> | <computed> |
| better | <better_price> | <h> | <loaded_hourly_cost> | <cost> | <computed> | <computed> |
| best | <best_price> | <h> | <loaded_hourly_cost> | <cost> | <computed, highest of the three in both columns> | <computed, highest> |

## Deliverables (each tier is a strict superset of the one below: same items, equal or higher quantity, equal or faster turnaround)

| deliverable | good qty / turnaround_days | better qty / turnaround_days | best qty / turnaround_days |
|---|---|---|---|
| <name> | <n> / <d> | <n> / <d> | <n> / <d> |
| <fence_deliverable> (the fence) | not included | <n> / <d> | <n> / <d> |
| <best-only deliverable> | not included | not included | <n> / <d> |

## Fence and default
- fence.omitted_deliverable: <fence_deliverable>
- fence.needed_for: <the ICP outcome this deliverable is needed for>
- fence.named_on_rate_sheet: true
- default_recommendation: better
- gap_justification.scope_difference: <only if a price gap sits outside the band; repeat it in a step's exit_criterion>

## Presentation
- order: best, better, good
- prices_visible: true

## Scope-up (mid-engagement)
- trigger: <a request outside the current tier's deliverable list>
- price_rule: difference between the two tier prices pro-rated to the remaining term
- approver: <role at the agency>
- written_confirmation_required: true
- free_goodwill_allowed: false

## Concessions
- method: remove_named_deliverable_or_quantity
- published_prices_vary_by_client: false

## Rollout steps

| id | name | exit_criterion (measurable; never "shipped") | output_location |
|---|---|---|---|
| s1 | cost every tier | <best margin leads in currency and percent, with the numbers> | <path> |
| s2 | publish best-first rate sheet | <rate sheet lists best, better, good with prices and the fence named> | <path> |
| s3 | brief account managers on scope-up | <every AM can state trigger, price rule, approver; first scope-up logged> | <path> |
