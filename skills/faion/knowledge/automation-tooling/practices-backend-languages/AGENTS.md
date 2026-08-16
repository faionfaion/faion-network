# Backend Languages Practices

## Summary

**One-sentence:** Produces a backend service scaffold in Go/Rails/Laravel/Spring Boot/.NET/Rust enforcing the canonical layout, error model, DI shape, and async discipline for the chosen language.

**One-paragraph:** Reference patterns for six backend languages. Go: cmd/internal/pkg layout, wrapped errors via fmt.Errorf with %w, consumer-side interfaces, worker-pool concurrency. Ruby on Rails: thin controllers + service/form/query objects. PHP Laravel: controller -> Form Request -> Service. Java Spring Boot: constructor injection (no @Autowired on fields), @Service @RequiredArgsConstructor, builder DTOs. C# .NET: IService interfaces + DI, async Task<T> throughout. Rust: thiserror Result types, tokio for async, no blocking I/O inside async fns. The artefact is the language tag + scaffold metadata; the validator checks the canonical fields per language are present.

**Ефективно для:**

- Greenfield service scaffolding in any of the six languages.
- Cross-language onboarding: produce equivalent service shape in two stacks.
- Code-review gate — check Go interfaces are consumer-side, Spring uses constructor injection, Rust async has no blocking calls.
- Refactor passes aligning an existing module to the known-good shape.

## Applies If (ALL must hold)

- Greenfield service scaffolding in one of Go, Rails, Laravel, Spring Boot, .NET, Rust.
- Cross-language onboarding where shape parity matters.
- Refactor passes aligning existing modules to canonical layout.
- Code-review gates checking idiomatic patterns per language.

## Skip If (ANY kills it)

- Architecture decisions (microservices vs monolith) — out of scope.
- Performance profiling or observability — out of scope.
- Frontend code — see practices-frontend-components / practices-js-ts-stack.
- Project already has a documented house style that diverges — agent will overwrite.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target language | one of: go | rails | laravel | spring | dotnet | rust | team decision |
| Service name + intended public surface | free text + endpoint list | task brief |
| DI framework (when applicable) | Spring / Symfony container / built-in | language defaults |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[testing-backend-languages]] | shared test runner conventions per language |
| [[trunk-based-ci-gates]] | scaffolded service must pass the CI gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-language-template` | haiku | lookup based on input field |
| `emit-canonical-scaffold` | sonnet | render layout + key files with idiomatic patterns |
| `review-against-rules` | sonnet | rule-by-rule check on generated tree |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-layout.txt` | Canonical Go project layout tree |
| `templates/go-service.go` | Go service skeleton with consumer-side interface + worker pool |
| `templates/spring-service.java` | Spring Boot service using constructor injection |
| `templates/rust-error.rs` | Rust error type via thiserror + async fn |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-backend-languages.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-python-ecosystem]]
- [[practices-django-coding]]
- [[testing-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-layout.txt`

```text
project/
|-- cmd/
|   \-- server/
|       \-- main.go
|-- internal/
|   |-- handlers/
|   |-- services/
|   \-- models/
|-- pkg/
|-- go.mod
\-- go.sum
```

### `templates/go-service.go`

```go
package handlers

import (
    "context"
    "fmt"
)

// Consumer-side interface (declared where it is used)
type OrderRepo interface {
    Find(ctx context.Context, id string) (*Order, error)
    Save(ctx context.Context, o *Order) error
}

type OrderHandler struct {
    repo OrderRepo
}

func NewOrderHandler(repo OrderRepo) *OrderHandler {
    return &OrderHandler{repo: repo}
}

func (h *OrderHandler) Charge(ctx context.Context, id string) error {
    o, err := h.repo.Find(ctx, id)
    if err != nil {
        return fmt.Errorf("charge order %s: %w", id, err)
    }
    o.Status = "charged"
    if err := h.repo.Save(ctx, o); err != nil {
        return fmt.Errorf("save order %s: %w", id, err)
    }
    return nil
}
```

### `templates/spring-service.java`

```java
package com.example.orders;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;

    public Order create(CreateOrderDto dto) {
        Order order = Order.builder()
            .customerId(dto.getCustomerId())
            .amount(dto.getAmount())
            .build();
        return orderRepository.save(order);
    }
}
```

### `templates/rust-error.rs`

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum OrderError {
    #[error("order not found: {0}")]
    NotFound(String),
    #[error("database error")]
    Db(#[from] sqlx::Error),
}

pub async fn charge_order(pool: &sqlx::PgPool, id: &str) -> Result<Order, OrderError> {
    let row = sqlx::query_as::<_, Order>("SELECT * FROM orders WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await?;
    row.ok_or_else(|| OrderError::NotFound(id.to_string()))
}
```

### `templates/artefact.json`

```json
{
  "language": "go",
  "layout_ok": true,
  "error_model_ok": true,
  "di_shape_ok": true,
  "async_ok": true,
  "notes": "cmd/internal/pkg layout; %w error wrapping; consumer-side OrderRepo."
}
```
