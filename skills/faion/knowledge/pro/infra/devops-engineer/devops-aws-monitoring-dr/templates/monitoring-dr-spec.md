<!-- purpose: Markdown skeleton for the monitoring+DR spec -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens when loaded -->

# AWS Monitoring + DR Spec

- **Workload:** 
- **Date:** 
- **RTO:** 
- **RPO:** 

## Dashboards (per tier)

| Tier | Widgets | Period |
|------|---------|--------|
| API | rps, latency p50/p99, 5xx rate | 5 min |
| Lambda | duration, errors, throttles, concurrency | 5 min |
| DynamoDB | consumed RCU/WCU, throttles | 5 min |
| Container | CPU/mem via Container Insights | 5 min |

## Alarms (tiered)

| Severity | SNS topic | Response |
|----------|-----------|----------|
| Critical | sns:critical | Page on-call |
| Warning | sns:warning | Business-hours notify |
| Info | sns:digest | Daily digest |

## X-Ray

- Active tracing: Lambda + API Gateway + DynamoDB instrumentation

## DR strategy

- Pattern: backup-restore / pilot-light / warm-standby / active-active
- Region pair: us-east-1 → us-west-2
- RTO: hours
- RPO: hours
- Drill cadence: quarterly
