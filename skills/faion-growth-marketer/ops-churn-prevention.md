---
id: churn-prevention
name: "Churn Prevention"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Churn Prevention

## Metadata

| Field | Value |
|-------|-------|
| **ID** | churn-prevention |
| **Name** | Churn Prevention |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | churn-basics, customer-success, onboarding-emails |

---

## Problem

You've identified churn patterns and at-risk customers. Now you need to intervene before they leave and recover those who already churned.

Churn prevention means taking action to save customers before cancellation and winning back those who left.

---

## Framework

Churn prevention follows this approach:

```
INTERVENE -> Act before they leave
RECOVER   -> Win back churned customers
OPTIMIZE  -> Continuous improvement
```

### Step 1: Intervene Early

**Intervention strategies by signal:**

| Signal | Intervention |
|--------|--------------|
| No login 7 days | Re-engagement email |
| No login 14 days | Personal outreach |
| Feature drop-off | "Did you know?" email |
| Support complaint | Manager follow-up |
| Cancel attempt | Save offer |
| Payment failure | Dunning sequence |

**Re-engagement email:**
```
Subject: We miss you, [Name]

Haven't seen you in a while. Is everything okay?

A few things you might have missed:
- [New feature]
- [Popular use case]

Need help? Just reply to this email.

[Your name]
```

**Save offer (at cancellation):**
```
Before you go...

We'd hate to lose you. How about:
- [ ] 50% off your next 2 months
- [ ] Free upgrade to [plan] for 1 month
- [ ] Pause your account for 30 days
- [ ] Schedule a call to discuss your needs

[Accept offer] [Continue cancellation]
```

### Step 2: Recover Churned Customers

**Win-back timing:**

| Time Since Churn | Message Focus | Offer |
|------------------|---------------|-------|
| 7 days | "Miss us?" | Extended trial |
| 30 days | "What's changed" | Discount |
| 90 days | New features | Fresh start |
| 6 months | Major update | Special offer |

**Win-back email:**
```
Subject: A lot has changed since you left

Hi [Name],

Since you left [X months ago], we've:
- Added [feature they requested]
- Fixed [issue they had]
- Improved [relevant area]

Would you give us another try?

[Special offer: X% off / free month]

[CTA: Come back]
```

---

## Templates

### Churn Prevention Playbook

```markdown
## Churn Prevention Playbook

### Early Warning Triggers
| Trigger | Condition | Action |
|---------|-----------|--------|
| No login | >7 days | Auto-email |
| No login | >14 days | Personal email |
| Support ticket | Negative sentiment | Escalate |
| Feature usage | <20% of norm | "Tips" email |
| Health score | <40 | Manual review |

### Save Offers
| Segment | Offer | Discount |
|---------|-------|----------|
| Price objection | 50% off 2 months | 50% |
| Time objection | Pause 30 days | N/A |
| Feature gap | Upgrade trial | Free upgrade |

### Win-Back Campaigns
| Timing | Subject | Offer |
|--------|---------|-------|
| Day 7 | "We want you back" | 30% off |
| Day 30 | "What's new" | Free month |
| Day 90 | "Major update" | 50% off |
```

---

## Examples

### Example 1: SaaS Churn Reduction

**Problem:** 7% monthly churn

**Actions:**
1. Added onboarding sequence
2. Implemented health scoring
3. Created save offer (50% off)
4. Launched win-back campaign

**Results:**
- Churn reduced to 4%
- Save offer converts 25%
- Win-back recovers 10%

### Example 2: Membership Churn

**Problem:** Annual members not renewing

**Actions:**
1. Quarterly check-ins
2. New content announcements
3. Renewal discount for multi-year
4. Community engagement push

**Results:**
- First-year retention: 60% → 75%
- Multi-year commitments: 20%

---

## Implementation Checklist

### Prevention
- [ ] Design re-engagement emails
- [ ] Create save offer flow
- [ ] Train on objection handling
- [ ] Set up dunning sequence

### Recovery
- [ ] Plan win-back campaigns
- [ ] Create win-back emails
- [ ] Track win-back success
- [ ] Learn from churned feedback

---

## Churn Reduction Priorities

| Action | Impact | Effort | Priority |
|--------|--------|--------|----------|
| Onboarding improvement | High | Medium | 1 |
| Save offer implementation | High | Low | 2 |
| Health score alerts | Medium | Medium | 3 |
| Win-back campaigns | Medium | Low | 4 |
| Feature adoption emails | Medium | Low | 5 |

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Generic save offer | Doesn't address issue | Segment by reason |
| Giving up after cancel | Missing recovery | Run win-back campaigns |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Email | Customer.io, Intercom |
| Dunning | Stripe, Churnkey, Chargebee |

---

## Related Methodologies

- **churn-basics:** Churn Basics (measurement and analysis)
- **subscription-models:** Subscription Models (retention design)
- **customer-success:** Customer Success (proactive retention)
- **onboarding-emails:** Onboarding Emails (first-month retention)

---

*Methodology: churn-prevention | Operations & Business | faion-growth-agent*
