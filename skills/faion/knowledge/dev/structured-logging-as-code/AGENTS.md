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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/redaction-config.yaml`

```yaml
rules:
  - field: user.email
    policy: hash
    algorithm: sha256
  - field: card_number
    policy: drop
  - regex: "(?i)password|secret|token"
    policy: drop
  - regex: "\\b\\d{16}\\b"
    policy: mask
    mask_value: "****-****-****-XXXX"
```

### `templates/logger.py`

```python
from __future__ import annotations
import json
import logging
import os
import sys
import time
from typing import Any

try:
    from opentelemetry.trace import get_current_span
except Exception:
    def get_current_span():
        return None


REDACT_FIELDS = {"password", "secret", "token", "card_number"}


def _redact(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: ("***" if k in REDACT_FIELDS else _redact(v)) for k, v in d.items()}
    if isinstance(d, list):
        return [_redact(x) for x in d]
    return d


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        span = get_current_span()
        ctx = span.get_span_context() if span else None
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "msg": record.getMessage(),
            "service": os.environ.get("SERVICE", "unknown"),
            "env": os.environ.get("ENV", "dev"),
            "request_id": getattr(record, "request_id", None),
            "trace_id": f"{ctx.trace_id:032x}" if ctx else None,
            "span_id": f"{ctx.span_id:016x}" if ctx else None,
            "fields": _redact(getattr(record, "fields", {})),
        }
        return json.dumps({k: v for k, v in payload.items() if v is not None})


def build_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter())
    log.addHandler(h)
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return log
```

### `templates/_smoke-test.json`

```json
{
  "required_fields": [
    "ts",
    "level",
    "msg",
    "service",
    "env",
    "request_id",
    "trace_id"
  ],
  "redaction_rules": [
    {
      "field_or_regex": "user.email",
      "policy": "hash"
    },
    {
      "field_or_regex": "card_number",
      "policy": "drop"
    }
  ],
  "trace_correlation": "otel",
  "per_env_levels": {
    "dev": "DEBUG",
    "staging": "INFO+SAMPLED-DEBUG",
    "prod": "INFO+SAMPLED-DEBUG-1pct"
  },
  "ci_parser_fixture": "tests/test_log_parser.py::test_redaction_and_schema",
  "owner": "ruslan@faion.net"
}
```
