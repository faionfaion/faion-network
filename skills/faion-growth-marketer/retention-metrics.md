---
id: retention-metrics
name: "Retention Metrics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Retention Metrics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | retention-metrics |
| **Name** | Retention Metrics |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | retention-basics, retention-strategies, cohort-analysis |

---

## Retention Benchmarks

### By Product Type

| Product Type | D1 | D7 | D30 |
|--------------|-----|-----|------|
| Social app | 40-60% | 25-35% | 15-25% |
| Mobile game | 35-45% | 15-25% | 5-10% |
| B2B SaaS | 50-70% | 40-55% | 30-45% |
| Consumer subscription | 60-80% | 50-65% | 40-55% |
| E-commerce | 15-25% | 8-15% | 3-8% |

### Engagement Ratios

| Ratio | Poor | Average | Good | Great |
|-------|------|---------|------|-------|
| DAU/MAU | <15% | 15-25% | 25-40% | >40% |
| WAU/MAU | <40% | 40-60% | 60-75% | >75% |

### By Industry

| Industry | Good Monthly Churn | Great Monthly Churn |
|----------|-------------------|---------------------|
| B2B SaaS | <5% | <2% |
| Consumer subscription | <8% | <5% |
| Mobile app | <10% | <7% |

---

## Templates

### Retention Loop Design Template

```markdown
# Retention Loop: [Name]

## Loop Type
[ ] Content  [ ] Social  [ ] Progress
[ ] Stored Value  [ ] Workflow  [ ] Network

## Loop Components

### Trigger
**External:**
- [Notification/email type]
- [Frequency]

**Internal (goal):**
- [What emotion/need triggers return?]

### Action
**Primary action:** [What user does]
**Friction level:** [Low/Medium/High]

### Reward
**Type:** [Tribe/Hunt/Self]
**Variable element:** [What changes?]
**Immediate feedback:** [What user sees]

### Investment
**What user puts in:** [Data/time/social capital]
**How it improves next experience:** [Personalization/value accrual]

## Metrics
- Daily retention target: ____%
- Weekly retention target: ____%
- Monthly retention target: ____%

## Implementation Plan
1. [First mechanism to build]
2. [Second mechanism]
3. [Triggers to add]
```

### Engagement Dashboard Template

```markdown
# Engagement & Retention Dashboard - [Week]

## Retention Rates
| Cohort | D1 | D7 | D30 | D90 |
|--------|-----|-----|------|------|
| This week | | | | |
| Last week | | | | |
| 4 weeks ago | | | | |

## Engagement Metrics
| Metric | Value | WoW | Target |
|--------|-------|-----|--------|
| DAU | | | |
| WAU | | | |
| MAU | | | |
| DAU/MAU | | | |
| Sessions/DAU | | | |
| Session length | | | |

## Retention Loop Health
| Loop | Participation | Completion | Impact |
|------|---------------|------------|--------|
| Streak | 45% have streak | 80% maintain | High |
| Social | 60% connected | 40% interact | Medium |
| Content | 90% view | 30% create | High |

## Churn Analysis
| Segment | At Risk | Churned | Reactivated |
|---------|---------|---------|-------------|
| New (0-30d) | | | |
| Core (30-90d) | | | |
| Mature (90d+) | | | |

## This Week's Focus
- Loop to optimize: ___
- Experiment: ___
- Re-engagement campaign: ___
```

---

## Churn Prediction

Identify at-risk users before they leave.

```
CHURN RISK SCORE

Low Risk (0-30):
- Daily active
- Multiple sessions
- Using core features

Medium Risk (30-70):
- Weekly active (down from daily)
- Shorter sessions
- Fewer features used

High Risk (70-100):
- Monthly or less
- Very short sessions
- Only checking, not engaging

Actions by risk:
- Low: Maintain current experience
- Medium: Re-engagement nudge
- High: Personal outreach
```

---

## Implementation Checklist

### Phase 1: Understand Current State
- [ ] Calculate D1, D7, D30 retention
- [ ] Map user journey post-signup
- [ ] Identify current triggers (if any)
- [ ] Analyze what retained users do differently

### Phase 2: Design Retention Loop
- [ ] Identify primary loop type for your product
- [ ] Define trigger strategy
- [ ] Design reward mechanism
- [ ] Create investment opportunities
- [ ] Map loop visually

### Phase 3: Build Engagement Mechanics
- [ ] Implement core loop
- [ ] Add streak/progress mechanics
- [ ] Set up notification system
- [ ] Build achievement system

### Phase 4: Measure and Optimize
- [ ] Set up retention dashboards
- [ ] Track loop participation
- [ ] Build churn prediction
- [ ] Create re-engagement campaigns
- [ ] A/B test loop variations

---

## Tools

| Purpose | Tools |
|---------|-------|
| Retention analytics | Amplitude, Mixpanel, Posthog |
| Push notifications | OneSignal, Braze, Intercom |
| Email re-engagement | Customer.io, Iterable |
| Gamification | Badgeville, Gamify |
| Churn prediction | ChurnZero, Totango |

---

## Related Methodologies

- **retention-basics:** Retention Basics & Hook Model
- **retention-strategies:** Retention Patterns & Strategies
- **cohort-analysis:** Cohort Analysis
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

*Methodology: retention-metrics | Growth | faion-growth-agent*
