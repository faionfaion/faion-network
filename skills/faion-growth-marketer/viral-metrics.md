---
id: viral-metrics
name: "Viral Metrics & K-factor"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Viral Metrics & K-factor

## Metadata

| Field | Value |
|-------|-------|
| **ID** | viral-metrics |
| **Name** | Viral Metrics & K-factor |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | viral-loops, viral-optimization, aarrr-pirate-metrics |

---

## Problem

You spend money to acquire every new user. Paid acquisition is expensive and does not scale. You need users to bring other users automatically.

The viral coefficient (K-factor) measures how many new users each existing user brings. If K > 1, your product grows exponentially without spending on ads.

---

## Framework

### What is the Viral Coefficient?

The viral coefficient (K-factor) measures the average number of new users that each existing user generates.

```
K = i × c

Where:
i = number of invites sent per user
c = conversion rate of invites (% who sign up)
```

### K-factor Interpretation

| K-factor | Meaning | Growth Pattern |
|----------|---------|----------------|
| K < 0.5 | Weak virality | Slow organic growth |
| K = 0.5-1.0 | Good virality | Steady amplification |
| K = 1.0 | Break-even | Each user brings 1 new user |
| K > 1.0 | Viral | Exponential growth |
| K > 2.0 | Highly viral | Rapid exponential growth |

---

## K-factor Calculation

### Basic Formula

```
K = Invites per User × Conversion Rate

Example:
- Average user sends 5 invites
- 20% of invitees sign up
- K = 5 × 0.20 = 1.0
```

### Extended Formula with Time

```
K(t) = (Users at time 0) × K^(t/cycle_time)

Where:
- cycle_time = average time from signup to invite conversion
```

### User Growth Projection

If you start with 1,000 users and K = 1.2:

| Cycle | Users | New from Viral | Total |
|-------|-------|----------------|-------|
| 0 | 1,000 | - | 1,000 |
| 1 | 1,000 | 1,200 | 2,200 |
| 2 | 2,200 | 2,640 | 4,840 |
| 3 | 4,840 | 5,808 | 10,648 |
| 4 | 10,648 | 12,778 | 23,426 |

With K > 1, growth becomes exponential.

---

## Components of Virality

### Factor 1: Invites Sent (i)

**How to increase invites per user:**

| Tactic | Description | Impact |
|--------|-------------|--------|
| Natural share moments | Prompt share when user achieves something | High |
| Referral incentives | Give rewards for inviting | Medium-High |
| Multi-channel invites | Email, SMS, social, copy link | Medium |
| Contact import | Make inviting easy with bulk import | Medium |
| Viral content | Create shareable content (results, badges) | High |
| Team features | Require others to use product | Very High |

### Factor 2: Conversion Rate (c)

**How to increase invite conversion:**

| Tactic | Description | Impact |
|--------|-------------|--------|
| Personal invitation | "John invited you" vs generic | High |
| Social proof | "5 of your friends use this" | High |
| Clear value prop | Why should they sign up? | High |
| Low friction signup | One-click, minimal fields | High |
| Incentive for invitee | "Get $10 when you join" | Medium |
| Preview value | Show what they will get | Medium |

---

## Measuring K-factor

### Step 1: Track Metrics

| Metric | Description | How to Track |
|--------|-------------|--------------|
| Invites sent | Total invitations | Count invite events |
| Invites per user | Average i | Total invites / Active users |
| Invite clicks | Recipients who clicked | UTM tracking |
| Invite signups | Recipients who signed up | Referral attribution |
| Conversion rate | c = signups / invites sent | Calculate ratio |

### K-factor Dashboard Template

