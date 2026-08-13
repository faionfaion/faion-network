# JPA / Hibernate Patterns

## Summary

**One-sentence:** Spring Data JPA + Hibernate methodology — LAZY by default, business-key equality, expand-contract migrations, @DataJpaTest slices, OSIV off, DTO projections in controllers.

**One-paragraph:** Production-grade JPA / Hibernate for Spring Boot 3 services. Entity associations are LAZY by default; eager loading is per-query via `JOIN FETCH` or `@EntityGraph`. `equals` / `hashCode` are implemented over a business key (never Lombok `@Data` on entities). Migrations are versioned with Flyway; every entity diff lands with a paired migration. Bulk modifying queries use `@Modifying(clearAutomatically = true)`. Tests use `@DataJpaTest` + Testcontainers; controllers return DTO projections rather than entities to avoid `LazyInitializationException` once OSIV is disabled.

**Ефективно для:**

- Greenfield Spring Boot 3 services using Spring Data JPA + Hibernate 6.
- Migrating from `FetchType.EAGER` defaults that produce Cartesian explosions under load.
- Hardening test suites that mistakenly use `@SpringBootTest` for repository slices.
- Locking schema-change discipline with Flyway expand-contract migrations.

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

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: lazy-by-default, business-key-equality, flyway-migration-per-entity-change, modifying-clearautomatically, datajpatest-for-repositories, dto-projection-in-controllers | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the JPA-layer manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: lombok-data-on-entities, eager-fetch-default, cascade-all-on-manytoone, missing-migration, modifying-without-clear, springboottest-for-slice | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: entity modelling → repository slice → migration → bulk op safety → test slice | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-entity` | sonnet | Translating domain to JPA mappings requires judgment. |
| `generate-migration` | sonnet | Expand-contract reasoning. |
| `audit-fetch-strategy` | haiku | Mechanical scan for EAGER fetches. |
| `design-bulk-operation` | opus | L1 cache + clearAutomatically reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/entity.java` | Entity skeleton with LAZY associations + business-key equals/hashCode. |
| `templates/repository.java` | Spring Data JPA repository with @Modifying + clearAutomatically. |
| `templates/application-test.yml` | `@DataJpaTest` configuration with Testcontainers DB. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-jpa-hibernate.py` | Validate the JPA-layer manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

- [[java-spring-boot]]
- [[java-junit-testing]]
- [[java-spring]]

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
