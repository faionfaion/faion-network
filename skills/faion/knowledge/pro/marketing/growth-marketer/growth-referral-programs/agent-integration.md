# Agent Integration — Referral Programs

## When to use
- You have product-market fit and at least a few hundred happy customers; referrals only amplify existing satisfaction.
- CAC via paid channels is climbing and unit economics still allow a 20-50% CAC reward to a referrer.
- LTV is high enough (>3x CAC) that double-sided cash/credit incentives are sustainable.
- An agent loop can own the full lifecycle: design → tracking → email/in-app promotion → fraud review → KPI reporting.

## When NOT to use
- Pre-PMF or NPS still negative — referrals will just propagate churn.
- Low-margin commodity (thin margins won't survive a $20 give/$20 get).
- B2B with long enterprise cycles where sales-assisted intros beat self-serve refs.
- Compliance-heavy verticals (regulated finance, health) where incentivized referrals trigger disclosure rules an agent can't safely navigate.

## Where it fails / limitations
- Fraud explosion: self-referrals, referral farms, multi-account abuse. Agents detect patterns but final ban decisions need human-in-loop.
- Mis-attribution when users clear cookies, switch devices, or use ad blockers — first-touch vs last-touch logic must be explicit.
- Reward fulfillment lag (manual credit approval) breaks the trust loop; needs idempotent automation.
- Viral coefficient (K) plateaus quickly; agents over-optimizing reward size erode margin without meaningful K lift.

## Agentic workflow
A growth agent designs the program (incentive curve, trigger map, fraud rules) on `opus`, then a `sonnet` agent generates landing-page copy, email sequences and dashboard SQL. A `haiku` operator polls the referral platform API daily, calculates K-factor and participation rate, and surfaces anomalies. Fraud-review and any reward >$X is escalated to human via a queue file.

### Recommended subagents
- `faion-growth-agent` (opus) — program design, reward sizing vs CAC, loop economics.
- Generic copy/sonnet subagent — emails, landing page, in-app modal copy.
- Generic data/haiku subagent — daily K-factor pull from ReferralCandy/GrowSurf/Mixpanel.

### Prompt pattern
```
Design a double-sided referral program for {product} with CAC=${cac},
LTV=${ltv}, monthly churn={churn}%. Output: reward structure, 5 trigger
points, fraud rules, K-factor target, and a 4-email launch sequence.
Constrain reward to <={max_pct}% of CAC.
```

```
Analyze last 30d referral events from {source}. Compute participation
rate, invites/referrer, conversion rate, K. Flag users with >5 invites
in <24h or shared payment method as fraud candidates. Return JSON.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `referralcandy` REST API | Manage referrals, rewards, fraud flags | https://www.referralcandy.com/api |
| `growsurf` API | Programmatic program creation, participant CRUD | https://docs.growsurf.com/api |
| `firstpromoter` API | Affiliate + referral hybrid, payouts | https://help.firstpromoter.com/api |
| `mixpanel` CLI / Python SDK | Track `referral_link_shared`, `referral_signup`, `referral_completed` | `pip install mixpanel` |
| `posthog` CLI | Same as above, OSS alternative | `pip install posthog` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| ReferralCandy | SaaS | Yes (REST + webhooks) | Shopify-heavy, full reward automation |
| GrowSurf | SaaS | Yes (REST + Zapier) | Best for B2B SaaS, waitlists |
| Viral Loops | SaaS | Partial | UI-driven; API exists but limited writes |
| FirstPromoter | SaaS | Yes (REST) | Affiliates + referrals, multi-tier |
| Rewardful | SaaS | Yes (REST) | Stripe-native, simple model |
| Tapfiliate | SaaS | Yes (REST) | Ecommerce + SaaS |
| Custom build | OSS | Yes | Stripe Coupons + signed referral codes; agent owns tracking table |

## Templates & scripts
See `templates.md` for landing-page and email copy. Inline K-factor calculator:

```python
# k_factor.py — drop-in for haiku ops agent
def k_factor(invites_sent: int, signups_from_invites: int, active_referrers: int) -> dict:
    if active_referrers == 0:
        return {"k": 0, "i": 0, "c": 0}
    i = invites_sent / active_referrers
    c = signups_from_invites / max(invites_sent, 1)
    return {"k": round(i * c, 3), "i": round(i, 2), "c": round(c, 3)}

# Usage from agent:
# print(k_factor(invites_sent=4200, signups_from_invites=630, active_referrers=850))
# -> {"k": 0.741, "i": 4.94, "c": 0.15}  # near-viral
```

## Best practices
- Anchor reward to 20-50% of CAC, not to a round-number gut feel; let the agent recompute as CAC drifts.
- Always double-sided unless margin forbids; one-sided programs feel exploitative and the referee converts worse.
- Promote immediately after a "win moment" event (purchase complete, milestone reached, 5-star review submitted) — not on first visit.
- Build the dashboard before launch so the agent has clean event names to optimize against.
- Sunset or rotate the program every 6-9 months; static programs decay as your best advocates exhaust their networks.

## AI-agent gotchas
- LLMs eagerly suggest "give 50% off" — always pass a hard `max_reward_pct_of_cac` constraint into the prompt.
- Fraud detection requires deterministic rules, not LLM judgment; agent should compute features (IP overlap, payment-method overlap, signup velocity) and pass to a rules engine, never decide bans alone.
- Reward fulfillment must be idempotent: if the agent retries the API call, do NOT double-credit. Use a unique `(referrer_id, referee_id, event)` key.
- Don't let the agent A/B-test reward amounts without finance approval — easy to blow burn budget.
- Translate legal copy through a human; incentivized referrals trigger different disclosure regimes per jurisdiction.

## References
- Andrew Chen, *The Cold Start Problem* (referral chapters)
- Sean Ellis & Morgan Brown, *Hacking Growth*
- Reforge, "Referral Programs" course (Casey Winters)
- David Skok, "Lessons Learned — Viral Marketing" — https://www.forentrepreneurs.com/lessons-learnt-viral-marketing/
- Dropbox referral case study — https://growthhackers.com/growth-studies/dropbox
