---
id: plg-basics
name: "PLG Basics & Models"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# PLG Basics & Models

## Metadata

| Field | Value |
|-------|-------|
| **ID** | plg-basics |
| **Name** | PLG Basics & Models |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | plg-metrics, plg-implementation |

---

## Problem

Traditional SaaS sales require expensive sales teams, long cycles, and high customer acquisition costs. You cannot scale revenue without scaling headcount.

Product-Led Growth (PLG) makes the product itself the main driver of acquisition, conversion, and expansion. Users can discover, try, buy, and upgrade without talking to sales.

---

## Framework

### What is Product-Led Growth?

PLG is a go-to-market strategy where the product is the primary vehicle for acquiring, activating, and retaining customers.

```
TRADITIONAL (SALES-LED)              PRODUCT-LED (PLG)
──────────────────────────           ──────────────────────
Marketing → MQL → Sales →            Marketing → Product →
Demo → Negotiate → Close             Self-serve → Activate →
Onboard → Support                    Expand → Upgrade

High touch, expensive                Low touch, scalable
$50K+ deals                          $0 to $XX,XXX deals
Long cycles (weeks/months)           Fast cycles (minutes/days)
```

### PLG vs Sales-Led vs Marketing-Led

| Aspect | Sales-Led | Marketing-Led | Product-Led |
|--------|-----------|---------------|-------------|
| Primary driver | Sales team | Content/ads | Product experience |
| First touch | Demo request | Content download | Free trial/freemium |
| Conversion | Sales negotiation | Marketing nurture | Self-serve upgrade |
| CAC | High ($500-5,000+) | Medium ($100-500) | Low ($10-100) |
| Deal size | Large ($10K+/yr) | Medium ($1K-10K) | Any size |
| Scale | Linear (add reps) | Semi-scalable | Exponential |

### The PLG Flywheel

```
        ┌─────────────────┐
        │   ACQUISITION   │
        │  (Free signup)  │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │   ACTIVATION    │
        │ (First value)   │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │   ENGAGEMENT    │
        │  (Habit loop)   │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │   MONETIZATION  │
        │   (Conversion)  │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │    EXPANSION    │←─────┐
        │   (Upsell)      │      │
        └────────┬────────┘      │
                 ↓               │
        ┌─────────────────┐      │
        │    REFERRAL     │──────┘
        │   (Virality)    │
        └─────────────────┘
```

---

## PLG Models

### Model 1: Freemium

Users get free access to a limited version forever.

```
FREE TIER                    PAID TIER
─────────────────────       ─────────────────────
Limited features             All features
Limited usage                Unlimited usage
Community support            Priority support
Ads (sometimes)              No ads

Examples: Spotify, Slack, Notion, Figma
```

**Best for:**
- Mass market products
- Network effect products
- Products with low marginal cost

**Conversion triggers:**
- Usage limits hit
- Need advanced features
- Team collaboration needs

### Model 2: Free Trial

Users get full access for limited time.

```
TRIAL (14-30 days)          PAID
─────────────────────       ─────────────────────
All features                 All features
Full usage                   Full usage
No credit card (opt)         Payment required

Examples: Netflix, HubSpot, Salesforce
```

**Best for:**
- Complex products needing time to evaluate
- B2B with clear ROI
- Products with high switching costs

**Conversion triggers:**
- Trial expiration
- Value demonstrated
- Urgency messaging

### Model 3: Open Core

Core product is free/open source, premium features paid.

```
OPEN SOURCE                 ENTERPRISE
─────────────────────       ─────────────────────
Core functionality           Advanced features
Self-hosted                  Cloud/managed
Community support            Enterprise support
No SLA                       SLA + compliance

Examples: GitLab, Elastic, Redis, MongoDB
```

**Best for:**
- Developer tools
- Infrastructure products
- Products with strong community

### Model 4: Usage-Based

Pay based on consumption.

```
Pricing: $X per [unit]

Examples:
- AWS: per compute hour
- Twilio: per API call
- Stripe: per transaction
- Snowflake: per query

Best for: Variable usage, clear value metric
```

---

## Is PLG Right for You?

### PLG Works Best When:

| Factor | Good Fit | Poor Fit |
|--------|----------|----------|
| Product complexity | Simple, intuitive | Requires training |
| Decision maker | End user | C-level/procurement |
| Price point | < $50K/year | > $50K/year |
| Time to value | Minutes to hours | Days to weeks |
| Trial feasibility | Easy to try | Requires implementation |
| Market size | Large TAM | Niche market |

### Hybrid PLG + Sales

Many companies combine PLG with sales:

```
SMB / Self-serve                    ENTERPRISE / Sales-assist
─────────────────────────          ─────────────────────────
< $1K/month                         > $1K/month
Product does the selling            Sales helps close
Automated onboarding                White-glove onboarding
In-product support                  Dedicated CSM
```

---

## Examples

### Example 1: Slack

**PLG Model:** Freemium

**Free tier:**
- 10K message history
- 10 integrations
- 1:1 video calls

**Aha moment:** First message in a channel with teammates

**TTV:** < 5 minutes (invite team → create channel → send message)

**Conversion triggers:**
- Message history limit
- Guest access needed
- Enterprise security requirements

**Results:**
- 30%+ teams convert to paid
- 143% net revenue retention
- > 750K paid customers

### Example 2: Zoom

**PLG Model:** Freemium + Usage-based

**Free tier:**
- Unlimited 1:1 calls
- 40-minute group calls
- 100 participants

**Aha moment:** First successful video call

**TTV:** < 2 minutes (join call → see faces → talk)

**Conversion triggers:**
- 40-minute limit hit
- Need cloud recording
- Webinar features

**Results:**
- Pandemic growth: 10M → 300M daily participants
- Low CAC through word of mouth

### Example 3: Notion

**PLG Model:** Freemium

**Free tier:**
- Unlimited pages (personal)
- Limited blocks (team)
- Basic integrations

**Aha moment:** First useful page created and used

**TTV:** 5-10 minutes with templates

**Conversion triggers:**
- Team collaboration needs
- Block limits for teams
- Admin controls

**Results:**
- 4M+ users
- High virality through templates
- Strong expansion within teams

### Example 4: Calendly

**PLG Model:** Freemium

**Free tier:**
- 1 event type
- Calendar integration
- Basic customization

**Aha moment:** First meeting booked via link

**TTV:** 3 minutes (connect calendar → create event → share link)

**Conversion triggers:**
- Need multiple event types
- Team scheduling
- Integrations (Salesforce, Stripe)

**Viral loop:**
- Every scheduled meeting = product exposure
- Recipients see "Powered by Calendly"
- Natural PLG + viral growth

---

## Related Methodologies

- **plg-metrics:** PLG Metrics & Tracking
- **plg-implementation:** PLG Implementation Guide
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **growth-loops:** Growth Loops

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

- [Product-Led Growth (Wes Bush)](https://productled.com/book/)
- [OpenView PLG Research](https://openviewpartners.com/product-led-growth/)
- [PLG Benchmarks (Kyle Poyar)](https://kylepoyar.substack.com/)
- [Elena Verna on PLG](https://www.elenaverna.com/plg)
- [Lenny's Newsletter: PLG Companies](https://www.lennysnewsletter.com/p/how-the-best-product-led-growth-companies)

---

*Methodology: plg-basics | Growth | faion-growth-agent*
