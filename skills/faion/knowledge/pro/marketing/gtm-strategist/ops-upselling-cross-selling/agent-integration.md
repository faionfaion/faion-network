# Agent Integration — Upselling & Cross-Selling

## When to use
- Existing customer base of >100 paying accounts where new-logo CAC has crept above 30% of LTV.
- Net Revenue Retention sub-100% — expansion lever is needed to offset churn before adding spend at top-of-funnel.
- Pricing has metered tiers (seats, usage, feature gates) that naturally produce upsell triggers.
- Catalog of 2+ adjacent products where current customers are obvious cross-sell candidates (course → coaching, tool → integration).

## When NOT to use
- Pre-PMF or unstable pricing — upsell offers train customers on prices that may change, generating churn risk.
- Customers in active support escalation — wrong moment, damages trust, depresses CSAT.
- One-and-done products without recurring usage signal (single-purchase ebooks); referral or repeat-buy is the right lever.
- When activation rate is the real problem; expansion off a low-activation base just lifts a tiny denominator.

## Where it fails / limitations
- "Upgrade?" CTAs without specific value framing get ignored; conversion rates 3-5x worse than usage-anchored offers.
- Aggressive cadence (multiple upsells/month) trains users to filter out product emails completely.
- Friction in upgrade flow: anything beyond 2 clicks loses 40-60% of intent.
- Discount-heavy upsells anchor downward; once 30% off is offered, full-price conversion drops permanently.
- Cross-sell to wrong segment (B2C product cross-sold to B2B users on a free plan) burns goodwill and surveys flag annoyance.

## Agentic workflow
Use Claude subagents on the discovery and personalization layer: who is at the threshold, what feature did they request, what's the specific value frame. Keep pricing offers and discount approval under human policy. Pipeline: nightly trigger detection (agent) → match offer to trigger (agent + rules) → draft message (agent) → human-approve (or rules-based auto-send for low-stakes) → fire campaign → track conversion → recompute opportunity list (agent).

### Recommended subagents
- `general-purpose` — usage-trigger detection (account at 80% of limit, advanced-feature usage), opportunity ranking.
- `faion-content-agent` — message draft per trigger × persona × tier.
- Custom `revenue-expansion-agent` (build): owns weekly expansion-opportunity packet — top accounts by potential ARR delta, suggested offer, evidence quote.

### Prompt pattern
- "From this account-event CSV, list every account that crossed 80% of its plan limit in the last 14 days and is on a plan below the next tier. For each: account, current MRR, projected MRR after upgrade, top usage data point as evidence."
- "Draft a 5-line in-app message for [account]. Trigger: 90% of subscriber-limit. Tone: helpful. Lead with their data point ('900 of 1000 subscribers'). Offer: Growth tier $49/mo with 5,000 limit. CTA: one-click upgrade."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Build expansion-trigger models in SQL | `pip install dbt-core` |
| `duckdb` | Local OLAP on event CSVs | `brew install duckdb` |
| `pandas` | Trigger scoring + cohort segmentation | `pip install pandas` |
| Stripe CLI | Pull subscription state, schedule prorations | `stripe login` |
| `httpx` | Fire programmatic upgrade prompts to in-app SDK | `pip install httpx` |
| `make` / `n8n` | Orchestrate trigger → message workflow | https://n8n.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Billing | SaaS | API yes | Subscription tier changes, proration |
| Chargebee | SaaS | API yes | Mid-market subscription mgmt |
| Recurly | SaaS | API yes | Subscription lifecycle |
| Customer.io | SaaS | API yes | Trigger-based lifecycle messaging |
| Iterable | SaaS | API yes | Cross-channel campaigns |
| Braze | SaaS | API yes | Mobile + web orchestration |
| Intercom | SaaS | API yes | In-app messages + product tours |
| Pendo | SaaS | API yes | In-app guides + NPS |
| Appcues | SaaS | API yes | Cheaper Pendo for smaller teams |
| Userpilot | SaaS | API yes | In-app upgrade prompts |
| Gainsight PX | SaaS | API yes | Product-led expansion |
| Reforge / Wynter | content | n/a | Upsell tactic libraries |

## Templates & scripts
See `templates.md` for upsell email templates and dashboard. Inline trigger:

```python
# triggers.py — emit expansion opportunities
def opportunities(accounts):
    for a in accounts:
        if a["usage_pct"] >= 0.80 and a["plan_rank"] < a["max_plan_rank"]:
            yield {
                "account": a["id"],
                "trigger": "usage_threshold",
                "evidence": f"{int(a['usage_pct']*100)}% of {a['limit']} {a['unit']}",
                "offer_plan": a["next_plan"],
                "delta_mrr": a["next_plan_price"] - a["current_price"],
            }
        if a["advanced_feature_uses_30d"] >= 5 and not a["on_pro_or_higher"]:
            yield {
                "account": a["id"],
                "trigger": "advanced_feature_use",
                "evidence": f"used {a['advanced_feature_name']} {a['advanced_feature_uses_30d']}× in 30d",
                "offer_plan": "pro",
                "delta_mrr": a["pro_price"] - a["current_price"],
            }
```

## Best practices
- Anchor every offer to a customer-specific data point ("900 of 1,000 subscribers"), not generic plan benefits.
- Offer prorated upgrade with one-click; require login + form fields and conversion drops 40-60%.
- Time annual-upgrade nudges to expense-cycle moments (Q4 budget season for B2B, January for prosumer).
- Set a max upsell cadence of one per quarter per account; the metric to optimize is expansion MRR, not message-send rate.
- Leave room for product-led expansion: a "you're at limit" banner outperforms a CSM email 3x for prosumer SaaS.
- Track expansion attribution by trigger type so you can kill the bottom-quartile triggers and double down on top.

## AI-agent gotchas
- LLMs default to salesy tone; constrain with "no superlatives, no scarcity, lead with their data point".
- Personalization can drift to fabrication ("we saw you doubled your team!") when data isn't there; require the agent to quote the source field.
- Don't auto-send price-change emails — pricing decisions require business owner sign-off.
- Discount logic: agents stretch margins to close hypothetical deals; codify discount caps in rules, not prompts.
- Watch for double-offers: same trigger firing across email + in-app + push annoys customers; dedupe by account-trigger-date.
- Subscription-state lag: agent acts on stale CSV showing customer on Free, but they upgraded yesterday → embarrassing message; pull live state before send.
- Cross-sell to wrong persona: agent doesn't see the org chart; require explicit "primary contact title" filter for B2B cross-sells.

## References
- ProfitWell Expansion Revenue: https://www.profitwell.com/recur/all/expansion-revenue
- ChartMogul Expansion MRR: https://chartmogul.com/blog/expansion-revenue/
- Reforge "Retention + Engagement" course materials
- Userpilot in-app upselling playbook: https://userpilot.com/blog/upselling/
- Patrick Campbell talks on price elasticity (ProfitWell)
