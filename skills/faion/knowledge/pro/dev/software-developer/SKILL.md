---
name: faion-pro-software-developer
description: "Pro-tier software developer: enterprise stacks (.NET, Java, PHP, Ruby), DDD/CQRS/event-sourcing impl, microservices, API gateway. 47 methodologies."
tier: pro
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> Part of **faion** umbrella — read on-demand, not individually invocable.

# Software Developer Domain Skill

## Purpose

Pro-tier implementation guidance for enterprise stacks (C#/.NET, Java/Spring, PHP/Laravel, Ruby/Rails) and the practical implementation of DDD, CQRS, event sourcing, and microservices patterns. Pairs with `faion-software-developer` (free tier) which covers Python, JS, and Go fundamentals.

## When to Use

| Scenario | Methodology |
|----------|-------------|
| Cross-cutting API entrypoint | api-gateway-patterns |
| Health, metrics, logs, alerts on APIs | api-monitoring-* |
| Layered, dependency-inverted code | clean-architecture |
| Continuous delivery pipeline | continuous-delivery |
| Read/write segregation in code | cqrs-pattern |
| ASP.NET Core service | csharp-aspnet-core |
| Background workers in .NET | csharp-background-services |
| .NET fundamentals | csharp-dotnet, csharp-dotnet-patterns |
| .NET data access | csharp-entity-framework |
| .NET testing | csharp-xunit-testing |
| DDD aggregates, repos, events, VOs | ddd-* |
| Event-sourced services | event-sourcing-* |
| Java + Hibernate | java-jpa-hibernate |
| Java testing | java-junit-testing |
| Spring / Spring Boot apps | java-spring*, java-spring-boot* |
| Spring async | java-spring-async |
| Laravel architecture | laravel-patterns |
| Microservices runtime concerns | microservices-* |
| PHP / Laravel impl | php-* |
| Ruby on Rails impl | ruby-* |

## Methodologies (47)

**API Layer**
- api-gateway-patterns.md
- api-monitoring-alerting.md
- api-monitoring-health-checks.md
- api-monitoring-logging.md
- api-monitoring-metrics.md

**Architecture Patterns**
- clean-architecture.md
- cqrs-pattern.md
- continuous-delivery.md
- ddd-aggregates.md
- ddd-anti-corruption-layer.md
- ddd-domain-events.md
- ddd-repositories.md
- ddd-value-objects.md
- event-sourcing-agentic.md
- event-sourcing-aggregate.md
- event-sourcing-fundamentals.md
- event-sourcing-projections.md
- event-sourcing-snapshots.md
- event-sourcing-versioning.md

**Microservices Implementation**
- microservices-circuit-breaker.md
- microservices-inter-service-comm.md
- microservices-observability.md
- microservices-saga-pattern.md
- microservices-service-boundaries.md

**.NET / C#**
- csharp-aspnet-core.md
- csharp-background-services.md
- csharp-dotnet.md
- csharp-dotnet-patterns.md
- csharp-entity-framework.md
- csharp-xunit-testing.md

**Java / Spring**
- java-jpa-hibernate.md
- java-junit-testing.md
- java-spring.md
- java-spring-async.md
- java-spring-boot.md
- java-spring-boot-patterns.md

**PHP / Laravel**
- laravel-patterns.md
- php-eloquent.md
- php-laravel.md
- php-laravel-patterns.md
- php-laravel-queues.md
- php-phpunit-testing.md

**Ruby / Rails**
- ruby-activerecord.md
- ruby-rails.md
- ruby-rails-patterns.md
- ruby-rspec-testing.md
- ruby-sidekiq-jobs.md

## Related Skills

- faion-software-architect — system-level design
- faion-code-quality — architecture-pattern theory
- faion-software-developer (free tier) — Python / JS / Go fundamentals
- faion-testing-developer — test strategies

---

*Software Developer v1.0 | 47 Methodologies*
