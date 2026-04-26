# Agent Integration — Go HTTP Handlers (Gin / Echo)

## When to use
- Building a Go HTTP service where the team wants ergonomic routing, middleware composition, and request binding without rolling everything on `net/http`.
- Pick **Gin** when ecosystem breadth, JSON-heavy endpoints, and gin-binding tag validation are first priorities.
- Pick **Echo** when you want first-party middleware (JWT, CORS, rate-limit, prometheus), interface-driven handlers, and built-in HTTP/2.
- Greenfield microservice on Linux/Hetzner/k8s where startup time and memory footprint matter.
- Migrating a Python/Node API to Go for cost or throughput reasons (5-20× lower CPU per req for JSON CRUD).

## When NOT to use
- Go 1.22+ shops where `net/http` ServeMux now supports method+path routing and the team prefers stdlib-only.
- High-performance edge cases where `fasthttp`-backed routers (fiber) win on benchmarks but break stdlib middleware compatibility.
- gRPC-first services — drive the HTTP layer via `grpc-gateway` instead.
- One-off CLIs or tools — don't pull a web framework for a five-route admin endpoint.
- Teams already standardized on **chi**, **fiber**, or **huma** — do not mix routers in one binary.

## Where it fails / limitations
- **Implicit middleware order.** `r.Use(...)` order changes auth/logging/recovery semantics; agents reorder this and silently disable Recovery.
- **Gin binding is reflection-heavy.** Tags like `binding:"required,email"` work but error messages are opaque; users see `Field validation for 'Email' failed on the 'email' tag` unless you wrap.
- **Echo's middleware breaking changes.** v4 → v5 renamed `middleware.JWT` config; agents trained on older docs emit broken code.
- **Context misuse.** Both frameworks expose a request `Context()` separate from `c.Request.Context()`; canceling one doesn't cancel the other. DB calls leak goroutines.
- **Goroutine + handler.** Spawning `go work()` inside a handler with `c.Request.Context()` panics or aborts when the request returns; you need a derived `context.Background()` with timeouts.
- **No structured concurrency.** Errors in middleware spawned goroutines vanish; observability requires manual instrumentation.
- **Routing wildcards.** `/users/:id` vs `/users/*action` — Gin and Echo differ; copy-pasting routes between frameworks breaks at runtime.
- **Built-in validator is global.** Customizing `validator.v10` in Gin requires touching a singleton; in Echo you wire it explicitly. Agents conflate the two.

## Agentic workflow
Drive Go HTTP work as a 4-stage SDD flow. (1) **Architect** picks Gin vs Echo vs stdlib, decides DI strategy (`wire`, manual constructor injection, or `fx`), and writes the layout: `cmd/server/`, `internal/handler/`, `internal/middleware/`, `internal/service/`, `internal/repo/`. (2) **Scaffolder** generates `main.go`, the router setup, and middleware skeletons from the README templates. (3) **Resource-builder** produces handler + request struct + service interface + handler test, one resource per cycle. (4) **Reviewer** verifies context propagation, graceful shutdown, structured logging, and that no handler creates background goroutines tied to the request context.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — gates Go PRs against the SDD task; rejects handlers without tests or schema validation.
- A purpose-built **go-handler-reviewer agent** (worth creating): runs `go vet`, `staticcheck`, `gosec`, parses handler files, and flags context misuse, missing recovery, hardcoded ports/origins, and goroutine leaks.
- `password-scrubber-agent` — scrubs example configs (`.env`, `config.yaml`) before sharing handler examples externally; Go services often inline DB URLs in `main.go`.
- `nero-sdd-executor-agent` — when targeting NERO services on `nero-prod`, drives the systemd unit + `caddy/nginx` reverse-proxy alignment alongside the Go binary.

### Prompt pattern
Scaffold pass:
```
Generate a Go 1.23 service using Gin with:
- Layout: cmd/server, internal/{handler,middleware,service,repo,model}.
- Router: /api/v1, JWT auth on /users, public /healthz and /readyz.
- Middleware: RequestID, Logger (zap), Recovery, RateLimit (uber-go/ratelimit), CORS.
- Graceful shutdown: 15s drain on SIGINT/SIGTERM.
- Handlers: ListUsers, GetUser, CreateUser, UpdateUser, DeleteUser.
- Use `context.Context` from `c.Request.Context()` everywhere.
Output: full file tree with go.mod (pinned modules), Makefile,
Dockerfile (distroless static).
```

