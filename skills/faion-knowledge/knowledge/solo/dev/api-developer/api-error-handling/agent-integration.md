# Agent Integration — API Error Handling (RFC 7807 / 9457)

## When to use
- Public REST APIs and internal service-to-service HTTP APIs that need a single, machine-readable error contract across endpoints, languages, and clients.
- Polyglot platforms where Python (FastAPI / DRF), Node (Express / Fastify), Go, and Rust services must emit a uniform error envelope so a single SDK / client error handler covers all.
- API gateways and BFFs (Kong, AWS API Gateway, Nginx) where downstream errors must be normalized before reaching browsers / mobile.
- B2B integrations where partners need stable, documented `type` URIs and `code` enums (linked to docs) for retries, backoff, and support tickets.
- LLM-driven backends — Problem Details (RFC 9457, the 7807 update) gives agents a deterministic structure to populate and unit-test against.

## When NOT to use
- gRPC / GraphQL services — they have their own error models (`google.rpc.Status` and `errors[]` payload) and shoehorning RFC 7807 fights the protocol.
- Internal-only RPC where logs + tracing already describe the failure and a JSON envelope adds no client value.
- Ultra-low-latency endpoints (HFT, hot caches) where serializing a structured Problem Details object on the error path is measurable overhead vs a 4-byte status.
- Pre-auth endpoints (`/health`, public CDN edges) — minimize attack surface; return bare codes, never echo internals.
- Codebases already standardized on `application/vnd.api+json` (JSON:API) or Google API design errors — switching mid-flight breaks clients.

## Where it fails / limitations
- **Information leakage.** Stack traces, SQL fragments, internal hostnames bleed into `detail`. Symptom: prod errors expose ORM internals. Mitigation: separate `internal_message` (logged) from `detail` (returned).
- **Inconsistent envelope across services.** One service uses `{"error": "..."}`, another `{"errors": [...]}`, a third RFC 7807. Clients write fragile parsers. Mitigation: enforce shape via shared library + contract tests.
- **Trace ID missing.** Root cause untraceable across microservices. Mitigation: middleware injects `traceparent` (W3C), echoes as `traceId` in body and `X-Request-ID` header.
- **Validation errors flattened.** Clients can't map errors to form fields. Mitigation: include `errors[]` with `field` (JSON pointer or dotted path), `code`, `message`.
- **HTTP status mismatch.** Body says `status: 422` but HTTP code is 400 — proxies cache wrong responses. Always sync HTTP code with body.
- **Translated `detail`.** Localized messages without `Content-Language` or stable `code` field force clients to string-match localized text.
- **Retry semantics absent.** Client cannot distinguish transient (502/503/504, network) from permanent (4xx). Mitigation: standardize `Retry-After` and a boolean `transient` extension.
- **`type` URI churn.** Changing the URI breaks clients keyed on it. Treat URIs as a public contract under versioning.
- **CORS preflight errors** bypass the handler — browsers see opaque network errors. Configure CORS first; preflight must succeed before handlers run.
- **PII in errors.** Emails / user IDs in `detail` get logged everywhere. Scrub before serialization.

## Agentic workflow
Drive error-handling work in four stages: (1) a **schema-curator** subagent owns the shared `ProblemDetail` Pydantic / Zod / Go struct and enumerated `code` registry; every new endpoint imports from this module; (2) an **exception-mapper** subagent generates per-framework handlers (FastAPI `exception_handler`, Express middleware, Gin middleware) that translate domain exceptions → Problem Details and emit logs with full stack + `traceId`; (3) a **contract-test** subagent writes property-based tests asserting every documented `code` round-trips through the handler with correct status + headers (`Retry-After`, `Content-Language`); (4) `faion-sdd-executor-agent` runs the standard quality gate. Pair with a **client-SDK-codegen** step so SDKs surface typed error classes per `code`. Never let an agent invent ad-hoc envelopes per endpoint — enforce shared module imports via lint rule.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — runs lint/build/test; rejects PRs that introduce new envelope shapes.
- A purpose-built **error-code-registrar** — appends new `code` enum values + `type` URI + docs page from a one-line description; refuses duplicates.
- A **pii-scrubber-agent** — scans `detail` / `instance` strings for emails, tokens, IPs; rewrites or fails the test.
- A **contract-fuzzer-agent** — hits each endpoint with malformed payloads, asserts response matches Problem Details schema and HTTP code matches body `status`.
- A **traceid-linter-agent** — fails build if any error path returns without a `traceId` extension.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — catches secrets in fixtures / examples.

### Prompt pattern
Adding a new error code:
```
Add error code USER_QUOTA_EXCEEDED to the shared registry.
- type: https://api.example.com/errors/user-quota-exceeded
- title: "User Quota Exceeded"
- HTTP status: 429
- transient: true
- Retry-After: from quota.reset_at - now()
- detail template: "Your plan allows {limit} requests/hour."
- extensions: { limit, used, resetAt }
- docs: https://docs.example.com/errors/user-quota-exceeded
Update src/errors/registry.py, openapi.yaml components.responses,
and add contract test asserting headers and body.
```

