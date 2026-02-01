---
id: churn-basics
name: "Churn Basics"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Churn Basics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | churn-basics |
| **Name** | Churn Basics |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | churn-prevention, subscription-models, customer-success |

---

## Problem

You're acquiring customers, but they keep leaving. Every churned customer costs you the acquisition spend plus all future revenue. At 5% monthly churn, you lose half your customers every year. Reducing churn from 5% to 3% can double your customer lifetime value.

Churn basics means understanding how to measure churn, identify patterns, and segment reasons.

---

## Framework

Churn measurement follows this approach:

```
MEASURE   -> Know your churn rate and patterns
IDENTIFY  -> Find leading indicators
SEGMENT   -> Understand who churns and why
```

### Step 1: Measure Churn

**Churn types:**

| Type | Definition | Formula |
|------|------------|---------|
| **Customer churn** | Customers who left | Lost / Starting customers |
| **Revenue churn** | Revenue lost | Lost MRR / Starting MRR |
| **Logo churn** | Accounts lost | Same as customer churn |
| **Net revenue retention** | Revenue including expansion | (Start + Expansion - Churn) / Start |

**Churn benchmarks:**

| Business Type | Monthly Churn | Annual Churn |
|---------------|---------------|--------------|
| Consumer SaaS | 5-7% | 45-60% |
| SMB SaaS | 3-5% | 30-45% |
| Mid-market | 1-2% | 10-20% |
| Enterprise | <1% | <10% |

**Calculate your churn:**
```
Monthly churn = Customers lost this month / Customers at start of month

Annual churn = 1 - (1 - monthly churn)^12
Example: 5% monthly = 1 - (0.95)^12 = 46% annual
```

### Step 2: Identify Warning Signs

**Leading indicators of churn:**

| Indicator | Signal | Risk Level |
|-----------|--------|------------|
| Login frequency | Decreasing logins | Medium |
| Feature usage | Using fewer features | High |
| Support tickets | Frustrated requests | High |
| Payment failures | Card declining | High |
| No engagement | Zero usage 14+ days | Critical |
| Feedback | Negative surveys | High |

**Build a health score:**

```
Health Score = (
  Login frequency (0-25) +
  Feature usage (0-25) +
  Support sentiment (0-25) +
  Account age (0-25)
) / 100

< 40 = At-risk
40-70 = Needs attention
> 70 = Healthy
```

### Step 3: Segment Churn Reasons

**Common churn reasons:**

| Reason | % of Churn | Preventable? |
|--------|------------|--------------|
| Not using product | 25-30% | Yes |
| Not seeing value | 20-25% | Yes |
| Switched to competitor | 15-20% | Sometimes |
| Budget/price | 15-20% | Partially |
| Business closed | 5-10% | No |
| Bad support experience | 5-10% | Yes |

**Churn survey:**
```markdown
We're sorry to see you go. To help us improve, could you share why?

- [ ] I wasn't using it enough
- [ ] It's too expensive
- [ ] Missing features I need
- [ ] Found a better alternative
- [ ] My needs changed
- [ ] Technical issues
- [ ] Other: [text field]
```

---

## Templates

### Churn Analysis Dashboard

```markdown
## Churn Report: [Month]

### Overview
- Starting MRR: $X
- Churned MRR: $X
- Expansion MRR: $X
- Net change: $X

- Customer churn: X%
- Revenue churn: X%
- Net revenue retention: X%

### Churn by Reason
| Reason | Customers | MRR Lost | % |
|--------|-----------|----------|---|
| Not using | X | $X | X% |
| Price | X | $X | X% |
| Competitor | X | $X | X% |
| Other | X | $X | X% |

### Churn by Cohort
| Cohort | Start | Churned | Rate |
|--------|-------|---------|------|
| Jan | X | X | X% |
| Feb | X | X | X% |
| Mar | X | X | X% |

### At-Risk Accounts
| Account | Health Score | MRR | Issue | Action |
|---------|--------------|-----|-------|--------|
| [Name] | 35 | $X | No login | Outreach |
```

---

## Examples

### Example 1: SaaS Churn Analysis

**Problem:** 7% monthly churn

**Analysis:**
- 40% churned without using product
- 30% cited price
- 30% other reasons

**Key insight:** Onboarding issue, not product issue

### Example 2: Membership Churn

**Problem:** Annual members not renewing

**Analysis:**
- Most churn at year 1 renewal
- Low engagement last 3 months
- "Got what I needed" reason

**Key insight:** Need ongoing value delivery

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Only measuring churn | Too late to act | Track leading indicators |
| No exit survey | Don't learn reasons | Ask every churner |
| Ignoring low usage | Silent churn | Monitor engagement |
| Blaming customers | Don't improve | Own the problem |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Analytics | Mixpanel, Amplitude, Heap |
| Health scoring | Vitally, Totango, Custom |
| Surveys | Typeform, SurveyMonkey |

---

## Related Methodologies

- **churn-prevention:** Churn Prevention (intervention strategies)
- **subscription-models:** Subscription Models (retention design)
- **customer-success:** Customer Success (proactive retention)
- **onboarding-emails:** Onboarding Emails (first-month retention)

---

*Methodology: churn-basics | Operations & Business | faion-growth-agent*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Pull analytics data from Mixpanel, format report | haiku | Data extraction and formatting |
| Analyze A/B test results for statistical significance | sonnet | Statistical analysis and interpretation |
| Generate cohort retention curve analysis | sonnet | Data interpretation and visualization |
| Design growth loop for new product vertical | opus | Strategic design with multiple levers |
| Recommend optimization tactics for viral coefficient | sonnet | Metrics understanding and recommendations |
| Plan AARRR framework for pre-launch phase | opus | Comprehensive growth strategy |
| Implement custom analytics event tracking schema | sonnet | Technical setup and validation |
