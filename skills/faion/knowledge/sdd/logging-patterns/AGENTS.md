# Logging Patterns

## Summary

**One-sentence:** Adopts structured JSON logging with request_id correlation, PII redaction at the formatter layer, and performance fields (duration_ms, db_queries).

**One-paragraph:** Adopts structured JSON logging with request_id correlation, PII redaction at the formatter layer, and performance fields (duration_ms, db_queries). Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service emits text logs that grep poorly at 3am.
- Need to correlate a single request across multiple services or workers.
- Compliance requires PII redaction at the log layer.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service emits text logs that grep poorly at 3am.
- Need to correlate a single request across multiple services or workers.
- Compliance requires PII redaction at the log layer.

## Skip If (ANY kills it)

- Service is a one-shot script with no production runtime.
- Logs already structured and queried successfully via existing dashboards.
- No log sink in place — pick a sink first (Loki, CloudWatch, Datadog).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Logging library | Python logging / pino / winston | team |
| Log sink | Loki / CloudWatch / Elastic / Datadog | infra |
| Request middleware | ASGI/Express/Django middleware for request_id injection | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[dev-methodologies-architecture]] | architecture rubric pairs with logging baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-logger` | sonnet | JSON formatter + request_id context. |
| `redaction-rules` | sonnet | PII redaction patterns. |
| `audit-printf` | haiku | Grep for printf-style logs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/structured_logger.py` | Python structured JSON logger with request_id context |
| `templates/redaction.py` | PII redaction patterns: email, phone, credit-card-like |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-logging-patterns.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[dev-methodologies-architecture]]
- [[best-practices-2026]]
- [[feature-flags-services-testing]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the service production-runtime AND does it have a log sink configured?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
