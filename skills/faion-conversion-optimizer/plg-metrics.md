---
id: plg-metrics
name: "PLG Metrics & Tracking"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# PLG Metrics & Tracking

## Metadata

| Field | Value |
|-------|-------|
| **ID** | plg-metrics |
| **Name** | PLG Metrics & Tracking |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | plg-basics, plg-implementation, aarrr-pirate-metrics |

---

## Core PLG Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Sign-up to Activation | Activated / Signups | 40-60% |
| Free to Paid Conversion | Paid / Free users | 2-5% (freemium), 10-25% (trial) |
| Time to Value (TTV) | Median time to Aha | < 5 minutes ideal |
| Natural Rate of Growth | Organic + viral / total | > 50% |
| PQL to Customer | Customers / PQLs | 15-30% |
| Expansion Revenue | Expansion MRR / Total MRR | > 30% |
| Net Revenue Retention | (MRR + expansion - churn) / MRR | > 120% |

---

## PLG Dashboard Template

```markdown
# PLG Metrics Dashboard - [Month]

## Acquisition
| Metric | Value | MoM | Target |
|--------|-------|-----|--------|
| New signups | 5,000 | +15% | 5,000 |
| Organic % | 65% | +5% | 60% |
| CAC (blended) | $45 | -10% | $50 |

## Activation
| Metric | Value | MoM | Target |
|--------|-------|-----|--------|
| Activation rate | 48% | +3% | 50% |
| Time to value | 8 min | -2 min | < 10 min |
| Onboarding complete | 72% | +5% | 75% |

## Monetization
| Metric | Value | MoM | Target |
|--------|-------|-----|--------|
| Free to paid | 3.5% | +0.5% | 4% |
| PQLs generated | 850 | +20% | 800 |
| PQL conversion | 22% | +2% | 20% |
| New MRR | $45K | +18% | $40K |

## Expansion
| Metric | Value | MoM | Target |
|--------|-------|-----|--------|
| Expansion MRR | $25K | +12% | $25K |
| Seat expansion | 35% | +5% | 30% |
| Plan upgrades | 8% | +1% | 8% |

## Retention
| Metric | Value | MoM | Target |
|--------|-------|-----|--------|
| Logo churn | 3.5% | -0.5% | < 4% |
| Net retention | 115% | +5% | 110% |
| DAU/MAU | 42% | +2% | 40% |
```

---

## Product-Qualified Leads (PQLs)

PQLs replace MQLs in PLG. They are users who show buying intent through product behavior.

### PQL Signals

| Signal | Weight | Example |
|--------|--------|---------|
| Heavy usage | High | 100+ actions/week |
| Team growth | High | Invited 5+ members |
| Premium feature attempt | High | Tried gated feature |
| Time in product | Medium | 10+ hours/month |
| Integration usage | Medium | Connected 3+ tools |
| Export/share | Medium | Downloaded reports |

### PQL Scoring Model

```
PQL Score = Sum of (Signal × Weight)

Thresholds:
- Score < 50: Nurture with product
- Score 50-80: Automated upgrade prompts
- Score > 80: Sales outreach (if enterprise)
```

---

## Key Metrics by Stage

### Acquisition Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| New Signups | Total new users | Growth |
| Signup Conversion | Visitors → Signups | 3-10% |
| Organic % | Organic + viral signups | > 50% |
| CAC (Blended) | Total marketing / new customers | < LTV/3 |
| Viral Coefficient | Invites sent × conversion | > 1.0 |

### Activation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Activation Rate | Users reaching Aha moment | 40-60% |
| Time to Value | Time to Aha moment | < 5 min |
| Onboarding Completion | Finished setup | 70-80% |
| First Week Retention | Active after 7 days | 40-50% |

### Monetization Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Free to Paid | Conversion rate | 2-5% (freemium), 10-25% (trial) |
| PQL Generation | PQLs / signups | 15-25% |
| PQL Conversion | Customers / PQLs | 15-30% |
| Average Contract Value | Revenue per customer | Increasing |
| Time to Purchase | Signup to payment | Decreasing |

