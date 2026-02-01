---
id: plg-optimization-tactics
name: "PLG Optimization Tactics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# PLG Optimization Tactics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | plg-optimization-tactics |
| **Name** | PLG Optimization Tactics |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | plg-implementation-guide, plg-metrics, activation-rate |

---

## Activation Optimization Tactics

### Reduce Friction

| Area | Bad Practice | Good Practice |
|------|--------------|---------------|
| Signup | 10 fields, email verification | 3 fields (name, email, password), instant access |
| Onboarding | 20-slide tutorial | Interactive walkthrough |
| Empty state | Blank canvas | Templates, sample data |
| First action | Complex setup | One-click quick start |

### Progressive Onboarding

```
DON'T: Show everything upfront
DO: Reveal features as needed

Example (Project Management Tool):
1. Login → Create first task (core value)
2. Add 3 tasks → Show task organization
3. Organize tasks → Show collaboration
4. Invite teammate → Show advanced features
```

### Templates & Examples

Provide ready-to-use templates that demonstrate value:

| Product Type | Template Examples |
|--------------|-------------------|
| Design tool | UI kits, component libraries |
| Doc tool | Meeting notes, project plans |
| CRM | Sales pipeline, customer database |
| Analytics | Dashboard templates |
| Email | Campaign templates |

### Onboarding Checklist

```markdown
□ Connect [integration]
□ Create your first [core object]
□ Invite team member
□ Customize settings
□ Explore [key feature]

Progress: 3/5 complete
```

---

## Free Tier Strategy

### Defining Free Tier Limits

| Limit Type | Examples | Conversion Trigger |
|------------|----------|-------------------|
| Feature gates | Basic vs premium features | Need advanced functionality |
| Usage limits | 5 projects, 100MB storage | Hit capacity |
| User limits | 1 user vs unlimited | Team needs |
| Time limits | 14-day trial | Trial expiration |
| Support limits | Community vs priority | Need help |

### Free Tier Best Practices

```
TOO GENEROUS                      TOO RESTRICTIVE
────────────────────             ────────────────────
Unlimited everything             1 project only
No reason to upgrade             Cannot see value
Low conversion                   High abandonment

BALANCED
────────────────────
Enough to hit Aha moment
Clear path to limits
Natural upgrade triggers
```

---

## Self-Serve Checkout Design

### Pricing Page Essentials

| Element | Description |
|---------|-------------|
| Clear tiers | 2-4 pricing tiers max |
| Feature comparison | What's included in each |
| Highlight popular | "Most Popular" badge |
| Annual discount | 15-20% off annual |
| No "Contact Sales" | For basic/pro tiers |
| FAQ | Address objections |

### Checkout Flow

```
1. Select Plan
   → Show benefits, pricing clearly

2. Account Creation (if new)
   → Social login option
   → Minimal fields

3. Payment
   → Multiple methods (card, PayPal)
   → Security badges

4. Instant Access
   → No approval wait
   → Immediate upgrade
```

---

## Expansion Playbooks

### Seat Expansion

```
TRIGGER: User invites 3rd teammate (on 2-seat plan)

IN-PRODUCT:
  "Your team is growing! 🎉
   Upgrade to Team plan for unlimited seats."
  [Upgrade Now] [Learn More]

EMAIL (to admin):
  Subject: Your team is ready for [Product] Team plan
  Body: Benefits of Team plan, social proof
  CTA: Upgrade to Team

FOLLOW-UP (7 days):
  Usage report showing team activity
  "Your team has collaborated on 15 projects.
   Upgrade to unlock advanced team features."
```

### Feature Upsell

```
TRIGGER: User attempts gated feature

CONTEXTUAL PROMPT:
  "Advanced reporting is available on Pro plan"
  [See Example Report]
  [Upgrade to Pro - $X/mo]

ALTERNATIVE:
  Show preview/demo of feature
  Highlight value delivered
  Offer trial of higher tier
```

---

## Activation Metrics to Track

| Metric | Definition | Target |
|--------|------------|--------|
| Time to Value | Signup to Aha moment | < 5 minutes |
| Activation Rate | % users hitting Aha | > 40% |
| Onboarding Completion | % completing checklist | > 60% |
| Day 1 Retention | % returning next day | > 30% |
| Empty State Time | Time with no data | < 2 minutes |

