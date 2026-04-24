---
id: cohort-implementation
name: "Cohort Analysis Implementation"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Cohort Analysis Implementation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | cohort-implementation |
| **Name** | Cohort Analysis Implementation |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | cohort-basics, funnel-optimization |

---

## Building Cohort Analysis

### Step 1: Define Cohorts

```sql
-- Example: Weekly acquisition cohorts
SELECT
  DATE_TRUNC('week', signup_date) AS cohort_week,
  user_id,
  signup_date
FROM users
```

### Step 2: Track Activity

```sql
-- Activity by day since signup
SELECT
  u.cohort_week,
  DATEDIFF('day', u.signup_date, e.event_date) AS days_since_signup,
  COUNT(DISTINCT e.user_id) AS active_users
FROM users u
JOIN events e ON u.user_id = e.user_id
WHERE e.event_type = 'login'
GROUP BY 1, 2
```

### Step 3: Calculate Retention

```sql
-- Retention percentages
SELECT
  cohort_week,
  days_since_signup,
  active_users,
  ROUND(100.0 * active_users / cohort_size, 1) AS retention_pct
FROM (
  -- Previous query
)
```

### Step 4: Pivot to Table

```
        D0    D1    D7    D30
Week1   100%  45%   22%   12%
Week2   100%  48%   25%   14%
...
```

---

## Implementation Checklist

- [ ] Define cohort grouping (weekly/monthly)
- [ ] Define retention metric (login, action, etc.)
- [ ] Build data pipeline
- [ ] Create cohort table
- [ ] Set up automated updates
- [ ] Establish benchmarks
- [ ] Review weekly
- [ ] Investigate any declines

---

## Tools

| Purpose | Tools |
|---------|-------|
| Product analytics | Amplitude, Mixpanel, Posthog |
| Data warehouse | BigQuery, Snowflake, Redshift |
| Visualization | Metabase, Looker, Mode |
| Spreadsheet | Google Sheets, Excel |

---

## Cohort Analysis Checklist

Weekly review:
- [ ] Pull latest cohort data
- [ ] Compare to previous cohorts
- [ ] Identify any significant changes
- [ ] Investigate declines
- [ ] Document insights

Monthly review:
- [ ] Analyze long-term retention (D60, D90)
- [ ] Compare cohort quality over time
- [ ] Correlate with acquisition channels
- [ ] Update benchmarks

---

## SQL Query Templates

### Basic Retention Query

```sql
-- Calculate D1, D7, D30 retention by cohort
WITH cohorts AS (
  SELECT
    DATE_TRUNC('week', signup_date) AS cohort_week,
    user_id,
    signup_date
  FROM users
),

user_activity AS (
  SELECT
    c.cohort_week,
    c.user_id,
    DATEDIFF('day', c.signup_date, e.event_date) AS days_since_signup
  FROM cohorts c
  LEFT JOIN events e ON c.user_id = e.user_id
  WHERE e.event_type = 'login'
    AND e.event_date >= c.signup_date
),

retention_by_day AS (
  SELECT
    cohort_week,
    days_since_signup,
    COUNT(DISTINCT user_id) AS active_users
  FROM user_activity
  GROUP BY 1, 2
),

cohort_sizes AS (
  SELECT
    cohort_week,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM cohorts
  GROUP BY 1
)

SELECT
  r.cohort_week,
  r.days_since_signup,
  r.active_users,
  c.cohort_size,
  ROUND(100.0 * r.active_users / c.cohort_size, 1) AS retention_pct
FROM retention_by_day r
JOIN cohort_sizes c ON r.cohort_week = c.cohort_week
WHERE r.days_since_signup IN (1, 7, 30)
ORDER BY 1, 2
```

### Behavioral Cohort Query

```sql
-- Compare users who completed onboarding vs those who did not
WITH cohorts AS (
  SELECT
    user_id,
    signup_date,
    CASE
      WHEN user_id IN (
        SELECT DISTINCT user_id
        FROM onboarding_completed
      ) THEN 'Completed'
      ELSE 'Not Completed'
    END AS cohort_type
  FROM users
  WHERE signup_date >= CURRENT_DATE - INTERVAL '30 days'
),

user_activity AS (
  SELECT
    c.cohort_type,
    c.user_id,
    DATEDIFF('day', c.signup_date, e.event_date) AS days_since_signup
  FROM cohorts c
  LEFT JOIN events e ON c.user_id = e.user_id
  WHERE e.event_type = 'login'
    AND e.event_date >= c.signup_date
),

retention_by_cohort AS (
  SELECT
    cohort_type,
    days_since_signup,
    COUNT(DISTINCT user_id) AS active_users
  FROM user_activity
  GROUP BY 1, 2
),

cohort_sizes AS (
  SELECT
    cohort_type,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM cohorts
  GROUP BY 1
)

SELECT
  r.cohort_type,
  r.days_since_signup,
  r.active_users,
  c.cohort_size,
  ROUND(100.0 * r.active_users / c.cohort_size, 1) AS retention_pct
FROM retention_by_cohort r
JOIN cohort_sizes c ON r.cohort_type = c.cohort_type
WHERE r.days_since_signup IN (1, 7, 30)
ORDER BY 1, 2
```

### Feature Adoption Cohort Query

