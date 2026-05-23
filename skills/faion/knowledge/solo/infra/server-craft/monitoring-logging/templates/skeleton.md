<!-- purpose: Monitoring audit listing journald + digest + alert routing. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Monitoring + Logging — Audit Report

## journald

- SystemMaxUse: 2G
- SystemKeepFree: 1G
- retention: ~30 days

## Daily digest

- channel: TG
- time: 07:00 UTC
- per_service_line: 1

## Alert routing

- silent on success: yes
- alert on fail: TG with retry-exhausted context

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
