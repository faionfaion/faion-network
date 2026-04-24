# Agent Integration — Go HTTP Handlers (Gin/Echo/Chi/net-http)

## When to use
- Building a JSON REST API in Go with Gin, Echo, Chi, or stdlib `net/http` (1.22+ enhanced muxer).
- Migrating from one router to another and need a consistent handler shape across files.
- Wiring middleware (auth, request ID, recovery, CORS, rate limit, tracing) into a router idiomatically.
- Generating CRUD handlers from a schema (OpenAPI, sqlc) where shape and validation rules are repetitive.
- Replacing reflection-heavy frameworks with stdlib + `chi` for performance-critical paths.

## When NOT to use
- gRPC services — use `grpc-go` and interceptors, not HTTP-handler patterns.
- WebSocket-first apps — `gorilla/websocket` or `nhooyr.io/websocket`, not HTTP middleware chains.
- Static asset serving — `http.FileServer` or a CDN; framework middleware is overhead.
- Streaming/SSE-heavy endpoints — Gin's response abstractions can buffer; drop to `http.ResponseWriter` directly.
- Stdlib-only constraints prefer `net/http` 1.22 muxer, not Gin/Echo (cuts a dep).

## Where it fails / limitations
- Gin's binding errors return a single string by default; you have to map `validator.ValidationErrors` to per-field messages explicitly.
- `c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})` is the wrong default for any production API — leak-prone, not RFC 7807.
- Echo's middleware order matters and is easy to misorder (recovery must be outermost; logger after request-id).
- Chi's `router.Use` applies to all routes after the call — easy to forget when mounting subrouters.
- `c.ShouldBindJSON` reads the body once; if a downstream middleware tries to re-read it, it's empty. Use `httputil.DumpRequest` carefully.
- Performance traps: per-request `gin.Default()` is fine; per-request `validator.New()` is not — cache it.
- Gin and Echo are not API-stable across major versions; pinned imports are required.

## Agentic workflow
The agent should (1) read the existing router setup and middleware stack to match style, (2) generate handlers as method-on-struct so dependencies (services, loggers) are injected, (3) emit request DTOs with `binding`/`validate` tags and a typed response struct, (4) wire the new route into the router with the same middleware slice, (5) generate table-driven tests with `httptest`. The single most common error is hard-coding string responses; insist on structured DTOs aligned with the project's error envelope (see `error-handling/`). For a brand-new service, first decide router (Gin vs Echo vs Chi vs stdlib) and lock it in the system prompt — do not let the LLM mix routers.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps the change as an SDD task; gates: `go test -race`, `go vet`, `golangci-lint`.
- A general implementer (Sonnet) for handler/test generation; an architect (Opus) for the middleware-order audit.
- `password-scrubber-agent` — review `c.JSON(... err.Error())` calls for secret leakage.

### Prompt pattern
```
Add CRUD handlers for <resource> in internal/handler/<resource>.go using Gin v1.10.
Inject *<resource>Service. Request/response DTOs with validator tags. Map validation
errors to RFC 7807 ProblemDetail (see internal/api/errors.go). Register routes in
SetupRouter(). Add table-driven tests using httptest.
```

```
Audit this router for: middleware order (recovery outermost, request-id before logger),
missing context propagation, hand-built error JSON instead of ProblemDetail, and reads
of c.Request.Body downstream of bind. Output file:line for each issue.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Run handler tests with race detector | stdlib |
| `httpie` / `curl` | Manual smoke against routes | https://httpie.io |
| `oapi-codegen` | Generate Echo/Chi handler stubs from OpenAPI | https://github.com/oapi-codegen/oapi-codegen |
| `swag` | Generate OpenAPI from Gin annotations | https://github.com/swaggo/swag |
| `vegeta` / `k6` | Load test handlers | https://github.com/tsenart/vegeta · https://k6.io |
| `mockery` | Mock services for handler tests | https://vektra.github.io/mockery/ |
| `golangci-lint` | Lint with revive/staticcheck | https://golangci-lint.run |
| `air` | Live-reload during dev | https://github.com/cosmtrek/air |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog APM | SaaS | Yes | `gintrace.Middleware`, `echotrace.Middleware` slot in. |
| OpenTelemetry Go | OSS | Yes | `otelgin`, `otelecho`, `otelchi` instrumentation packages. |
| Sentry | SaaS | Yes | `sentrygin`, `sentryecho` HTTP middleware. |
| Postman / Bruno | SaaS / OSS | Yes (collections) | Drives handlers via collections; agent can author runs. |
| Stoplight | SaaS | Indirect | OpenAPI source for `oapi-codegen`. |
| Cloudflare / Fastly | SaaS edge | Yes | Origin still serves the handlers; CORS + cache headers matter. |
| Kong / Tyk | OSS / SaaS gateway | Yes | Auth/rate-limit at edge; handlers stay thin. |

## Templates & scripts
See `templates.md` for full Gin/Echo routers. Inline stdlib 1.22 muxer pattern (no framework):

```go
package main

