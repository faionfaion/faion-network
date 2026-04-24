# Agent Integration — Sidekiq Background Jobs

## When to use
- Rails application that needs durable async work: emails, webhooks, file processing, third-party API fan-out, scheduled cleanups.
- Bulk processing via `Sidekiq::Batch` (Pro/Enterprise) or `find_each` chunking with per-chunk jobs.
- Reliable retry/backoff for flaky external integrations (payment gateways, email providers).
- Cron-like scheduling via `sidekiq-cron` or `sidekiq-scheduler`.

## When NOT to use
- Sub-second latency requirements between user action and effect — Sidekiq's pickup latency is typically 50-500ms even idle.
- Cross-language consumers — payload is JSON but conventions are Ruby-specific (constantize class names).
- Strict global ordering — Sidekiq is parallel by design; use a single-thread queue + lock or a different broker (Kafka with partition keys).
- Workloads needing exactly-once — Sidekiq is at-least-once; design for idempotency.

## Where it fails / limitations
- Memory-bound workers leak over time; use `MAX_THREADS` + `MAX_MEMORY_MB` + restart hooks (`sidekiq-worker-killer`).
- `sidekiq_options retry: true` defaults to 25 retries over ~21 days — rarely what you want for user-facing jobs. Set explicit `retry: 3` or `retry: 5`.
- Dead-letter queue (`dead`) is bounded (10k jobs / 6 months by default) — silent loss past that.
- Argument serialization is JSON, not Marshal — `ActiveRecord::Base` instances are coerced to GlobalID strings; arbitrary objects break.
- `perform_in` / `perform_at` with timestamps in the past run immediately, not "never" — common bug.
- `Sidekiq::Cron` jobs share global Redis — multi-tenant apps need namespaced keys.
- Long jobs blocking a thread starve the rest of the queue; split with `find_each` + re-enqueue.

## Agentic workflow
A coding subagent should: (1) generate the job class with `include Sidekiq::Job`, explicit `sidekiq_options queue: …, retry: N, dead: true`, custom `sidekiq_retry_in` for known transient errors, (2) parameterize on IDs not records, (3) implement idempotency check (`return if record.processed?`), (4) handle `ActiveRecord::RecordNotFound` for deleted records, (5) write a request spec using `Sidekiq::Testing.fake!` for dispatch and `inline!` for end-to-end, (6) add the job to the appropriate `config/sidekiq.yml` queue weighting. Pause for human review before: changing retry/dead settings on existing jobs, modifying `Sidekiq::Cron` schedules, or touching `failed`/`dead` queues in production.

### Recommended subagents
- `general-purpose` Claude subagent — job class generation + dispatch site updates.
- Code-review subagent (Sonnet) — flags missing idempotency, naive retry, full-record arguments, swallowed exceptions.

### Prompt pattern
```
Create app/jobs/process_order_job.rb: includes Sidekiq::Job, sidekiq_options queue: :default, retry: 3, dead: true, custom sidekiq_retry_in (linear 60s for PaymentGatewayError, exponential for others). perform(order_id): find Order, return if order.processed?, OrderProcessor.new(order).process!, enqueue NotifyCustomerJob. Rescue ActiveRecord::RecordNotFound (log and return), let other exceptions propagate. Add spec/jobs/process_order_job_spec.rb with Sidekiq::Testing.fake! covering enqueue + retry behavior.
```
```
Refactor BatchExportJob to chunk by 1000 IDs: parent job ExportInitJob enqueues N ExportChunkJob, each writes to S3 with chunk_index, ExportFinalizerJob composes when all done. Use Sidekiq::Batch (assume Pro license). Track Export#status across batch lifecycle hooks.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bundle exec sidekiq -C config/sidekiq.yml` | Run worker | gem `sidekiq` |
| `bundle exec sidekiq-monitor` | TUI for queues (community) | gem `sidekiq-monitor` |
| `redis-cli MONITOR` | See raw job push/pop in dev | redis-tools |
| `bundle exec rake sidekiq:stats` | Quick CLI stats (custom rake) | manual |
| `bundle exec sidekiqmon` | Built-in console monitor | bundled with Sidekiq 7+ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sidekiq Web UI | OSS | Yes | Mount at `/sidekiq` (auth-protected); JSON via `Sidekiq::Stats` API |
| Sidekiq Pro / Enterprise | Commercial | Yes | Batches, super-fetch (lossless), unique jobs, periodic jobs |
| Redis (Valkey) | OSS | Yes | Required broker; size for `5 KB × max_jobs_in_flight` |
| Sentry / Rollbar / Honeybadger | SaaS | Yes | `Sidekiq.configure_server { |c| c.error_handlers << ... }` |
| Datadog APM | SaaS | Yes | `dd-trace-rb` auto-instruments Sidekiq jobs |
| sidekiq-cron / sidekiq-scheduler | OSS | Yes | Cron-style recurring jobs without Sidekiq Enterprise |
| sidekiq-unique-jobs | OSS | Caution | Adds dedupe; complex semantics, easy to mis-configure |

