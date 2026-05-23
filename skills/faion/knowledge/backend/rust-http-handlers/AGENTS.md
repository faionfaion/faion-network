# Rust HTTP Handlers (Axum)

## Summary

**One-sentence:** Handler shape for Axum / Actix: typed DTOs with validator, Arc<AppState>, AppError IntoResponse, #[tracing::instrument] per handler, public message scrubbing.

**One-paragraph:** Handler pattern for Axum (and Actix-web): typed request/response DTOs with validator derives, shared AppState behind Arc, AppError enum implementing IntoResponse, and #[tracing::instrument] on every handler. Public response messages are scrubbed; internal details stay in tracing fields. Output is a handler module set + AppError module + integration tests.

**Ефективно для:**

- Standardising every handler in a service on the same DTO + state + error shape.
- Adding tracing instrumentation across all routes without manual span construction.
- Scrubbing internal error detail from public responses while preserving telemetry.
- Replacing ad-hoc StatusCode returns with a typed AppError → IntoResponse pipeline.

## Applies If (ALL must hold)

- Service uses Axum or Actix-web.
- Team can mandate the same handler skeleton across all routes.
- Telemetry stack (tracing + Jaeger / OpenTelemetry) is in place.
- Validation library (validator) is acceptable.

## Skip If (ANY kills it)

- Service uses tonic / pure gRPC — handler shape differs.
- Service is a Lambda function — different entry pattern.
- Quick prototype where typing every DTO is overkill.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Route list + DTOs | yaml / md | team |
| AppState fields | yaml | team |
| Tracing exporter | config | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/rust-backend/AGENTS.md` | layout precedes handlers |
| `pro/dev/backend-systems/rust-error-handling/AGENTS.md` | AppError is shared |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-handler-shape` | sonnet | DTO + extractor wiring needs judgement. |
| `review-public-messages` | sonnet | Message scrubbing needs language judgement. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/handler_example.rs` | Axum CRUD handler skeleton |
| `templates/app_error.rs` | AppError with IntoResponse + scrubbed public messages |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-http-handlers.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-backend]]
- [[rust-error-handling]]
- [[rust-project-structure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
