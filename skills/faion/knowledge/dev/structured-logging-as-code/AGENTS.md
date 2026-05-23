# Structured Logging as Code

## Summary

**One-sentence:** Structured-logging spec: required JSON fields, PII redaction policy, trace correlation, per-environment log levels, ingestion contract validated in CI, owner signed.

**One-paragraph:** Generic logging-patterns guidance leaves teams shipping prose logs with PII leaks, missing trace ids, and per-env volume blowups. This methodology produces a logging spec: required JSON shape (ts, level, msg, request_id, user_id_hashed), PII redaction rules (denylist + regex), trace correlation (OpenTelemetry trace_id + span_id propagation), per-environment level matrix (dev=DEBUG, staging=INFO, prod=INFO with SAMPLED DEBUG), and an ingestion contract (parser fixture) that CI validates. Result: logs that humans can read, machines can index, and lawyers can defend.

**Ефективно для:**

- First production deploy - закрити PII leak в access log одразу.
- Перехід з f-string logs на structured JSON - зафіксувати baseline.
- Post-incident коли trace_id губиться між сервісами - впровадити propagation.
- Compliance audit (GDPR / CCPA) - продемонструвати redaction policy.
- Log volume blow-up - впровадити per-env sampling + level matrix.

## Applies If (ALL must hold)

- Service runs in at least one non-dev environment.
- Logs are aggregated to a queryable destination (Loki, ELK, Datadog, CloudWatch).
- Team can deploy code that controls the log shape (no fully managed black-box).
- PII may pass through the service (user identifiers, emails, payment tokens).

## Skip If (ANY kills it)

- Pure CLI tool with no remote log destination.
- Service has zero PII surface and zero compliance burden.
- Logging already standardised at a platform layer the team cannot modify.
- Pre-MVP prototype with no users - delay until launch.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Log destination | URL + index + retention | platform |
| PII inventory | list of fields with sensitivity | product/legal |
| Trace context | OpenTelemetry SDK or vendor equivalent | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-testing]] | PII / regulatory context the redaction policy plugs into. |
| [[rest-api-design]] | request_id propagation contract this spec relies on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: required-fields, PII redaction, trace correlation, per-env levels, CI parser fixture, skip-gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: shape, redaction, trace, levels, CI fixture | ~800 |
| `content/05-examples.xml` | essential | Worked example: FastAPI service with OTel + denylist + Loki | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals to a rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-required-fields` | haiku | Mechanical field list per the spec. |
| `design-redaction-policy` | sonnet | Per-service PII inventory plus regex authoring. |
| `wire-trace-correlation` | sonnet | OTel context propagation across boundaries. |
| `compliance-review` | opus | Stakes high; missed redaction = privacy incident. |

## Templates

| File | Purpose |
|------|---------|
| `templates/logging-spec.md` | Markdown skeleton for the logging spec (fields + redaction + levels). |
| `templates/redaction-config.yaml` | YAML denylist + regex rules for the redaction layer. |
| `templates/logger.py` | Python structured logger with OTel + redaction adapter. |
| `templates/_smoke-test.json` | Filled-in minimum viable logging spec for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-logging-as-code.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[security-testing]]
- [[rest-api-design]]
- [[spec-driven-debugging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree checks preconditions, then PII surface, then trace propagation, then per-env levels, then CI fixture. Every leaf maps to a rule id from `content/01-core-rules.xml`, with skip-this-methodology as the default for pre-MVP or no-PII services.
