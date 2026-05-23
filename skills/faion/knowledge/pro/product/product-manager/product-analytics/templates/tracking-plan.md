<!-- purpose: Tracking-plan skeleton with event table + version field. -->
<!-- consumes: input from methodology -->
<!-- produces: artefact for downstream agent -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-500 tokens when loaded as context -->

# Tracking Plan: [Product]

<!-- Source of truth for event taxonomy. Runtime catalogs drift toward this file via PR, never the reverse.
     Each event must state which decision it informs. Run tracking-plan-lint.sh before committing. -->

## User Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| user_id | string | Unique user ID | "usr_123" |
| plan | string | Subscription tier | "pro" |
| signup_date | date | When they signed up | "2024-01-15" |
| company_size | number | Team size | 25 |
| source | string | Acquisition channel | "organic_search" |

## Events

### Onboarding Events

| Event | Trigger | Side | Owner | Decision It Informs | Properties |
|-------|---------|------|-------|---------------------|------------|
| signup_started | Click signup button | client | @pm-handle | Activation funnel drop-off | source |
| signup_completed | Form submitted | server | @pm-handle | Activation rate baseline | method (email/google) |
| onboarding_step_completed | Each step done | client | @pm-handle | Step-level drop-off | step_name, duration_sec |
| onboarding_completed | All steps done | server | @pm-handle | Activation event (frozen) | total_duration_sec |

### Core Feature Events

| Event | Trigger | Side | Owner | Decision It Informs | Properties |
|-------|---------|------|-------|---------------------|------------|
| [object]_[action] | [when it fires] | server/client | @owner | [which decision] | [properties] |

### Conversion Events

| Event | Trigger | Side | Owner | Decision It Informs | Properties |
|-------|---------|------|-------|---------------------|------------|
| upgrade_initiated | Click upgrade CTA | client | @pm-handle | Paywall placement A/B | from_plan, to_plan, entry_point |
| checkout_started | Enter payment page | server | @pm-handle | Checkout conversion | plan, billing_period |
| purchase_completed | Payment success | server | @pm-handle | Revenue by cohort | amount_cents, plan, billing_period |
| purchase_failed | Payment failed | server | @pm-handle | Payment failure rate | error_type |

## Naming Convention

All events: `object_action` in `snake_case`.
Objects: account, project, feature, member, subscription.
Actions: created, updated, deleted, shared, exported, invited, started, completed, failed.
