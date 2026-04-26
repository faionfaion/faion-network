# Agent Integration — Laravel Queues

## When to use
- Move slow IO (email, PDF rendering, third-party API calls, image processing) out of the request lifecycle.
- Fan-out work via `Bus::batch` for bulk imports/exports with progress tracking.
- Schedule retries with exponential backoff for flaky external services.
- Decouple webhooks: receive → push to queue → respond 200 immediately.

## When NOT to use
- Sub-millisecond pub/sub between services → use Redis pub/sub or NATS, not Laravel queues.
- Strict event ordering across many producers → Laravel `WithoutOverlapping` only serializes per-key on a single worker; use Kafka with partition keys.
- High-throughput streaming (>10k msg/s sustained) → reach for a real broker (RabbitMQ, SQS FIFO, Kafka) accessed directly, not through the Laravel `database` driver.
- Cross-language consumers — Laravel job payload is PHP-serialized; Python/Go workers cannot read it.

## Where it fails / limitations
- `database` driver is fine for low volume; switch to `redis` (Horizon) before ~50 jobs/s.
- `SerializesModels` re-fetches the model on `handle()` — if it was deleted, `ModelNotFoundException` fires unless you handle it. Pass IDs, not full models, for high-volume jobs.
- `WithoutOverlapping` lock release on crash relies on TTL; default 60s can let a duplicate run if worker is OOM-killed during a long job.
- `failed_jobs` table grows unbounded — must be pruned or it tanks `php artisan queue:retry`.
- Long-running jobs (>worker `--timeout`) are SIGTERMed mid-flight; idempotency required for retries.
- Horizon is Redis-only and not multi-tenant aware — multi-tenant apps need per-tenant queues + scoped supervisors.

## Agentic workflow
A coding subagent should: (1) generate the job class with explicit `$tries`, `$backoff`, `$timeout`, (2) decide between passing model vs ID — default to ID for jobs older than 5 minutes, (3) implement `failed()` for terminal-failure logging, (4) wire dispatch site to queue name, (5) write a feature test using `Bus::fake` and a unit test running `handle()` synchronously. For batches, scaffold `Bus::batch([...])->then()->catch()->finally()` plus a UI/route for batch progress polling. Pause for human review before changing global `failed_jobs` table or removing dead-letter handling.

### Recommended subagents
- `general-purpose` Claude subagent — job class scaffolding + dispatch site wiring.
- Code-review subagent (Sonnet) — verifies idempotency, retry policy, exception mapping in `failed()`.

### Prompt pattern
```
Create job ProcessOrderJob: implements ShouldQueue, $tries=3, $backoff=60, $timeout=120, queue 'orders', WithoutOverlapping($order->id), constructor takes Order $order via $orderId int (re-fetch in handle), handle() must be idempotent (check $order->isProcessed()), failed() updates status to 'failed' and logs to <error tracker>. Add Bus::fake test for dispatch + sync test for handle() retry behavior using Queue::assertPushed + actingAs.
```
```
Convert ExportUsersAction into a Bus::batch of ExportUsersJob chunks of 1000 user IDs. Track via $batch->id stored on Export model. Add ->then/->catch/->finally callbacks updating Export.status. Expose GET /exports/{id} returning Bus::findBatch(...) progress.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan queue:work --queue=high,default --tries=3 --max-time=3600` | Run worker (use `--max-time` to recycle workers) | bundled |
| `php artisan queue:listen` | Dev mode (reloads code per job) | bundled |
| `php artisan queue:failed` / `queue:retry {id\|all}` / `queue:flush` | Manage failed jobs | bundled |
| `php artisan horizon` / `horizon:status` / `horizon:terminate` | Redis-backed worker supervisor with metrics UI | https://laravel.com/docs/horizon |
| `php artisan queue:monitor orders,emails --max=100` | Alert when queue depth crosses threshold | bundled (10.x+) |
| `php artisan schedule:work` | Drives `dispatch()->everyMinute()` patterns locally | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Horizon | OSS | Yes | Dashboard at `/horizon`, metrics JSON endpoints |
| Redis (Valkey) | OSS | Yes | Production queue driver of choice |
| AWS SQS | SaaS | Yes (SDK) | Use FIFO for ordering; standard for cheap throughput |
| RabbitMQ | OSS | Yes (vyuldashev/laravel-queue-rabbitmq) | When you need exchanges/topics, not just queues |
| Laravel Pulse | OSS | Yes | Per-job duration percentiles, slow-job listing |
| Sentry / Bugsnag | SaaS | Yes | `failed()` hook → error tracker captures terminal failures |

## Templates & scripts
See `templates.md` for job, batch, and dispatch examples. Inline systemd unit the agent can drop into `/etc/systemd/system/laravel-worker@.service`:

```ini
[Unit]
Description=Laravel queue worker (%i)
After=network.target redis.service

[Service]
User=www-data
Group=www-data
Restart=always
RestartSec=3
ExecStart=/usr/bin/php /var/www/app/artisan queue:work redis \
  --queue=%i --sleep=3 --tries=3 --max-time=3600 --max-jobs=1000
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
Enable: `systemctl enable --now laravel-worker@orders laravel-worker@notifications`.

## Best practices
- Pass IDs, re-fetch in `handle()`. Saves payload size and avoids stale-model bugs.
- All jobs must be idempotent — assume at-least-once delivery.
- Set `--max-time` and `--max-jobs` on workers to bound memory leaks; let the supervisor restart.
- Use named queues per priority (`high`, `default`, `low`, `notifications`) and start workers with explicit `--queue=high,default` to enforce priority.
- `WithoutOverlapping` keys must include the resource ID, not just the class.
- For batches, persist `$batch->id` on the parent record so the UI can poll `Bus::findBatch($id)`.
- Cron `php artisan queue:prune-failed --hours=168` weekly. Cron `queue:prune-batches`.
- Never deploy without restarting workers (`queue:restart`) — old code keeps running.

## AI-agent gotchas
- LLM defaults to passing the full Eloquent model — fine for small tables, breaks for large or soft-deleted ones. Force ID-based dispatch in prompt.
- Agent often forgets `failed()` and `retryUntil()` — review must require both for production jobs.
- Generated tests use `Queue::push` directly, bypassing the dispatch chain. Use `Bus::fake()` + `Bus::assertDispatched(Job::class, fn ($j) => …)` instead.
- LLM may wrap job body in a try/catch that swallows exceptions — defeats retry. Let exceptions bubble; only catch what you intend to recover from.
- Horizon balancing strategies (`simple` vs `auto`) are usually wrong-defaulted by LLMs. `auto` requires `min`/`max` per queue or it starves low-traffic queues.
- Human-in-loop checkpoint: any job that mutates billing, sends external notifications, or calls a paid API must have explicit dedupe key and idempotency review before merge.
- LLM forgets that `dispatch_sync` exists for tests; mandate it in the test plan to keep determinism without `Queue::fake`.

## References
- https://laravel.com/docs/queues
- https://laravel.com/docs/horizon
- https://laravel.com/docs/queues#job-batching
- https://laravel.com/docs/queues#failed-jobs
- "The Twelve-Factor App: Concurrency" — https://12factor.net/concurrency
