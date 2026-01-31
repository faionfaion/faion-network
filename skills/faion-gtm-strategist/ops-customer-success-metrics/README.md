---
id: customer-success-metrics
name: "Customer Success Metrics"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
parent: customer-success
---

# Customer Success Metrics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | customer-success-metrics |
| **Name** | Customer Success Metrics |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | customer-success-basics, churn-prevention, analytics |

---

## Problem

Without measurement, you can't tell which customers are healthy or at risk. Health scoring provides early warning signals before customers churn, enabling proactive intervention and expansion opportunities.

---

## Framework

### Health Score Components

**Health score components:**

| Component | Weight | Data Source |
|-----------|--------|-------------|
| Product usage | 30% | Analytics |
| Feature adoption | 25% | Analytics |
| Support sentiment | 20% | Support tickets |
| Engagement | 15% | Email, activity |
| Payment health | 10% | Billing |

### Scoring System

**Scoring example:**

```
Usage Score (0-30):
- Daily active: 30
- Weekly active: 20
- Monthly active: 10
- Inactive: 0

Feature Score (0-25):
- Using all core features: 25
- Using most: 20
- Using some: 10
- Using few: 5

Support Score (0-20):
- Positive interactions: 20
- Neutral: 15
- Negative: 5
- Escalated: 0

Engagement Score (0-15):
- High email engagement: 15
- Medium: 10
- Low: 5
- None: 0

Payment Score (0-10):
- Current, no issues: 10
- Current, minor issues: 7
- Overdue: 3
- Failed: 0

Health Score = Usage + Feature + Support + Engagement + Payment
```

**Health categories:**

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Maintain, upsell |
| 60-79 | Stable | Monitor, engage |
| 40-59 | At-risk | Intervene |
| 0-39 | Critical | Urgent outreach |

---

## Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **NPS** | Promoters - Detractors | > 50 |
| **CSAT** | Satisfied / Total | > 4.5/5 |
| **Time to value** | Days to first success | < 7 days |
| **Adoption rate** | Users active / Total | > 80% |
| **Expansion rate** | Customers expanded / Total | > 20% |
| **Net retention** | MRR after churn + expansion | > 100% |

**Detailed metric definitions:**

### 1. Net Promoter Score (NPS)

```
Question: "How likely are you to recommend us? (0-10)"

Promoters: 9-10
Passives: 7-8
Detractors: 0-6

NPS = % Promoters - % Detractors

Example:
100 responses: 60 promoters, 30 passives, 10 detractors
NPS = 60% - 10% = 50
```

### 2. Customer Satisfaction (CSAT)

```
Question: "How satisfied are you? (1-5)"

CSAT = (4+5 ratings) / Total responses

Example:
100 ratings: 80 gave 4-5
CSAT = 80% or 4.5/5 average
```

### 3. Time to Value

```
Time from signup to first success metric

SaaS tool: Days to complete first key action
Course: Days to complete first module
Service: Days to first deliverable

Track by cohort to identify onboarding improvements
```

### 4. Feature Adoption

```
% of customers using each feature

Core feature adoption = Critical for retention
Advanced feature adoption = Expansion signal

Track:
- % using feature at all
- % using regularly (weekly)
- Depth of usage
```

### 5. Customer Health Score

See scoring system above.

---

## Templates

### Customer Health Dashboard

```markdown
## Customer Health: [Month]

### Overview
| Status | Customers | % | MRR |
|--------|-----------|---|-----|
| Healthy (80+) | X | X% | $X |
| Stable (60-79) | X | X% | $X |
| At-risk (40-59) | X | X% | $X |
| Critical (<40) | X | X% | $X |

### At-Risk Accounts
| Customer | Health | MRR | Issue | Action |
|----------|--------|-----|-------|--------|
| [Name] | 45 | $X | Low usage | Outreach |
| [Name] | 38 | $X | Support issue | Escalate |

### Critical Accounts
| Customer | Health | MRR | Days Critical | Owner |
|----------|--------|-----|---------------|-------|
| [Name] | 25 | $X | 14 | [Name] |

### Expansion Ready
| Customer | Health | Current | Opportunity |
|----------|--------|---------|-------------|
| [Name] | 95 | Pro | Enterprise |
| [Name] | 88 | Basic | Pro |
```

