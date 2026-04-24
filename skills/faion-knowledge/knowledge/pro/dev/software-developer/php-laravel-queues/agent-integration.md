# Agent Integration — Laravel Queues

## When to use
- Offload work that takes >200ms from HTTP requests (emails, PDF/CSV generation, third-party API calls, image processing).
- Fan-out operations where a single user action triggers many side-effects (e.g. notify N subscribers).
- Batch jobs (`Bus::batch`) for parallel processing of large datasets with then/catch/finally callbacks.
- Scheduled retries with exponential backoff for unreliable downstream APIs.
- Webhook processing where you must ack the sender quickly and process later.

## When NOT to use
- Hard real-time requirements (<1s end-to-end) — queue overhead and worker polling add latency.
- Workloads where the database write IS the result the user is waiting for.
- Single-host deployments without a daemonized worker (`php artisan queue:work` must run continuously).
- Jobs that depend on request-scoped state (auth user, session, request headers) — pass primitives only.
- When you have no Horizon/supervisor and no plan to monitor failed_jobs.

## Where it fails / limitations
- `SerializesModels` re-fetches Eloquent models at run time — if the model was deleted, the job fails on `findOrFail`. Pass IDs + reload defensively.
- `WithoutOverlapping` requires a cache lock backend (Redis/database). File/array cache silently breaks it.
- `database` queue driver is fine for low volume but locks rows under load — use Redis/SQS/Beanstalkd for >100 jobs/sec.
- Long-running jobs hit PHP `max_execution_time` and worker `--timeout`; Laravel kills the worker and the job retries from scratch (not idempotent by default).
- After deploys, `queue:restart` must be called or workers run stale code (cached opcodes + container).

## Agentic workflow
Use a subagent to scaffold a job class, register middleware, write a feature test that asserts dispatch with `Queue::fake()`, and add a `failed_jobs` migration if missing. The agent must check `config/queue.php` for the configured connection and confirm a worker/Horizon is supervised before declaring "done". Always end with `php artisan queue:work --once` to smoke-test the job locally.

### Recommended subagents
- `faion-sdd-executor-agent` — scaffolds Job + test + binding, runs `php artisan test --filter=JobName` as a quality gate.
- A custom `php-backend-agent` (not present in repo) for Laravel-specific lint (Larastan level 8) and PHPStan/Pint.

### Prompt pattern
```
Create a Laravel queued job <Name> that <action>. Constraints: tries=3, backoff=exponential, timeout<=120s, WithoutOverlapping by <key>. Pass IDs only (not models). Add Tests\Feature with Queue::fake() asserting dispatch + chain. Confirm config/queue.php uses redis connection.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `php artisan queue:work` | Daemon worker (production: under supervisord/systemd) | Built-in |
| `php artisan queue:listen` | Dev-only worker (reloads code per job) | Built-in |
| `php artisan queue:failed` / `queue:retry` / `queue:flush` | Manage failed jobs | Built-in |
| `php artisan horizon` | Redis-backed dashboard + auto-balancing | `composer require laravel/horizon` |
| `php artisan queue:restart` | Graceful worker reload after deploy | Built-in |
| `php artisan queue:monitor` | Alert on queue depth | Built-in (Laravel 9+) |
| `php artisan tinker` | REPL for ad-hoc dispatch + state inspection | Built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Horizon | OSS | Yes | Redis only; rich dashboard, supervisor config, metrics. Standard for prod. |
| Redis (Valkey) | OSS | Yes | Default queue backend. Already on faion-net server (port 6379). |
| AWS SQS | SaaS | Yes | First-class driver. 256KB message limit, no FIFO unless explicitly enabled. |
| Beanstalkd | OSS | Yes | Lightweight alternative to Redis. |
| Laravel Forge / Vapor | SaaS | Yes | Provisions Horizon + Redis automatically. |
| Sentry / Bugsnag | SaaS | Yes | Auto-captures `failed()` exceptions via Laravel integration. |
| Telescope | OSS | Yes | Dev-only deep-inspection; logs every job + payload. |

## Templates & scripts
See templates.md and the README's Job Structure / Job Batching examples. Inline supervisor snippet for a self-hosted worker:

```ini
; /etc/supervisor/conf.d/laravel-worker.conf
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /var/www/app/artisan queue:work redis --queue=high,default,low --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
user=www-data
numprocs=4
redirect_stderr=true
stdout_logfile=/var/log/laravel-worker.log
stopwaitsecs=3600
```

## Best practices
- Pass primitives (IDs, scalars) into job constructors; reload Eloquent models inside `handle()`. Smaller payloads, less stale-data risk.
- Make every job idempotent — check `isProcessed()` early; the same message can be delivered twice (especially on SQS at-least-once).
- Set `--max-time` and `--max-jobs` on workers so memory leaks recycle naturally; pair with supervisor autorestart.
- Use named queues per priority (`high`, `default`, `low`, `notifications`) and order them on the worker command line.
- For batches >10k items, dispatch a meta-job that paginates and dispatches sub-jobs — never load all IDs into one batch payload.
- Always implement `failed()` for jobs touching external state (refunds, webhooks); update the related model so the UI can surface "failed" to a human.
- Run `php artisan queue:restart` in your deploy script AFTER atomic symlink swap.

## AI-agent gotchas
- The agent often forgets `ShouldQueue`. Without it, `dispatch()` runs synchronously — tests pass, prod blocks. Verify the interface is present before commit.
- `Queue::fake()` in feature tests means `failed()` is never exercised. Add a separate unit test that calls `failed()` directly with a synthetic Throwable.
- Agents may serialize entire request DTOs that contain closures/resources — those are unserializable and break silently. Reduce to primitives.
- Job classes inside `app/Jobs/` are auto-discovered, but the `failed_jobs` migration is NOT scaffolded by `make:job`. Agent must run `php artisan queue:failed-table && php artisan migrate`.
- Human checkpoint: review chosen `tries`/`backoff`/`timeout` against the downstream SLA — agents pick defaults that work for everything and excel at nothing. Especially review for payment/billing jobs.
- Agents tend to dispatch jobs from inside a DB transaction; default behavior fires the job before commit and the worker can't find the row. Set `after_commit => true` in `config/queue.php` or use `dispatch()->afterCommit()`.

## References
- https://laravel.com/docs/queues
- https://laravel.com/docs/horizon
- https://divinglaravel.com/queue-system (deep dive on internals)
- https://laravel-news.com/laravel-queue-best-practices
