<!-- purpose: Pipeline hygiene 15-min checklist -->
<!-- consumes: pipeline CRM export + win/loss notes -->
<!-- produces: deltas + next actions per opp -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300-700 tokens -->

# Pipeline Hygiene — <date>

| # | Item                                          | Status | Action if not green        |
|---|-----------------------------------------------|--------|----------------------------|
| 1 | All opps have stage + close date              |        | Fill missing fields        |
| 2 | All opps moved or marked stuck                |        | Mark stuck + reason        |
| 3 | Hot opps next 30d have next-step + owner      |        | Add next-step              |
| 4 | Lost opps from last week tagged with reason   |        | Backfill loss reasons      |
| 5 | New opps from last week tagged with source    |        | Backfill source            |
