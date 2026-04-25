# Agent Integration — Logging Patterns

## When to use
- New service or module: agent scaffolds a structured-logging baseline (JSON formatter, contextvars, request middleware) before any business logic ships.
- Refactor of legacy `print` / `console.log` / `fmt.Println` debris into structured logs.
- Adding distributed tracing: pair `trace_id` / `request_id` injection across services so logs join with spans.
- Compliance/audit (SOC2, HIPAA, PCI): structured logs with retention policy + PII redaction.
- Onboarding a log aggregator (Loki, ELK, Datadog, CloudWatch): agents map fields to indices and dashboards.
- After a P1 incident: postmortems revealing missing logs become input for an agent that proposes new log calls and levels.
- Cost reduction: agents identify high-volume, low-value log lines and propose level downgrades or sampling.

## When NOT to use
- Tiny throwaway scripts where stderr suffices.
- Hot paths where logging cost is measurable (per-row inside a 100k iteration loop) — sample or move to metrics.
- Security-sensitive code paths where any log line is a leak risk (raw payloads, secrets) — emit metric counters instead.
- Real-time / latency-critical signal paths (audio, video, trading) — buffered async logging only; never block.

## Where it fails / limitations
- **Structured-but-not-really:** teams emit JSON with one giant `message` field that contains a sprintf'd English sentence; defeats query.
- **Context loss across async boundaries:** Python `contextvars` work for asyncio; thread pools / Celery workers / FastAPI background tasks lose the request_id silently.
- **Level abuse:** everything logged at INFO; or warnings used for routine events. Alerting becomes noise → ignored.
- **PII / secret leakage:** README mentions "no sensitive info" but does not provide a redaction pipeline. JWTs, emails, tokens, full user objects end up in logs.
- **Unbounded cardinality:** `user_id`, `request_id` as labels in metrics-friendly log indexers (Loki, Splunk) blow up costs. Methodology doesn't warn.
- **Cost blindness:** retention defaults to 30/90 days; no per-environment policy in templates.
- **Local vs production formatter drift:** dev sees pretty stdout, prod gets JSON — but configs differ in ways nobody reviews.
- **Error logs without `exc_info`:** agents emit `logger.error("oops")` with no traceback; useless during incident.
- **Multi-language consistency:** Python uses `structlog`, Go uses `zerolog`, Node uses `pino`. Without a shared field convention, joining logs across services is painful.

## Agentic workflow
Drive logging hygiene as a four-pass agent flow: (1) **bootstrap agent** generates the structured-logging config (formatter, contextvars, middleware) per language using `templates.md`; (2) **migrator agent** finds `print` / `fmt.Println` / `console.log` and rewrites to `logger.<level>(...)` with proper kwargs; (3) **redactor agent** wraps log calls with a PII filter (auto-mask emails, tokens, card numbers, JWT) before they hit handlers; (4) **noise reducer agent** runs weekly against aggregator data, identifies log lines whose volume:value ratio is bad, and proposes level downgrades or sampling. Persist a `docs/logging.md` field convention (must include `service`, `env`, `version`, `request_id`, `trace_id`, `user_id_hash`, `event`).

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts logging-migration work into SDD tasks (one task per service, one per logger module).
- A **PII-redactor agent** (purpose-built, worth creating): regex + LLM pass that wraps log records before serialization; ships a denylist + allowlist.
- A **field-convention enforcer agent**: reads project conventions; flags any new log call missing required keys (`event`, `service`, `request_id`).
- A **noise-reduction agent**: queries Loki/Datadog/Splunk via API for top-N log lines by volume, scores them, proposes downgrade/drop.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — last-mile scrub of log files before they leave the network (e.g., into a bug report).

### Prompt pattern
Bootstrap (Python):
```
Generate a Python logging baseline for service "<name>" using
structlog. Requirements from
solo/dev/software-developer/logging-patterns/README.md:
- JSON output in production, key=value pretty in dev.
- contextvars for request_id, trace_id, user_id_hash.
- FastAPI middleware that binds those at request start, unbinds at end.
- Auto-mask PII (email, phone, JWT, card number) before render.
- Log level configurable via env (LOG_LEVEL).
Output: logging.py + middleware.py + sample handler showing usage.
```