## Templates & scripts
See `templates.md` for job and batch examples. Inline `config/sidekiq.yml` for sane defaults the agent should ensure exists:

```yaml
:concurrency: 10
:timeout: 25
:queues:
  - [critical, 6]
  - [default, 3]
  - [notifications, 2]
  - [low, 1]
:max_retries: 3
:dead_max_jobs: 10000
:dead_timeout_in_seconds: 15552000  # 180 days
production:
  :concurrency: 25
```

Inline systemd service for production:
```ini
[Unit]
Description=sidekiq
After=syslog.target network.target

[Service]
Type=notify
WatchdogSec=10
User=deploy
WorkingDirectory=/var/www/app/current
ExecStart=/usr/local/bin/bundle exec sidekiq -e production -C config/sidekiq.yml
ExecReload=/bin/kill -TSTP $MAINPID
Restart=always
RestartSec=1
KillMode=mixed
TimeoutStopSec=60

[Install]
WantedBy=multi-user.target
```

## Best practices
- Every job must be idempotent. Treat retries as the default, not the exception.
- Pass IDs, not records. Re-fetch in `perform`.
- Set explicit `retry:` and `dead: true` on every job. Default 25 retries is rarely correct.
- Wrap external API calls with circuit breakers (`stoplight`, `circuitbox`) — Sidekiq retry alone is not enough during outages.
- Custom `sidekiq_retry_in` per-exception for cleaner retry curves (linear for rate-limit, exponential for transient).
- Use `Sidekiq::Limiter` (Enterprise) or `sidekiq-rate-limiter` for third-party rate limits.
- Set `Sidekiq.strict_args!(true)` in initializer — fails loudly on non-JSON-serializable args.
- Keep job classes thin: `perform` calls a service object that holds the logic and is unit-testable without Sidekiq.

## AI-agent gotchas
- LLM passes ActiveRecord objects as job args — Sidekiq 7 raises in strict mode but legacy code silently `marshal_dumps`. Force ID-only.
- Agent forgets `sidekiq_options retry:` and `dead:` → defaults to 25 retries silently. Make required in prompt.
- Generated specs use `perform_now` (ActiveJob) instead of `Sidekiq::Testing.inline!` — semantics differ for retries. Use Sidekiq's testing module directly.
- LLM swallows `StandardError` in `perform` to "be safe" — defeats retry. Mandate: only rescue `RecordNotFound` (log + return) and known transients (re-raise after annotation).
- Confusing ActiveJob API (`perform_later`, queue_as) with native Sidekiq API (`perform_async`, `sidekiq_options queue:`). Pick one per project; native is recommended for non-trivial Sidekiq use.
- `WithoutOverlapping` is Laravel terminology — Sidekiq equivalent is `sidekiq-unique-jobs` `lock: :until_executed` or hand-rolled Redis locks. Don't let LLM cargo-cult the API.
- Human checkpoint: any change to retry/dead/queue weights, any clearing of `Sidekiq::DeadSet`, any removal of cron entries.

## References
- https://github.com/sidekiq/sidekiq/wiki
- https://github.com/sidekiq/sidekiq/wiki/Best-Practices
- https://github.com/sidekiq/sidekiq/wiki/Error-Handling
- https://github.com/sidekiq/sidekiq/wiki/Pro
- "Working with Ruby Threads" — Jesse Storimer (concurrency primer)
- https://github.com/mperham/connection_pool
