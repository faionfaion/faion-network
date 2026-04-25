# Agent Integration — Error Handling (RFC 7807)

Methodology specifies a standardized API error response format following RFC 7807 (Problem Details for HTTP APIs): `type, title, status, detail, instance, errors[], traceId`. Use this file as a contract that an LLM agent enforces across endpoints, regardless of language.

## When to use
- New REST API where consistent client-side error handling matters.
- Refactor of inconsistent error responses (some `{error: "..."}`, some `{detail: "..."}`, some HTML) into one shape.
- Public-facing API where error shape becomes part of the contract.
- Multi-service architecture — clients should not memorize each service's error format.
- API gateway / BFF setups translating downstream errors into a unified shape.

## When NOT to use
- gRPC services — use `google.rpc.Status` + `google.rpc.error_details` instead; RFC 7807 is HTTP-specific.
- GraphQL — errors live in the response `errors[]` array per spec; RFC 7807 doesn't fit.
- Internal-only APIs where stability is low and the cost of an envelope outweighs benefit.
- Streaming endpoints (Server-Sent Events, WebSockets) — error frames have their own conventions.
- Static asset / file download endpoints — return raw HTTP status, no body.

## Where it fails / limitations
- README is **schema-only**: no language-specific implementation, no integration with FastAPI/DRF/Express/Gin.
- `traceId` is shown but no guidance on how to populate it (W3C `traceparent` header, OTel context, etc.).
- `errors[]` is a custom extension to RFC 7807 — clients written to the spec may not parse it. Document explicitly.
- `type` is supposed to be a URL pointing to docs; without that infra (`/errors/<slug>` page hosted), it's a dead string.
- No anti-fingerprint guidance — `detail` should not leak stack traces, internal paths, SQL errors, or PII.
- `instance` is sometimes a path, sometimes a request ID — RFC says URI of the specific occurrence; agents pick whichever.
- Doesn't cover localization (`title` in user's language vs always English).
- No content-type discussion (`application/problem+json` is the spec; `application/json` is technically wrong).

## Agentic workflow
For each endpoint: (1) define a small set of error `type` slugs (e.g., `validation-error`, `not-found`, `unauthorized`, `rate-limited`, `internal-error`), (2) host a docs page per slug at `/errors/<slug>`, (3) implement a framework-level exception handler that returns Problem Details with `Content-Type: application/problem+json`, (4) propagate `traceparent` from request → response, (5) add a contract test asserting the error shape on each error class. Validate via `schemathesis` or a custom Pydantic/Zod schema check in CI.

### Recommended subagents
- `faion-api-developer` — Owns the contract definition and per-error documentation pages.
- `faion-code-agent` — Implements per-framework exception handlers (DRF custom handler, FastAPI `RequestValidationError` override, Express middleware, gin handler).
- `faion-test-agent` — Writes contract tests asserting Problem Details shape.
- `faion-software-architect` — Decides which errors are exposed vs suppressed (5xx detail leaks, etc.).
- `faion-sdd-execution` — Drives the rollout as a feature with a backwards-compat phase.

### Prompt pattern
DRF custom exception handler:

```
Implement apps/common/exceptions.py + settings DEFAULT_EXCEPTION_HANDLER
that turns DRF exceptions into RFC 7807 Problem Details per
free/dev/software-developer/error-handling/README.md.
Set Content-Type to application/problem+json.
Map DRF errors:
  ValidationError -> 400 + errors[] populated from field errors
  NotAuthenticated/AuthenticationFailed -> 401
  PermissionDenied -> 403
  NotFound -> 404
  Throttled -> 429 + Retry-After
  Unhandled -> 500 with detail="An internal error occurred" (NEVER raw exc str)
Include traceId from request.META.get('HTTP_TRACEPARENT') or generate UUID.
Add tests/test_exception_handler.py covering each mapping.
```

FastAPI:

```
Replace default FastAPI HTTPException handler with a Problem Details
middleware. Map RequestValidationError to 400 with errors[] of
{field, code, message}. Map starlette.HTTPException to the matching
title. Reject any handler that calls JSONResponse with shape != ProblemDetail.
Add scripts/check-error-shape.sh that calls 5 endpoints with bad input and
asserts the response Content-Type and JSON keys.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `schemathesis` | Property tests against OpenAPI; checks error responses match spec | https://schemathesis.readthedocs.io |
| `dredd` | API contract testing against OpenAPI/Blueprint | https://dredd.org |
| `oasdiff` | Detect breaking changes including error response shape | https://github.com/Tufin/oasdiff |
| `httpie` / `curl -i` | Manual probe; inspect Content-Type | bundled / `apt install httpie` |
| `jq` | Assert JSON shape in shell | `apt install jq` |
| `ajv` (CLI) | JSON Schema validation against captured response | https://ajv.js.org |
| `bunyan` / `pino` (Node) + `slog` (Go) + `structlog` (Python) | Structured error logging matching `traceId` | per-lang |
| `otel-cli` | Inject + propagate W3C traceparent in tests | https://github.com/equinix-labs/otel-cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry | SaaS APM | Yes — captures `error.type`, `error.handled` | Tag with `error.type=<slug>` for grouping |
| Datadog APM | SaaS | Yes — `error.message`, `error.type` tags | Build dashboards per error type slug |
| Honeycomb | SaaS | Yes — high-cardinality `error.code` | Best for slug-based slicing |
| OpenTelemetry Collector | OSS | Yes — convert HTTP error responses to spans | Provides `traceId` propagation |
| Stoplight Studio | SaaS | Yes — define error responses per endpoint in OAS | Pairs well with Problem Details |
| Cloudflare WAF / API Shield | SaaS | Partial — generates own error shape on block | May need rewrite middleware to reformat |

## Templates & scripts
README has the schema. Add a JSON Schema for validation in CI/tests (≤45 lines):

```yaml
# docs/api/problem-details.schema.yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://api.example.com/schemas/problem-details"
type: object
required: [type, title, status]
properties:
  type:
    type: string
    format: uri
  title: {type: string}
  status: {type: integer, minimum: 100, maximum: 599}
  detail: {type: string}
  instance: {type: string}
  traceId: {type: string}
  errors:
    type: array
    items:
      type: object
      required: [field, code, message]
      properties:
        field: {type: string}
        code: {type: string}
        message: {type: string}
