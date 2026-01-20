# Software Developer Methodologies

106 methodologies for full-stack software development.

## Categories

### API Design (12)
| File | Description |
|------|-------------|
| api-authentication.md | Authentication methods (API Keys, JWT, OAuth, mTLS) |
| api-contract-first.md | Contract-first development workflow |
| api-documentation.md | API documentation tools and patterns |
| api-error-handling.md | RFC 7807 Problem Details, error format |
| api-gateway-patterns.md | Gateway functions, routing, load balancing |
| api-graphql.md | GraphQL schema, queries, mutations |
| api-monitoring.md | API health, metrics, alerting |
| api-openapi-spec.md | OpenAPI 3.1 specification |
| api-rate-limiting.md | Rate limiting strategies and headers |
| api-rest-design.md | REST resource-oriented design |
| api-testing.md | Contract testing, testing pyramid |
| api-versioning.md | URL path, header, content-type versioning |

### Architecture (6)
| File | Description |
|------|-------------|
| clean-architecture.md | Layered architecture, dependency rule |
| cqrs-pattern.md | Command Query Responsibility Segregation |
| domain-driven-design.md | DDD entities, aggregates, bounded contexts |
| event-sourcing.md | Event store, projections, snapshots |
| microservices-design.md | Service decomposition, communication |
| monorepo-turborepo.md | Turborepo setup, remote caching |

### C# / .NET (5)
| File | Description |
|------|-------------|
| csharp-aspnet-core.md | ASP.NET Core controller patterns |
| csharp-background-services.md | Background services, hosted services |
| csharp-dotnet-patterns.md | .NET patterns, minimal APIs |
| csharp-entity-framework.md | EF Core entity configuration |
| csharp-xunit-testing.md | xUnit testing patterns |

### Databases (4)
| File | Description |
|------|-------------|
| caching-strategy.md | Multi-level caching, invalidation |
| database-design.md | Schema design, normalization, indexing |
| nosql-patterns.md | MongoDB, Redis, Cassandra patterns |
| sql-optimization.md | Query optimization, EXPLAIN ANALYZE |

### Django / Python (8)
| File | Description |
|------|-------------|
| django-base-model.md | Base model with UUID, timestamps |
| django-coding-standards.md | Django conventions, imports |
| django-decision-tree.md | Code placement decision framework |
| django-pytest.md | pytest-django fixtures, factories |
| python-async-patterns.md | asyncio, TaskGroup, semaphores |
| python-fastapi.md | FastAPI standards, Pydantic |
| python-poetry-setup.md | Poetry dependency management |
| python-type-hints.md | Modern Python typing patterns |

### Frontend (14)
| File | Description |
|------|-------------|
| accessibility.md | WCAG, ARIA, keyboard navigation |
| css-in-js.md | styled-components, Emotion patterns |
| design-tokens.md | Design system tokens |
| mobile-responsive.md | Mobile-first, fluid layouts |
| nextjs-app-router.md | Next.js 13+ App Router patterns |
| pwa-development.md | Progressive Web Apps, service workers |
| react-component-architecture.md | Component organization, composition |
| react-hooks.md | Hooks best practices, custom hooks |
| seo-for-spas.md | SEO for Single Page Applications |
| shadcn-ui-architecture.md | shadcn/ui component patterns |
| storybook-setup.md | Storybook configuration, stories |
| tailwind-architecture.md | Tailwind configuration, design tokens |
| tailwind-patterns.md | Utility-first patterns |
| ui-component-library.md | Component library architecture |

### Go (6)
| File | Description |
|------|-------------|
| go-concurrency.md | Goroutines, channels, worker pools |
| go-concurrency-patterns.md | Concurrency patterns (Gin/Echo) |
| go-error-handling.md | Go error handling patterns |
| go-error-handling-patterns.md | Error wrapping, sentinel errors |
| go-http-handlers.md | HTTP handlers (Gin/Echo) |
| go-project-structure.md | Standard Go project layout |
| go-standard-layout.md | Standard layout with cmd/internal |

### Java / Spring (5)
| File | Description |
|------|-------------|
| java-jpa-hibernate.md | JPA/Hibernate entity patterns |
| java-junit-testing.md | JUnit 5, MockMvc testing |
| java-spring-async.md | Spring async configuration |
| java-spring-boot.md | Spring Boot layered architecture |
| java-spring-boot-patterns.md | Spring Boot controller patterns |

### JavaScript / TypeScript (5)
| File | Description |
|------|-------------|
| bun-runtime.md | Bun runtime, bundler, test runner |
| nodejs-express-fastify.md | Express/Fastify patterns |
| nodejs-service-layer.md | Controller-Service-Repository |
| pnpm-package-management.md | pnpm workspaces, configuration |
| typescript-strict-mode.md | TypeScript strict configuration |

### PHP / Laravel (5)
| File | Description |
|------|-------------|
| laravel-patterns.md | Laravel architecture patterns |
| php-eloquent.md | Eloquent ORM patterns |
| php-laravel-patterns.md | Laravel controller structure |
| php-laravel-queues.md | Laravel queue jobs |
| php-phpunit-testing.md | PHPUnit feature tests |

### Ruby / Rails (5)
| File | Description |
|------|-------------|
| ruby-activerecord.md | ActiveRecord query objects |
| ruby-rails.md | Rails architecture patterns |
| ruby-rails-patterns.md | Rails service objects |
| ruby-rspec-testing.md | RSpec model/request specs |
| ruby-sidekiq-jobs.md | Sidekiq background jobs |

### Rust (6)
| File | Description |
|------|-------------|
| rust-error-handling.md | Result, Option, error types |
| rust-http-handlers.md | Axum HTTP handlers |
| rust-ownership.md | Ownership, borrowing, lifetimes |
| rust-project-structure.md | Actix/Axum project layout |
| rust-testing.md | Rust testing patterns |
| rust-tokio-async.md | Tokio async patterns |

### Testing (11)
| File | Description |
|------|-------------|
| code-coverage.md | Coverage tools, metrics |
| e2e-testing.md | Playwright, Cypress E2E |
| integration-testing.md | Database, API integration tests |
| mocking-strategies.md | Mocks, stubs, fakes |
| performance-testing.md | Load testing, profiling |
| security-testing.md | SAST, DAST, dependency scanning |
| tdd-workflow.md | Red-Green-Refactor cycle |
| test-fixtures.md | Fixture patterns, factories |
| unit-testing.md | Unit test structure, assertions |

### Development Practices (14)
| File | Description |
|------|-------------|
| ab-testing.md | A/B testing implementation |
| claude-md-creation.md | CLAUDE.md project setup |
| code-review.md | Code review best practices |
| documentation.md | Code documentation patterns |
| error-handling.md | Error handling strategies |
| feature-flags.md | Feature flag implementation |
| graphql-api-design.md | GraphQL API design patterns |
| internationalization.md | i18n implementation |
| logging-patterns.md | Structured logging |
| message-queues.md | RabbitMQ, Redis, Kafka patterns |
| openapi-specification.md | OpenAPI/Swagger specification |
| refactoring-patterns.md | Refactoring techniques |
| rest-api-design.md | REST API design patterns |
| technical-debt.md | Technical debt management |
| websocket-design.md | WebSocket implementation |

## Naming Convention

- Semantic lowercase-with-dashes filenames
- No M-XXX IDs or numbers
- Descriptive names reflecting content

## Usage

Reference methodologies in code or documentation:

```markdown
See [rest-api-design.md](methodologies/rest-api-design.md) for REST patterns.
```