Refactor ad-hoc to RFC 7807:
```
Find every JSONResponse / res.json with status>=400 in src/.
For each, replace with ProblemDetail.from_code(code=...).
List occurrences where I must supply additional context fields.
Output a unified diff and a checklist of unmapped errors.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pydantic` | Typed `ProblemDetail` model + validation (Python) | https://docs.pydantic.dev |
| `zod` | Typed schema + parser (TS/JS) | https://zod.dev |
| `openapi-core` | Validate runtime responses against spec | https://github.com/python-openapi/openapi-core |
| `schemathesis` | Property-based contract testing | https://schemathesis.readthedocs.io |
| `dredd` | OpenAPI contract test runner | https://dredd.org |
| `spectral` | Lint OpenAPI spec; rules can require Problem Details on 4xx/5xx | https://stoplight.io/open-source/spectral |
| `redocly` | Lint + render docs from OpenAPI | https://redocly.com/docs/cli |
| `httpx` / `curl` | Manual probing during agent dev loops | https://www.python-httpx.org |
| `problem-details` (Node) | RFC 7807 helper for Express/Fastify | https://www.npmjs.com/package/problem-details |
| `Hydra Problem JSON` (Java/Spring) | Spring Boot Problem support | https://github.com/zalando/problem-spring-web |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | yes | Capture server-side error with `traceId` correlated to client report. |
| Datadog APM | SaaS | yes | Spans correlate with `traceparent`/`traceId` in Problem Details. |
| OpenTelemetry Collector | OSS | yes | Propagate W3C `traceparent`; log exporter ties errors to traces. |
| Honeycomb / Lightstep | SaaS | yes | High-cardinality error querying by `code` and `traceId`. |
| Stripe / GitHub / Twilio API | SaaS reference | n/a | Read public docs as gold-standard error envelope examples. |
| Kong / AWS API Gateway | OSS / SaaS | yes | Translate upstream errors → Problem Details at the edge. |

## Templates & scripts
See `templates.md` for FastAPI / Express handlers and OpenAPI fragments. Pre-commit hook to forbid ad-hoc error envelopes:

```bash
#!/usr/bin/env bash
# error-envelope-guard.sh — block raw JSON error responses.
# Allow only ProblemDetail.from_code(...) / problemDetail({...}).
set -euo pipefail
SRC="${1:-src}"
BAD=$(grep -rEn --include='*.py' --include='*.ts' --include='*.js' \
  -e 'JSONResponse\(.*status_code=4' \
  -e 'JSONResponse\(.*status_code=5' \
  -e 'res\.status\((4|5)[0-9]{2}\)\.json' \
  "$SRC" \
  | grep -v 'ProblemDetail' || true)
if [ -n "$BAD" ]; then
  echo "FAIL — raw error response detected; use ProblemDetail.from_code(...)"
  echo "$BAD"
  exit 1
fi
echo "OK"
```

## Best practices
- **Single source of truth.** One `errors/registry.{py,ts,go}` per service; codes are enums, not free strings.
- **Body status === HTTP status.** Always. Proxies cache by HTTP code.
- **Always emit `traceId`** (W3C `traceparent`-derived). Surface in client error UI.
- **`code` enum** is the contract for clients; `detail` is human-readable, possibly localized via `Accept-Language`.
- **Never echo internals.** Stack, SQL, file paths, env names — log server-side, scrub from response.
- **Validation errors → 422** (or 400 if your style guide prefers); list field-level errors with stable `code`s and dotted paths.
- **`Retry-After` on 429 / 503**; mark errors as `transient: true|false` in extensions.
- **Document every code** with a `type` URI that resolves to a docs page.
- **Contract test on every PR.** Schemathesis or dredd against the OpenAPI spec.
- **i18n.** Send `Content-Language`; SDKs key off `code`, not message text.
- **Authorization vs authentication.** 401 for missing/invalid token, 403 for valid token without permission. Don't conflate.
- **Idempotency keys** + duplicate handling → 409 Conflict with previous result reference, not 500.

## AI-agent gotchas
- **Inventing new envelopes.** Agent forgets the shared registry exists; rolls a one-off `{"error": "..."}` per endpoint. Lint rule + import-only access prevents drift.
- **Echoing exception messages directly.** `detail = str(exc)` leaks DB constraint names, SQLAlchemy reprs, `KeyError: 'password'`. Wrap with sanitizer.
- **Forgetting `traceId` on uncaught exceptions.** Generic 500 handler must inject trace ID before serializing.
- **Mismatched body/HTTP status.** Agent edits body `status: 400` but route still returns 422. Test must compare both.
- **Hardcoded `type` URIs per service.** Use a central base URL constant; agents otherwise duplicate `https://api.example.com/errors/...` everywhere.
- **Retry advice in prose, not headers.** Agent writes "try again later" in `detail` but omits `Retry-After`. Clients can't auto-retry.
- **CORS missing on error responses.** Browser sees opaque error; agent debugs handler instead of `Access-Control-Allow-Origin` on the failing route.
- **Dropping `errors[]` for validation.** Agent returns one consolidated `detail`; frontend can't map per-field. Always include the array.
- **Using `instance` for stack info.** `instance` is the request URI, not a stack. Don't repurpose schema fields.
- **Validation framework error format unmapped.** FastAPI's `RequestValidationError` has `loc[]` tuples; agents serialize raw without converting to dotted paths or JSON pointers.
- **Returning HTML on accept negotiation.** Agent registers default text/html error page; API clients get garbage. Force `application/problem+json` for API routes.
- **Logging raw PII.** Logging the entire request body for context dumps tokens and emails to log aggregator; configure scrubbers in middleware.

## References
- RFC 9457 — Problem Details for HTTP APIs (replaces RFC 7807): https://datatracker.ietf.org/doc/html/rfc9457
- RFC 7807 (original): https://datatracker.ietf.org/doc/html/rfc7807
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- FastAPI exception handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- Microsoft REST API Guidelines — Errors: https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses
- Zalando RESTful API Guidelines — Problem JSON: https://opensource.zalando.com/restful-api-guidelines/#problem
- Spectral OpenAPI rules: https://docs.stoplight.io/docs/spectral
- Sibling methodologies: `solo/dev/api-developer/api-rest-design/`, `solo/dev/api-developer/api-documentation/`, `solo/dev/api-developer/api-openapi-spec/`.
