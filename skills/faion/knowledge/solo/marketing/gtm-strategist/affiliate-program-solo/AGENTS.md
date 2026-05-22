---
slug: affiliate-program-solo
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "97e5a4ea25ab6ad2"
summary: Solo-scale affiliate / referral program setup using built-in platform tools (Lemon Squeezy, Gumroad, Stripe, Rewardful) with fraud and refund safeguards.
tags: [affiliate, referral, solo, indie-hacker, lemon-squeezy, rewardful, fraud-prevention]
---
# Solo-Scale Affiliate Program

## Summary

**One-sentence:** Solo-scale affiliate / referral program setup using built-in platform tools (Lemon Squeezy, Gumroad, Stripe, Rewardful) with fraud and refund safeguards.

**One-paragraph:** Existing pro-tier affiliate marketing methodology assumes a marketing team; the solo indie hacker needs a cheap, self-service path. Mechanism: pick the right tool tier (LS native if you're on Lemon Squeezy, Gumroad native if Gumroad, Rewardful + Stripe if you need flexibility, Stripe coupons + manual payout if &lt; 5 affiliates), set commission (15-30% recurring is standard, 50% on first month is aggressive), build fraud guardrails (cookie window, anti-self-referral check, payout hold, refund clawback), and launch via 1-tweet + 1-newsletter + 1-DM-batch. Outcome: a working program with 5-20 affiliates in 30 days that doesn't burn margin to fraud.

## Applies If (ALL must hold)

- you operate a paid SaaS / digital product / info product as a solo founder
- MRR ≥ $500 OR you have ≥ 100 paying users
- payment platform is Lemon Squeezy, Gumroad, Stripe, Paddle, or similar
- you can spend 2-6 hours setup + 30-60 min/month on payout management
- product has clear referral mechanics (not enterprise sales with 6-month cycles)

## Skip If (ANY kills it)

- pre-revenue (no MRR / no products sold) — no commission to pay
- enterprise / B2B with multi-month sales cycle — affiliate attribution breaks down
- regulated industry where commission disclosure is fraught (healthcare, financial) — use referral credits instead
- you don't have a refund window or refund processing — fraud risk too high
- product is free with no upgrade path — nothing to affiliate

## Prerequisites (must be true before starting)

- payment platform identified + admin access
- commission policy decided (% rate, recurring vs. first-month-only, payout schedule)
- refund window length (defines fraud clawback timing)
- target affiliate persona ("creators in {niche}", "existing users", "your newsletter readers")
- launch channels: own newsletter, X / Twitter, IndieHackers, niche communities
- a referral-tracking link format that you control (UTM, ?ref=, /r/{code})

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | Commission % depends on margins set there |
| `solo/marketing/gtm-strategist/ops-subscription-models` | Recurring vs. one-time affects payout structure |
| `pro/marketing/gtm-strategist/growth-affiliate-marketing` | Pro-tier reference for graduating later |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: platform-native first, commission within margin, fraud guards required, refund clawback, disclose terms in writing | ~900 |
| `content/02-output-contract.xml` | essential | Program-config schema, payout-batch schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (margin death, self-referral, cookie stuffing, refund leak, payout delay, FTC non-disclosure) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `platform_tier_recommendation` | sonnet | Match user's existing stack to the right tool tier |
| `commission_calc_from_margin` | haiku | Deterministic computation from margin + LTV |
| `fraud_guard_config_synthesis` | sonnet | Compose cookie window + anti-self + payout-hold settings |
| `launch_message_draft` | sonnet | Tweet / newsletter / DM templates |

## Templates

| File | Purpose |
|------|---------|
| `templates/program-policy.md` | Public-facing affiliate terms page |
| `templates/launch-tweet.md` | Tweet announcing the program with referral mechanics |
| `templates/affiliate-onboarding-email.md` | Welcome email for new affiliates with their unique link |
| `templates/payout-run-checklist.md` | Monthly payout safety checklist (refund window, fraud check) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-commission-from-margin.py` | Solve for max safe % given margin + LTV + churn | At program design |
| `scripts/audit-payout-batch.py` | Pre-payout: flag self-referrals, refund-window pending, suspicious traffic | Before each payout run |

## Related

- parent skill: `solo/marketing/gtm-strategist/`
- peer methodologies: `growth-indiehackers-strategy`, `growth-product-hunt-launch`, `ops-subscription-models`
- external: [Rewardful](https://www.rewardful.com/) · [Lemon Squeezy affiliates docs](https://docs.lemonsqueezy.com/help/affiliates) · [FTC endorsement guides](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
