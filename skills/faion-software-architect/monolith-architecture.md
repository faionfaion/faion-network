# Monolith Architecture

When and how to build monolithic applications.

## What is a Monolith?

Single deployable unit containing all application functionality.

```
┌─────────────────────────────────────┐
│           MONOLITH                  │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ UI  │ │ API │ │Logic│ │ DB  │   │
│  └─────┘ └─────┘ └─────┘ └─────┘   │
└─────────────────────────────────────┘
         Single deployment
```

## When to Choose Monolith

| Scenario | Monolith is good |
|----------|------------------|
| Small team | < 10 developers |
| MVP/Startup | Speed matters most |
| Simple domain | Clear boundaries |
| Limited DevOps | No K8s expertise |
| Tight budget | Lower infra cost |

## Advantages

- **Simple deployment** - One artifact
- **Easy debugging** - Single process, stack traces
- **No network calls** - In-process communication
- **Atomic transactions** - ACID across features
- **Lower latency** - No inter-service hops
- **Easier testing** - Integration tests straightforward

## Disadvantages

- **Scaling is coarse** - Scale everything together
- **Tech stack lock-in** - One language/framework
- **Deployment risk** - All or nothing
- **Team coupling** - Code conflicts
- **Longer build times** - As codebase grows

## Monolith Patterns

### Layered Architecture

```
┌─────────────────────────┐
│    Presentation Layer   │  Controllers, Views
├─────────────────────────┤
│     Business Layer      │  Services, Domain
├─────────────────────────┤
│   Persistence Layer     │  Repositories, ORM
├─────────────────────────┤
│      Database           │
└─────────────────────────┘
```

### Feature Folders (Vertical Slices)

```
src/
├── users/
│   ├── controller.py
│   ├── service.py
│   ├── repository.py
│   └── models.py
├── orders/
│   ├── controller.py
│   ├── service.py
│   └── ...
└── payments/
    └── ...
```

## Best Practices

### Code Organization

1. **Clear module boundaries** - Each feature in its folder
2. **Dependency direction** - Higher layers depend on lower
3. **Interface segregation** - Define contracts between modules
4. **No circular dependencies** - Enforce with linting

### Database

1. **One database** - But separate schemas per domain
2. **Migrations** - Versioned, reversible
3. **Indexing** - Plan for growth

### Deployment

1. **Blue-green deployments** - Zero downtime
2. **Feature flags** - Deploy without releasing
3. **Health checks** - Quick rollback capability

## Scaling Monolith

### Vertical Scaling
- Bigger server (more CPU, RAM)
- Database optimization
- Caching (Redis)

### Horizontal Scaling
```
         Load Balancer
              │
    ┌─────────┼─────────┐
    │         │         │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│ App 1 │ │ App 2 │ │ App 3 │
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              │
         Database
```

**Requirements for horizontal:**
- Stateless application
- Session storage (Redis)
- Shared file storage (S3)

## When to Migrate Away

Signs you've outgrown monolith:
- Deployments take hours
- Teams stepping on each other
- Can't scale specific features
- Build times > 30 minutes
- Different scaling needs per feature

**Migration path:** Monolith → Modular Monolith → Microservices

## Related

- [modular-monolith.md](modular-monolith.md) - Next evolution
- [microservices-architecture.md](microservices-architecture.md) - Alternative
