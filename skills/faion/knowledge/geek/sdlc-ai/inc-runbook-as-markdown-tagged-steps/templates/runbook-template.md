<!-- purpose: runbook markdown skeleton with tagged steps -->
<!-- consumes: runbook parser -->
<!-- produces: parsed step list + execution -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~250 tokens -->

# Runbook: <name>

Owner: <team-handle>  ·  Last drilled: <YYYY-MM-DD>  ·  Severity scope: SEV2+

## Preconditions
- Service: <name>
- On-call ack received

## Steps

### `[read]` id=check-replica-lag
```bash
psql -c "select client_addr, state, sync_state, replay_lag from pg_stat_replication"
```

### `[approval-required]` id=promote-replica
```bash
patronictl failover --candidate <replica>
```

### `[verify]` id=verify-traffic
```bash
curl -fsS https://api/healthz
```
assertion: `status==200`

### `[read]` id=collect-evidence
```bash
kubectl logs -l app=payments --since=10m > /tmp/evidence.log
```
