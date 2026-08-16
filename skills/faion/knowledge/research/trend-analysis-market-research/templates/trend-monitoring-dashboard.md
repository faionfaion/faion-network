<!-- purpose: Monthly recurring trend-watch dashboard tracking monitored trends, new signals and counter-signals. -->
<!-- consumes: prior trend-analysis-report.md outputs + this month's source scan, per AGENTS.md Prerequisites -->
<!-- produces: updated monitoring dashboard with stage changes and a mandatory counter-signal log -->
<!-- depends-on: content/01-core-rules.xml (valid-until-per-trend, named-disconfirming-signal) -->
<!-- token-budget-impact: ~400-800 tokens when loaded as context -->

## Monthly Trend Watch: <month_year>

### Trends Currently Monitored

| Trend | Score/5 | Stage | Status | Next Review |
|-------|---------|-------|--------|-------------|
| <trend_1> | [X] | [Stage] | Watching | <watching> |
| <trend_2> | [X] | [Stage] | Promising | <promising> |
| <trend_3> | [X] | [Stage] | Cooling | <cooling> |

### New Trends Identified This Month

1. **<trend_name>**
   - First seen: [Source URL, date]
   - Initial assessment: [1-2 sentences with quantitative signal]
   - Quantitative anchor: [Google Trends index / funding round / category spend — required]
   - Action: <monitor_analyze_ignore>

### Trend Status Changes

| Trend | Previous Stage | Current Stage | Signal | Source |
|-------|---------------|---------------|--------|--------|
| <name> | [Stage] | [Stage] | [What changed and why] | [URL] |

### Sources Checked This Month
- [ ] Google Trends — top 5 category terms
- [ ] Product Hunt — new entrants in monitored categories (last 30 days)
- [ ] Hacker News front page — weekly scan
- [ ] Crunchbase — funding rounds in monitored categories
- [ ] FRED / World Bank — macro indicators relevant to trend drivers
- [ ] EUR-Lex / Federal Register — regulatory pipeline for regulated categories
- [ ] SEC EDGAR — 10-K risk factor updates for top 3 incumbents per trend

### Counter-Signal Log (mandatory — at least 1 per active trend)

| Trend | Counter-signal | Source | Strength |
|-------|---------------|--------|----------|
| <trend> | [What could reverse or slow this trend] | [URL] | <high_med_low> |
