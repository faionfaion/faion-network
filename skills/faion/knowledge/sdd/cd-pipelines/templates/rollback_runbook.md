<!-- __faion_header_v1__ -->
<!-- purpose: Rollback runbook: criteria, commands, comms -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: config; depends-on: content/01-core-rules.xml#discrete-stages -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Rollback runbook: criteria, commands, comms","consumes":"see content/02-output-contract.xml","produces":"config","depends_on":"content/01-core-rules.xml#discrete-stages","token_budget_impact":"~150 tokens when loaded"}} -->
# Rollback Runbook

## Triggers (any 1 → roll back)
- Error rate > 2x baseline for >5 minutes
- p95 latency > 1.5x baseline for >5 minutes
- Saturation alert (CPU/mem > 90%)

## Steps
1. `./scripts/deploy.sh production --rollback`
2. Notify #ops with reason + commit SHA reverted
3. Open an incident ticket; capture metrics screenshots
