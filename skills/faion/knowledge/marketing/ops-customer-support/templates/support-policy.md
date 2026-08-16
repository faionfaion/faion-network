<!-- purpose: Support policy -- channels, SLA by plan tier, escalation contacts, refund policy, out-of-hours message. -->
<!-- consumes: plan tiers + escalation email addresses + refund policy -->
<!-- produces: Markdown support policy -->
<!-- depends-on: content/01-core-rules.xml (r2-sla-tiered-by-plan) -->
<!-- token-budget-impact: ~250-400 tokens when loaded as context -->

# Support Policy: <product>

## Support Channels
| Channel | Availability | Response Time |
|---------|--------------|---------------|
| Help Center | 24/7 | Instant (self-serve) |
| Email | 24/7 | See SLA by plan |
| Chat | <business_hours> | [X minutes during hours] |
| Phone | Enterprise only | Scheduled |

## SLA by Plan
| Plan | Channels | First Response SLA |
|------|----------|--------------------|
| Free | Help Center | Self-serve only |
| Pro | Help Center + Email | 24 hours |
| Team | + Chat during hours | 4 hours |
| Enterprise | + Phone | 1 hour |

*All new paying customers receive a first response within 4 hours regardless of plan tier.*

## Escalation Contacts
- Bug reports: [support@product.com]
- Account or billing issues: [billing@product.com]
- Security vulnerabilities: [security@product.com]
- Data deletion requests (GDPR): [privacy@product.com]
- Urgent / product down: <urgent_product_down>

## Refund Policy
[Your refund policy — e.g., "30-day money-back guarantee, no questions asked."]

## Out of Hours
When support is unavailable, auto-reply reads:
"Thanks for reaching out. We're currently unavailable and will respond by [next business day/time]. For urgent issues, see our status page at <url>."
