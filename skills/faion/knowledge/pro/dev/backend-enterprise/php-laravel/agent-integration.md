# Agent Integration — PHP Laravel (umbrella)

## When to use
- You need a single entry point for an agent to plan a Laravel feature end-to-end (controller + Eloquent + tests + queue), pulling from the four sub-methodologies in this group.
- New service or solo-dev SaaS where Laravel's batteries-included posture (auth, mail, queues, validation, routing) materially compresses delivery time.
- Internal tools, B2B SaaS, content sites, marketplaces — Laravel's sweet spot.

## When NOT to use
- Hard real-time / low-latency (<10 ms) APIs — PHP request lifecycle is per-request bootstrap; reach for Go, Rust, or Laravel Octane only after benchmarking.
- Heavy CPU/data pipelines — use Python (pandas), Spark, or Go.
- Microservice mesh with strict contract boundaries — Laravel's Active Record + facades encourage shortcuts that break contracts; pick a hexagonal stack.

## Where it fails / limitations
- This file is an umbrella. The four operational methodologies (`php-laravel-patterns`, `php-eloquent`, `php-laravel-queues`, `php-phpunit-testing`) are the sources of truth. Treat this file as a router, not a deep dive.
- README.md content here duplicates patterns/queues/testing files — keep edits there to avoid drift.
- Laravel's "magic" (facades, global helpers, Eloquent macros) defeats LLM static reasoning. Static analysis (Larastan) is non-negotiable for agent-generated code.

## Agentic workflow
Treat this as a dispatcher: the agent first identifies which sub-area the task touches, then loads the dedicated `agent-integration.md` for that subdir. For multi-area tasks (e.g., "build orders endpoint + background processing + tests") the agent should sequence:
1. `php-laravel-patterns/agent-integration.md` — controller/service/resource scaffold.
2. `php-eloquent/agent-integration.md` — model + relationships + scopes.
3. `php-laravel-queues/agent-integration.md` — async job for the slow step.
4. `php-phpunit-testing/agent-integration.md` — feature + unit tests.
After each step, run `composer test`, `vendor/bin/pint`, `vendor/bin/phpstan analyse`. Insert a human checkpoint before adding new packages or running `php artisan migrate` on shared environments.

### Recommended subagents
- `general-purpose` Claude subagent — sequencing and scaffolding via Artisan.
- Code-review subagent (Sonnet) — layer-boundary enforcement and security review.

### Prompt pattern
```
Build CRUD feature <Resource>. Use the 4-step Laravel sequence: patterns → eloquent → queues (only if any step >300ms) → phpunit-testing. Stop after each step for `composer test && vendor/bin/pint && vendor/bin/phpstan analyse`. Do not add new composer packages without confirmation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `composer create-project laravel/laravel <name>` | New project | https://laravel.com/docs/installation |
| `php artisan` | Code generation, migrations, queue, scheduler | bundled |
| `vendor/bin/pint` | Style formatter | `composer require laravel/pint --dev` |
| `vendor/bin/phpstan` (Larastan) | Static analysis | https://github.com/larastan/larastan |
| `vendor/bin/rector` | Automated upgrades | https://getrector.com |
| `php artisan octane:start` | High-perf runtime (Swoole/RoadRunner/FrankenPHP) | https://laravel.com/docs/octane |
| `vendor/bin/pest` | Faster test syntax (alternative to PHPUnit) | https://pestphp.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Laravel Forge | SaaS | Limited | Server provisioning + deploys via API |
| Laravel Vapor | SaaS | Yes (CLI) | Serverless on AWS Lambda |
| Laravel Cloud | SaaS | Yes | Managed Laravel hosting (2024+) |
| FrankenPHP | OSS | Yes | Modern Laravel runtime, agent-friendly Docker image |
| Filament | OSS | Yes | Admin panel generator; agents can scaffold resources |
| Sentry / Honeybadger | SaaS | Yes | Error tracking SDK |

## Templates & scripts
This is an umbrella file. Templates live in:
- `php-laravel-patterns/templates.md` — controller/service/repository.
- `php-eloquent` — model patterns.
- `php-laravel-queues/templates.md` — jobs and batches.
- `php-phpunit-testing/templates.md` — feature/unit tests.

Inline `composer.json` snippet the agent should ensure exists for any new project:

```json
{
  "scripts": {
    "test": "@php artisan test --parallel",
    "lint": "vendor/bin/pint --test",
    "fix":  "vendor/bin/pint",
    "stan": "vendor/bin/phpstan analyse --memory-limit=2G"
  },
  "require-dev": {
    "laravel/pint": "^1.0",
    "larastan/larastan": "^3.0",
    "rector/rector": "^1.0"
  }
}
```

## Best practices
- One pattern source per concern: this umbrella is for orientation, not for editing logic. Edit the sub-methodology files.
- Pin PHP version explicitly in `composer.json` `"php"` constraint and CI matrix.
- Run Larastan at level 6+ on any agent-generated code; Laravel magic hides bugs at lower levels.
- Use `php artisan about` to dump the runtime config — feed into agent prompts so it knows queue driver, cache driver, DB.
- Keep `.env.example` in sync; agents that add config keys must update both `.env.example` and any deploy secrets manifest.

## AI-agent gotchas
- The README in this directory aggregates content from sibling methodologies — agents may edit it and create drift. Treat as read-only.
- LLM tendency: pull all four sub-areas into one giant migration. Force step-wise execution with checkpoints between artisan generators.
- Larastan errors on agent code are usually about facade types or Eloquent magic — install `barryvdh/laravel-ide-helper` and run `ide-helper:generate` before letting the agent reason about Eloquent.
- Human-in-loop checkpoint: adding a composer package, running migrations on prod, deleting any `failed_jobs` rows, modifying `.env`.

## References
- https://laravel.com/docs (canonical)
- https://spatie.be/laravel-beyond-crud (enterprise patterns)
- https://github.com/larastan/larastan
- https://laravel-news.com (community patterns + release notes)
- Sub-methodologies: `php-laravel-patterns/`, `php-eloquent/`, `php-laravel-queues/`, `php-phpunit-testing/`