additionalProperties: true
```

Contract test (Python):

```python
import json, jsonschema, requests

SCHEMA = json.load(open("docs/api/problem-details.schema.yaml"))

def assert_problem(resp):
    assert resp.headers["content-type"].startswith("application/problem+json")
    assert 400 <= resp.status_code < 600
    jsonschema.validate(resp.json(), SCHEMA)
```

## Best practices
- **Use `application/problem+json` content-type.** RFC 7807 requires it; clients that look for the suffix `+json` still parse correctly.
- **Stable `type` URIs.** Treat them as part of the API contract. Changing `type: ".../validation-error"` to `.../validation` is breaking.
- **Slugs over numeric codes** in `errors[].code`. `email_invalid` beats `E1042`. Easier client-side handling, better in logs.
- **Never put exception messages in `detail` for 5xx.** Always a generic string + `traceId` for support to look up internally.
- **Always populate `traceId`.** Map W3C `traceparent` if present; else generate. Without it, supporting customers requires log scraping by timestamp.
- **Map framework exceptions exhaustively.** Default handler for unmatched exceptions returns 500 + safe `detail`. No raw stack ever.
- **Localize `title` and `errors[].message`.** Pull from i18n bundle keyed on `code`. `detail` may stay English (machine-friendly).
- **Document each `type` URI with**: trigger condition, status code, `errors[]` shape, recovery hint. One page per slug.
- **Include `Retry-After` on 429 / 503**, in seconds or HTTP-date. Clients implementing exponential backoff need it.
- **Don't abuse `errors[]`** for non-validation errors. Put a single `detail` for 401/403/404/409/429.
- **Pair `traceId` with structured logs** including same field name. Operators can `grep traceId="abc"` across all services.

## AI-agent gotchas
- **`detail` leaking PII / SQL / paths.** Generic phrases like `"Operation failed"` are boring but safe; agents tend to interpolate the exception message and ship it.
- **Wrong content-type.** Returning `application/json` instead of `application/problem+json` makes some clients (e.g., Spring's `RestClient` with `ProblemDetail`) parse as generic JSON, losing typed handling.
- **`type` as a literal type discriminator** is tempting (`type: "validation"`) but spec says URI. Use full URL even for stable IDs.
- **`status` field vs HTTP status mismatch.** RFC says they MUST match. Easy to mismatch when re-wrapping downstream errors.
- **`instance` ambiguity.** Some implementations put request path, some put unique trace ID URI. Pick one per project; document it.
- **Stack traces in `errors[]`** for debugging mode are tempting; ensure they're stripped in prod env.
- **CORS preflight errors** never go through your handler — browser sees them as raw OPTIONS failures. RFC 7807 won't help; fix CORS config.
- **`traceparent` propagation chain** breaks if a downstream service re-generates instead of forwarding. Audit middleware.
- **Custom `errors[]` field absent in actual RFC 7807** — clients written to the spec may not see field-level errors. Document the extension.
- **Throttling response shape varies by framework.** DRF returns `{detail: "Request was throttled.", available_in: 30}`; Express `express-rate-limit` returns plaintext. Normalize via custom handler.
- **GraphQL endpoint mistakenly using Problem Details** — GraphQL spec mandates `errors[]` in body with `data: null`. Don't apply this methodology there.
- **i18n translation of `code`** is a bug — code is machine-readable. Translate `message` only.
- **`additionalProperties: true`** in your schema vs strict client. Some validators reject unknown fields. Decide and document policy.

## References
- README: `./README.md`
- Sibling Go-specific: `../go-error-handling/`
- RFC 7807: https://datatracker.ietf.org/doc/html/rfc7807
- RFC 9457 (RFC 7807 update, 2023): https://datatracker.ietf.org/doc/html/rfc9457
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- OpenAPI Problem Details example: https://opensource.zalando.com/restful-api-guidelines/#176
- Spring `ProblemDetail`: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- DRF custom exception handler: https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
- FastAPI exception handlers: https://fastapi.tiangolo.com/tutorial/handling-errors/
- json-schema 2020-12: https://json-schema.org/draft/2020-12/schema