### Expansion Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Expansion MRR | Upsell/cross-sell revenue | > 30% of total |
| Seat Expansion | Users added to accounts | Growing |
| Plan Upgrades | Tier increases | 5-10%/mo |
| Feature Adoption | Usage of premium features | > 50% |

### Retention Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Logo Churn | % accounts churned | < 5%/mo |
| Revenue Churn | % MRR churned | < 3%/mo |
| Net Revenue Retention | Revenue retained + expansion | > 100% |
| DAU/MAU | Daily active / monthly | 20-40% |
| Product Engagement | Actions per user | Increasing |

---

## Cohort Analysis for PLG

Track cohorts by signup month to understand retention and monetization patterns.

### Cohort Template

| Signup Month | M0 | M1 | M2 | M3 | M6 | M12 |
|--------------|----|----|----|----|----|----|
| Jan 2026 | 100% | 45% | 38% | 32% | 25% | 20% |
| Feb 2026 | 100% | 48% | 40% | 35% | - | - |
| Mar 2026 | 100% | 50% | 42% | - | - | - |

Track multiple dimensions:
- Activation cohorts
- Free to paid cohorts
- Expansion cohorts
- Churn cohorts

---

## PLG-Specific Analytics

### Time to Value Tracking

Measure time from signup to Aha moment for each cohort:

```
TTV = Median(Aha_timestamp - Signup_timestamp)

Track by:
- Signup source
- User segment
- Onboarding path
- Product version
```

### Natural Rate of Growth

```
Natural Growth Rate = (Organic + Viral) / Total Signups

Organic: Direct, referral, content, SEO
Viral: Product invites, shares
Paid: Ads, sponsored content

Target: > 50% natural growth
```

### Expansion Analysis

```
Expansion Categories:
1. Seat expansion (add users)
2. Plan upgrades (tier increase)
3. Feature add-ons
4. Usage-based growth

Net Revenue Retention = (Start MRR + Expansion - Churn) / Start MRR
Target: > 100% (negative churn)
```

---

## Tools

| Purpose | Tools |
|---------|-------|
| Product analytics | Amplitude, Mixpanel, Posthog |
| Onboarding | Appcues, Pendo, Userflow |
| In-app messaging | Intercom, Drift |
| Billing | Stripe, Paddle, Chargebee |
| PQL scoring | Madkudu, Clearbit Reveal |
| Trial management | Chargebee, Custom |

---

## Reporting Cadence

### Weekly PLG Review

- New signups (volume + source)
- Activation rate
- Free to paid conversions
- PQL generation
- Top opportunities

### Monthly PLG Deep Dive

- Full dashboard review
- Cohort analysis
- Experiment results
- Expansion trends
- Churn analysis

### Quarterly PLG Strategy

- Model evaluation (freemium vs trial)
- Pricing review
- Feature gating strategy
- PQL scoring refinement
- Sales-assist thresholds

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Tracking vanity metrics | No actionable insights | Focus on conversion/retention |
| Not defining Aha moment | Cannot optimize activation | Find and measure it |
| Ignoring cohorts | Miss retention patterns | Cohort every metric |
| No PQL scoring | Missed sales opportunities | Implement behavioral scoring |
| Only tracking revenue | Miss leading indicators | Track full funnel |

---

## Related Methodologies

- **plg-basics:** PLG Basics & Models
- **plg-implementation:** PLG Implementation Guide
- **aarrr-pirate-metrics:** AARRR Framework
- **cohort-analysis:** Cohort Analysis
- **activation-rate:** Activation Rate Optimization

---

## Sources

- [PLG Metrics Guide (OpenView)](https://openviewpartners.com/blog/product-led-growth-metrics/)
- [PQL Scoring Framework (Madkudu)](https://www.madkudu.com/resources/product-qualified-lead)
- [Net Revenue Retention (ChartMogul)](https://chartmogul.com/resources/net-revenue-retention/)
- [Natural Rate of Growth (Lenny's Newsletter)](https://www.lennysnewsletter.com/p/how-to-measure-product-led-growth)
- [Cohort Analysis Guide (Amplitude)](https://amplitude.com/blog/cohort-analysis)

---

*Methodology: plg-metrics | Growth | faion-growth-agent*