import (
	"encoding/json"
	"log/slog"
	"net/http"
)

type App struct{ users UserService }

func (a *App) routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/v1/users/{id}", a.getUser)
	mux.HandleFunc("POST /api/v1/users", a.createUser)
	return withRequestID(withRecover(withLogger(mux)))
}

func (a *App) getUser(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	u, err := a.users.Get(r.Context(), id)
	if err != nil { writeProblem(w, r, err); return }
	writeJSON(w, http.StatusOK, u)
}

func writeJSON(w http.ResponseWriter, code int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(v)
}

// writeProblem writes RFC 7807 — see error-handling/ methodology.
func writeProblem(w http.ResponseWriter, r *http.Request, err error) {
	slog.ErrorContext(r.Context(), "handler", "err", err)
	// ... map err to ProblemDetail, encode
}
```

## Best practices
- Inject dependencies via a `Handler` struct; never use package-level globals (`var DB *sql.DB`) inside handlers.
- Always pass `r.Context()` (or `c.Request.Context()` in Gin) into services — long-running handlers must respect client cancellation.
- Use one validation library across the codebase (go-playground/validator) and one error envelope (RFC 7807) — agents copy the local style.
- Bind input DTOs, validate, then convert to a domain type before calling the service. Don't pass DTOs deeper than the handler.
- Write tests with `httptest.NewRecorder` + `router.ServeHTTP` rather than spinning a real server; they're faster and parallel-safe.
- Cache the validator instance (`var v = validator.New()`) at package level — recreating it per request is allocation-heavy.
- Set sensible server timeouts (`ReadHeaderTimeout`, `WriteTimeout`, `IdleTimeout`) at `http.Server` level — frameworks don't.
- For 1.22+, prefer the stdlib enhanced muxer for new services unless team-wide tooling already standardized on a framework.

## AI-agent gotchas
- LLMs mix Gin and Echo handler signatures (`func(c *gin.Context)` vs `func(c echo.Context) error`) when context is long; pin the framework in the system prompt.
- Agents add `c.Bind` (without `Should`) on Gin which writes a 400 directly and continues — bug-prone. Insist on `c.ShouldBindJSON`.
- Generated handlers often forget `defer r.Body.Close()` for stdlib code, leaking sockets under load.
- LLMs return raw `err.Error()` in JSON, leaking stack-like strings; require RFC 7807 mapping.
- Middleware order is silently wrong — recovery placed *inside* logger means a panic crashes the logger middleware first. Require an order audit.
- Path param parsing differs across libs (`c.Param("id")`, `r.PathValue("id")`, `chi.URLParam(r, "id")`); agents pick whichever appeared most in training. Validate against the chosen router.
- Human-in-loop checkpoint: any handler that takes file uploads or long bodies — review for `MaxBytesReader` and timeout settings, agents skip these.
- Test generation often forgets to test the unhappy paths (missing field, invalid type, oversized body); require a coverage matrix.

## References
- Gin docs: https://gin-gonic.com/docs/
- Echo docs: https://echo.labstack.com/docs
- Chi: https://github.com/go-chi/chi
- net/http (1.22 muxer): https://pkg.go.dev/net/http
- go-playground/validator: https://github.com/go-playground/validator
- httptest: https://pkg.go.dev/net/http/httptest
- OpenTelemetry Go contrib: https://github.com/open-telemetry/opentelemetry-go-contrib
