---
id: metrics-basics
name: "Metrics Basics"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Metrics Basics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | metrics-basics |
| **Name** | Metrics Basics |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | dashboard-setup, financial-planning, analytics-setup |

---

## Problem

You're running your business on gut feeling. You don't know your key numbers. When asked "How's business?" you can't give a real answer. Without metrics, you can't improve what you can't measure.

Metrics management means knowing your numbers so you can make better decisions.

---

## Framework

Metrics management follows this approach:

```
IDENTIFY  -> Choose the right metrics
TRACK     -> Collect data systematically
VISUALIZE -> Create useful dashboards
ANALYZE   -> Extract insights
ACT       -> Make data-driven decisions
```

---

## Step 1: Choose Your Metrics

**Metric categories:**

| Category | Purpose | Examples |
|----------|---------|----------|
| **North Star** | Ultimate success measure | Active users, Revenue |
| **Leading** | Predict future outcomes | Signups, Trial starts |
| **Lagging** | Measure past results | Revenue, Churn |
| **Input** | Actions you control | Emails sent, Ads spend |
| **Output** | Results you want | Conversions, Revenue |

**Solopreneur essential metrics:**

| Metric | What It Measures | Frequency |
|--------|------------------|-----------|
| Revenue | Money in | Daily |
| MRR/ARR | Recurring revenue | Weekly |
| Customers | Active paying | Weekly |
| Churn rate | Customers lost | Monthly |
| CAC | Cost to acquire | Monthly |
| LTV | Customer value | Monthly |
| Profit margin | Money kept | Monthly |
| Runway | Time left | Monthly |

**Don't track everything.** Focus on 5-10 metrics that matter.

---

## Step 2: Implement Tracking

**Data sources:**

| Data Type | Sources |
|-----------|---------|
| Revenue | Stripe, PayPal, accounting |
| Customers | CRM, payment processor |
| Usage | Product analytics |
| Marketing | GA4, ad platforms |
| Support | Help desk, email |

**Tracking setup:**

| Layer | Tool | Purpose |
|-------|------|---------|
| Collection | Segment, GTM | Event capture |
| Storage | Database, spreadsheet | Data warehouse |
| Analysis | Analytics tools | Process data |
| Visualization | Dashboard tools | Display metrics |

**Simple stack for solopreneurs:**
```
Stripe → Google Sheets → Looker Studio
GA4 → Native dashboards
Product → Mixpanel/Amplitude free tier
```

---

## Step 3: Set Targets and Alerts

**Target setting:**

| Metric | Current | Target | Basis |
|--------|---------|--------|-------|
| MRR | $50K | $75K | 50% growth |
| Churn | 5% | 3% | Best practice |
| LTV:CAC | 5:1 | 8:1 | Improve efficiency |

**Status indicators:**

| Status | Meaning | Visual |
|--------|---------|--------|
| On track | Within 10% of target | Green |
| Watch | 10-20% off target | Yellow |
| Off track | >20% off target | Red |

**Alerts to set up:**

| Alert | Trigger | Action |
|-------|---------|--------|
| Revenue drop | Down 20% WoW | Investigate |
| Churn spike | Above threshold | Review immediately |
| Zero sales | 24+ hours | Check system |
| High CAC | Above target | Review ads |

---

## Step 4: Create Review Cadence

**Review rhythm:**

| Frequency | Focus | Time |
|-----------|-------|------|
| Daily | Pulse check | 2 min |
| Weekly | Performance review | 30 min |
| Monthly | Deep analysis | 2 hours |
| Quarterly | Strategy review | Half day |

**Weekly review template:**

```markdown
## Weekly Review: [Date]

### Key Metrics
| Metric | This Week | Last Week | Change | Target |
|--------|-----------|-----------|--------|--------|
| Revenue | $X | $X | +X% | $X |
| Customers | X | X | +X | X |
| Churn | X% | X% | -X% | X% |

### What Went Well
- [Highlight 1]
- [Highlight 2]

### What Needs Attention
- [Issue 1]
- [Issue 2]

### Actions for Next Week
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## Metric Definitions

| Metric | Formula |
|--------|---------|
| MRR | Sum of all monthly recurring revenue |
| ARR | MRR x 12 |
| Churn rate | Customers lost / Starting customers |
| LTV | ARPU / Churn rate |
| CAC | Marketing spend / New customers |
| LTV:CAC | LTV / CAC |
| ARPU | Revenue / Customers |
| Net retention | (Starting + Expansion - Churn) / Starting |

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Too many metrics | Analysis paralysis | Focus on 5-10 |
| Vanity metrics | Don't drive decisions | Track actionable metrics |
| No targets | No accountability | Set clear goals |
| Stale data | Outdated decisions | Automate updates |
| Complex dashboards | Nobody uses them | Keep simple |
| No action | Data without decisions | Review and act |

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

- **dashboard-setup:** Dashboard Setup (visualization)
- **financial-planning:** Financial Planning (financial metrics)
- **analytics-setup:** Analytics Setup (marketing analytics)
- **annual-planning:** Annual Planning (annual targets)
- **customer-success:** Customer Success (customer metrics)

---

*Methodology: metrics-basics | Operations & Business | faion-growth-agent*

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
