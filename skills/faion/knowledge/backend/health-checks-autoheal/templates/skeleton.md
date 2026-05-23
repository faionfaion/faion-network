<!-- purpose: Health-check audit report listing endpoints + retries + escalation. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Health Checks + Auto-Heal — Audit Report

## Services

| service | endpoint | timeout | retry | escalate |
|---------|----------|---------|-------|----------|
| api | http://127.0.0.1:8000/health | 5s | 3 | TG |
| worker | systemctl status worker | n/a | 3 | TG |

## systemd hooks

- Restart=on-failure: yes
- OnFailure=service-failed@%i: yes
- StartLimitBurst: 3

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
