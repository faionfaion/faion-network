# Laravel Queues

## Summary

Laravel's queue system for offloading background work: job classes implementing `ShouldQueue`, named queues for priority, `WithoutOverlapping` middleware for deduplication, retry/backoff/timeout configuration, and `Bus::batch` for parallel dataset processing. Jobs must be idempotent (check `isProcessed()` early), pass primitive IDs only (not Eloquent models), and implement `failed()` to surface failures to operators.

## Why

Work exceeding 200ms in HTTP handlers blocks the FPM worker thread and degrades all concurrent requests. Queues decouple the ack from the work: the controller dispatches and returns immediately; the worker processes asynchronously. Named queues (`high`, `default`, `notifications`) let high-priority work skip ahead. Retry + backoff handles unreliable downstream APIs without manual intervention.

## When To Use

- Any work taking >200ms from HTTP: email, PDF/CSV generation, third-party API calls, image processing.
- Fan-out: one user action triggers many side-effects (notify N subscribers).
- Batch jobs (`Bus::batch`) with then/catch/finally callbacks for large dataset processing.
- Webhook processing where you must ack the sender quickly and process asynchronously.
- Scheduled retries with exponential backoff for unreliable downstream services.

## When NOT To Use

- Hard real-time requirements (<1s end-to-end) — queue overhead and worker polling add latency.
- When the DB write IS the result the user is waiting for.
- Single-host deployments without a daemonized worker (`queue:work` must run continuously).
- Jobs that depend on request-scoped state (auth user, session) — pass primitive IDs only.
- When there is no Horizon/supervisor plan and no `failed_jobs` monitoring.

## Content

| File | What's inside |
|------|---------------|
| `content/01-job-rules.xml` | Job structure rules: ShouldQueue, idempotency, primitive args, middleware, retry/backoff/timeout, failed() |
| `content/02-batching.xml` | Bus::batch pattern, chunk sizing, then/catch/finally, cancellation check |
| `content/03-antipatterns.xml` | Missing ShouldQueue, models in args, dispatch inside transaction, missing failed_jobs migration |

## Templates

| File | Purpose |
|------|---------|
| `templates/job.php` | ProcessOrderJob with ShouldQueue, WithoutOverlapping, tries/backoff/timeout, idempotency check, failed() |
| `templates/batch-job.php` | ExportUsersJob with Batchable, cancellation check, Bus::batch dispatch |
| `templates/supervisor.ini` | Supervisor config for queue:work daemon with priority queues and autorestart |
