# Product Analytics

## Summary

Framework for measuring user behavior to drive product decisions. Starts with defining the questions analytics must answer, then designs a minimal tracking plan (max 12 events per feature, Object-Action naming), implements dashboards per audience, and establishes weekly/monthly review rituals. Connects raw event data to actionable insights without tracking everything.

## Why

Teams that instrument first and ask questions later produce dashboards nobody looks at and analysis paralysis. The root failure is no connection between metrics and decisions. Defining key questions before writing a single tracking call forces discipline: every event answers a question, every dashboard serves a decision-maker, and every analysis has a "so what". The five-category AARRR lens (Acquisition/Activation/Engagement/Retention/Revenue) provides a minimal but complete coverage model.

## When To Use

- Designing tracking plan for a new product or feature pre-launch.
- Auditing existing event taxonomy: detect duplicates, naming inconsistencies, undocumented properties.
- Generating SQL/cohort queries from natural-language questions.
- Weekly anomaly summaries from PostHog/Amplitude/Mixpanel exports.
- Stitching multiple analytics sources into one cohort view.

## When NOT To Use

- Real-time alerting/SLO monitoring — use Prometheus/Grafana, not LLMs.
- Compliance-bound metrics (HIPAA, GDPR-deletion, SOX revenue) — agent-generated SQL needs lawyer-grade audit trail.
- High-volume operational dashboards — LLM-in-loop adds latency, breaks "glance" rituals.
- No user analytics instrumented yet — install before agentizing.

## Content

| File | What's inside |
|------|---------------|
| `content/01-analytics-framework.xml` | Maturity levels, 5 metric categories (AARRR), implementation process, naming conventions, dashboard types, and review cadence. |
| `content/02-analytics-examples.xml` | Concrete examples: onboarding funnel analysis, feature-usage-to-retention correlation, antipatterns, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tracking-plan.md` | User properties table + events by stage (onboarding/core/conversion) with trigger and properties columns. |
| `templates/dashboard-spec.md` | Audience-specific dashboard: metrics table, chart list, segment breakdown, refresh cadence. |
| `templates/analysis-report.md` | Structured report: question, methodology, findings with insights and implications, recommendations, limitations. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/query-safe.py` | sqlglot-based SQL validator: rejects LLM-generated queries referencing unknown columns before execution. |
