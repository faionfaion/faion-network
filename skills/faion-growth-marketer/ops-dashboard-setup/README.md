---
id: dashboard-setup
name: "Dashboard Setup"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Dashboard Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | dashboard-setup |
| **Name** | Dashboard Setup |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | metrics-basics, analytics-setup, annual-planning |

---

## Problem

You have metrics, but they're scattered across tools. No single place to see your business health. You waste time hunting for numbers instead of making decisions.

Dashboard setup means centralizing your key metrics for quick, actionable insights.

---

## Framework

Dashboard creation follows this approach:

```
DESIGN   -> Define purpose and audience
BUILD    -> Create visualizations
AUTOMATE -> Connect data sources
OPTIMIZE -> Refine based on usage
```

---

## Step 1: Design Your Dashboard

**Dashboard design principles:**

| Principle | Implementation |
|-----------|----------------|
| Glanceable | See status in 5 seconds |
| Focused | 5-10 key metrics max |
| Current | Real-time or daily updates |
| Actionable | Numbers you can influence |
| Comparative | Show trends, not just values |

**Dashboard types:**

| Type | Purpose | Update |
|------|---------|--------|
| Daily pulse | Quick health check | Daily |
| Weekly review | Deeper analysis | Weekly |
| Monthly report | Full analysis | Monthly |
| Real-time | Live monitoring | Real-time |

**Dashboard layout:**

```
┌─────────────────────────────────────────┐
│  NORTH STAR METRIC                      │
│  ████████████████████████ $50K MRR      │
└─────────────────────────────────────────┘

┌───────────────┬───────────────┬─────────┐
│  Revenue      │  Customers    │  Churn  │
│  $52,000      │  125          │  3.2%   │
│  ↑ 8%         │  ↑ 12         │  ↓ 0.5% │
└───────────────┴───────────────┴─────────┘

┌───────────────┬───────────────┬─────────┐
│  CAC          │  LTV          │  Ratio  │
│  $150         │  $1,200       │  8:1    │
└───────────────┴───────────────┴─────────┘

┌─────────────────────────────────────────┐
│  Revenue Trend (12 months)              │
│  [Line chart showing growth]            │
└─────────────────────────────────────────┘
```

---

## Step 2: Build Dashboards

### Essential Metrics Tracker (Spreadsheet)

```markdown
## Monthly Metrics Tracker

### Revenue
| Month | MRR | Growth | New | Churned | Net |
|-------|-----|--------|-----|---------|-----|
| Jan | $X | X% | $X | $X | $X |
| Feb | $X | X% | $X | $X | $X |

### Customers
| Month | Total | New | Churned | Net | Churn % |
|-------|-------|-----|---------|-----|---------|
| Jan | X | X | X | X | X% |
| Feb | X | X | X | X | X% |

### Unit Economics
| Month | CAC | LTV | Ratio | Payback |
|-------|-----|-----|-------|---------|
| Jan | $X | $X | X:1 | X mo |
| Feb | $X | $X | X:1 | X mo |

### Marketing
| Month | Visits | Signups | Conv % | Spend | CPA |
|-------|--------|---------|--------|-------|-----|
| Jan | X | X | X% | $X | $X |
| Feb | X | X | X% | $X | $X |
```

### Dashboard Specification

```markdown
## Dashboard: [Name]

### Purpose
[What decisions this dashboard supports]

### Audience
[Who will use it]

### Metrics
| Metric | Definition | Source | Update |
|--------|------------|--------|--------|
| [Metric 1] | [How calculated] | [Data source] | [Frequency] |

### Visualizations
1. **[Chart 1]**: [Type] showing [what]
2. **[Chart 2]**: [Type] showing [what]

### Filters
- Date range: [Options]
- Segments: [Options]

### Access
- Location: [URL]
- Permissions: [Who can access]
```

### Monthly Metrics Report

```markdown
## Monthly Report: [Month Year]

### Executive Summary
[2-3 sentence overview]

### Key Metrics
| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Revenue | $X | $X | On/Off track |
| Growth | X% | X% | On/Off track |
| Churn | X% | X% | On/Off track |

### Revenue Analysis
- MRR: $X (↑X% MoM)
- New MRR: $X from X new customers
- Expansion: $X from upgrades
- Churned: $X from X customers

### Customer Analysis
- Total customers: X
- New this month: X
- Churned: X (X%)
- Net change: +X

### Channel Performance
| Channel | Visitors | Signups | Conv | Revenue |
|---------|----------|---------|------|---------|
| Organic | X | X | X% | $X |
| Paid | X | X | X% | $X |
| Referral | X | X | X% | $X |

### Insights
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]

### Next Month Focus
- [Priority 1]
- [Priority 2]
```

---

## Examples

### Example 1: SaaS Dashboard

**North Star:** Monthly Active Users

**Key metrics:**
```
Revenue Dashboard:
├── MRR: $25,000 (↑8% MoM)
├── ARR: $300,000
├── New MRR: $3,500
├── Churned MRR: $1,500
└── Net New: $2,000

Customer Dashboard:
├── Total: 150
├── New: 20
├── Churned: 5
├── Churn rate: 3.3%
└── LTV:CAC: 6:1

Product Dashboard:
├── MAU: 1,200
├── DAU: 400
├── Feature adoption: 65%
└── NPS: 45
```

### Example 2: Info Product Dashboard

**North Star:** Course Completion Rate

**Key metrics:**
```
Revenue Dashboard:
├── Monthly sales: $15,000
├── Units sold: 30
├── Avg order value: $500
└── Refund rate: 2%

Funnel Dashboard:
├── Visitors: 10,000
├── Email signups: 500 (5%)
├── Sales page visits: 200
└── Purchases: 30 (15% of page)

Student Dashboard:
├── Active students: 200
├── Completion rate: 60%
├── Avg rating: 4.7/5
└── Testimonials: 25
```

---

## Implementation Checklist

### Setup
- [ ] Define 5-10 key metrics
- [ ] Identify data sources
- [ ] Choose dashboard tool
- [ ] Set up data connections

### Build
- [ ] Create metric calculations
- [ ] Design dashboard layout
- [ ] Build visualizations
- [ ] Add comparisons and targets

### Process
- [ ] Set review cadence
- [ ] Create alert rules
- [ ] Document definitions
- [ ] Train team (if applicable)

### Optimize
- [ ] Review weekly
- [ ] Update targets quarterly
- [ ] Add/remove metrics as needed
- [ ] Improve visualizations

---

## Tools

| Purpose | Tools |
|---------|-------|
| Dashboards | Looker Studio, Geckoboard, Databox |
| Spreadsheets | Google Sheets, Airtable |
| Product analytics | Mixpanel, Amplitude, PostHog |
| Revenue | Baremetrics, ProfitWell, ChartMogul |
| Marketing | GA4, Plausible |
| Data warehouse | BigQuery, Snowflake |

---

## Related Methodologies

- **metrics-basics:** Metrics Basics (choosing metrics)
- **financial-planning:** Financial Planning (financial metrics)
- **analytics-setup:** Analytics Setup (data collection)
- **annual-planning:** Annual Planning (targets)

---

*Methodology: dashboard-setup | Operations & Business | faion-growth-agent*

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