```sql
-- Compare users who used feature X vs those who did not
WITH feature_usage AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_type = 'feature_x_used'
    AND event_date <= signup_date + INTERVAL '7 days'
),

cohorts AS (
  SELECT
    u.user_id,
    u.signup_date,
    CASE
      WHEN fu.user_id IS NOT NULL THEN 'Used Feature X'
      ELSE 'Did Not Use'
    END AS cohort_type
  FROM users u
  LEFT JOIN feature_usage fu ON u.user_id = fu.user_id
  WHERE u.signup_date >= CURRENT_DATE - INTERVAL '90 days'
),

user_activity AS (
  SELECT
    c.cohort_type,
    c.user_id,
    DATEDIFF('day', c.signup_date, e.event_date) AS days_since_signup
  FROM cohorts c
  LEFT JOIN events e ON c.user_id = e.user_id
  WHERE e.event_type = 'login'
    AND e.event_date >= c.signup_date
)

SELECT
  cohort_type,
  days_since_signup,
  COUNT(DISTINCT user_id) AS active_users,
  (SELECT COUNT(*) FROM cohorts WHERE cohort_type = ua.cohort_type) AS cohort_size,
  ROUND(100.0 * COUNT(DISTINCT user_id) /
    (SELECT COUNT(*) FROM cohorts WHERE cohort_type = ua.cohort_type), 1) AS retention_pct
FROM user_activity ua
WHERE days_since_signup IN (1, 7, 30, 90)
GROUP BY 1, 2
ORDER BY 1, 2
```

---

## Python Implementation (Using Pandas)

### Load and Prepare Data

```python
import pandas as pd
import numpy as np

# Load user data
users = pd.read_sql("SELECT user_id, signup_date FROM users", conn)
events = pd.read_sql("SELECT user_id, event_date FROM events WHERE event_type = 'login'", conn)

# Convert to datetime
users['signup_date'] = pd.to_datetime(users['signup_date'])
events['event_date'] = pd.to_datetime(events['event_date'])

# Create weekly cohorts
users['cohort_week'] = users['signup_date'].dt.to_period('W')
```

### Calculate Retention

```python
# Merge users and events
df = events.merge(users, on='user_id', how='left')

# Calculate days since signup
df['days_since_signup'] = (df['event_date'] - df['signup_date']).dt.days

# Filter for specific retention points
retention_points = [1, 7, 30, 60, 90]
df_retention = df[df['days_since_signup'].isin(retention_points)]

# Calculate cohort retention
cohort_retention = df_retention.groupby(['cohort_week', 'days_since_signup'])['user_id'].nunique().reset_index()
cohort_sizes = users.groupby('cohort_week')['user_id'].nunique().reset_index()
cohort_sizes.columns = ['cohort_week', 'cohort_size']

# Merge and calculate percentages
retention = cohort_retention.merge(cohort_sizes, on='cohort_week')
retention['retention_pct'] = (retention['user_id'] / retention['cohort_size'] * 100).round(1)
```

### Pivot to Cohort Table

```python
# Pivot to cohort table format
cohort_table = retention.pivot(index='cohort_week', columns='days_since_signup', values='retention_pct')
cohort_table.columns = [f'D{int(col)}' for col in cohort_table.columns]

print(cohort_table)
```

---

## Visualization Examples

### Heatmap (Python with Matplotlib)

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(cohort_table, annot=True, fmt='.1f', cmap='RdYlGn', vmin=0, vmax=100)
plt.title('Cohort Retention Heatmap')
plt.xlabel('Days Since Signup')
plt.ylabel('Cohort Week')
plt.tight_layout()
plt.savefig('cohort_heatmap.png')
```

### Line Chart (Retention Trends)

```python
import matplotlib.pyplot as plt

# Plot D30 retention over time
d30_retention = retention[retention['days_since_signup'] == 30][['cohort_week', 'retention_pct']]

plt.figure(figsize=(12, 6))
plt.plot(d30_retention['cohort_week'].astype(str), d30_retention['retention_pct'], marker='o')
plt.title('D30 Retention by Cohort')
plt.xlabel('Cohort Week')
plt.ylabel('Retention %')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d30_retention_trend.png')
```

---

## Data Warehouse Setup

### BigQuery Table Schema

```sql
-- Users table
CREATE TABLE analytics.users (
  user_id STRING NOT NULL,
  signup_date TIMESTAMP NOT NULL,
  signup_source STRING
);

-- Events table
CREATE TABLE analytics.events (
  event_id STRING NOT NULL,
  user_id STRING NOT NULL,
  event_type STRING NOT NULL,
  event_date TIMESTAMP NOT NULL,
  properties JSON
);

-- Cohort retention materialized view
CREATE MATERIALIZED VIEW analytics.cohort_retention AS
SELECT
  DATE_TRUNC(u.signup_date, WEEK) AS cohort_week,
  DATE_DIFF(e.event_date, u.signup_date, DAY) AS days_since_signup,
  COUNT(DISTINCT e.user_id) AS active_users,
  COUNT(DISTINCT u.user_id) AS cohort_size,
  ROUND(100.0 * COUNT(DISTINCT e.user_id) / COUNT(DISTINCT u.user_id), 1) AS retention_pct
FROM analytics.users u
LEFT JOIN analytics.events e
  ON u.user_id = e.user_id
  AND e.event_type = 'login'
  AND e.event_date >= u.signup_date
WHERE DATE_DIFF(e.event_date, u.signup_date, DAY) IN (1, 7, 30, 60, 90)
GROUP BY 1, 2;
```

---

## Automation

### Daily Refresh Script

```python
import schedule
import time
from google.cloud import bigquery

def refresh_cohort_data():
    client = bigquery.Client()
    query = """
    REFRESH MATERIALIZED VIEW analytics.cohort_retention
    """
    client.query(query).result()
    print(f"Cohort data refreshed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule daily refresh at 2 AM
schedule.every().day.at("02:00").do(refresh_cohort_data)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

---

## Related Methodologies

- **cohort-basics:** Cohort analysis fundamentals and examples
- **funnel-optimization:** Funnel analysis and optimization
- **aarrr-pirate-metrics:** AARRR framework integration

---

*Methodology: cohort-implementation | Growth | faion-growth-agent*

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
