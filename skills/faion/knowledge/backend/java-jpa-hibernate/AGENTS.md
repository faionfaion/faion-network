# JPA / Hibernate Patterns

## Summary

**One-sentence:** Spring Data JPA + Hibernate methodology — LAZY by default, business-key equality, expand-contract migrations, @DataJpaTest slices, OSIV off, DTO projections in controllers.

**One-paragraph:** Production-grade JPA / Hibernate for Spring Boot 3 services. Entity associations are LAZY by default; eager loading is per-query via `JOIN FETCH` or `@EntityGraph`. `equals` / `hashCode` are implemented over a business key (never Lombok `@Data` on entities). Every entity carries audit timestamps, and user-editable aggregates carry `@Version`; every cascade / `orphanRemoval` / fetch choice carries a written justification. Migrations are versioned with Flyway; every entity diff lands with a paired migration. Bulk modifying queries use `@Modifying(clearAutomatically = true)`. Services consume narrow repository interfaces — never raw `JpaRepository` — and own the transaction boundary (`readOnly = true` on reads). Tests use `@DataJpaTest` + Testcontainers; reads project to DTOs and controllers return DTO projections rather than entities, so `LazyInitializationException` cannot fire once OSIV is disabled.

**Ефективно для:**

- Greenfield Spring Boot 3 services using Spring Data JPA + Hibernate 6.
- Migrating from `FetchType.EAGER` defaults that produce Cartesian explosions under load.
- Hardening test suites that mistakenly use `@SpringBootTest` for repository slices.
- Locking schema-change discipline with Flyway expand-contract migrations.
- High-throughput read paths that need DTO projection instead of entity hydration.
- Inventory / balance domains requiring optimistic or pessimistic locking.
- Teams that have suffered N+1 or open-in-view incidents.
- AI-generated code that defaults to `CascadeType.ALL` on every relation.

## Applies If (ALL must hold)

- Java 17+ service running Spring Boot 3 with Spring Data JPA and Hibernate 6.
- Entity model with ≥3 aggregate roots and non-trivial associations.
- Production deployment that requires zero-downtime schema migrations.

## Skip If (ANY kills it)

- Read-only reporting layer — use Spring Data JDBC or jOOQ; JPA change tracking is overhead.
- Hot-path microservice under sub-ms latency requirements — JPA proxy + first-level cache cost dominates.
- Schema-less / event-store services — JPA's relational assumptions fight the grain.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Domain entity model | Java classes or ERD | domain modelling |
| Migration policy | Flyway expand-contract checklist | DBA / SRE |
| Testcontainers DB image | Docker image name | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Sub-module for service / controller layering. |
| [[java-junit-testing]] | Test layering that drives `@DataJpaTest` vs `@SpringBootTest`. |
| [[ddd-repositories]] | Narrow-repository pattern the `narrow-repo-interface` rule builds on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 rules: lazy-by-default, business-key-equality, flyway-migration-per-entity-change, modifying-clearautomatically, datajpatest-for-repositories, dto-projection-in-controllers, audit-timestamps, justified-cascade-fetch, optimistic-locking-on-editable-aggregates, narrow-repo-interface, dto-projection-on-reads, service-owns-transaction-boundary | 2000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the JPA-layer manifest (+ optional narrow-repository / service spec) + valid/invalid examples | 1200 |
| `content/03-failure-modes.xml` | essential | 15 antipatterns: lombok-data-on-entities, id-based-equality, eager-fetch-default, cascade-all-on-manytoone, missing-migration, modifying-without-clear, springboottest-for-slice, open-in-view, lazy-outside-tx, n-plus-1, cascade-all-unjustified, optional-get-without-context, entity-serialised-directly, native-query-string-concat, entitymanager-in-singleton | 1700 |
| `content/04-procedure.xml` | essential | 5-step procedure: entity modelling → paired migration → narrow repository + bulk-op safety → transactional service with DTOs → test slice | 900 |
| `content/05-examples.xml` | reference | Worked fragments for the mapping / repository / narrow-repository / service rules; full bodies in templates/ | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain to JPA mappings requires judgment. |
| `generate-migration` | sonnet | Expand-contract reasoning. |
| `audit-fetch-strategy` | haiku | Mechanical scan for EAGER fetches. |
| `design-bulk-operation` | opus | L1 cache + clearAutomatically reasoning. |
| `design-entity-mapping` | sonnet | Cascade + orphanRemoval + fetch judgment. |
| `write-narrow-repository` | sonnet | Interface naming + method-set segregation. |
| `audit-existing-queries` | sonnet | Hunt N+1 and cascade misuse in an existing codebase. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity.java` | Entity skeleton with LAZY associations + business-key equals/hashCode. |
| `templates/repository.java` | Spring Data JPA repository with @Modifying + clearAutomatically. |
| `templates/NarrowRepository.java` | Narrow read/write repository interfaces per `narrow-repo-interface`. |
| `templates/Service.java` | Transactional service with JOIN FETCH + DTO projection. |
| `templates/application-test.yml` | `@DataJpaTest` configuration with Testcontainers DB. |
| `templates/application-jpa.yml` | Runtime JPA defaults: OSIV off, ddl-auto=validate, batch inserts, Hikari pool sizing. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate the JPA-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-junit-testing]]
- [[java-spring]]
- [[ddd-repositories]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (read vs write path, fetch strategy, test layer) to a rule from `01-core-rules.xml`. Use it before scaffolding a new entity or refactoring a hot query.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/entity.java`

