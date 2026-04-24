# Agent Integration — Error Handling (RFC 7807 Problem Details)

## When to use
- Designing or refactoring HTTP API error responses across a service so every endpoint emits the same envelope.
- Mapping exceptions/Result types to HTTP responses in FastAPI, Express, Spring, ASP.NET, Axum, Actix.
- Wiring `traceId`/`trace_id` into responses and logs so Sentry/Datadog/Tempo correlate end-to-end.
- Generating OpenAPI/Problem schema components for SDK code-gen so clients get typed error objects.
- Migrating ad-hoc `{"error": "..."}` payloads to a single, documented error contract.

## When NOT to use
- Internal RPC/gRPC paths — use `google.rpc.Status` (richer) instead of forcing JSON Problem.
- WebSocket frames or SSE event streams — Problem is HTTP-response shaped; design a separate envelope.
- Browser-only client errors — use console + Sentry-JS, not RFC 7807.
- Hot paths where every byte matters (mobile-bandwidth APIs) — strip the envelope to `code`/`message`.
- Public, unauthenticated endpoints where exposing `instance` and `traceId` leaks request topology.

## Where it fails / limitations
- Validation errors don't fit RFC 7807 cleanly; the `errors[]` extension is non-standard and must be documented.
- `type` URIs that 404 are common in practice — keep them stable or move docs behind a permalink.
- Stack traces in `detail` leak in non-prod by accident; need an env-gated `debug` mode.
- Multi-error responses (batch endpoints) need `errors[]` with per-item statuses; `status` at top is then redundant.
- Localizing messages requires either Accept-Language handling server-side or codes-only payloads with client-side i18n.
- Some frameworks (Django REST default, Rails) ship their own error shape; integration requires a custom renderer.

## Agentic workflow
Drive RFC 7807 adoption with an LLM by handing the agent the existing exception-handler/middleware file plus the OpenAPI spec; the agent (1) inventories existing error shapes, (2) defines `ProblemDetail` + `FieldError` schemas, (3) writes framework-specific exception handlers, (4) updates OpenAPI components and per-endpoint `responses`. Always run a regeneration step on the typed client SDK and a contract test pass to catch consumers that hard-coded the old shape. Trace-ID propagation should be wired through the logging middleware in the same task — otherwise the `traceId` in the body and the trace in the log won't match.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps the change in an SDD task with quality gates (lint, tests, contract diff).
- `password-scrubber-agent` — strip secrets from `detail`/`errors[]` strings before they leave the service.
- A general code-implementer subagent (Sonnet) to write the framework-specific handler; a reviewer subagent (Opus) to audit for info leakage.

### Prompt pattern
```
You are upgrading <service> to RFC 7807. Read src/api/errors.py, src/api/main.py, openapi.yaml.
Output: (1) ProblemDetail pydantic model, (2) exception_handler for ValidationError, HTTPException, Exception,
(3) OpenAPI component + 4xx/5xx response refs added to every operation,
(4) test cases per status. Never put stack traces in `detail` unless DEBUG=1.
```

```
Audit these handlers for info leakage. Flag any case where DB error text, file paths,
internal hostnames, env vars, or stack frames could reach the client.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openapi-generator` | Generate typed clients from updated Problem schema | https://openapi-generator.tech |
| `schemathesis` | Property-test that every response matches OpenAPI ProblemDetail | https://schemathesis.readthedocs.io |
| `dredd` | Contract-test API against OpenAPI/HAR | https://dredd.org |
| `spectral` | Lint OpenAPI for missing `responses[4xx,5xx]` refs | https://stoplight.io/open-source/spectral |
| `sentry-cli` | Upload sourcemaps so trace IDs in Problem responses link to stack traces | https://docs.sentry.io/cli/ |
| `httpx` / `curl -i` | Manually verify Problem envelope on each endpoint | stdlib |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS + OSS | Yes (REST API, MCP) | Ingest `traceId`; tag `errors[]` codes; alert on type frequency. |
| Datadog APM | SaaS | Yes (REST API) | Use `dd.trace_id` as `traceId` so logs+errors join. |
| Grafana Tempo | OSS | Indirect | Same idea via OTel `trace_id`. |
| Stoplight Studio | SaaS | Indirect | Edit Problem schema collaboratively; export OpenAPI. |
| Postman | SaaS | Yes (collections, tests) | Add tests asserting `type/title/status/traceId` on every response. |
| Apigee / Kong | SaaS / OSS gateway | Yes | Wrap upstream errors in Problem at the edge for legacy services. |

## Templates & scripts
See `templates.md` for a full FastAPI handler. Inline check below validates that every 4xx/5xx response in an OpenAPI doc points at `ProblemDetail`:

```python
# scripts/check_problem_refs.py
import sys, yaml
spec = yaml.safe_load(open(sys.argv[1]))
ok = True
for path, ops in spec.get("paths", {}).items():
    for method, op in ops.items():
        if method.startswith("x-") or method == "parameters":
            continue
        for code, resp in op.get("responses", {}).items():
            if not (code.startswith("4") or code.startswith("5")):
                continue
            ref = (resp.get("content", {}).get("application/json", {})
                       .get("schema", {}).get("$ref", ""))
            if not ref.endswith("/ProblemDetail"):
                print(f"FAIL {method.upper()} {path} {code} -> {ref or 'no schema'}")
                ok = False
sys.exit(0 if ok else 1)
```

## Best practices
- Pin the `type` URI to a versioned docs path (`/errors/v1/validation-error`) so renames don't break clients.
- Generate `traceId` as the same value used by your tracing SDK (OTel `trace_id`), not a fresh UUID.
- For validation errors, set `code` to a stable machine-friendly slug (`invalid_format`), keep `message` human and localizable.
- Keep `title` short and the same for a given `type`; let `detail` carry the per-request specifics.
- Return `application/problem+json` Content-Type, not `application/json` — proxies and clients can branch on it.
- Add a 5xx response with `traceId` even on unhandled exceptions so support can find the trace without reproducing.
- Document every error code in the same OpenAPI doc; agents should regenerate docs in the same PR as the handler change.
- Strip newlines and control chars from any user-supplied data before placing it in `detail` to prevent log injection.

## AI-agent gotchas
- LLMs love to dump exception messages straight into `detail` — that leaks DSN strings, query text, internal hostnames. Always include a scrubbing step.
- An agent regenerating handlers may forget the `Exception` (catch-all) handler and break shutdown traces; require a test for unhandled-exception path.
- When the agent edits OpenAPI it tends to add `ProblemDetail` to 4xx but skip 5xx — enforce both.
- Trace-ID propagation: agent often invents `uuid.uuid4()` instead of pulling from existing tracer context; require reading the tracing setup file first.
- Multi-language stacks: an LLM will copy a Python pattern into Go/Java verbatim — require per-language idioms (errors.As, ControllerAdvice) before commit.
- Human-in-loop checkpoint: review every change to the `type` URI namespace — it's a public contract; once shipped, renames break clients silently.
- Validate that pre-existing client SDKs still parse the new envelope; an agent has no way to know about an undocumented mobile client unless told.

## References
- RFC 7807 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc7807
- RFC 9457 — Problem Details for HTTP APIs (replaces 7807): https://www.rfc-editor.org/rfc/rfc9457
- FastAPI exception handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- Spring `ProblemDetail`: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- ASP.NET Core problem details: https://learn.microsoft.com/aspnet/core/web-api/handle-errors
- OpenTelemetry trace context: https://www.w3.org/TR/trace-context/
