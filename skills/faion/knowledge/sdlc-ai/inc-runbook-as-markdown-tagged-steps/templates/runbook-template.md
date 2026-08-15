<!--
purpose: runbook markdown skeleton with tagged steps
consumes: runbook parser
produces: parsed step list + execution
depends-on: content/01-core-rules.xml
token-budget-impact: ~250 tokens
variables:
  - name: runbook_name
    type: string
    required: true
    description: What this runbook does, named as the alert that fires it names the problem. The person reading it is matching a page against a title at 3am and has no patience for a clever one.
  - name: owner_team
    type: string
    required: true
    description: The team handle that owns this runbook. Personal ownership rots when the person leaves; a team handle is who answers when a step turns out to be wrong.
  - name: last_drilled
    type: string
    required: true
    description: The date this was last executed as a drill, ISO. An undrilled runbook is a hypothesis about your own systems, and the failover step is exactly where you find that out.
  - name: service_name
    type: string
    required: true
    description: The service this operates on, as the deploy and monitoring tools name it. The commands below are typed verbatim under pressure, so the name has to be the real one.
  - name: severity_scope
    type: enum
    required: true
    options: [sev1-only, sev2-plus, sev3-plus]
    description: The severity at which running this is authorised. The approval-required step below has real cost - saying when it is allowed is what stops it being run during a minor blip.
  - name: url
    type: string
    required: true
    description: The health endpoint the verify step curls. It must return 200 only when the service is genuinely serving - a health check that passes during the outage makes this whole runbook lie.
-->

# Runbook: {{runbook_name}}

Owner: {{owner_team}}  ·  Last drilled: {{last_drilled}}  ·  Severity scope: {{severity_scope}}

## Preconditions
- Service: {{service_name}}
- On-call ack received

## Steps

### `[read]` id=check-replica-lag
```bash
psql -c "select client_addr, state, sync_state, replay_lag from pg_stat_replication"
```

### `[approval-required]` id=promote-replica
```bash
patronictl failover --candidate [replica-name]
```

### `[verify]` id=verify-traffic
```bash
curl -fsS {{url}}
```
assertion: `status==200`

### `[read]` id=collect-evidence
```bash
kubectl logs -l app={{service_name}} --since=10m > /tmp/evidence.log
```
