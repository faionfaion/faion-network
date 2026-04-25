# Agent Integration — Pricing Strategy

## When to use
- New product needs initial pricing before launch; no data exists yet
- Existing pricing is below market and owner suspects leaving revenue on the table
- Adding a new tier (freemium, enterprise) and need to define feature gating
- Conversion rate is < 1% and pricing objections are common — need diagnostic
- Quarterly pricing review cycle; need to compare conversion and churn data against benchmarks
- Competitor has changed pricing and you need a rapid response analysis

## When NOT to use
- Pricing change affects existing paying customers — requires careful communication strategy beyond an agent's output; risk of churn spike
- Enterprise pricing involving custom contracts and negotiation — agents can set anchor points but cannot negotiate
- Regulated industries (healthcare, finance, gov) where pricing is constrained by compliance rules
- The product has < 10 paying customers; there is not enough data for quantitative analysis — do customer interviews first

## Where it fails / limitations
- Van Westendorp survey data must be collected by humans; agents can design the survey but cannot run it or interpret qualitative nuance
- Competitor pricing research is time-sensitive; agent knowledge has a training cutoff and prices change frequently — always verify current prices manually
- Willingness-to-pay estimation without real survey data is speculative; agents should mark such estimates as "illustrative" not "research-backed"
- A/B testing pricing requires proper experimental controls (geo-based or feature-based) that the agent cannot implement — only advise on design
- Agents cannot predict churn impact of a price increase; provide historical churn data and let agent model scenarios, not extrapolate from nothing

## Agentic workflow
An agent is most useful for: (1) structuring the pricing document given cost data, competitor prices, and customer value estimates provided as input; (2) generating the pricing page comparison table and psychological pricing variants; (3) analyzing conversion and churn data by tier and flagging anomalies. The agent should not set final prices — it outputs options with trade-off summaries. A human makes the final call. For price increases on existing customers, require a separate communication review step.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — pricing model design, tier structure, pricing document generation
- A `pricing-analysis-agent` could ingest Stripe billing data and compute effective ARPU, upgrade/downgrade rates, and churn by tier monthly

### Prompt pattern
```
You are a pricing strategist for a SaaS product.
Context:
- Fixed monthly costs: $[X]
- Variable cost per customer: $[Y]
- Value delivered: [e.g., saves 10 hrs/month for customers billing at ~$100/hr]
- Competitor pricing: [Competitor A: $X/mo, Competitor B: $Y/mo]
- Current conversion rate: [Z]%

Task:
1. Recommend a pricing model (flat/tiered/usage/freemium) with rationale.
2. Propose 3 price points for a Pro tier using value-based pricing (target 10-20% of value delivered).
3. Generate a 3-tier comparison table (Free/Pro/Business) with feature gates.
4. List 3 signals that would indicate the price should be raised.
Output: structured markdown.
```

```
Here is last quarter's Stripe data by plan: [CSV or JSON].
Task:
1. Calculate ARPU per tier.
2. Identify which tier has the highest churn rate.
3. Flag any tiers where conversion rate is below 1% or above 10%.
4. Recommend one pricing adjustment with expected impact (qualitative).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe-cli` | Pull plan subscriber counts, MRR by price ID | https://stripe.com/docs/stripe-cli |
| Paddle API | Revenue, refund, churn data for Paddle-billed products | https://developer.paddle.com |
| `profitwell-python` | ProfitWell SDK for SaaS pricing analytics | https://github.com/profitwell/profitwell-python |
| Baremetrics API | MRR, churn, ARPU by plan | https://developers.baremetrics.com |
| Typeform API | Automate Van Westendorp survey creation | https://developer.typeform.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe | SaaS | Yes — REST API | Plans, prices, subscription data; billing portal |
| Paddle | SaaS | Yes — REST API | SaaS billing with VAT handling; good for global products |
| ProfitWell | SaaS | Yes — REST API | Pricing intelligence and willingness-to-pay research |
| Baremetrics | SaaS | Yes — REST API | MRR, churn, ARPU breakdowns by plan |
| Optimizely | SaaS | Yes — REST API | Landing page A/B testing (price page variants) |
| G2 / Capterra | SaaS | Partial — scraping | Competitor pricing research; no official API |
| Typeform | SaaS | Yes — REST API | Van Westendorp and pricing survey automation |

## Templates & scripts
See templates.md for: pricing strategy document, price comparison table (landing page).

Inline script — model reinvestment allocation at different profit levels:

```python
def pricing_tiers_to_mrr(tiers: list[dict], conversion_rate: float, traffic: int) -> dict:
    """
    Estimate MRR from a tiered pricing structure.
    tiers: [{"name": "Pro", "price": 49, "expected_share": 0.6}, ...]
    """
    total_conversions = traffic * conversion_rate
    result = {}
    for tier in tiers:
        customers = total_conversions * tier["expected_share"]
        mrr = customers * tier["price"]
        result[tier["name"]] = {"customers": round(customers), "mrr": round(mrr)}
    result["total_mrr"] = sum(v["mrr"] for v in result.values())
    return result

# Example:
tiers = [
    {"name": "Basic", "price": 19, "expected_share": 0.30},
    {"name": "Pro",   "price": 49, "expected_share": 0.55},
    {"name": "Business", "price": 149, "expected_share": 0.15},
]
print(pricing_tiers_to_mrr(tiers, conversion_rate=0.03, traffic=5000))
```

## Best practices
- Always set a price before launching, even if it's wrong — "free for now, will charge later" trains users to expect free access and makes future monetization harder
- Charge annually with a 2-month discount (equivalent to ~17% off); annual contracts dramatically reduce churn and improve cash flow predictability
- Present the highest-priced tier first on the pricing page (anchoring); users anchor on the first number they see and evaluate others relative to it
- Implement a "most popular" badge on the middle tier — it acts as social proof and a decoy that makes the middle tier look optimal
- Never show a 12-month plan without showing the monthly equivalent alongside it; hiding the math creates buyer suspicion
- Review pricing at least quarterly; a 12-month window of no pricing change in a growing SaaS means you are almost certainly underpriced

## AI-agent gotchas
- Agents applying value-based pricing (10-20% of value) will produce very different numbers depending on how "value delivered" is stated — validate the value assumption before accepting the price output
- Van Westendorp analysis requires real survey data; agents cannot simulate population responses — instruct agent to flag all willingness-to-pay outputs as estimates requiring validation
- Price recommendations should be labeled as "options" with trade-offs, not "the answer" — the final price decision requires business context the agent does not have
- Agents may recommend freemium reflexively for SaaS products; freemium is only appropriate when viral coefficient > 1 or when per-user marginal cost is near zero — prompt agent to justify the recommendation
- Human-in-loop checkpoint: any price change implemented in Stripe or Paddle requires human execution; never automate billing system changes via agent output alone
- When analyzing competitor pricing, instruct the agent to note that prices are unverified and may be outdated — hallucinated competitor prices are a common failure mode

## References
- https://www.profitwell.com/recur/all/pricing-strategy — Data-driven SaaS pricing methodology and benchmarks
- https://openviewpartners.com/blog/saas-pricing/ — OpenView's SaaS pricing research and PLG pricing models
- https://www.paddle.com/resources/pricing — Paddle's SaaS pricing best practices guide
- Monetizing Innovation by Madhavan Ramanujam — value-based pricing framework (book)
- Priceless by William Poundstone — psychology of pricing and anchoring effects (book)
- https://stripe.com/docs/billing — Stripe billing API for implementing pricing changes
