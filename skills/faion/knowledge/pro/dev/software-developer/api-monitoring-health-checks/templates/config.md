<!-- purpose: config artefact skeleton for API Monitoring — Health Checks -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-800 tokens when loaded as context -->

# API Monitoring — Health Checks — config skeleton

See `AGENTS.md` for usage. Skeleton — fill per artefact.

## Required fields

- `liveness_endpoint`
- `readiness_endpoint`
- `probe_latency_p99_ms_max`
- `startup_probe_configured`
