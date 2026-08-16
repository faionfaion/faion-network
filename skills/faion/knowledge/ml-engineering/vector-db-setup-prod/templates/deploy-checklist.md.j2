<!--
purpose: pre+post-deploy checklist for production vector DB
consumes: prod-deploy.yaml + sibling configs
produces: report (checklist results recorded in prod-deploy.yaml)
depends-on: vector-db-monitoring + vector-db-security in place
token-budget-impact: 0
-->

# Vector DB Prod Deploy Checklist

## Pre-deploy
- [ ] storage.class durable + PVC bound in staging
- [ ] resources.cpu/memory limits set
- [ ] ha.strategy matches DB class
- [ ] backup CronJob scheduled
- [ ] last_restore_drill within 120 days
- [ ] monitoring.yaml applied; Grafana dashboard imported
- [ ] security-config.yaml applied; auth + TLS verified
- [ ] index-tuning.yaml applied (or defaults documented)

## Post-deploy
- [ ] pod healthy (readiness probe passes)
- [ ] smoke ingest 10 vectors → search returns ≥1
- [ ] p95 latency within SLO
- [ ] memory + disk metrics scraping
- [ ] backup snapshot ran on next schedule
- [ ] rollback path verified (previous version reachable for 24h)

## Sign-offs
- ML engineer:
- SRE / on-call:
- Date:
