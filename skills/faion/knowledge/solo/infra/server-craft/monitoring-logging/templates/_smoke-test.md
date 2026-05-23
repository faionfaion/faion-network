<!-- purpose: Minimum viable filled-in monitoring audit. -->
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

- channel: TG @nero-ops
- time: 07:00 UTC
- per_service_line: 1

## Alert routing

- silent on success: yes
- alert on fail: TG with retry-exhausted context
- correlation-id: x-request-id header echoed in all service logs

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
