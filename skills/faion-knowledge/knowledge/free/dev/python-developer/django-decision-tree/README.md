# Django Decision Tree

A comprehensive decision framework for Django development. Covers framework selection, architecture patterns, API framework choices, database selection, deployment strategies, and third-party package evaluation.

## Overview

Making the right architectural decisions early in a Django project prevents costly refactoring later. This methodology provides structured decision trees for:

1. **Framework Selection** - When to choose Django vs alternatives
2. **API Framework Choice** - DRF vs Django Ninja vs Django views
3. **Architecture Patterns** - Service layer, clean architecture, DDD
4. **Database Selection** - PostgreSQL vs MySQL vs SQLite
5. **Deployment Strategy** - VPS vs PaaS vs Kubernetes vs Serverless
6. **Third-Party Packages** - Evaluation criteria and recommendations
7. **Code Organization** - Where to place code in Django projects

## When to Use

- Starting a new Django project
- Choosing between Django and other frameworks
- Selecting API framework (DRF, Django Ninja, raw views)
- Evaluating architecture patterns
- Choosing database backend
- Planning deployment strategy
- Evaluating third-party packages
- Code review for proper placement
- Onboarding developers to project architecture

## Key Decision Areas

### 1. Framework Selection

| Scenario | Recommendation |
|----------|----------------|
| Full-featured web app with admin | Django |
| API-only, high concurrency | FastAPI |
| Django + FastAPI-like API syntax | Django Ninja |
| Microservices, async-first | FastAPI |
| CMS with content editing | Django + Wagtail |
| Simple REST API | Django Ninja or FastAPI |

### 2. API Framework Selection

| Need | Recommendation |
|------|----------------|
| Full CRUD with ViewSets | Django REST Framework |
| Performance-critical API | Django Ninja |
| Auto OpenAPI docs | Django Ninja or DRF with drf-spectacular |
| Large existing DRF ecosystem | Django REST Framework |
| Modern type hints + async | Django Ninja |
| GraphQL | Graphene-Django or Strawberry |

### 3. Architecture Patterns

| Project Size | Pattern |
|--------------|---------|
| Small/MVP | Fat models, simple views |
| Medium | Service layer pattern |
| Large/Enterprise | Clean architecture / DDD-inspired |
| Microservices | Domain-driven design |

### 4. Database Selection

| Scenario | Database |
|----------|----------|
| Production, complex queries | PostgreSQL |
| Simple apps, side projects | SQLite (with Litestream) |
| Legacy MySQL infrastructure | MySQL 8+ |
| Geographic applications | PostgreSQL + PostGIS |
| Development/testing | SQLite |

### 5. Deployment Options

| Need | Platform |
|------|----------|
| Simplicity, managed | PaaS (Render, Fly.io, Railway) |
| Full control | VPS (DigitalOcean, Hetzner) |
| Enterprise, scaling | Kubernetes |
| Cost optimization | Serverless (Cloud Run, Lambda) |
| Static sites + API | Vercel/Netlify + Django API |

## LLM Usage Tips

### For Claude/GPT

1. **Context is key** - Provide project constraints (team size, budget, timeline)
2. **Be specific** - "Django REST API for e-commerce" not "web app"
3. **State trade-offs** - "Prioritize developer experience over raw performance"
4. **Include constraints** - "Must support PostgreSQL, deployed on Kubernetes"

### Effective Prompting Patterns

```
Decision: [What you're deciding]
Context: [Project type, team, constraints]
Options considered: [List of options]
Trade-offs priority: [Performance/DX/Maintenance/Cost]
```

### Anti-patterns

- Asking for "best" without context
- Ignoring team expertise
- Over-engineering for small projects
- Premature optimization

## Quick Reference

### Code Placement Decision Tree

```
What does the function do?
|
+-> Changes database? -> services/
+-> External API call? -> services/ or integrations/
+-> Pure function? -> utils/
+-> HTTP handling? -> views/
+-> Data structure? -> models/
+-> Input validation? -> serializers/
+-> Background task? -> tasks/
+-> Reusable? -> core/ or common/
```

### Package Evaluation Criteria

1. **Maintenance** - Recent commits, active issues
2. **Compatibility** - Django 5.x support
3. **Community** - GitHub stars, downloads
4. **Documentation** - Quality and completeness
5. **Test coverage** - CI passing, good coverage
6. **Security** - No known vulnerabilities

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step decision checklists |
| [examples.md](examples.md) | Real-world decision examples |
| [templates.md](templates.md) | Copy-paste decision templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted decisions |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## External Resources

### Official Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Ninja](https://django-ninja.dev/)
- [Django Packages](https://djangopackages.org/)

### Architecture Resources

- [Architecture Patterns with Python](https://www.cosmicpython.com/) - Clean architecture, DDD
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-5-0) - Best practices
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Django Design Philosophies](https://docs.djangoproject.com/en/5.2/misc/design-philosophies/)

### Comparison Resources

- [Django vs FastAPI Comparison 2025](https://medium.com/@technode/fastapi-vs-django-a-detailed-comparison-in-2025-1e70c65b9416)
- [DRF vs Django Ninja](https://www.loopwerk.io/articles/2024/drf-vs-ninja/)
- [Django Database Choices](https://medium.com/@anas-issath/best-database-for-django-in-2025-postgres-vs-mysql-explained-6a309a14390e)

### Deployment Guides

- [Django Deployment Guide](https://www.saaspegasus.com/guides/django-deployment/)
- [Django on Kubernetes](https://cloud.google.com/python/django/kubernetes-engine)
- [SQLite in Production Guide](https://alldjango.com/articles/definitive-guide-to-using-django-sqlite-in-production)

### Package Discovery

- [State of Django 2025](https://blog.jetbrains.com/pycharm/2025/10/the-state-of-django-2025/)
- [Top Django Packages 2025](https://learndjango.com/tutorials/essential-django-3rd-party-packages)
- [Django Ecosystem Page](https://www.djangoproject.com/weblog/2025/nov/02/five-ways-to-discover-django-packages/)

## Key Principles

1. **Single responsibility** - Each module has one clear purpose
2. **Dependency direction** - Views depend on services, not vice versa
3. **Testability** - Pure functions in utils, side effects in services
4. **Explicit boundaries** - Clear separation between layers
5. **Predictable location** - Any team member can find any code
6. **Framework leverage** - Use Django's batteries before reinventing

## Version Compatibility

| Component | Minimum Version (2025) |
|-----------|------------------------|
| Django | 5.0+ |
| Python | 3.11+ |
| PostgreSQL | 14+ |
| MySQL | 8.0+ |
| DRF | 3.15+ |
| Django Ninja | 1.0+ |

---

*Last updated: 2026-01-25*
*Part of faion-python-developer skill*