```markdown
# Viral Metrics Dashboard - Week of [DATE]

## K-factor Calculation

| Metric | Value | Trend |
|--------|-------|-------|
| Active users | 10,000 | +5% |
| Invites sent (total) | 2,500 | +12% |
| Invites per user (i) | 0.25 | +7% |
| Invite signups | 500 | +10% |
| Conversion rate (c) | 20% | -2% |
| **K-factor** | **0.05** | **+5%** |

## Invite Funnel

```
Invites Sent:     ██████████████████████ 2,500  (100%)
Invites Opened:   ████████████ 1,250             (50%)
Clicked to Site:  ████████ 875                   (35%)
Signed Up:        ████ 500                       (20%)
```

## By Channel

| Channel | Sent | Converted | Rate |
|---------|------|-----------|------|
| Email | 1,000 | 250 | 25% |
| WhatsApp | 500 | 125 | 25% |
| Copy link | 800 | 100 | 12.5% |
| Twitter | 200 | 25 | 12.5% |

## Top Referrers

| User | Invites | Conversions | K-contribution |
|------|---------|-------------|----------------|
| User A | 50 | 15 | 0.30 |
| User B | 30 | 8 | 0.27 |
| User C | 25 | 6 | 0.24 |

## Actions This Week
1. [Action to improve i]
2. [Action to improve c]
```

---

## K-factor Benchmarks

### By Product Type

| Product Type | Typical K | Great K |
|--------------|-----------|---------|
| B2B SaaS | 0.1-0.3 | 0.5+ |
| Consumer app | 0.2-0.5 | 1.0+ |
| Collaboration tool | 0.5-1.5 | 2.0+ |
| Marketplace | 0.1-0.4 | 0.5+ |
| Content platform | 0.3-0.8 | 1.0+ |
| Gaming | 0.1-0.5 | 1.0+ |

### Notable K-factors

| Company | Peak K | Loop Type |
|---------|--------|-----------|
| Hotmail (1996) | 1.0+ | Outbreak |
| Dropbox | 0.7 | Incentivized |
| Slack | 1.0+ | Inherent |
| WhatsApp | 1.2 | Inherent |
| TikTok | 0.8 | Content |
| Wordle | 1.5+ | Content |

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Assuming K > 1 is easy | Very few products achieve this | Aim for K = 0.3-0.5 |
| Only counting referrals | Ignores other viral loops | Track all viral sources |
| Spam-like invite flow | Damages trust, annoys users | Natural share moments |
| Generic invite messages | Low conversion | Personal, contextual invites |
| One channel only | Misses preferences | Multi-channel sharing |
| No tracking | Cannot optimize | Attribute all referrals |
| Over-incentivizing | Attracts fraud, low quality | Balance incentives |

---

## Viral Loop Calculator

### Basic Calculator

```
INPUT:
- Users: 1,000
- Invites per user (i): ___
- Conversion rate (c): ___%
- Viral cycle time: ___ days

CALCULATE:
K = i × c = ___

PROJECTION (5 cycles):
Cycle 0: 1,000 users
Cycle 1: 1,000 + (1,000 × K) = ___ users
Cycle 2: ___ + (___ × K) = ___ users
...
```

### Break-even Analysis

```
To achieve K = 1.0:

If c = 10%, need i = 10 invites/user
If c = 20%, need i = 5 invites/user
If c = 30%, need i = 3.3 invites/user
If c = 50%, need i = 2 invites/user

Current state:
- i = ___
- c = ___
- Gap to K=1: ___
```

---

## Tools

| Purpose | Tools |
|---------|-------|
| Referral tracking | ReferralCandy, Viral Loops, Friendbuy |
| Attribution | Branch, AppsFlyer, Adjust |
| Analytics | Mixpanel, Amplitude |
| A/B testing | Optimizely, LaunchDarkly |
| Social sharing | AddThis, ShareThis |

---

## Related Methodologies

- **viral-loops:** Types of viral loops and mechanics
- **viral-optimization:** Optimization experiments and tactics
- **aarrr-pirate-metrics:** AARRR Pirate Metrics (referral is the 5th stage)
- **growth-loops:** Growth Loops (viral is one type of loop)

---

*Methodology: viral-metrics | Growth | faion-growth-agent*