---

## Conversion Optimization Best Practices

### In-Product Upgrade Prompts

**When to Show:**
- User hits 80% of limit (not 100%)
- User attempts premium feature
- User shows high engagement (PQL signal)
- Natural workflow pause

**When NOT to Show:**
- During first session
- During critical workflow
- More than once per session
- After recent dismissal

### Pricing Page Copy

**Bad Examples:**
```
"Get More Features"
"Upgrade Now"
"Premium Plan"
```

**Good Examples:**
```
"Unlock unlimited projects for your growing team"
"Remove limits and collaborate with 10+ members"
"Get priority support and advanced analytics"
```

### Feature Gate Messaging

**Bad:**
```
"This feature is for Pro users only"
[Upgrade]
```

**Good:**
```
"Advanced reporting helps teams like [Similar Company]
save 10 hours per week on analysis.
Available on Pro plan."
[See Example] [Upgrade to Pro]
```

---

## A/B Testing Ideas

### Onboarding Tests
- [ ] Number of signup fields (2 vs 3 vs 5)
- [ ] Social login vs email/password only
- [ ] Tutorial video vs interactive walkthrough
- [ ] Empty state vs pre-filled templates
- [ ] Checklist vs progress bar

### Upgrade Prompt Tests
- [ ] Prompt timing (70% vs 80% vs 90% of limit)
- [ ] Prompt format (banner vs modal vs sidebar)
- [ ] CTA copy ("Upgrade" vs "Unlock" vs "Get unlimited")
- [ ] Price anchoring (monthly vs annual first)
- [ ] Social proof presence (with/without testimonials)

### Pricing Page Tests
- [ ] Number of tiers (2 vs 3 vs 4)
- [ ] Annual discount amount (15% vs 20% vs 25%)
- [ ] Feature comparison layout (table vs cards)
- [ ] CTA position (top vs bottom vs both)
- [ ] FAQ placement (above vs below fold)

---

## Expansion Signals to Monitor

### Team Growth Signals
- Multiple users from same domain
- Sharing/collaboration actions
- @mentions in comments
- External invitations sent
- Workspace creation

### Power User Signals
- Daily active usage
- Advanced feature adoption
- API usage
- Integration connections
- High data volume

### Upsell Readiness Signals
- Feature gate hits (3+ times)
- Limit notifications viewed
- Pricing page visits
- Competitor comparison searches
- Support requests for premium features

---

## Related Methodologies

- **plg-implementation-guide:** PLG Implementation Steps & Playbooks
- **plg-basics:** PLG Basics & Models
- **plg-metrics:** PLG Metrics & Tracking
- **activation-rate:** Activation Rate Optimization
- **funnel-optimization:** Funnel Optimization
- **ab-testing-framework:** A/B Testing Framework

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Map funnel metrics and baseline metrics | haiku | Direct query of existing data |
| A/B test hypothesis generation and prioritization | sonnet | Reasoning about impact/confidence/ease |
| Landing page copywriting and design feedback | sonnet | Creative iteration, user psychology |
| Funnel optimization campaign setup | opus | Complex multi-funnel strategy, org-wide impact |
| Free trial flow analysis and recommendations | sonnet | Understanding conversion psychology |
| PLG product strategy and feature design | opus | Architecture decisions, product-market fit |
| Onboarding flow user testing interpretation | sonnet | Qualitative analysis and recommendations |

---

## Sources

- [Freemium Pricing Strategy (ProfitWell)](https://www.profitwell.com/recur/all/freemium-pricing-strategy)
- [Self-Serve Checkout Best Practices (Stripe)](https://stripe.com/guides/saas-checkout-optimization)
- [Expansion Revenue Playbooks (ChartMogul)](https://chartmogul.com/blog/expansion-revenue/)
- [Progressive Onboarding (Appcues)](https://www.appcues.com/blog/progressive-onboarding)
- [Feature Gate Optimization (Reforge)](https://www.reforge.com/blog/feature-gating-strategies)

---

*Methodology: plg-optimization-tactics | Growth | faion-growth-agent*
