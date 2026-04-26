# Runbook: <AlertName>

> service: <service-name>
> owner: <team-handle>
> severity_default: SEV2

## Symptoms

- What firing alerts look like (alert names, sample message text).
- Customer-visible behavior (one bullet per affected surface).

## Diagnose

<!-- All Diagnose steps are read-only and always agent-runnable. -->

- Check pod health: `kubectl top pods -n <ns>`
- Check current connections: `prom-query 'pg_stat_activity_count{db="<svc>"}'`
- Tail recent logs: `kubectl logs -n <ns> deploy/<svc> --tail=200`
- Recent deploys: `gh run list --workflow=deploy --limit=5`

## Remediate

<!--
Each step MUST end with one of:
  <!-- agent:auto -->         agent runs unattended
  <!-- agent:approval -->     agent waits for signed approval
A step without a tag is invalid and the agent will refuse to start.
-->

- Scale read replicas: `kubectl scale --replicas=+1 sts/<svc>-replica` <!-- agent:auto -->
- Clear stale connections: `psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state='idle' AND state_change &lt; now() - interval '10m'"` <!-- agent:auto -->
- Restart leader pod: `kubectl rollout restart sts/<svc>-primary` <!-- agent:approval -->
- Failover primary: `patroni failover --candidate <svc>-replica-1` <!-- agent:approval -->

## Escalate

- Page <team-handle> if Remediate did not lower the alert within 15 minutes.
- File a SEV1 if customer-impacting and revenue is affected.
- Link the postmortem template: `runbooks/_postmortem.md`.
