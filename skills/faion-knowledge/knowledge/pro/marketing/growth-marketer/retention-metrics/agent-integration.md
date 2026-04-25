# Agent Integration — Retention Metrics

## When to use
- You're standing up retention reporting and need an agent to generate D1/D7/D30 cohort tables and engagement ratios.
- You're benchmarking against industry norms (B2B SaaS, social, mobile, ecom) to set realistic targets.
- You want automated weekly retention digests with WoW deltas and at-risk-cohort flags.
- You're building a churn-risk score and need an agent to compute features per user.

## When NOT to use
- One-off transactional products (single-use utility, gift purchase) — retention is not the right primitive; conversion + LTV matter more.
- Pre-PMF: retention numbers are noisy with <100 users/cohort and lead to overfitting on accidental patterns.
- B2B products with monthly/quarterly usage patterns — D1/D7 retention misleads; use feature-event retention or contract-tied metrics.
- Heavily seasonal products where cohort comparison across periods is invalid without de-seasonalizing.

## Where it fails / limitations
- Definitional drift: "DAU" can mean session-open, login, key-action — agents must lock the SQL definition or numbers are uncomparable.
- Cohort thinning: small cohorts produce wild D30 swings; agent should suppress/flag cohorts <50 users.
- Identity stitching errors inflate or deflate retention (logged-out sessions split a single user into two).
- Survivorship-only views miss the dropout shape; need rolling retention or N-day-active retention to see plateau vs decay.
- Engagement ratios (DAU/MAU) hide power-user concentration; one whale skews the average.
- Churn prediction ML models lose calibration over time; agent should retrain monthly, not just score.

## Agentic workflow
A `sonnet` analyst writes the cohort SQL (BigQuery / warehouse / product-analytics tool) and pulls D1/D7/D30 + DAU/WAU/MAU weekly. An `opus` strategist reviews retention curves vs benchmarks and recommends loop interventions. A `haiku` ops agent posts a weekly digest with WoW deltas and flags any cohort outside expected band. A `sonnet` ML agent computes churn-risk features and segments users into low/medium/high; a human reviewer signs off on the action plan per segment.

### Recommended subagents
- `faion-growth-agent` (opus) — strategy, loop design, target setting.
- Data/sonnet subagent — cohort SQL, retention computation.
- Logger/haiku subagent — weekly digest, WoW deltas, anomaly flags.
- ML/sonnet subagent — churn-risk feature engineering and scoring.

### Prompt pattern
```
Generate cohort retention SQL for {events_table}, signup_event=
{signup_event}, return_event={return_event}, return D0 through D30 by
weekly cohort for last 12 weeks. Suppress cohorts with <50 users.
Dialect: BigQuery.
```

```
Given retention curves for last 8 weeks (data attached), compare to
{product_type} benchmark. Identify weeks where D7 deviates >20% from
median. Diagnose: cohort composition shift / seasonal / product change.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Versioned SQL models for retention metrics | `pip install dbt-bigquery` (or duckdb/snowflake) |
| `bq` CLI | Run cohort SQL on GA4 BigQuery export | https://cloud.google.com/bigquery/docs/bq-command-line-tool |
| `duckdb` | Local cohort math on parquet/CSV exports | `pip install duckdb` |
| `pandas` + `numpy` | Quick cohort matrices | `pip install pandas` |
| Mixpanel/Amplitude/PostHog SDKs | Hosted retention queries | per-vendor |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Amplitude Retention | SaaS | Yes (REST) | N-day, unbounded, rolling retention built-in |
| Mixpanel Retention | SaaS | Yes (REST) | Cohort builder + retention API |
| PostHog | OSS | Yes (REST + self-host) | Agent-friendly self-hosted |
| Heap | SaaS | Yes (REST) | Auto-capture + retention reports |
| ChurnZero / Totango / Gainsight | SaaS | Partial | CS platforms; APIs exist for at-risk push |
| Customer.io / Iterable / Braze | SaaS | Yes (REST) | Trigger re-engagement on risk-tier changes |
| OneSignal | SaaS | Yes (REST) | Push notifications for retention loops |

## Templates & scripts
See `templates.md` for retention-loop and dashboard templates. Inline cohort table generator:

```python
# cohort.py — agent's quick cohort matrix
import pandas as pd

def cohort_matrix(events: pd.DataFrame, user_col="user_id",
                  date_col="event_date", signup_col="signup_date",
                  max_day=30) -> pd.DataFrame:
    events = events.copy()
    events["day_n"] = (events[date_col] - events[signup_col]).dt.days
    events = events[(events.day_n >= 0) & (events.day_n <= max_day)]
    cohort_size = events.groupby("signup_date")[user_col].nunique()
    retained = (events.groupby(["signup_date", "day_n"])[user_col]
                      .nunique().unstack(fill_value=0))
    return retained.div(cohort_size, axis=0).round(3)
```

## Best practices
- Lock retention definitions in a `metrics.yaml` or dbt model; never let an agent recompute with a slightly different filter mid-week.
- Use rolling retention (still active in last N days) not classical (active on exact day N) for low-frequency products.
- Always show the cohort size next to the retention rate; small cohorts deserve grey-text "underpowered" labels.
- Compare to industry benchmark band, not a single number — show min/typical/max, not a target percent.
- Pair retention dashboards with a "retention loop" map: which mechanic produces the next session.
- Re-baseline benchmarks yearly; D1 retention has shifted across categories with privacy + ATT changes.

## AI-agent gotchas
- An agent computing "DAU" from `event_count > 0` instead of `distinct_user_id` will inflate by users with multi-session days.
- "Activated" vs "retained" cohorts overlap — agent reports must label which cohort is being measured.
- Time-zone bugs: cohort dates in UTC but events in local time produce phantom retention dips at midnight UTC.
- DAU/MAU on tiny products (<1k MAU) is a noise indicator, not a signal — agent should suppress when MAU < threshold.
- Push-notification retention spikes are short-term; agent must distinguish habitual return from notification-induced bounces.
- Don't let a churn-risk agent send re-engagement emails autonomously to high-risk users — fatigue risks the brand; require human approval for cadence.
- "Reactivated" classification needs a clear inactivity-window definition; agent must use the canonical one across all reports.

## References
- Reforge, "Retention + Engagement" course (Casey Winters)
- Andrew Chen, "New data shows up to 77% of your DAUs disappear after 3 days"
- Nir Eyal, *Hooked*
- Mixpanel, "Mastering Retention" guide
- Lenny's Newsletter, "What good retention looks like" — https://www.lennysnewsletter.com/
