# Ops Customer Success Metrics - Checklist

## Quick Start

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