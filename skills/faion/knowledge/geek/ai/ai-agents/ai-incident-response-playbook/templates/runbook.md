<!--
purpose: Markdown skeleton for AI incident response runbook
consumes: signals, kill-switch + rollback endpoints, escalation schedule
produces: ops-repo runbook ready to drill
depends-on: content/01-core-rules.xml
token-budget-impact: ~500 tokens when rendered
-->
# Runbook — {{incident_class}}

> ESCALATION: minute 10 → {{primary_escalation}}
> minute 25 → {{secondary_escalation}}
> Incident channel: `{{incident_channel}}`
> Drill last completed: {{drill_completed_at}}

## Steps

| # | Action | Signal | Threshold | Budget |
|---|---|---|---|---|
| 1 | Confirm signal | `{{dashboard_path}}` | `>{{threshold_1}}` | 2 min |
| 2 | Throttle | `POST {{throttle_endpoint}}` | qps≤10 | 3 min |
| 3 | Decide kill-switch vs rollback | time since last good eval | `<24h → kill-switch; else rollback` | 5 min |
| 4 | Kill-switch | `POST {{killswitch_endpoint}}` | `flag.enabled=false` | 2 min |
| 5 | Rollback bundle | rollback-button click | bundle_version=prior | 5 min |
| 6 | Notify customers | status-page + email | impacted accounts emailed | 10 min |
| 7 | Open postmortem | use ai-incident-postmortem-template | postmortem within 24h | n/a |

## Escalation

- Primary: `{{primary_escalation}}`
- Secondary: `{{secondary_escalation}}`
- Compliance contact (regulated incidents only): `{{compliance_contact}}`
