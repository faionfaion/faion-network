# Agent Integration — API Error Handling (RFC 7807 / Problem Details)

## When to use
- Any new public or partner-facing HTTP API: standardize errors before the first endpoint ships.
- Existing API with inconsistent error shapes — agent runs an audit and proposes a one-shot migration to RFC 7807 Problem Details.
- Multi-service architectures: enforce a single error envelope across services so clients (and agents) don't have to special-case each.
- Generating client SDKs: a uniform error schema makes generated clients predictable and idempotency-safe.
- Designing retry / circuit-breaker behavior: clients can rely on `status` + `type` for deterministic decisions.
- Compliance/audit (PCI, GDPR, SOC2): structured errors with trace IDs are auditor-friendly.

## When NOT to use
- Internal RPC where both sides are owned by you and prefer richer error types (gRPC `google.rpc.Status` with details, GraphQL union types) — Problem Details is HTTP-only and lossy in those contexts.
- Server-Sent Events / WebSockets — error frames don't fit the JSON-document shape; pair with framing protocol.
- Ultra-low-latency hot paths where the JSON serialization cost is measurable — but this is rare; profile first.
- Public APIs where you're already on a stable, documented schema; don't break clients for purity.

## Where it fails / limitations
- **`type` URI fiction:** the spec wants a stable URI documenting the problem; teams put `https://example.com/errors/foo` that 404s forever. Agents replicate the placeholder.
- **`detail` leaks PII / internals:** "User 12345 not found" exposes IDs, "SQL syntax error near 'OR 1=1'" exposes schema. Agents helpfully include too much context.
- **Inconsistent error codes:** README has good `ErrorCode` enum, but services drift; one service uses `validation_error`, another `validation-error`, another `VALIDATION_ERROR`.
- **Field error format not in spec:** the example's `errors[]` array is a vendor extension. Clients must know to look for it.
- **HTTP status mismatch:** teams return `200 OK` with an error body. Breaks routers, retries, monitoring, agents.
- **i18n absent:** `title`/`detail` are English; spec leaves localization to extensions, methodology doesn't address it.
- **Trace ID distribution:** `traceId` field is suggested but not standard — different services pick `trace_id`, `traceId`, `request_id`, breaking correlation.
- **Idempotency / retry hints absent:** clients must guess from status code; methodology doesn't recommend `Retry-After` or an `extensions.retryable` flag.

## Agentic workflow
Drive API error handling as a four-pass agent flow: (1) **catalog agent** scans handlers across the repo, builds an inventory of every error shape currently returned, and clusters them by intent; (2) **schema agent** generates a canonical `ProblemDetail` Pydantic/Zod/Go struct + a versioned `errors.yaml` registry of `code → http_status, type_uri, title, retryable` rows; (3) **handler refactor agent** inserts a global exception/error middleware (FastAPI `exception_handler`, Express error middleware, Gin recovery, Spring `@ControllerAdvice`) that maps domain errors → ProblemDetail; (4) **redactor agent** runs in CI on responses captured from contract tests, flagging PII / stack-trace leaks in `detail`. Persist the registry as `docs/api/errors.yaml` and treat changes to it as breaking changes (require ADR).

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts the migration to Problem Details into SDD `todo/` tasks (one task per service / endpoint group).
- A **schema generator agent** (purpose-built, worth creating): given the codebase, emits `ProblemDetail` types for each language plus an OpenAPI fragment ready to import.
- A **redactor agent** (purpose-built): runs against captured responses, flags PII (emails, phones, IDs), and recommends safe rewordings.
- A **client-mapper agent**: generates client-side `if e.status == 429 && e.extensions.retryable: backoff()` logic from the registry.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — sanitize logged ProblemDetail bodies before they hit a long-term log store.

### Prompt pattern
Catalog:
```
Scan <paths>. For every handler that returns an error response,
extract: file, status code, JSON body shape, exception class.
Group by error intent (validation, auth, rate-limit, conflict,
not-found, internal). Output a markdown table; do not modify code.
```

Schema generation:
```
Using RFC 7807 + the methodology in
solo/dev/software-developer/api-error-handling/README.md, generate a
canonical ProblemDetail type for <language>. Include a separate
ErrorCode enum aligned with the codes in the README. Add an
`extensions` field for `retryable: bool`, `trace_id: str`, and
field-level errors. Output: type definitions + one `to_response()`
helper. Match existing project style (snake_case in Python,
camelCase in TS).
```

