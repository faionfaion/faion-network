---
name: faion-backend-systems
description: "Systems backends: Go, Rust, databases, caching."
tier: pro
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> Part of **faion** umbrella — read on-demand, not individually invocable.

# Backend Developer: Systems

Systems-level backend development in Go and Rust, plus database design and infrastructure patterns.

## Purpose

Handles high-performance backend services using Go and Rust, database design, caching strategies, and backend infrastructure.

---

## Context Discovery

### Auto-Investigation

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `go.mod` | `Read("go.mod")` | Go module, dependencies |
| `Cargo.toml` | `Read("Cargo.toml")` | Rust crate, dependencies |
| `cmd/` or `internal/` | `Glob("**/cmd/*")` | Go standard layout |
| `src/main.rs` | `Glob("**/src/main.rs")` | Rust binary |
| Web framework | `Grep("gin\|echo\|fiber", "go.mod")` | Go web framework |
| Async runtime | `Grep("tokio\|actix", "Cargo.toml")` | Rust async framework |
| Database driver | `Grep("sqlx\|gorm\|diesel", "**/*")` | Database library |

### Discovery Questions

#### Q1: Systems Language (if not detected)

```yaml
question: "Which language for this backend?"
header: "Language"
multiSelect: false
options:
  - label: "Go"
    description: "Simple concurrency, fast compile"
  - label: "Rust"
    description: "Memory safety, maximum performance"
```

#### Q2: Service Type

```yaml
question: "What type of service?"
header: "Service"
multiSelect: false
options:
  - label: "HTTP API"
    description: "REST or GraphQL endpoints"
  - label: "gRPC service"
    description: "High-performance internal API"
  - label: "Worker/processor"
    description: "Background job processing"
  - label: "CLI tool"
    description: "Command-line application"
```

#### Q3: Concurrency Needs

```yaml
question: "What are your concurrency requirements?"
header: "Concurrency"
multiSelect: false
options:
  - label: "High concurrency (1000s of connections)"
    description: "Need goroutines/async"
  - label: "Moderate (standard web traffic)"
    description: "Standard patterns"
  - label: "CPU-bound processing"
    description: "Parallel computation"
  - label: "Simple sequential"
    description: "Minimal concurrency"
```

---

## When to Use

- Go microservices and HTTP APIs
- Rust backend services
- Database design and optimization
- Caching strategies
- Message queues
- Error handling patterns

## Methodologies (44 files)

**Go (13):** `go-backend`, `go-channels`, `go-concurrency-patterns`, `go-error-handling`, `go-error-handling-patterns`, `go-goroutines`, `go-http-handlers`, `go-project-structure`, `go-standard-layout`, `go-layout-agentic-workflow`, `go-layout-directory-structure`, `go-layout-layer-rules`, `go-layout-toolchain`

**Rust (12):** `rust-backend`, `rust-error-handling`, `rust-http-handlers`, `rust-ownership`, `rust-project-structure`, `rust-testing`, `rust-tokio-async`, `rust-testing-antipatterns`, `rust-testing-ci-toolchain`, `rust-testing-integration`, `rust-testing-property`, `rust-testing-unit`

**Database (7):** `database-design`, `sql-optimization`, `nosql-patterns`, `nosql-cassandra-patterns`, `nosql-mongodb-patterns`, `nosql-neo4j-patterns`, `nosql-redis-patterns`

**Caching (6):** `caching-strategy`, `caching-http-headers`, `caching-in-memory`, `caching-invalidation`, `caching-stampede-prevention`, `caching-write-patterns`

**Messaging (5):** `message-queues`, `mq-broker-implementations`, `mq-idempotent-consumers`, `mq-patterns`, `mq-reliability`

**Infrastructure (1):** `error-handling`

## Tools

**Go:** Standard library, Gin, Echo, GORM, sqlx
**Rust:** Actix-web, Rocket, Tokio, Diesel, sqlx
**Database:** PostgreSQL, MySQL, MongoDB, Redis
**Queues:** RabbitMQ, Kafka, Redis

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-backend-developer:enterprise | Enterprise web frameworks (Java, C#, PHP, Ruby) |
| faion-python-developer | Python backends (Django, FastAPI) |
| faion-javascript-developer | Node.js backends |
| faion-api-developer | API design patterns |

## Integration

Invoked by parent skill `faion-backend-developer` for Go/Rust/database work.

---

*faion-backend-developer:systems v1.0 | 22 methodologies*
