# Agent Integration — Affiliate Marketing

## When to use
- Recurring-revenue product (SaaS, subscription, course) with LTV high enough to support 20-40% commissions and stay under 30% of LTV all-in.
- Digital product with self-serve checkout and clean attribution; avoids manual fulfillment friction with affiliates.
- Niche audiences where 20-50 quality publishers/creators reach the entire ICP — manageable program scale.
- Product with a discount-code or unique-link friendly checkout (Stripe, Paddle, Lemon Squeezy, Shopify, ConvertKit).

## When NOT to use
- Sub-$30 transactional products with thin margin — payouts + admin overhead exceed value.
- Pre-PMF or volatile pricing — affiliates need stable offers; you'll burn relationships when you change terms.
- Brand-sensitive verticals (finance, medical, regulated) — affiliate copy can produce compliance violations.
- When you have no asset library — affiliates without swipes/banners/landing pages won't promote you.
- Marketplace-like products where customers shop on price; coupon-site affiliates cannibalize organic conversions.

## Where it fails / limitations
- Coupon-site / cashback fraud: affiliates inject themselves last-click and steal organic conversions; rules + exclusions must be aggressive.
- Two-tier / MLM structures attract low-quality recruiters and create FTC + tax-form headaches; usually skip.
- Inactive-affiliate tail: 80% of affiliates produce 0 sales; healthy programs continually recruit + prune.
- Brand-keyword bidding: affiliates running PPC on your trademark cannibalize cheap clicks; explicit terms + monitoring required.
- Tracking decay: iOS 14.5, ITP, ad-blockers — cookie-only attribution is unreliable; backstop with codes + logged-in-user attribution.
- Refund/chargeback exposure: paying out before refund window closes loses you money on cancellations.

## Agentic workflow
Subagents excel at the recruiting funnel, asset distribution, performance reports, and fraud-flagging. Keep payment release, terms negotiation, and partner termination decisions human. Pipeline: prospect list (agent) → outreach (agent draft + human send) → onboarding sequence (agent) → weekly performance digest (agent) → fraud sweep (agent) → human payout approval → quarterly recruit/prune review (human + agent data).

### Recommended subagents
- `general-purpose` — affiliate prospect discovery (newsletter writers, bloggers, comparison sites), recruitment list scoring.
- `faion-content-agent` — onboarding emails, monthly affiliate digests, asset-library copy variants.
- `password-scrubber-agent` — sanitize affiliate tax-form data (W-9/W-8BEN) before sharing logs.
- Custom `affiliate-ops-agent` (build): owns weekly stats, fraud-pattern detection, end-of-month payout calc and confirmation packet.

### Prompt pattern
- "Find 30 newsletter authors in [niche] with >5K subs and >25% open rate, with prior affiliate links in their footer or sponsor disclosure. For each: name, newsletter URL, audience size, recent affiliate-disclosed offers."
- "From this CSV of affiliate transactions, flag rows where same IP recorded >3 sales in 1h, or referrer is a known coupon site, or click-to-conversion <30s. Output: txn_id, reason."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Stripe CLI | Pull `charge` + `refund` data for affiliate reconciliation | `stripe login` |
| `pandas` | Compute commissions, fraud flags, leaderboards | `pip install pandas` |
| `httpx` | Drive PartnerStack/FirstPromoter/Rewardful APIs | `pip install httpx` |
| `gh` | Audit OSS/blog ecosystems for partner candidates | `apt install gh` |
| `playwright` | Headless check of brand-keyword bidding violations | `pip install playwright` |
| `pdftotext` | Parse uploaded W-9/W-8BEN forms | `apt install poppler-utils` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Rewardful | SaaS | API yes | Stripe-native, SaaS-friendly |
| FirstPromoter | SaaS | API yes | SaaS affiliate platform |
| PartnerStack | SaaS | API yes | B2B SaaS, deeper PRM |
| Tapfiliate | SaaS | API yes | Mid-market |
| Impact | SaaS | API yes | Enterprise-grade affiliate cloud |
| ShareASale / CJ Affiliate | SaaS | API limited | Networks, broader publisher reach |
| Refersion | SaaS | API yes | E-commerce-focused (Shopify) |
| Awin | SaaS | API yes | EU + US publisher network |
| LeadDyno | SaaS | API yes | Lower-cost option |
| GoAffPro | SaaS | API yes | Shopify-focused |
| Lemon Squeezy | SaaS | API yes | Built-in affiliate for digital products |
| Paddle | SaaS | API yes | MoR + built-in affiliate option |
| Wise / PayPal Mass-Pay | SaaS | API yes | Cross-border payouts |

## Templates & scripts
See `templates.md` for affiliate agreement and welcome email. Inline payout calc with refund holdback:

```python
# payout.py — compute monthly affiliate payout, holding back refunds
from datetime import datetime, timedelta

def monthly_payout(affiliate_id, charges, refunds, commission_rate=0.30, holdback_days=30):
    cutoff = datetime.utcnow() - timedelta(days=holdback_days)
    eligible = [c for c in charges
                if c["affiliate_id"] == affiliate_id and c["created"] <= cutoff]
    refunded_ids = {r["charge_id"] for r in refunds}
    eligible = [c for c in eligible if c["id"] not in refunded_ids]
    gross = sum(c["amount"] for c in eligible) / 100  # cents → dollars
    return round(gross * commission_rate, 2)
```

## Best practices
- Make the offer competitive but cap commission at ~30% of 12-month LTV; anything more makes the program net-loss.
- Pay reliably on a schedule (e.g., 30 days post-month-close); affiliates rate programs on payment trust above all else.
- Provide a curated asset library — banners, swipe copy, demo video, comparison landing pages; affiliates promote what's easy.
- Run a "top 10 starter playbook" onboarding so new affiliates know the highest-converting tactics; shortens time-to-first-sale.
- Build allowlist/denylist of traffic sources; explicitly prohibit brand-keyword PPC, coupon-site listing, incentivized traffic.
- Recruit niche newsletter writers — usually highest CPM-equivalent ROI vs broad bloggers.
- Recompute LTV quarterly and adjust commission tiers; offering 40% on a product with $99 LTV is a slow bleed.

## AI-agent gotchas
- LLMs over-promise affiliate earnings to recruit; constrain copy to "average affiliate earns $X" backed by your real distribution.
- Don't let an agent draft FTC disclosure language autonomously; legal team reviews boilerplate, agent slot-fills.
- Brand-safety: scan partner sites before approving (controversial niches, NSFW adjacency); one bad listing surfaces in branded SERPs.
- Currency / tax form: agent should never auto-issue payouts to international affiliates without W-8BEN on file.
- Fraud detection prompts must include explicit features (IP-velocity, time-to-conversion, referrer-domain reputation); zero-shot "is this fraud?" misses obvious cases.
- Refund-window arithmetic: agent commonly forgets the 30-day holdback and triggers premature payouts; codify in code, not prompt.
- Tracking attribution: never let an agent change attribution windows mid-program; affiliates rage-quit.
- Tax: 1099-NEC required for US affiliates earning ≥$600/year; agent can prepare but human verifies addresses + TIN.

## References
- FTC Endorsement Guides: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Rewardful docs: https://rewardful.com/docs
- FirstPromoter affiliate guide: https://firstpromoter.com/blog/affiliate-marketing-guide
- PartnerStack resources: https://www.partnerstack.com/resources
- Impact academy (publisher fraud detection)
- Pat Flynn affiliate-marketing playbook (Smart Passive Income)
