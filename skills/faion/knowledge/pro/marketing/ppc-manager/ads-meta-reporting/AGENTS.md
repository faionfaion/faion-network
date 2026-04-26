# Meta Ads Reporting & Analysis

## Summary

Structured analyze-decide-act cycle for Meta Ads: set up custom column presets (CPM, CTR, CPC, CVR, CPA, ROAS), run weekly breakdowns by age/placement/device, and diagnose performance issues by mapping symptoms (high CPA, low CTR, high frequency) to root causes (creative fatigue, audience fatigue, landing page failure). Every report must produce a list of concrete actions.

## Why

Default Meta reports surface vanity metrics. Decisions made on the wrong metrics waste budget on underperforming ads. A structured diagnostic flow — CPM → CTR → CVR → CPA — pinpoints exactly where the funnel breaks and what to fix. Reporting without action is overhead; every session must produce a decision.

## When To Use

- Weekly performance review for any active Meta campaign.
- Diagnosing a CPA spike or CTR decline.
- Presenting results to stakeholders (executive summary, creative analysis).
- Deciding which campaigns to scale, hold, or pause.

## When NOT To Use

- Daily micro-optimization — too noisy; check spend pacing and errors daily, but full analysis weekly.
- Campaigns in learning phase (<50 conversions in the optimization window) — data is not representative.
- Attribution decisions that require cross-platform modeling — use dedicated attribution tools, not Meta-only data.

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics.xml` | Key metric definitions, formulas, benchmarks, and diagnostic decision tree. |
| `content/02-reporting-workflow.xml` | Cadence (daily/weekly/monthly), breakdown analysis, custom report setup, antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-report.md` | Weekly performance report: summary, campaign table, top ads, insights, actions. |
| `templates/creative-analysis.md` | Creative performance breakdown by format and fatigue signals checklist. |