Migration:
```
Read <PR diff>. Replace any print/fmt.Println/console.log with the
project's structured logger:
- Pick correct level (DEBUG/INFO/WARNING/ERROR/CRITICAL) from the
  README's level guide.
- Convert string interpolation to keyword args (no f-strings inside
  log calls).
- Add exc_info=True for any error log inside an except block.
Output as a unified diff.
```

PII redaction check:
```
Given the following candidate log entries, identify any value that
might be PII or a secret (email, phone, full name, token, JWT,
SSN/EIN, credit-card-like). For each: field name, why it's risky,
and a safe replacement (hash, mask, drop). Output as table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `structlog` (Python) | Canonical structured logger; agent-friendly contextvars | `pip install structlog` |
| `pythonjsonlogger` | JSON formatter for stdlib logging | `pip install python-json-logger` |
| `loguru` | Alternative Python logger with simpler API | `pip install loguru` |
| `pino` (Node) | Fast JSON logger, default for NestJS/Fastify | `npm i pino` |
| `winston` (Node) | Multi-transport logger | `npm i winston` |
| `zerolog` / `zap` (Go) | High-performance Go structured loggers | https://github.com/rs/zerolog / https://github.com/uber-go/zap |
| `slog` (Go stdlib, 1.21+) | Built-in structured logging | https://pkg.go.dev/log/slog |
| `tracing` + `tracing-subscriber` (Rust) | Structured logs + spans | https://tracing.rs |
| `jq` | Local query of JSON log files | `apt install jq` |
| `lnav` | Log viewer that auto-parses JSON | https://lnav.org |
| `vector.dev` | Reshape, filter, redact, route logs at the edge | https://vector.dev |
| `fluent-bit` | Lightweight log shipper with redact filter | https://fluentbit.io |
| `logcli` (Loki) | Query Loki from agents | https://grafana.com/docs/loki/latest/tools/logcli/ |
| `claude` (Anthropic CLI) | Run migrator/redactor/noise-reducer headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana Loki + Promtail/Vector | OSS | yes | Cheapest log aggregator for solo teams; agent-callable via Loki HTTP API. |
| Elastic Stack (Elasticsearch + Kibana + Beats) | OSS / SaaS | yes | Full-text + structured; expensive at scale. |
| Datadog Logs | SaaS | API yes | Best UX, integrated with APM/traces; agent-driven via API + Terraform. |
| New Relic Logs | SaaS | API yes | Same niche; price-competitive. |
| Splunk Cloud / Enterprise | SaaS / self-host | API yes | Enterprise default; SPL queryable from agents. |
| AWS CloudWatch Logs + Logs Insights | SaaS | API yes | Default for AWS-heavy stacks. |
| GCP Cloud Logging | SaaS | API yes | Default for GCP. |
| Honeycomb | SaaS | API yes | Treats logs as wide events; great for high-cardinality fields. |
| Better Stack / Logtail | SaaS | API yes | Solo-priced; live-tail UX. |
| OpenTelemetry Logs | OSS spec | yes | Vendor-neutral; bridge from existing loggers. |
| Sentry (breadcrumbs) | SaaS | API yes | Pairs error events with last N log lines for context. |

## Templates & scripts

`templates.md` ships logging configurations for Python and FastAPI middleware. The gap is a runtime PII-redaction processor that an agent can drop into any structlog pipeline. Inline drop-in (≤50 lines):

```python
# logging_redact.py — structlog processor masking PII before JSON render.
# Add to processors before JSONRenderer:
#   structlog.configure(processors=[..., redact_pii, JSONRenderer()])
import re
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d\s().-]{8,}\d")
JWT   = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+")
CARD  = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
SECRETS = re.compile(r"(?i)\b(sk_live_[A-Za-z0-9]+|gh[pousr]_[A-Za-z0-9]{30,}|xox[bopars]-[A-Za-z0-9-]+)\b")
DENY_KEYS = {"password", "passwd", "pwd", "secret", "token", "api_key", "authorization", "ssn", "set-cookie", "cookie"}
def _mask(value: object) -> object:
    if isinstance(value, str):
        v = value
        v = EMAIL.sub("***@***", v)
        v = PHONE.sub("***-PHONE-***", v)
        v = JWT.sub("***JWT***", v)
        v = CARD.sub("***CARD***", v)
        v = SECRETS.sub("***SECRET***", v)
        return v
    if isinstance(value, dict):
        return {k: ("***" if k.lower() in DENY_KEYS else _mask(v)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(_mask(x) for x in value)
    return value
def redact_pii(_logger, _name, event_dict):
    return {k: ("***" if k.lower() in DENY_KEYS else _mask(v)) for k, v in event_dict.items()}
```
Equivalent processors exist for Go (`zerolog.HookFunc`) and Node (`pino` redact option). The redactor agent should propose project-specific rules to extend this baseline.

## Best practices
- One field convention per org: `service`, `env`, `version`, `request_id`, `trace_id`, `user_id_hash` (never raw user_id), `event` (snake_case noun-verb), plus domain fields. Lint it.
- Always pass kwargs, never f-strings inside log calls (`logger.info("user_signed_up", user_id=...)`, not `logger.info(f"User {id} signed up")`). Keeps cardinality controlled and indexable.
- DEBUG locally, INFO for business events, WARNING for recoverable degradations, ERROR for actionable failures, CRITICAL for "page on-call". No personal interpretation.
- Always `exc_info=True` (or equivalent) in error/critical paths — methodology shows the pattern; enforce it via lint.
- Log only the minimum needed for triage. If a sensitive value is required, hash it (`hashlib.sha256(user_id).hexdigest()[:12]`).
- Pair every alert with the exact log query that fires it; pair every dashboard panel with a single field convention.
- Sampling for high-volume INFO events: methodology omits this — add a counter every N events plus full sampling at WARNING+.
- Test logging like code: assert structured fields in unit tests when behavior depends on them (e.g., security audit events).
- Keep dev formatter close to prod (just `pretty=True`); avoid dual-format bugs where dev parses fine but prod doesn't.

## AI-agent gotchas
- LLMs default to f-strings inside log calls (cardinality bombs). Pin a rule that any `logger.X("…{…}…")` is rewritten to `logger.X("event", **kwargs)`.
- Agents drop `exc_info=True` constantly. Add a lint or PR check; otherwise debug context is gone forever.
- Agents add new fields without registering them; cardinality grows unbounded. Require any new log key to update `docs/logging.md` + the field schema.
- Agents propose logging full request bodies "for completeness." Block via redactor + size cap.
- Long async chains lose context — verify that the request_id appears in every log line of a single request via integration test.
- Agents reach for `loguru` or `winston` defaults that bypass project config. Pin the logger module path in CONVENTIONS.md.
- Human-in-loop checkpoints: (1) any change to the logging schema (downstream parsers may break), (2) any new field that could be PII, (3) sampling/dropping rules in production paths — these are all silent-failure prone.

## References
- 12-Factor App — Logs — https://12factor.net/logs
- structlog docs — https://www.structlog.org
- Go `slog` — https://pkg.go.dev/log/slog
- pino docs — https://getpino.io
- OpenTelemetry Logs — https://opentelemetry.io/docs/specs/otel/logs/
- Google SRE Workbook — Monitoring — https://sre.google/workbook/monitoring/
- Loki best practices — https://grafana.com/docs/loki/latest/best-practices/
- Datadog Log Cost Optimization — https://www.datadoghq.com/blog/log-cost-optimization/
- Charity Majors — Observability ≠ Logs — https://charity.wtf/2018/10/27/observability-a-3-year-retrospective/
- Local methodology: `logging-patterns/README.md`, `templates.md`, `examples.md`, `checklist.md`
