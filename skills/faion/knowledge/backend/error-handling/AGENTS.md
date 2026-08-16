# Error Handling (RFC 7807 Problem Details)

## Summary

**One-sentence:** Produces a per-service error-envelope spec: RFC 7807 / 9457 Problem Details (`type`, `title`, `status`, `detail`, `instance`, `traceId`), single exception mapper, and validation error array.

**Ефективно для:**

- REST / GraphQL APIs with multiple consumer types.
- Multi-service backends sharing a tracing system.
- Public APIs needing self-documenting errors (`type` URI).
- Validation-heavy endpoints with field-level errors.

**One-paragraph:** Standardized HTTP API error envelope following RFC 7807 / RFC 9457: every 4xx and 5xx response carries `type` (URI), `title`, `status`, `detail`, `instance`, and `traceId` fields, with an optional `errors[]` array for field-level validation failures. A single exception handler per framework maps all error types to this shape so client code parses one envelope rather than five.

## Applies If (ALL must hold)

- Service exposes HTTP / JSON responses (REST, OpenAPI, GraphQL HTTP).
- Observability stack carries a `trace_id` per request.
- Framework has a global exception handler hook.
- Consumers can rely on a stable error envelope.

## Skip If (ANY kills it)

- Wire protocol is not HTTP / JSON — gRPC uses `google.rpc.Status` + `error_details`; GraphQL puts errors in the response `errors[]` per spec; SSE / WebSocket frames follow their own conventions.
- Static asset or file-download endpoints — raw HTTP status, no body.
- Internal-only RPC with bespoke error envelope contracted.
- Public spec already locked to non-7807 shape (don't break clients).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Framework with global exception handler | code | team |
| Tracing system + `trace_id` propagation | infra doc | SRE |
| Error type catalogue (URIs) | doc site | team |
| Localisation strategy (single locale vs multi) | product decision | PM |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules: required fields, type is a stable URI, traceId from traceparent, single mapper, errors[] scope + shape, status match, no stack leak, problem+json content-type, static 5xx detail, type URIs are contract | ~1400 |
| `content/02-output-contract.xml` | essential | Two contracts: the spec artefact, and the ProblemDetails response envelope schema + valid/invalid HTTP examples | ~1300 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: free-form codes, multiple shapes, stack leak, status mismatch, wrong content-type, errors[] misuse, missing traceId | ~1200 |
| `content/04-procedure.xml` | essential | 10 steps: 5 to produce the spec, 5 to implement it (URIs → model → one handler → traceId → contract test) | ~1500 |
| `content/05-examples.xml` | recommended | One end-to-end worked example + FastAPI / Express / Spring handlers + the reusable contract test | ~1500 |
| `content/06-decision-tree.xml` | essential | Protocol + commitment gate, then preconditions and duplicate check; run / update / skip | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-envelope` | haiku | RFC 7807 fields from spec. |
| `write-mapper` | sonnet | Framework-specific global handler. |
| `audit-error-leaks` | sonnet | Detects stack-trace leaks + multi-shape drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-handling.json` | JSON Schema for the Error Handling (RFC 7807 Problem Details) output contract |
| `templates/error-handling.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a error-handling record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a error-handling record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/problem-details.schema.yaml` | JSON Schema 2020-12 for the ProblemDetails response body — drop-in for jsonschema / ajv / schemathesis |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-handling.py` | Enforce the Error Handling (RFC 7807 Problem Details) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-error-handling]]
- [[go-error-handling-patterns]]
- [[database-design]]
- [[python-fastapi]] — FastAPI exception-handler integration.
- [[django-api]] — the DRF `EXCEPTION_HANDLER` hook this envelope is wired into.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/error-handling.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/error-handling.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^eh\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```

### `templates/problem-details.schema.yaml`

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://api.example.com/schemas/problem-details"
type: object
required: [type, title, status]
properties:
  type:
    type: string
    format: uri
  title:
    type: string
    minLength: 1
  status:
    type: integer
    minimum: 100
    maximum: 599
  detail:
    type: string
  instance:
    type: string
  traceId:
    type: string
    minLength: 1
  errors:
    type: array
    items:
      type: object
      required: [field, code, message]
      properties:
        field:
          type: string
        code:
          type: string
        message:
          type: string
additionalProperties: true
```
