<!--
purpose: Escalation runbook skeleton for an autonomous agent in production.
consumes: on-call rota + agent action surfaces + alert thresholds.
produces: A runbook pinned BEFORE the agent takes traffic.
depends-on: ../scripts/validate-agentic-ai-product-development.py.
token-budget-impact: ~300 tokens when filled.
-->

# Escalation runbook — <agent>

## Human role

- Primary: <role:person>
- Backup: <role:person>

## Channel

- Slack: <#channel>
- Pager: <pager-route>

## SLA

- Acknowledge: <minutes>
- Mitigate: <minutes>

## Triggers (alarm conditions)

- confidence < 0.7
- retry_count > 2
- refund > 100
- regression-status == red
- daily_budget_consumed > 80%

## Mitigation steps

1. Pause agent traffic (`agent.traffic = 0`).
2. Confirm cause (regression / provider update / data drift).
3. Roll back to last green model_id OR raise budget cap with named approver.
4. Re-enable traffic at 10% canary, monitor for 30 min, ramp.

## Post-incident

- File incident note within 24h, link telemetry traces, update runbook if a new failure pattern surfaced.
