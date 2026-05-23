<!-- purpose: legacy template for ads-analytics-setup — event-tracking-plan -->
<!-- consumes: per AGENTS.md Prerequisites -->
<!-- produces: artefact per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/06-decision-tree.xml -->
<!-- token-budget-impact: ~400-1200 tokens when loaded as context -->

# Event Tracking Plan: [Product Name]

## Business Model: [saas | ecom | leadgen | content]

## Page Events (automatic via enhanced measurement)

| Event | Trigger | Conversion |
|-------|---------|------------|
| page_view | All pages | No |
| scroll | 90% scroll depth | No |
| click | Outbound links | No |
| file_download | PDF, ZIP downloads | No |
| video_start | Embedded video start | No |

## User Events

| Event Name | Trigger | Parameters | Conversion |
|------------|---------|------------|------------|
| sign_up | Account created | method, plan | Yes |
| login | User logged in | method | No |
| trial_started | Trial begins | plan_name | Yes |
| purchase | Subscription/transaction | value, currency, plan, transaction_id | Yes |

## Engagement Events

| Event Name | Trigger | Parameters | Conversion |
|------------|---------|------------|------------|
| feature_used | Key feature accessed | feature_name, user_type | No |
| content_viewed | Article or doc viewed | content_id, content_type | No |
| invite_sent | Team invite sent | count | No |

## E-commerce Events (add if applicable)

| Event Name | Trigger | Parameters |
|------------|---------|------------|
| view_item | Product page view | items: [{item_id, item_name, price}] |
| add_to_cart | Add to cart click | items, value, currency |
| begin_checkout | Checkout start | items, value, currency |
| purchase | Order complete | transaction_id, value, currency, items |

## Custom Dimensions

| Name | Scope | Source | Purpose |
|------|-------|--------|---------|
| plan_name | event | sign_up.plan | Segment conversion by plan |
| user_type | user | server-set | Free vs paid |

## Notes

- GA4 reserved names NOT to use: session_start, first_visit, user_engagement, scroll, click
- Max custom dimensions: 50 event-scoped, 25 user-scoped
- All events tested in GA4 DebugView before production deploy
