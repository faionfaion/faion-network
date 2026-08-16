<!-- purpose: Subscription model spec -- model type, billing, tiers, metric targets, lifecycle automation, dunning. -->
<!-- consumes: model intent + feature/cost inventory + billing platform config -->
<!-- produces: Markdown subscription model doc -->
<!-- depends-on: content/01-core-rules.xml (r1-pick-exactly-one-model, r4-dunning-auto-then-manual, r5-lifecycle-policy-coverage) -->
<!-- token-budget-impact: ~400-600 tokens when loaded as context -->

# Subscription Model: <product_name>

## Model Type
- [ ] SaaS (software access)
- [ ] Membership (community/content access)
- [ ] Replenishment (regular product delivery)
- [ ] Curation (curated selections)
- [ ] Access (exclusive availability)

## Billing
- Monthly: $X
- Annual: $X (presented as "2 months free")
- Usage component: <usage_component>

## Tiers
| Tier   | Price    | Target Customer | Key Differentiator | Usage Limit |
|--------|----------|-----------------|-------------------|-------------|
| Free   | $0       | [Persona]       | [Feature]         | <limit>     |
| Pro    | $X/mo    | [Persona]       | [Feature]         | Unlimited   |
| Team   | $X/mo    | [Persona]       | Collaboration     | Custom      |

## Metric Targets
- MRR goal (month 6): $X
- Monthly churn target: <X%
- LTV target: $X
- LTV:CAC target: X:1
- NRR target: >100%

## Lifecycle Automation
| Stage | Trigger | Action |
|-------|---------|--------|
| Trial Day 1 | Signup | Welcome email + first action prompt |
| Trial Day 3 | No first action completed | Check-in + help |
| Trial Day 7 | End of trial | Conversion offer email |
| Active monthly | Monthly | Usage report email |
| At-risk | Usage drop 50%+ week-over-week | Outreach email + help offer |
| Cancel request | Cancellation click | Save offer (pause / downgrade / discount) |
| Churned Day 30 | 30 days post-churn | Win-back campaign |

## Payment Recovery (Dunning)
- Retry Day 1 + email
- Retry Day 3 + email
- Retry Day 7 + final warning email
- Day 10: downgrade to free, retain data 30 days
