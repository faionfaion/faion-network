---
id: plg-implementation-guide
name: "PLG Implementation Guide"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# PLG Implementation Guide

## Metadata

| Field | Value |
|-------|-------|
| **ID** | plg-implementation-guide |
| **Name** | PLG Implementation Guide |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | plg-basics, plg-metrics, plg-optimization-tactics |

---

## Implementing PLG

### Step 1: Define Your Aha Moment

The "Aha moment" is when users first experience core value.

**Examples:**

| Product | Aha Moment |
|---------|------------|
| Slack | First message in channel |
| Dropbox | First file synced across devices |
| Zoom | First successful video call |
| Notion | First page created and shared |
| Figma | First design collaboration |

**How to find your Aha moment:**

1. Interview converted users: "When did you decide to pay?"
2. Analyze behavior of retained vs churned users
3. Find the action most correlated with retention
4. Validate with cohort analysis

---

### Step 2: Optimize Time to Value (TTV)

TTV = Time from signup to Aha moment

```
BAD TTV (days/weeks)              GOOD TTV (minutes)
─────────────────────────         ─────────────────────
Long onboarding                   Skip onboarding
Setup required                    Pre-configured
Learning curve                    Intuitive UI
Empty state                       Sample data/templates
```

**TTV Reduction Tactics:**

| Tactic | Description | Impact |
|--------|-------------|--------|
| Progressive onboarding | Learn while doing | High |
| Templates | Start with examples | High |
| Pre-filled data | Show populated state | Medium |
| Interactive tutorials | Guided first use | High |
| Single-player mode | Work alone first | Medium |
| Social login | Reduce signup friction | Medium |

---

### Step 3: Build In-Product Upgrade Triggers

**Types of upgrade triggers:**

| Trigger | Example | When to Show |
|---------|---------|--------------|
| Usage limit | "You've used 80% of storage" | Near limit |
| Feature gate | "Upgrade to export as PDF" | Feature use |
| Time limit | "Trial ends in 3 days" | Trial ending |
| Collaboration | "Invite team members" | Ready to expand |
| Value milestone | "You've saved 10 hours" | Value proven |

**In-product upgrade UI:**

```
Bad:  Intrusive pop-up on every page
Good: Contextual prompt when user hits limit

Bad:  "Upgrade to Pro for $99/mo"
Good: "You're trying to invite a 4th member.
       Upgrade to Team plan to add unlimited members."
```

---

### Step 4: Enable Self-Serve Purchasing

**Self-serve checkout essentials:**

| Element | Description |
|---------|-------------|
| Clear pricing | No "contact sales" for basic plans |
| Plan comparison | Feature matrix |
| Instant access | No approval wait |
| Multiple payment | Card, PayPal, invoicing |
| Proration | Upgrade mid-cycle |
| Easy downgrade | Reduce friction to try higher tier |

---

### Step 5: Implement Product-Qualified Leads (PQLs)

See [plg-metrics.md](plg-metrics.md) for PQL scoring details.

---

## PLG Playbooks

### Playbook 1: Freemium to Paid

```
TRIGGER: User hits usage limit

DAY 0: Show limit notification
  "You've reached 5 projects. Upgrade to Pro for unlimited."
  [Upgrade Now] [See Plans]

DAY 2: If no action, email
  Subject: "You're close to your project limit"
  Body: Value of upgrading + testimonial

DAY 5: In-product reminder
  "1 project remaining. Here's what you get with Pro..."

DAY 7: Offer incentive
  "Upgrade this week: 20% off first 3 months"
```

### Playbook 2: Trial to Paid

```
TRIAL DAY 1-3: Activation focus
  - Welcome email with quickstart
  - In-app checklist to Aha moment
  - Chat widget for questions

TRIAL DAY 4-7: Value demonstration
  - Usage report email: "You've done X, saved Y"
  - Feature discovery prompts
  - Social proof: similar companies

TRIAL DAY 8-11: Conversion intent
  - PQL scoring check
  - High PQL: Sales outreach
  - Low PQL: Automated nurture

TRIAL DAY 12-14: Urgency
  - Countdown in product
  - Final offer email
  - What you'll lose messaging
```

### Playbook 3: Expansion (Seat Growth)

```
TRIGGER: Team is actively collaborating

SIGNALS:
- 3+ active users
- Mentions of other team members
- @mentions in comments
- External sharing

ACTIONS:
1. In-product: "Your team is growing! Add more members."
2. Email to admin: "See how Team plan can help your team"
3. If high PQL score: Sales call for Team/Enterprise
```

---

## PLG Implementation Checklist

### Phase 1: Foundation
- [ ] Define Aha moment
- [ ] Measure current TTV
- [ ] Map user journey to value
- [ ] Identify conversion triggers
- [ ] Set up product analytics

### Phase 2: Free Tier Design
- [ ] Choose PLG model (freemium/trial/usage)
- [ ] Define free tier limits
- [ ] Create upgrade triggers
- [ ] Design self-serve checkout
- [ ] Build pricing page

### Phase 3: Activation Optimization
- [ ] Simplify signup (< 3 fields)
- [ ] Create onboarding flow
- [ ] Add templates/examples
- [ ] Build interactive tutorials
- [ ] Reduce TTV to < 5 min

### Phase 4: Monetization
- [ ] Define PQL criteria
- [ ] Build PQL scoring
- [ ] Create upgrade prompts
- [ ] Set up automated emails
- [ ] (Optional) Add sales assist

### Phase 5: Expansion
- [ ] Identify expansion triggers
- [ ] Build seat/usage upgrade flows
- [ ] Create upsell playbooks
- [ ] Track expansion revenue
- [ ] Optimize net retention

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Free tier too generous | No reason to upgrade | Add meaningful limits |
| Free tier too limited | Users cannot see value | Give enough to hit Aha |
| Complex onboarding | Users abandon | Reduce to essentials |
| No clear Aha moment | Users do not activate | Define and optimize for it |
| Sales-first mindset | Friction, high CAC | Trust the product |
| No PQL tracking | Missed opportunities | Instrument behavior |
| Upgrade nag too early | Annoys users | Wait for value delivery |

---

## Tools & Tech Stack

| Category | Tools |
|----------|-------|
| Product Analytics | Amplitude, Mixpanel, PostHog |
| Onboarding | Appcues, Pendo, Userflow, Chameleon |
| In-app Messaging | Intercom, Drift, Crisp |
| User Feedback | Hotjar, FullStory, Heap |
| Billing | Stripe, Paddle, Chargebee |
| Email Automation | Customer.io, Autopilot, Klaviyo |
| PQL Scoring | Madkudu, Clearbit Reveal, custom |

---

## Related Methodologies

- **plg-basics:** PLG Basics & Models
- **plg-metrics:** PLG Metrics & Tracking
- **plg-optimization-tactics:** Activation, Free Tier, Checkout, Expansion
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **growth-loops:** Growth Loops
- **activation-rate:** Activation Rate Optimization

## Sources

- [Product-Led Growth by Wes Bush](https://productled.com/book/)
- [OpenView PLG Benchmarks](https://openviewpartners.com/product-led-growth/#benchmarks)
- [Elena Verna PLG Playbook](https://www.elenaverna.com/plg-playbook)
- [PQL Definition and Scoring (Madkudu)](https://www.madkudu.com/blog/what-is-a-product-qualified-lead)
- [Time to Value Optimization (Amplitude)](https://amplitude.com/blog/time-to-value)

---

*Methodology: plg-implementation-guide | Growth | faion-growth-agent*
