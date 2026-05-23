<!--
purpose: Append-only ledger skeleton with fixed columns + header
consumes: postmortem action items + SLO policy
produces: report (markdown ledger persisted in repo or wiki)
depends-on: content/01-core-rules.xml (append-only, fixed-columns, named-cadence-and-owner)
token-budget-impact: low — ~200 tokens when loaded as context
-->

# Postmortem Action Item Ledger

owner: <person> (<role>)
review_cadence: weekly
retention_months: 24

| id | ts (ISO) | owner | hypothesis_or_event | evidence_link | outcome | next | slo_class | slo_due |
|----|----------|-------|---------------------|---------------|---------|------|-----------|---------|
| 1  | 2026-05-12T09:30:00Z | ruslan | INC-441 prod 500s after Redis upgrade | https://github.com/org/repo/issues/441 | pending | Add max-connections alert at 80% | P1 | 2026-05-26 |
