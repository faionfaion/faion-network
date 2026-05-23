<!-- purpose: Minimum viable filled-in health audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Health Checks + Auto-Heal — Audit Report

## Services

| service | endpoint | timeout | retry | escalate |
|---------|----------|---------|-------|----------|
| faion-net-api | http://127.0.0.1:8000/health | 5s | 3 | TG |
| faion-net-api-dev | http://127.0.0.1:8001/health | 5s | 3 | TG |

## systemd hooks

- Restart=on-failure: yes
- OnFailure=service-failed@%i.service: yes
- StartLimitBurst: 3 / StartLimitIntervalSec: 60

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
