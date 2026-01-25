---
id: aarrr-pirate-metrics
name: "AARRR Pirate Metrics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# AARRR Pirate Metrics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | aarrr-pirate-metrics |
| **Name** | AARRR Pirate Metrics |
| **Category** | Growth |
| **Difficulty** | Beginner |
| **Agent** | faion-growth-agent |
| **Related** | north-star-metric, cohort-basics, retention-basics |

---

## Problem

Tracking everything leads to tracking nothing. AARRR provides 5 critical metrics that tell your complete growth story: Acquisition, Activation, Retention, Revenue, Referral.

---

## Framework

### The 5 Stages

```
Acquisition → Activation → Retention → Revenue → Referral
     ↓            ↓            ↓          ↓          ↓
How users    First value   Coming     Making    Spreading
find you      delivered     back       money     the word
```

### 1. Acquisition

**Question:** How do users find you?

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| CPA | Marketing spend / New users | <$50 (SaaS) |
| Channel mix | % per channel | Diverse |
| Sign-up rate | Sign-ups / Visitors x 100% | 2-5% |

**Channels to track:**
- Organic search
- Paid ads
- Social media
- Referrals
- Direct
- Email

### 2. Activation

**Question:** Do users experience core value?

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Activation rate | Activated users / Sign-ups x 100% | 30-50% |
| Time to first value | Avg time to key action | <10 min |
| Onboarding completion | Completed / Started x 100% | 60-80% |

**Define activation as:** The action that correlates with D30 retention (not vanity metrics like "created profile").

### 3. Retention

**Question:** Do users come back?

| Metric | Formula | Benchmark (SaaS) |
|--------|---------|------------------|
| D1 retention | Active Day 1 / Signups x 100% | 40-60% |
| D7 retention | Active Day 7 / Signups x 100% | 20-30% |
| D30 retention | Active Day 30 / Signups x 100% | 10-15% |
| Churn rate | Lost users / Starting users x 100% | <5%/month |

### 4. Revenue

**Question:** How do you monetize?

| Metric | Formula | Use Case |
|--------|---------|----------|
| MRR | Paying customers x Avg monthly price | SaaS |
| ARPU | Total revenue / Total users | All |
| LTV | ARPU x Avg customer lifespan (months) | All |
| Free to paid | Paid / Free x 100% | Freemium |

### 5. Referral

**Question:** Do users tell others?

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| K-factor | Invites sent x Invite conversion | >1.0 = viral |
| Referral rate | Referred users / Total users x 100% | 5-15% |
| NPS | % Promoters - % Detractors | >50 |

---

## Dashboard Template

```markdown
## Weekly AARRR - Week of [DATE]

### Acquisition
| Channel | Visitors | Sign-ups | CPA | Δ |
|---------|----------|----------|-----|---|
| Organic | 5,000 | 500 | $0 | +12% |
| Paid | 3,000 | 300 | $5 | -3% |
| **Total** | **8,000** | **800** | **$1.88** | **+10%** |

### Activation
- Rate: 45% (target: 50%)
- TTV: 4 min (target: <3 min)

### Retention
| Cohort | D1 | D7 | D30 |
|--------|-----|-----|------|
| This week | 52% | - | - |
| Last week | 48% | 22% | - |
| 4 weeks ago | 50% | 21% | 12% |

### Revenue
- MRR: $45,000 (+5%)
- New MRR: $3,500
- Churned MRR: $1,200
- ARPU: $45

### Referral
- Invites: 340
- Conversions: 68 (20%)
- K-factor: 0.08
```

---

## Examples

### SaaS Product

**Product:** Project management tool

| Stage | Metric | Current | Target | Action |
|-------|--------|---------|--------|--------|
| Acquisition | Monthly signups | 2,000 | 2,500 | SEO optimization |
| Activation | Completed 1st project | 35% | 50% | Simplify onboarding |
| Retention | D30 retention | 18% | 20% | Email campaigns |
| Revenue | Free to paid | 3% | 5% | Better upgrade prompts |
| Referral | K-factor | 0.05 | 0.15 | Incentive program |

**Priority:** Activation (35% too low - fix before scaling acquisition)

### E-commerce

| Stage | Metric | Value |
|-------|--------|-------|
| Acquisition | Monthly visitors | 50,000 |
| Activation | Add to cart | 12% |
| Retention | Repeat purchase (30d) | 8% |
| Revenue | Conversion rate | 2.5% |
| Referral | Share rate | 1% |

### Mobile App

```
ACQUISITION: 5,000 downloads/month, $2.50 CAC
ACTIVATION: 40% created first workout
RETENTION: D1: 55%, D7: 30%, D30: 15%
REVENUE: 4% free to premium, $8/month ARPU, $48 LTV
REFERRAL: 5% invite rate, 15% conversion, K=0.075
```

---

## Implementation Checklist

- [ ] Define key metric for each stage
- [ ] Set up tracking (GA, Mixpanel, Amplitude)
- [ ] Define activation event (correlate with retention)
- [ ] Create weekly dashboard
- [ ] Set targets for each metric
- [ ] Review weekly with team
- [ ] Prioritize worst-performing stage
- [ ] Run experiments to improve

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tracking too many metrics | ONE key metric per stage |
| Focusing only on acquisition | Fix worst stage first |
| Wrong activation metric | Must correlate with retention |
| Ignoring referral | Add referral program early |
| Not segmenting | Segment by cohort, channel, plan |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Web analytics | Google Analytics, Plausible |
| Product analytics | Amplitude, Mixpanel, Posthog |
| Retention | Mixpanel, Amplitude |
| Revenue | Stripe, ChartMogul, ProfitWell |
| Referral | ReferralCandy, Viral Loops |

---

## Sources

- [Dave McClure's Startup Metrics for Pirates (2007)](https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version)
- [Sean Ellis - Hacking Growth: How Today's Fastest-Growing Companies Drive Breakout Success](https://www.sean-ellis.com/)
- [Andrew Chen - The Cold Start Problem: Using Network Effects to Scale Your Product](https://andrewchen.com/)
- [Reforge - Growth Series: AARRR Framework](https://www.reforge.com/blog/growth-loops)
- [Amplitude - The North Star Playbook](https://amplitude.com/north-star)

---

## Related Methodologies

- **north-star-metric:** North Star Metric (the one metric that matters)
- **cohort-basics:** Cohort Analysis (analyze retention properly)
- **retention-basics:** Retention fundamentals
- **viral-metrics:** Viral Metrics & K-factor (maximize referral)
- **activation-framework:** Activation optimization

---

*Methodology: aarrr-pirate-metrics | Growth | faion-growth-agent*