### Metric Tracking Sheet

```markdown
## Customer Success Metrics: [Month]

### Health Distribution
| Status | Count | Change | MRR | Change |
|--------|-------|--------|-----|--------|
| Healthy | X | +X | $X | +X% |
| Stable | X | -X | $X | -X% |
| At-risk | X | +X | $X | +X% |
| Critical | X | +X | $X | +X% |

### Key Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| NPS | X | >50 | ✅ |
| CSAT | X | >4.5 | ⚠️ |
| Time to value | X days | <7 | ✅ |
| Adoption rate | X% | >80% | ❌ |
| Expansion rate | X% | >20% | ✅ |
| Net retention | X% | >100% | ✅ |

### Cohort Analysis
| Signup Month | Customers | Active | Health Avg | Retained |
|--------------|-----------|--------|------------|----------|
| [Month-3] | X | X | X | X% |
| [Month-2] | X | X | X | X% |
| [Month-1] | X | X | X | X% |
| [Month] | X | X | X | - |

### Actions Required
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]
```

---

## Implementation

### Setup Health Scoring

```
1. Define components and weights
2. Set up data collection
3. Build scoring calculation
4. Create dashboards
5. Define alert thresholds
6. Train team on interpretation
```

### Data Collection

| Data Type | Source | Collection |
|-----------|--------|------------|
| Usage | Analytics | Event tracking |
| Features | Analytics | Feature flags |
| Support | Helpdesk | Ticket sentiment |
| Engagement | Email/CRM | Open rates, replies |
| Payment | Billing | Payment status |

### Automation

**Automated alerts:**

```
Health drops below 60:
→ Alert CSM
→ Add to weekly review

Health drops below 40:
→ Urgent alert
→ Immediate outreach
→ Daily monitoring

Health rises above 80:
→ Expansion opportunity alert
→ Schedule review call
```

---

## Analysis

### Monthly Review Process

```
1. Review health distribution trends
2. Identify cohort patterns
3. Analyze at-risk segments
4. Review expansion opportunities
5. Update playbooks based on learnings
6. Share insights with team
```

### Leading vs. Lagging Indicators

**Leading indicators (predict churn):**
- Declining usage
- Support escalations
- Feature abandonment
- Low engagement
- Payment issues

**Lagging indicators (churn happened):**
- Cancellation
- Downgrade
- Non-renewal

**Focus on leading indicators for proactive intervention.**

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No health tracking | Blind to issues | Build health scoring |
| Too complex scoring | Can't calculate | Start simple, iterate |
| Vanity metrics | Don't predict outcomes | Focus on leading indicators |
| No automation | Manual, delayed | Automate alerts |
| Ignoring trends | Miss patterns | Review cohorts monthly |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Health scoring | Vitally, Totango, ChurnZero |
| Analytics | Mixpanel, Amplitude, Heap |
| Surveys | Delighted, Typeform, SurveyMonkey |
| Dashboards | Databox, Geckoboard, Custom |
| Alerts | Zapier, Make, Custom webhooks |

---

## Related Methodologies

- **customer-success-basics:** Customer Success Framework
- **churn-prevention:** Churn Prevention & At-Risk Intervention
- **analytics:** Analytics Setup & Event Tracking
- **cohort-analysis:** Cohort Analysis for User Behavior
- **north-star-metric:** North Star Metric Definition

---

*Methodology: customer-success-metrics | Operations & Business | faion-growth-agent*

## Sources

- [SaaS Metrics Guide by ChartMogul](https://chartmogul.com/blog/saas-metrics-guide/) - Comprehensive SaaS metrics definitions
- [Sixteen Ventures Customer Success Metrics](https://sixteenventures.com/customer-success-metrics) - CS-specific KPIs
- [Totango Health Score Guide](https://www.totango.com/customer-success-resources/customer-health-score/) - Customer health scoring methodology
- [ProfitWell Metrics Academy](https://www.profitwell.com/recur/all) - SaaS economics and retention metrics
- [OpenView SaaS Benchmarks](https://openviewpartners.com/saas-benchmarks/) - Industry benchmarks for CS metrics