Redaction:
```
Given this captured error response <json>, identify any field that
might contain PII (email, phone, full name, numeric ID > 6 digits),
secrets, internal hostnames, or stack traces. For each, propose a
safe replacement (e.g., "user u_*** not found"). Output as table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `schemathesis` | Property-based testing of OpenAPI errors against running server | `pip install schemathesis` |
| `dredd` | Validate API responses match the documented error schemas | `npm i -g dredd` |
| `spectral` (Stoplight) | Lint OpenAPI for missing/inconsistent error responses | `npm i -g @stoplight/spectral-cli` |
| `redocly lint` | Same niche, opinionated about Problem Details | `npm i -g @redocly/cli` |
| `ajv-cli` | JSON Schema validate ProblemDetail samples in CI | `npm i -g ajv-cli` |
| `httpie` / `curl` | Manual round-trip checks of error shapes | https://httpie.io |
| `mitmproxy` / `httpyac` | Capture real responses to feed redactor agent | https://mitmproxy.org |
| `protoc-gen-openapiv2` | gRPC services exposing HTTP errors via gateway | https://github.com/grpc-ecosystem/grpc-gateway |
| `gosec` / `bandit` / `semgrep` | Detect leakage of stack traces / SQL fragments in errors | https://semgrep.dev |
| `claude` (Anthropic CLI) | Run catalog + schema + redactor passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS errors | API yes | Best ROI for capturing 5xx + stitching trace IDs into ProblemDetail. |
| Datadog APM / New Relic / Honeycomb | SaaS observability | API yes | Use the `traceId` from ProblemDetail to deep-link. |
| Bugsnag | SaaS errors | API yes | Same niche as Sentry. |
| Stoplight Studio / Redocly | SaaS docs | API yes | Renders RFC 7807 error tables in API docs. |
| Postman / Bruno | SaaS / OSS API client | yes | Test collections that assert ProblemDetail shape. |
| Kong / Apigee / Tyk / AWS API Gateway | SaaS API gateways | API yes | Most can rewrite gateway-level errors into ProblemDetail. |
| Spring Boot `ProblemDetail` (since 6) | OSS framework | yes | Built-in ProblemDetail type — agents should adopt it instead of rolling their own. |
| FastAPI / Hapi / NestJS Problem JSON plugins | OSS | yes | Drop-in middleware. |
| GitHub Octokit error model | docs | n/a | Reference for a public API done well; agents can mimic. |
| Stripe error model | docs | n/a | Long-running standard for error code + idempotency hint design. |

## Templates & scripts

`templates.md` ships a Python ProblemDetail and OpenAPI fragment. The gap is a runnable lint script that asserts ProblemDetail-shape on every error response captured from contract tests. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# problem-lint.py — validate captured error responses against ProblemDetail shape.
# Usage: problem-lint.py captured/*.json
import json, sys, re, pathlib
REQUIRED = {"type", "title", "status"}
ALLOWED = REQUIRED | {"detail", "instance", "trace_id", "errors", "extensions"}
PII = re.compile(r"(?i)\b([\w.+-]+@[\w-]+\.[\w.-]+|\+?\d[\d\s().-]{8,}|sk_live_[A-Za-z0-9]+)\b")
fail = 0
for path in (pathlib.Path(p) for arg in sys.argv[1:] for p in [arg]):
    try:
        body = json.loads(path.read_text())
    except Exception as e:
        print(f"PARSE {path}: {e}"); fail = 1; continue
    miss = REQUIRED - body.keys()
    if miss: print(f"MISS  {path}: {sorted(miss)}"); fail = 1
    extra = body.keys() - ALLOWED
    if extra: print(f"EXTRA {path}: {sorted(extra)}"); fail = 1
    if not isinstance(body.get("status"), int): print(f"BAD   {path}: status not int"); fail = 1
    if "type" in body and not str(body["type"]).startswith("https://"):
        print(f"BAD   {path}: type must be https URI"); fail = 1
    blob = json.dumps(body)
    for m in PII.finditer(blob):
        print(f"LEAK  {path}: possible PII '{m.group(0)[:32]}…'"); fail = 1
    if fail == 0: print(f"OK    {path}")
sys.exit(fail)
```
Wire into CI after contract tests dump captured responses to `captured/*.json`.

## Best practices
- Pin one canonical `ProblemDetail` type per language and import it everywhere; ban ad-hoc `{"error": "..."}` JSON.
- Maintain a versioned `errors.yaml` registry (code, http_status, type_uri, title, retryable). Code reviews check the registry, not the response strings.
- `type` URI must resolve. Host the docs page in the same repo (`/docs/errors/<slug>`) so the URL is part of the deploy.
- Always include `trace_id` and propagate it to your tracer/logger; clients copy it into bug reports.
- Strip stack traces and SQL fragments from `detail` in production builds (env-gated).
- Use `Retry-After` HTTP header for 429 / 503; mirror it in `extensions.retry_after` for non-HTTP transports.
- Localize via `Accept-Language` in the request and `Content-Language` in the response; cache localized titles.
- Include the registry in your OpenAPI / AsyncAPI spec so generated clients render typed error responses.

## AI-agent gotchas
- LLMs invent endpoint paths in `instance` and made-up `type` URIs that 404 — both are user-visible. Verify against the registry.
- Agents over-share `detail` (stack traces, SQL, internal IDs). Always run a redactor pass.
- Generated OpenAPI fragments often forget to set `application/problem+json` content-type — clients then mis-parse.
- Default LLM error code style is `INVALID_INPUT` / `invalid-input` / `invalidInput` mixed within one PR. Pin a casing rule in the prompt.
- Long handler files cause agents to skip outer error mappers; feed only the handler + the central error middleware.
- Agents conflate domain errors with HTTP 4xx (returning 500 for "user not allowed"). Force a mapping table in `errors.yaml`.
- Human-in-loop checkpoints: (1) any registry change (breaking for clients), (2) any `detail` field rewording in a public error, (3) status-code remapping (4xx ↔ 5xx) — these silently break consumers.

## References
- RFC 7807 — Problem Details for HTTP APIs — https://datatracker.ietf.org/doc/html/rfc7807
- RFC 9457 — Problem Details (updated) — https://datatracker.ietf.org/doc/html/rfc9457
- Microsoft REST API Guidelines — Errors — https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses
- Google API Design Guide — Errors — https://cloud.google.com/apis/design/errors
- Stripe Error Object — https://stripe.com/docs/api/errors
- Spring `ProblemDetail` (Spring 6) — https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- FastAPI Exception Handling — https://fastapi.tiangolo.com/tutorial/handling-errors/
- Schemathesis — https://schemathesis.readthedocs.io
- Local methodology: `api-error-handling/README.md`, `templates.md`, `examples.md`, `checklist.md`