Resource pass:
```
For resource <X> given the model in internal/model/<x>.go:
- Generate handler in internal/handler/<x>.go with Gin.
- Request struct with `binding:"required,..."` tags.
- Service interface in internal/service/<x>.go.
- Table-driven test in internal/handler/<x>_test.go using
  httptest.NewRecorder + gin.CreateTestContext.
- No globals; constructor injection only.
- All errors wrapped with fmt.Errorf("...: %w", err).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go` toolchain | Build / test / vet | https://go.dev/dl/ |
| `staticcheck` | Linter beyond `go vet` | `go install honnef.co/go/tools/cmd/staticcheck@latest` |
| `golangci-lint` | Aggregate linter (govet, staticcheck, gosec, errcheck, ...) | https://golangci-lint.run |
| `gosec` | Security scanner for Go | `go install github.com/securego/gosec/v2/cmd/gosec@latest` |
| `air` | Live-reload during dev | `go install github.com/cosmtrek/air@latest` |
| `delve` (`dlv`) | Debugger | `go install github.com/go-delve/delve/cmd/dlv@latest` |
| `pprof` | Profiling (CPU, heap, goroutine) | bundled with Go |
| `oapi-codegen` | Generate Echo/Gin handlers from OpenAPI | https://github.com/oapi-codegen/oapi-codegen |
| `wire` (Google) | Compile-time DI | https://github.com/google/wire |
| `httpie` / `xh` / `curl` | API smoke tests | https://github.com/ducaale/xh |
| `vegeta` | Load testing | `go install github.com/tsenart/vegeta/v12@latest` |
| `grype` / `trivy` | Image vulnerability scanning | https://github.com/anchore/grype |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Gin | OSS framework | yes | Most common LLM-trained option; large middleware ecosystem. |
| Echo | OSS framework | yes | Cleaner middleware API; first-party Prometheus, OpenAPI plugins. |
| chi | OSS router | yes | Stdlib-compatible; preferred when avoiding "framework lock-in." |
| huma | OSS framework | yes | OpenAPI-first; agents love spec-driven generation. |
| Fiber | OSS (`fasthttp`) | partial | Faster on synthetic benches; not net/http-compatible — middleware ecosystem fragments. |
| OpenTelemetry SDK (Go) | OSS | yes | Auto-instrumentation for Gin and Echo; vendor-neutral telemetry. |
| Sentry / Honeycomb / Datadog | SaaS APM | yes (SDK) | Drop-in Go SDKs; a few dozen lines in middleware. |
| Render / Fly.io / Railway / Hetzner | PaaS / IaaS | yes (CLI) | All deploy a static-binary Dockerfile in one step. |
| Caddy / Nginx | OSS reverse proxy | yes | Front the Go service; Caddy automates TLS. |
| Vault / SOPS / Doppler | SaaS / OSS secrets | yes | Inject DB / JWT secrets at boot; prefer over `.env`. |

## Templates & scripts

The README ships Gin and Echo router skeletons. Missing for agents: a graceful shutdown wrapper that the README skips. Inline drop-in (≤50 lines):

```go
// internal/server/server.go
package server

import (
	"context"
	"errors"
	"net/http"
	"os/signal"
	"syscall"
	"time"

	"go.uber.org/zap"
)

// Run starts srv and blocks until SIGINT/SIGTERM, then drains for `grace`.
func Run(srv *http.Server, grace time.Duration, log *zap.Logger) error {
	ctx, stop := signal.NotifyContext(context.Background(),
		syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	errCh := make(chan error, 1)
	go func() {
		log.Info("listen", zap.String("addr", srv.Addr))
		if err := srv.ListenAndServe(); err != nil &&
			!errors.Is(err, http.ErrServerClosed) {
			errCh <- err
		}
	}()

	select {
	case err := <-errCh:
		return err
	case <-ctx.Done():
		log.Info("shutdown signal received")
	}

	shutCtx, cancel := context.WithTimeout(context.Background(), grace)
	defer cancel()
	if err := srv.Shutdown(shutCtx); err != nil {
		return err
	}
	log.Info("shutdown complete")
	return nil
}
```

Wire from `main.go`:
```go
srv := &http.Server{Addr: ":8080", Handler: r, ReadHeaderTimeout: 5 * time.Second}
if err := server.Run(srv, 15*time.Second, log); err != nil { log.Fatal(err.Error()) }
```

