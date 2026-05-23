<!-- purpose: Markdown skeleton for the backup spec -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens when loaded -->

# Backup Spec

- **Workload:** 
- **Author:** 
- **Date:** 
- **RPO target:** 
- **RTO target:** 
- **Retention:** 

## 3-2-1-1-0

| # | Copy | Media | Location | Immutable? |
|---|------|-------|----------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Restore verification

- Cadence: nightly / weekly
- Method: pg_restore to isolated DB / velero restore to namespace
- Alert: missed verification → page on-call
