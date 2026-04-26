# Agent Integration — Ruby Sidekiq Jobs

## When to use
- Rails apps that need background processing (mailers, webhooks, third-party API calls, image/video pipelines).
- High-throughput job execution (Sidekiq's threaded model handles 10x the throughput of forking workers like Resque on the same box).
- Scheduled / cron-style jobs via `sidekiq-cron` or `sidekiq-scheduler`.
- Workflows with batches, callbacks, and unique-job semantics (Sidekiq Pro/Enterprise) — or `sidekiq-unique-jobs` for OSS.
- When Redis is already part of the stack (cache, ActionCable backend) — no new infra dep.

## When NOT to use
- Single-threaded code that mutates global state — Sidekiq runs N jobs concurrently per process and will trigger races.
- Low-volume one-shot tasks where Rails 8's Solid Queue / `ActiveJob` with the async adapter is enough.
- When you cannot run a long-lived worker process (serverless without persistent compute) — choose a queue-as-a-service (e.g. SQS + an ECS task) instead.
- Jobs that must persist beyond Redis durability constraints — Redis without AOF/RDB tuning loses jobs on crash. Consider GoodJob (Postgres-backed) or Solid Queue.
- Strict FIFO requirements per partition — Sidekiq is best-effort ordering.

## Where it fails / limitations
- Jobs are NOT guaranteed exactly-once. Network blips during ack cause re-execution. Code must be idempotent.
- Argument serialization: only JSON-safe primitives. Passing an `ActiveRecord` object serializes via GlobalID and re-fetches on the worker → fails if the row was deleted.
- A worker crash during `perform` without proper retry config drops the job to the Dead set after 25 retries (~21 days). If you raise non-retryable errors silently, jobs vanish.
- Memory bloat — long-running workers leak; rely on `sidekiq` `--max-memory` or `puma_worker_killer`-style restarts.
- Poison-pill jobs (raising every retry) consume queue slots forever unless you use `sidekiq_options retry: false` for known fatal errors.
- Default Sidekiq dashboard exposes job arguments — secrets in args (API keys, tokens) leak to anyone with dashboard access.

## Agentic workflow
A subagent generates the job class with explicit `sidekiq_options` (queue, retry policy, dead set), an idempotency check at the top of `perform`, and an RSpec test using `Sidekiq::Testing.inline!` (or `fake!` + `Sidekiq::Worker.drain`). The agent must also wire `app/jobs/application_job.rb` if missing, register the queue in `config/sidekiq.yml`, and confirm the worker process is supervised. Quality gates: `bundle exec rspec`, `bundle exec rubocop`, `bundle exec brakeman` for security on any newly serialized arguments.

### Recommended subagents
- `faion-feature-executor` — sequential implementation per slice (job + test + queue config + dispatcher).
- `faion-sdd-executor-agent` — runs RSpec / RuboCop / Brakeman as quality gates.

### Prompt pattern
```
Create a Sidekiq job <Name>Job that <action>. sidekiq_options queue: :<name>, retry: 3, dead: true. Pass primitive ids only. Inside perform: short-circuit if already processed, wrap external calls with timeouts, capture and re-raise non-fatal errors so retry can fire. Add RSpec spec asserting enqueue + execution under Sidekiq::Testing.inline!. Update config/sidekiq.yml.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bundle exec sidekiq` | Worker daemon | `gem 'sidekiq'`; https://github.com/sidekiq/sidekiq |
| `sidekiqctl quiet|stop` | Graceful shutdown helpers | Bundled |
| `bundle exec rake sidekiq:install` (custom) | Wire defaults | Project-specific |
| Mission Control – Jobs | Rails 8 dashboard | https://github.com/rails/mission_control-jobs |
| `redis-cli` | Inspect queues, retry/dead sets directly | `apt install redis-tools` |
| `rails console` | Push jobs ad-hoc, drain in tests | Built-in |
| `bundle exec rspec` / `minitest` | Tests | Built-in |
| `rubocop`, `brakeman`, `bundle audit` | Lint / security | gems |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sidekiq Pro / Enterprise | Commercial | Yes | Adds batches, unique jobs, rate limiting, encryption-at-rest. |
| Redis / Valkey / Upstash / Redis Cloud | OSS / SaaS | Yes | Sidekiq backing store. Already on faion-net (port 6379). |
| GoodJob | OSS | Yes | Postgres-backed alternative; durable jobs without Redis. |
| Solid Queue (Rails 8 default) | OSS | Yes | DB-backed Active Job adapter; simpler when Redis isn't desired. |
| Honeybadger / Sentry / Bugsnag | SaaS | Yes | Built-in Sidekiq middleware captures failures + payload. |
| sidekiq-cron / sidekiq-scheduler | OSS | Yes | Cron-style scheduling on top of Sidekiq. |
| sidekiq-unique-jobs | OSS | Yes | Lock-based dedupe for OSS users. |
| Datadog / New Relic Ruby APM | SaaS | Yes | Auto-traces job duration, queue latency. |

## Templates & scripts
See templates.md and README (Job Structure, Batch Processing). Sample `config/sidekiq.yml`:

```yaml
:concurrency: 10
:max_retries: 5
:queues:
  - [critical, 4]
  - [default, 2]
  - [notifications, 2]
  - [exports, 1]
production:
  :concurrency: 25
```

Sample systemd unit:

```ini
[Service]
Type=simple
WorkingDirectory=/var/www/app/current
ExecStart=/usr/local/bin/bundle exec sidekiq -e production -C config/sidekiq.yml
Restart=always
KillSignal=SIGTERM
TimeoutStopSec=30
User=deploy
```

## Best practices
- Pass IDs only into `perform`. Reload AR objects inside the job with explicit `find_by` and short-circuit if missing.
- Make every job idempotent: check `already_done?` first; use a unique key + Redis `SET NX EX` for in-flight dedupe if needed.
- Set per-queue priorities in `sidekiq.yml`; never run all queues at the same weight.
- Use `Sidekiq::Job#sidekiq_options retry: 3` (or fewer) for jobs that interact with external systems; pair with `sidekiq_retry_in` for deterministic backoff.
- Configure Sidekiq middleware to capture errors with Sentry/Honeybadger before re-raise, so the dashboard's Dead set isn't your only signal.
- Protect the dashboard: `mount Sidekiq::Web => '/sidekiq', constraints: AdminConstraint`. Never expose unauthenticated.
- Use `wait` carefully — `perform_in(10.minutes, …)` consumes Redis memory linearly; for very long delays, prefer cron + DB state.
- Restart workers on deploy. With Capistrano: `sidekiqctl quiet && sleep <timeout> && systemctl restart sidekiq`.

## AI-agent gotchas
- Agents pass full ActiveRecord objects (or hashes containing them). They serialize via GlobalID and re-fetch — works in tests, breaks in prod when the record was deleted between enqueue and run. Force IDs only.
- The agent may use `perform_async(job_args)` inside an AR transaction; the worker picks it up before the transaction commits and finds no row. Use `after_commit :enqueue_job, on: :create` or wrap in `ActiveRecord::Base.transaction { … }` followed by `perform_later`.
- `sidekiq_options retry: false` discards on first failure — agents add it "to keep things simple" and you lose data. Default to `retry: 3-5` and dead-set capture.
- `Sidekiq::Testing.inline!` masks ordering bugs; supplement with `fake!` + manual `drain` to test enqueue order.
- Argument leakage: agents log `params.inspect` inside jobs that include API keys. Strip secrets before logging; consider Sidekiq Pro encryption.
- Human checkpoint: review the chosen `queue:` name + concurrency in `sidekiq.yml`. Agents add new queues but forget to register them and the jobs sit silently in Redis.
- Long-running jobs (>30s) — agents don't add `Sidekiq.options[:timeout]` or break the work into chunks. Force batching for any job that processes >1000 records.

## References
- https://github.com/sidekiq/sidekiq/wiki
- https://www.mikeperham.com (Sidekiq author's blog — many "do this, not that" posts)
- https://github.com/mhenrixon/sidekiq-unique-jobs
- https://github.com/bensheldon/good_job (alternative)
- https://guides.rubyonrails.org/active_job_basics.html
