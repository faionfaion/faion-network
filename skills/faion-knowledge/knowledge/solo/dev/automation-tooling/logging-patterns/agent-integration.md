# Agent Integration — Logging Patterns

## When to use
- Standing up a new service that will hit production: structured JSON from day one.
- Migrating from `print()` / `console.log` to a real logger before observability rollout.
- Adding correlation IDs to a multi-service flow so a single trace can be reconstructed.
- Compliance domains needing audit trails (who did what, when, with what payload hash).
- Debugging async/concurrent code where order of execution is non-trivial.

## When NOT to use
- One-off CLI scripts where stderr/stdout suffices.
- Hot loops (>1M iterations/sec) — even structured logging is too slow; use sampling or metrics counters.
- Replacing tracing — logs answer "what happened", traces answer "how long and where". Use both.
- High-PII contexts without scrubbing infra in place — better to not log than to leak.

## Where it fails / limitations
- Logger config drift between dev/prod (text vs JSON) means dev logs look different and devs don't trust prod format.
- Python `logging` is global mutable state — multiple `dictConfig` calls clobber each other; agents iterating on configs hit this.
- structlog `contextvars` lost across `asyncio.create_task` boundaries unless explicitly propagated.
- Sampling sensitive log lines for cost reasons drops the one line you needed during an incident.
- Forwarders (Vector, Fluent Bit) parse-fail on multi-line tracebacks unless `multiline.parser` is configured.
- Log-volume cost in Datadog/New Relic balloons silently; one DEBUG-in-prod incident costs $5k.

## Agentic workflow
A logging agent: scans repo for `print`/`console.log` (`ruff T20`, `eslint no-console`), proposes replacements with a chosen logger, adds context binding (request_id, user_id), and ensures a single config module is the source of truth. For new services, it reads `templates.md` and emits a `logging.py` / `logger.ts` module. For incident replay, an agent can pull JSON logs by `request_id` and reconstruct a timeline. `faion-sdd-executor-agent` enforces the "no print" gate.

### Recommended subagents
- `faion-sdd-executor-agent` — quality gate including `ruff check . --select T20` and ESLint `no-console`.
- `password-scrubber-agent` — scans logs/code for accidental secret prints before commit.

### Prompt pattern
```
Convert <module> to use structured logging:
- Replace print/console.log with logger.<level>("event_name", **context).
- Add request_id + user_id from contextvars (Python) / AsyncLocalStorage (Node).
- Levels: DEBUG=internal, INFO=lifecycle, WARN=recoverable, ERROR=user-visible failure.
- NEVER log password, token, secret, authorization headers, raw card numbers.
- Show diff first, wait for approval, then apply.
```

```
Reconstruct timeline for request_id=<id> from logs.json (last 1h).
Output: chronological table <ts | service | level | event | context_keys>.
Highlight any ERROR/WARN and the 3 INFO events preceding them.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Slice JSON logs at the shell | `apt install jq` |
| `lnav` | TUI log navigator with SQL queries | `apt install lnav` |
| `gron` | Make JSON greppable | `brew install gron` |
| `vector` | High-perf log shipper/transformer | `cargo install vector` |
| `fluent-bit` | Lightweight forwarder for K8s | https://fluentbit.io/ |
| `stern` | Multi-pod K8s log tailer | `brew install stern` |
| `humanlog` | Pretty-print JSON logs in dev | `go install github.com/humanlogio/humanlog/cmd/humanlog@latest` |
| `pino-pretty` | Node's pino dev formatter | `npm i -D pino-pretty` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog Logs | SaaS | Yes — REST + log API | Fastest agent-driven search; cost ramps fast. |
| Grafana Loki | OSS | Yes — LogQL via API | Cheap, label-based; pair with Grafana. |
| Better Stack (Logtail) | SaaS | Yes — REST | Solo-friendly pricing. |
| Axiom | SaaS | Yes — APL queries | Cheap retention, AI-friendly query API. |
| AWS CloudWatch Logs Insights | SaaS | Yes — query API | Default for AWS workloads. |
| Elastic / OpenSearch | OSS | Yes — REST | Heavy ops; powerful ad-hoc. |
| Sentry | SaaS | Yes — SDK + API | Great for ERROR-level; not a log store. |
| OpenTelemetry Logs | OSS spec | Yes | Future-proof shipping path. |

## Services & apps — agent recipes
- Datadog: `dogapi search-events --query 'service:web request_id:abc123'` → JSON timeline.
- Loki: `logcli query '{service="web"} | json | request_id="abc123"'`.
- Axiom: `axiom query "['logs'] | where request_id == 'abc123' | sort by _time"`.

## Templates & scripts
See `templates.md` for full Python/structlog and Node/pino starters. Pre-commit guard against `print` (Python) + `console.log` (TS):

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--select, T20, --fix]
  - repo: local
    hooks:
      - id: no-console-log
        name: no console.log in src
        entry: bash -c '! grep -RIn "console\.log" src/'
        language: system
        files: \.(ts|tsx|js|jsx)$
```

## Best practices
- One config file (`logging_config.py` / `logger.ts`) imported everywhere; never call `getLogger` configuration inline.
- Use event names like `user.login.failed`, not free-text English. Enables grep + dashboards without regex.
- Always include request_id, user_id, tenant_id (when applicable) on every log line via context-vars.
- Redact list as a constant: `password|token|secret|authorization|set-cookie|card_number|cvv` — apply in formatter, not at call site.
- Sample DEBUG in prod (1%); never sample ERROR/WARN.
- Tag environment, service, version on every line — ops will need them.
- Prefer logger.exception (Python) / `err` field (pino) so stack traces are structured, not stringified.

## AI-agent gotchas
- LLMs love `f"{user}"` format strings — they bypass structured logging. Force `logger.info("event", user_id=user.id)`.
- Agents log full request/response bodies "for debugging" — costs explode and PII leaks. Set max-payload-size in formatter.
- Auth headers in `requests.headers` get logged when an agent dumps `dict(req)`. Add a header allowlist.
- Async context loss: agents add `asyncio.create_task(work())` without `copy_context()` — request_id disappears mid-flow.
- Multi-line tracebacks break Loki/Vector parsers if not collapsed; an agent's "just print the exception" creates 50 unrelated log entries.
- Human-in-loop checkpoint: review the redact-list and log-level-per-module map before merging the logging config; once in prod, retrofitting is painful.
- `password-scrubber-agent` should run on every PR touching logger config or formatters.

## References
- 12-Factor App, Logs — https://12factor.net/logs
- structlog docs — https://www.structlog.org/
- pino docs — https://getpino.io/
- OpenTelemetry Logs Data Model — https://opentelemetry.io/docs/specs/otel/logs/data-model/
- "Logs and Metrics" — Cindy Sridharan, Distributed Systems Observability (O'Reilly).
- Sibling: `feature-flags/` (log flag state) and `perf-test-tools/` (log perf metrics together).
