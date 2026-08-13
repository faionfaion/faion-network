# API Error Handling

## Summary

**One-sentence:** Builds an RFC 7807 Problem Details error envelope + a typed error catalogue with stable type URIs, traceId on every error, and 4xx/5xx split policy.

**One-paragraph:** Inconsistent error envelopes are the largest source of partner-integration friction. This methodology emits an error-catalogue: one envelope shape (RFC 7807), a stable `type` URI per error class (not per occurrence), a mandatory `traceId` for log correlation, and a strict 4xx/5xx split (4xx = caller fixable, 5xx = our fault). Output: catalogue + envelope schema + per-language handler templates.

**Ефективно для:**

- Solo dev shipping an API where every endpoint returns a different error shape.
- Adding `traceId` so support can correlate a customer complaint with logs.
- Replacing hard-coded 500s with categorised 4xx where the user can fix it.
- Wiring a partner integration where the partner needs stable type URIs to handle errors programmatically.

## Applies If (ALL must hold)

- API has &gt;= 2 distinct error classes already in production.
- Logging infrastructure produces a traceId (OTel / Datadog / Sentry).
- Author has authority to break clients on a documented version bump (or roll out behind a header).

## Skip If (ANY kills it)

- API has zero error classes (e.g. pure proxy) — defer.
- Legacy SOAP stack — out of scope.
- Internal RPC with proto errors — separate methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing error inventory | list of {endpoint, status, body shape} | code or runtime sampling |
| Tracer | OTel-compatible tracer | platform |
| Auth scheme | AUTH-* artefact | api-authentication |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-documentation]] | Error catalogue links from the Error Codes section. |
| [[api-rate-limiting]] | 429 envelope shape is shared. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_error_handling_draft` | sonnet | Bounded synthesis. |
| `api_error_handling_validate` | haiku | Mechanical schema check. |
| `api_error_handling_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-handler.py` | FastAPI middleware that wraps every error into RFC 7807 envelope with traceId |
| `templates/problem-detail.json` | RFC 7807 Problem Details example body |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-error-handling artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-error-handling artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-error-handling.py` | Validate api-error-handling artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rest-design]]
- [[api-rate-limiting]]
- [[logging-patterns]]
- [[api-authentication]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/error-handler.py`

```python
"""Global exception handlers for FastAPI — RFC 7807 Problem Detail responses."""
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None


app = FastAPI()


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=ProblemDetail(
            type="https://api.example.com/errors/validation-error",
            title="Validation Error",
            status=400,
            detail="Request validation failed",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
            errors=[
                {"field": e["loc"][-1], "code": e["type"], "message": e["msg"]}
                for e in exc.errors()
            ],
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ProblemDetail(
            type="https://api.example.com/errors/internal-error",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
        ).model_dump(),
    )
```

### `templates/problem-detail.json`

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body contains invalid fields",
  "instance": "/users/create",
  "traceId": "abc-123-xyz",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address"
    },
    {
      "field": "age",
      "code": "out_of_range",
      "message": "Must be between 18 and 120"
    }
  ]
}
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-error-handling.json",
  "type": "object",
  "required": [
    "catalogue_id",
    "envelope_shape",
    "errors",
    "traceid_field"
  ],
  "properties": {
    "catalogue_id": {
      "type": "string",
      "pattern": "^ERR-[A-Z0-9-]{2,40}$"
    },
    "envelope_shape": {
      "type": "string",
      "const": "rfc-7807"
    },
    "errors": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "type",
          "title",
          "status",
          "class"
        ],
        "properties": {
          "type": {
            "type": "string",
            "format": "uri"
          },
          "title": {
            "type": "string",
            "minLength": 3
          },
          "status": {
            "type": "integer",
            "minimum": 400,
            "maximum": 599
          },
          "class": {
            "type": "string",
            "enum": [
              "client",
              "server"
            ]
          },
          "detail_example": {
            "type": "string"
          }
        }
      }
    },
    "traceid_field": {
      "type": "string",
      "enum": [
        "traceId",
        "trace_id"
      ]
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "catalogue_id": "ERR-PUBLIC-API-V1",
  "envelope_shape": "rfc-7807",
  "errors": [
    {
      "type": "https://api.example.com/errors/insufficient-funds",
      "title": "Insufficient funds",
      "status": 402,
      "class": "client",
      "detail_example": "Account balance 12.50 EUR; charge 50.00 EUR exceeds available."
    },
    {
      "type": "https://api.example.com/errors/upstream-timeout",
      "title": "Upstream timeout",
      "status": 504,
      "class": "server",
      "detail_example": "Stripe charges API did not respond within 30s."
    }
  ],
  "traceid_field": "traceId"
}
```