## Best practices
- **Always set timeouts on `http.Server`.** `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`. Default zero values are slow-loris-friendly.
- **Use `c.Request.Context()` everywhere.** Pass it down to services, repos, DB. Cancel-on-disconnect propagates and saves goroutines.
- **Wrap errors with `%w`.** `fmt.Errorf("create user %s: %w", id, err)`. Use `errors.Is/As` upstream. Never log + return; pick one.
- **One handler per file** for resources >5 endpoints; otherwise grouping by resource is fine.
- **Keep handlers thin.** Bind → call service → translate to HTTP. No business logic in handler files.
- **Validate in the request struct, not in the handler body.** Use `binding:"required,email,..."` (Gin) or a centralized validator (Echo) — never `if req.Email == ""`.
- **Structured logging only.** `zap` or `slog`; include `request_id`, `user_id`, `route`, `latency_ms`. Plain `fmt.Println` is banned.
- **`/healthz` (liveness) ≠ `/readyz` (readiness).** Liveness should never check downstream dependencies; readiness must.
- **Build distroless static images.** `CGO_ENABLED=0` + `gcr.io/distroless/static-debian12` keeps containers <20 MB and CVE-free.
- **`pprof` behind a separate listener** on `127.0.0.1:6060` — never expose on the public router.
- **Recovery middleware first, logger second, request-ID even earlier** so panics are logged with the correct request.
- **No background goroutines tied to request context.** If you need fire-and-forget, derive from `context.Background()` with an explicit timeout, and log + recover inside.

## AI-agent gotchas
- **Implicit middleware order.** Agents trained on Gin "Hello World" emit `r := gin.Default()` (which already includes Logger + Recovery), then add `r.Use(middleware.Logger())` again — duplicates logs. Reject `gin.Default()`; use `gin.New()` and explicit middleware.
- **`gin.H` vs typed responses.** Agents return `gin.H{"data": ...}` everywhere; lose static typing. Force typed response structs.
- **Mixing Echo v4 and v5 imports.** Module-aware go.sum will pin one; the agent's import path must match. Verify before generation.
- **Hardcoded `:8080`.** Agents inline ports / DB URLs; force `os.Getenv` or a `config` package.
- **Forgetting Recovery.** A panic kills the process; agents skip Recovery in "minimal" examples. Mandate it in middleware list.
- **`context.Background()` in handlers.** Agents create background contexts inside handlers, breaking cancellation. Lint for `context.Background()` outside `main` and tests.
- **Goroutine leaks via `c.Request.Context()` after return.** A `go func() { db.Query(c.Request.Context(), ...) }()` panics; agents do this often. Reviewer must flag.
- **Validator messages exposed raw.** Agents do `c.JSON(400, gin.H{"error": err.Error()})` — leaks struct field names and tag rules. Wrap in a translator.
- **CORS wildcard.** Default LLM output is `AllowOrigins: ["*"], AllowCredentials: true` — invalid combo at the browser. Use specific origins.
- **JWT signing key.** Agents hard-code `[]byte("secret")` as in the Echo example; reject anything < 32 bytes and prefer RS256 with a key file or KMS.
- **`for _, x := range slice { go func() { use(x) } }`** — pre-Go 1.22 captures by ref; agents trained on older code reproduce the bug. Confirm Go version and either use 1.22+ semantics or the explicit shadowed-var pattern.
- **`json:"-"` on password fields forgotten.** Agents return user models directly with hashed passwords inside; require a Response DTO for every model.
- **Shutdown swallowed.** Agents call `srv.Shutdown(ctx)` but exit without waiting; container kills mid-request. Reviewer must verify.
- **Hand-rolled rate-limit.** Agents implement IP-keyed maps without TTL — memory leak. Use `uber-go/ratelimit` or `httprate` (chi).

## References
- Gin Web Framework. https://gin-gonic.com/docs/
- Echo Web Framework. https://echo.labstack.com
- Go `net/http` (1.22 mux). https://pkg.go.dev/net/http#ServeMux
- "How I write HTTP services in Go" — Mat Ryer. https://grafana.com/blog/2024/02/09/how-i-write-http-services-in-go-after-13-years/
- `go-playground/validator/v10`. https://github.com/go-playground/validator
- "Effective Go." https://go.dev/doc/effective_go
- OpenTelemetry Go SDK. https://opentelemetry.io/docs/instrumentation/go/
- gosec. https://github.com/securego/gosec
- Sibling methodologies in this repo: `free/dev/software-developer/go-backend/`, `free/dev/software-developer/go-error-handling/`, `free/dev/software-developer/go-concurrency/`.
