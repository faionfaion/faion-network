<!-- purpose: Post-handover warranty runbook skeleton -->
<!-- consumes: handover spec + SLA window -->
<!-- produces: numbered steps with precondition + actor + artefact + rollback -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~600-1500 tokens populated -->

# <Service> — Warranty Runbook (window: <30|60|90> days)

| # | Precondition | Actor (role+system) | Action | Artefact | Rollback / STOP | Budget |
|---|--------------|---------------------|--------|----------|------------------|--------|
| 1 | alert X fires | on-call SRE (PagerDuty) | restart service Y | run-record-NN | systemctl revert previous unit | 5m |
