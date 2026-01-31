# Backend Systems

> **Entry point:** `/faion-net` — invoke for automatic routing.

Systems-level backend development: Go, Rust, databases, infrastructure.

**Methodologies:** 22 | **Files:** 112

## Methodologies

All methodologies now have folder structure with:
- README.md - Core concepts and patterns
- checklist.md - Step-by-step implementation guide
- templates.md - Production-ready code templates
- examples.md - Real-world use cases
- llm-prompts.md - AI-assisted development prompts

### Go Development (11 methodologies)

| Methodology | Focus | Key Tools |
|-------------|-------|-----------|
| [go-backend/](go-backend/) | Core Go patterns, project structure | Gin, Echo, Chi |
| [go-http-handlers/](go-http-handlers/) | HTTP server patterns, routing | net/http, Gin, Echo |
| [go-channels/](go-channels/) | Channel patterns, buffering, select | Go runtime, Context |
| [go-goroutines/](go-goroutines/) | Goroutine lifecycle, concurrency | Go runtime, pprof |
| [go-concurrency-patterns/](go-concurrency-patterns/) | Worker pools, rate limiting | sync package, Errgroup |
| [go-error-handling/](go-error-handling/) | Error wrapping, custom errors | errors package, fmt.Errorf |
| [go-error-handling-patterns/](go-error-handling-patterns/) | Error patterns, recovery | pkg/errors, Sentry |
| [go-project-structure/](go-project-structure/) | Directory layout, package org | Go modules, cmd/internal |
| [go-standard-layout/](go-standard-layout/) | Project layout conventions | Go modules, Make, Docker |

### Rust Development (7 methodologies)

| Methodology | Focus | Key Tools |
|-------------|-------|-----------|
| [rust-backend/](rust-backend/) | Axum/Actix patterns, project structure | Axum, Actix-web, Tokio |
| [rust-http-handlers/](rust-http-handlers/) | Handler patterns, extractors | Axum, Actix-web, Warp |
| [rust-tokio-async/](rust-tokio-async/) | Async runtime, tokio patterns | Tokio, futures, async-std |
| [rust-error-handling/](rust-error-handling/) | Result type, error propagation | anyhow, thiserror |
| [rust-ownership/](rust-ownership/) | Ownership rules, borrowing | Rust compiler, Clippy |
| [rust-project-structure/](rust-project-structure/) | Module organization, workspace | Cargo, Workspaces |
| [rust-testing/](rust-testing/) | Unit tests, integration tests | cargo test, mockall |

### Database & Data (3 methodologies)

| Methodology | Focus | Key Tools |
|-------------|-------|-----------|
| [database-design/](database-design/) | Schema design, normalization, indexing | PostgreSQL, MySQL, Alembic |
| [sql-optimization/](sql-optimization/) | Query optimization, EXPLAIN | PostgreSQL, EXPLAIN, pg_stat |
| [nosql-patterns/](nosql-patterns/) | Document, key-value patterns | MongoDB, DynamoDB, Redis |

### Infrastructure (3 methodologies)

| Methodology | Focus | Key Tools |
|-------------|-------|-----------|
| [caching-strategy/](caching-strategy/) | Multi-level caching, invalidation | Redis, Memcached, CDN |
| [message-queues/](message-queues/) | Queue patterns, reliability | RabbitMQ, Kafka, SQS |
| [error-handling/](error-handling/) | Error types, recovery, monitoring | Sentry, Logging frameworks |

## Quick Reference

### Go Patterns
- [go-backend/README.md](go-backend/README.md) - Project structure, handlers
- [go-concurrency-patterns/README.md](go-concurrency-patterns/README.md) - Worker pools, channels
- [go-error-handling-patterns/README.md](go-error-handling-patterns/README.md) - Error wrapping

### Rust Patterns
- [rust-backend/README.md](rust-backend/README.md) - Axum/Actix setup
- [rust-tokio-async/README.md](rust-tokio-async/README.md) - Async patterns
- [rust-error-handling/README.md](rust-error-handling/README.md) - Result types

### Database
- [database-design/README.md](database-design/README.md) - Schema design
- [sql-optimization/README.md](sql-optimization/README.md) - Query tuning
- [nosql-patterns/README.md](nosql-patterns/README.md) - NoSQL patterns

### Infrastructure
- [caching-strategy/README.md](caching-strategy/README.md) - Caching layers
- [message-queues/README.md](message-queues/README.md) - Queue patterns

## Related Skills

- [faion-backend-enterprise](../faion-backend-enterprise/CLAUDE.md) - Java, C#, PHP, Ruby
- [faion-api-developer](../faion-api-developer/CLAUDE.md) - API design
- [faion-infrastructure-engineer](../faion-infrastructure-engineer/CLAUDE.md) - Deployment
