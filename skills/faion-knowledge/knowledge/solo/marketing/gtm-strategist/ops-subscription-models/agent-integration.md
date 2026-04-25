# Agent Integration — Subscription Models

## When to use
- Designing pricing architecture for a new SaaS or membership product
- Diagnosing high churn (>5% monthly) or low net revenue retention (<100%)
- Setting up automated dunning and payment recovery sequences
- Evaluating tier structures for upgrade path clarity
- Building LTV/CAC models to justify acquisition spend

## When NOT to use
- One-time digital products with no recurring component
- Marketplaces where platform takes a transaction cut (different economics)
- Early pre-product stage before any paying customer validation
- Physical product businesses without a clear replenishment angle

## Where it fails / limitations
- Churn prediction requires 6-12 months of cohort data — agents cannot shortcut this
- Pricing advice without real willingness-to-pay interviews is speculative
- Dunning optimization is provider-specific (Stripe vs Paddle have different retry logic)
- Annual vs monthly mix depends on CAC payback period, which requires actual CAC data
- Expansion MRR strategies only work once core retention is above ~90% monthly

## Agentic workflow
A Claude subagent is most useful here for generating dunning email sequences, analyzing tier structures against a provided competitor set, and drafting metrics dashboards from CSV exports. The agent should receive the current MRR, churn rate, ARPU, and CAC as structured input before making any pricing or retention recommendations. Human sign-off is required before any billing configuration changes or pricing page updates.

### Recommended subagents
- `faion-sdd-executor-agent` — run structured analysis tasks (tier comparison, metrics audit) from SDD task files
- No dedicated billing agent exists; use a general content/strategy subagent for copywriting dunning emails

### Prompt pattern
```
You are analyzing subscription metrics for [product].
Inputs:
- MRR: $X
- Monthly churn: Y%
- ARPU: $Z
- LTV:CAC: A:1
- Current tiers: [list]

Task: Identify the top 3 churn risk factors and propose one dunning sequence
change with expected recovery impact. Output as JSON:
{"risk_factors": [...], "dunning_change": {...}, "expected_recovery_pct": N}
```

```
Generate a 3-email dunning sequence for [product] targeting involuntary churn.
Tone: direct, non-apologetic. Each email: subject + body under 150 words.
Day cadence: 1, 4, 8. Final email: downgrade warning with data retention clause.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe` CLI | Manage subscriptions, test webhooks, list invoices | `brew install stripe/stripe-cli/stripe` / stripe.com/docs/stripe-cli |
| `chargebee-cli` | Not official; use Chargebee REST API via `curl`/`httpie` | chargebee.com/docs/2.0/api |
| `baremetrics` | MRR/churn export via REST API | baremetrics.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Billing | SaaS | Yes — REST API + webhooks | Industry default; dunning via Smart Retries |
| Paddle | SaaS | Partial — REST API | Better for global tax handling; less granular dunning |
| Chargebee | SaaS | Yes — REST API | Richer subscription lifecycle management than Stripe |
| Baremetrics | SaaS | Yes — REST API | MRR/churn analytics; exportable cohort data |
| ChartMogul | SaaS | Yes — REST API | Best cohort analysis; integrates with Stripe/Paddle |
| Churnkey | SaaS | Partial | Cancellation flow optimization; no API for content |
| ProfitWell | SaaS (free tier) | Partial | Metrics only; no action surface for agents |

## Templates & scripts
See `templates.md` for subscription model canvas and dunning email sequence.

Inline: minimal Python script to pull Stripe MRR snapshot via API:

```python
import stripe, os
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

subscriptions = stripe.Subscription.list(status="active", limit=100)
mrr = sum(
    sub["items"]["data"][0]["price"]["unit_amount"] / 100
    * (1 if sub["items"]["data"][0]["price"]["recurring"]["interval"] == "month" else 1/12)
    for sub in subscriptions.auto_paging_iter()
)
print(f"MRR: ${mrr:,.2f}")
```

## Best practices
- Instrument every subscription event (created, upgraded, downgraded, paused, cancelled) as structured logs before building any retention workflow
- Set annual discount at exactly 2 months free (17% off); discounts above 25% cannibalize monthly signups
- Dunning retry logic should space retries on card-network-recommended intervals (1, 3, 7 days) not arbitrary ones
- Track revenue churn separately from customer churn — expansion can mask serious churn problems
- Run a "save offer" experiment at cancellation with a 30-day pause option before full cancel
- Net Revenue Retention above 100% means you grow even with zero new customers; below 100% means you're on a treadmill
- Freemium tier limits must create genuine friction — not just feature flags on unused features

## AI-agent gotchas
- Agents must not auto-apply coupon codes or pricing changes to live Stripe subscriptions without human approval
- LTV calculations from agents are estimates — actual LTV requires survival analysis over real cohort data
- Dunning copy generated by LLMs tends toward over-apologetic tone; specify "direct" and "non-apologetic" explicitly
- Do not ask an agent to set proration rules or billing cycle anchors — these have permanent accounting implications
- Agents cannot predict willingness-to-pay; pricing recommendations need real user interview data as input
- Payment recovery stats from agents are based on industry benchmarks, not your actual card network behavior

## References
- The Automatic Customer — John Warrillow (subscription model types)
- Subscribed — Tien Tzuo (subscription economy framework)
- https://stripe.com/docs/billing/subscriptions/overview
- https://chartmogul.com/blog/net-revenue-retention/
- https://baremetrics.com/academy/saas-churn
