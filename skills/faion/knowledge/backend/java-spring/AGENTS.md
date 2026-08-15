# Java Spring Boot Backend

## Summary

**One-sentence:** Canonical layered Spring Boot 3 architecture — @RestController → @Service → JpaRepository, Bean Validation, MapStruct DTOs, @Transactional writes, Pageable lists, BCrypt password hashing.

**One-paragraph:** Canonical layered architecture for Spring Boot 3.x: `@RestController` validates input via Bean Validation, delegates to `@Service`, which calls `JpaRepository`. Controllers return record-based DTOs (never entities). Write methods are `@Transactional`; list endpoints accept `Pageable`; passwords are hashed via `PasswordEncoder` (BCrypt) inside the service. MapStruct generates DTO ↔ entity mappers via the annotation processor. Spring Boot 3 means `jakarta.*` imports throughout. This is the starter Spring Boot pattern; for richer search (Specifications) and CQRS see related methodologies.

**Ефективно для:**

- New Spring Boot 3.x service with standard CRUD endpoints.
- Adding endpoints with Bean Validation, MapStruct DTO mapping, and paginated list queries.
- Refactoring code that mixes controller/service/repository concerns or returns entity types to clients.
- Wiring BCrypt `PasswordEncoder` and `Pageable` defaults in the service layer.

## Applies If (ALL must hold)

- New Spring Boot 3.x service with standard CRUD endpoints.
- Standard JPA persistence (Hibernate) with `JpaRepository`.
- Java 17+ codebase with record support.

## Skip If (ANY kills it)

- WebFlux / reactive stack — blocking JPA, `@Transactional`, and `ResponseEntity` semantics differ.
- Hexagonal / Clean Architecture with explicit ports/adapters — layering on top doubles up indirection.
- CQRS or event-sourced systems — service + JPA hides the command/query split.
- Quarkus / Micronaut / serverless — annotations differ; pattern translates conceptually but not literally.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API contract | OpenAPI YAML or Markdown | product / API design |
| Entity model | ERD or Markdown table | data modelling |
| Target Spring Boot version | `3.x` | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sibling for richer enterprise-grade patterns. |
| [[java-jpa-hibernate]] | Repository layer discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: dto-record-never-entity, transactional-on-writes, pageable-on-list, bcrypt-in-service, mapstruct-annotation-processor, jakarta-not-javax, thin-controller, transactional-on-service-only, record-dtos-with-validation, async-via-named-executor | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the service-scaffold manifest (+ optional controller / DTO / async / ProblemDetail blocks) + valid/invalid examples | 1400 |
| `content/03-failure-modes.xml` | essential | 10 antipatterns: entity-leak-via-jsonignore, missing-transactional, unbounded-findall, mapstruct-missing-from-pom, jakarta-vs-javax-mix, transactional-self-invocation, transactional-on-controller, fat-controller-with-repository, async-self-invocation, custom-error-envelope | 1400 |
| `content/04-procedure.xml` | essential | 5-step procedure: thin controller + validated record DTOs → service → repository → DTO + mapper → ProblemDetail advice, async config and tests | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-crud-endpoint` | sonnet | Layered code generation with judgment on validation. |
| `wire-mapstruct-mapper` | sonnet | Mapper interface design. |
| `audit-transactional-discipline` | haiku | Mechanical scan for missing `@Transactional` on writes. |
| `audit-controller-thinness` | haiku | Mechanical scan for `@Transactional` / repository autowiring in controllers. |
| `design-async-executor` | sonnet | Pool sizing + bean extraction for `@Async`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check.sh` | CI script verifying jakarta imports + MapStruct annotation processor + @Transactional on writes. |
| `templates/Controller.java` | Thin @RestController skeleton per `thin-controller`. |
| `templates/Service.java` | @Transactional service skeleton returning DTOs only. |
| `templates/AsyncConfig.java` | Named ThreadPoolTaskExecutor + @Async target bean. |
| `templates/maven-annotation-processors.xml` | pom.xml `annotationProcessorPaths` block with Lombok + MapStruct in the required order. |
| `templates/prompt-vertical-slice.txt` | Codegen prompt for a full vertical slice of this pattern. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-spring.py` | Validate the service-scaffold manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-jpa-hibernate]]
- [[java-junit-testing]]
- [[java-spring-async]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (Spring stack, endpoint shape, architecture style) to a rule from `01-core-rules.xml`. Use it before scaffolding a new endpoint or wiring DTO mapping.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/check.sh`

```bash
# check.sh — block PR if entities leak from controllers or build/style fails.
# Usage: bash scripts/check.sh
set -euo pipefail

./mvnw -q -DskipTests compile spotless:check checkstyle:check

# Forbid returning entity types from REST controllers
if rg -nP 'public\s+(ResponseEntity<[A-Z]\w+>|[A-Z]\w+)\s+\w+\([^)]*\)\s*\{' \
     src/main/java -g '*Controller.java' \
   | grep -vE 'Response|Dto|ProblemDetail|Page<|Void|String|byte\[\]'; then
  echo "ERROR: Controller appears to return an entity directly — return a DTO."
  exit 1
fi

echo "OK: build clean, no entity leaks"
```

