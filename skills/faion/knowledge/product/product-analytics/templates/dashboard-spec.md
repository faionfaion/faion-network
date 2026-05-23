## Dashboard: {Name} — {Audience}

### Purpose
{One sentence: what decision or ritual this dashboard supports}

### Metrics

| Metric | Formula | Target | Alert Threshold |
|--------|---------|--------|-----------------|
| DAU | Unique users with core action per day | {X} | <80% target |
| WAU | Unique users with core action per week | {X} | <80% target |
| D1 Retention | % returning on day 1 after signup | 40% | <35% |
| D7 Retention | % returning on day 7 after signup | 20% | <15% |
| Activation Rate | % completing onboarding | 60% | <50% |
| {Custom metric} | {Formula} | {Target} | {Alert} |

### Charts

1. **DAU Trend** — 7-day rolling line chart
2. **Retention Cohort** — weekly cohort heatmap (signup week × day-N)
3. **Feature Usage** — top 5 features by unique user count
4. **Conversion Funnel** — signup → activation → first key action → paid

### Segments
- By plan: free / paid / enterprise
- By cohort: signup week (not signup date)
- By source: organic / paid / referral

### Refresh Cadence
- Real-time: DAU counter
- Daily: retention cohorts, funnel
- Weekly: cohort curves, feature usage

### Audience
{Product team / Leadership / Feature owner} — {what decisions they make from this}