```java
// JPA entity skeleton — explicit @Table, @Column, @Version, business-key equals
// Replace: User, users, user_roles, Role, Order

package com.example.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@Entity
@Table(
    name = "users",
    indexes = { @Index(name = "idx_users_email", columnList = "email") }
)
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Version
    private Long version;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @Builder.Default
    private Set<Role> roles = new HashSet<>();

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Business-key equals/hashCode — never use @Data on JPA entities
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User u)) return false;
        return email != null && email.equalsIgnoreCase(u.email);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email != null ? email.toLowerCase() : null);
    }
}
```

### `templates/repository.java`

```java
// Spring Data JPA repository skeleton
// Replace: User, Role, UserRepository

package com.example.repository;

import com.example.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived methods — no @Query needed
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);

    // JOIN FETCH — load roles in one query, avoid N+1
    @Query("SELECT u FROM User u JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);

    // Pageable search with nullable filters
    @Query("""
        SELECT u FROM User u
        WHERE (:name IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :name, '%')))
        AND (:isActive IS NULL OR u.isActive = :isActive)
        """)
    Page<User> search(
        @Param("name") String name,
        @Param("isActive") Boolean isActive,
        Pageable pageable
    );

    // Bulk update — must clear L1 cache after
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query("UPDATE User u SET u.isActive = false WHERE u.lastLoginAt < :cutoff")
    int deactivateInactive(@Param("cutoff") LocalDateTime cutoff);
}
```

### `templates/application-test.yml`

```yaml
spring:
  jpa:
    show-sql: false
    open-in-view: false
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true   # log query count per test
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
  flyway:
    enabled: true

logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.stat: DEBUG
    org.hibernate.orm.jdbc.bind: TRACE
```

### `templates/NarrowRepository.java`

```java
// purpose: narrow read/write repository interfaces per narrow-repo-interface rule
// consumes: Order + DTO projections
// produces: Spring Data interface segregated for read vs write
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.infra.orders;

import faion.domain.orders.Order;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

@NoRepositoryBean
public interface OrderRepository {

    Optional<Order> findById(UUID id);

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);

    Order save(Order order);

    void delete(Order order);
}

interface OrderRepositoryJpa extends OrderRepository, JpaRepository<Order, UUID> {

    @Override
    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    @Override
    @Query("SELECT new faion.infra.orders.OrderSummaryDto(o.id, o.customerName, o.total) FROM Order o")
    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);
}

record OrderSummaryDto(UUID id, String customerName, java.math.BigDecimal total) {}
```

### `templates/Service.java`

```java
// purpose: transactional service returning DTOs (not entities)
// consumes: OrderRepository + request inputs
// produces: service class for the controller
// depends-on: content/01-core-rules.xml, templates/NarrowRepository.java
// token-budget-impact: ~250 tokens when loaded as reference

package faion.app.orders;

import faion.domain.orders.Order;
import faion.infra.orders.OrderRepository;
import faion.infra.orders.OrderSummaryDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        Order order = repository.findByIdWithItems(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
        return OrderResponse.from(order);
    }

    public Page<OrderSummaryDto> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        Order order = new Order(req.customerName());
        repository.save(order);
        return OrderResponse.from(order);
    }
}

record CreateOrderRequest(String customerName) {}
record OrderResponse(UUID id, String customerName, java.math.BigDecimal total) {
    static OrderResponse from(Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
```

### `templates/application-jpa.yml`

```yaml
# purpose: Safe JPA/Hibernate application.yml defaults for Spring Boot
# consumes: the service's existing application.yml plus its datasource settings
# produces: config conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded

# application.yml — Safe JPA/Hibernate defaults for Spring Boot.
# Copy this block into your application.yml and adjust values for your environment.

spring:
  jpa:
    # Disable open-in-view to prevent lazy-loading outside transactions.
    open-in-view: false
    hibernate:
      # Use validate in production; create/create-drop only in test.
      ddl-auto: validate
    properties:
      hibernate:
        # Batch inserts/updates for bulk operations.
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
        # Enable SQL statistics for N+1 detection.
        generate_statistics: true
  datasource:
    hikari:
      # Tune based on DB server max_connections / number of app instances.
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

logging:
  level:
    # SQL log in dev — disable in production or route to a separate appender.
    org.hibernate.SQL: DEBUG
    org.hibernate.orm.jdbc.bind: TRACE
```