### `templates/Controller.java`

```java
// purpose: thin @RestController skeleton conforming to thin-controller rule
// consumes: OrdersService + request DTO
// produces: HTTP controller artefact
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

package faion.web.orders;

import faion.app.orders.OrdersService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/orders")
public class OrdersController {

    private final OrdersService service;

    public OrdersController(OrdersService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> getById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.getById(id));
    }

    @GetMapping
    public Page<OrderSummary> list(Pageable pageable) {
        return service.list(pageable);
    }

    @PostMapping
    public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        OrderResponse created = service.create(req);
        return ResponseEntity.created(java.net.URI.create("/api/orders/" + created.id())).body(created);
    }
}
```

### `templates/Service.java`

```java
// purpose: @Transactional service skeleton returning DTOs only
// consumes: OrderRepository (narrow) + DTOs
// produces: service class for the controller
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

package faion.app.orders;

import faion.infra.orders.OrderRepository;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrdersService {

    private final OrderRepository repository;

    public OrdersService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        return repository.findByIdWithItems(id)
            .map(OrderResponse::from)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }

    public Page<OrderSummary> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        var saved = repository.save(new faion.domain.orders.Order(req.customerName()));
        return OrderResponse.from(saved);
    }
}

record CreateOrderRequest(
    @NotBlank @Size(max = 200) String customerName,
    @Positive BigDecimal total
) {}

record OrderResponse(UUID id, String customerName, BigDecimal total) {
    static OrderResponse from(faion.domain.orders.Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

record OrderSummary(UUID id, String customerName, BigDecimal total) {}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
```

### `templates/AsyncConfig.java`

```java
// purpose: named ThreadPoolTaskExecutor + @Async configuration per async-via-named-executor rule
// consumes: pool-size config from application.yml
// produces: Spring config bean defining the executor + @Async target bean
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Service;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "emailExecutor")
    public Executor emailExecutor(
        @Value("${faion.email.pool.core-size:4}") int core,
        @Value("${faion.email.pool.max-size:16}") int max,
        @Value("${faion.email.pool.queue-capacity:1000}") int queue
    ) {
        ThreadPoolTaskExecutor exec = new ThreadPoolTaskExecutor();
        exec.setCorePoolSize(core);
        exec.setMaxPoolSize(max);
        exec.setQueueCapacity(queue);
        exec.setThreadNamePrefix("email-");
        exec.initialize();
        return exec;
    }
}

@Service
class EmailSender {

    @Async("emailExecutor")
    public void sendOrderConfirmation(String to, String orderId) {
        // call SMTP / SES; if it throws, the executor logs.
    }
}
```

### `templates/maven-annotation-processors.xml`

```xml
<!-- purpose: Maven compiler plugin snippet with Lombok + MapStruct in required order -->
<!-- consumes: lombok.version + mapstruct.version properties -->
<!-- produces: annotationProcessorPaths block for pom.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->
<!-- Place inside <build><plugins> in pom.xml -->
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <annotationProcessorPaths>
      <!-- Lombok MUST come before mapstruct-processor -->
      <path>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>${lombok.version}</version>
      </path>
      <path>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct-processor</artifactId>
        <version>${mapstruct.version}</version>
      </path>
      <!-- Binding artifact ensures Lombok setters are visible to MapStruct -->
      <path>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok-mapstruct-binding</artifactId>
        <version>0.2.0</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

### `templates/prompt-vertical-slice.txt`

```text
# purpose: vertical-slice prompt for AI codegen of a Spring Boot feature package
# consumes: <Entity> + <package> + <fields>
# produces: prompt string fed to the codegen subagent
# depends-on: content/01-core-rules.xml, templates/Controller.java, templates/Service.java
# token-budget-impact: ~250 tokens when loaded as system prompt

Add a vertical slice for "<Entity>" under com.example.<package>:
- entity <Entity> (id Long, <fields>) extending BaseEntity if available
- <Entity>Repository extends JpaRepository<<Entity>, Long>
- <Entity>Service interface { create(req): Resp; findById(id): Resp; delete(id) }
- <Entity>ServiceImpl with @Transactional(readOnly=true) class-level, @Transactional on writes
- <Entity>Controller: GET /api/v1/<entities>, GET /{id}, POST, DELETE with @Valid
- MapStruct mapper <Entity>Mapper
- DTOs as Java records: Create<Entity>Request, <Entity>Response
- @WebMvcTest for controller, @ExtendWith(MockitoExtension) for service
- Flyway migration V<yyyymmdd>__create_<entities>.sql
Use constructor injection (@RequiredArgsConstructor). No field injection. No entity returns from public service methods.
```
