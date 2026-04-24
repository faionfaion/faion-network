# Python Web Framework Selection Checklist

**Step-by-step guide to choosing the right framework for your project.**

---

## Pre-Selection Assessment

Before evaluating frameworks, answer these questions:

### Project Scope

- [ ] What type of application am I building?
  - [ ] Full-stack web application with UI
  - [ ] REST API only
  - [ ] Microservice
  - [ ] Internal tool
  - [ ] Prototype/MVP

- [ ] What is the expected scale?
  - [ ] Small (< 1K users)
  - [ ] Medium (1K - 100K users)
  - [ ] Large (100K+ users)
  - [ ] Enterprise (millions of users)

- [ ] What is the expected traffic pattern?
  - [ ] Steady load
  - [ ] Spiky/bursty
  - [ ] Real-time heavy
  - [ ] Background job heavy

### Technical Requirements

- [ ] Do I need real-time features (WebSockets)?
- [ ] Is high concurrency required (3000+ RPS)?
- [ ] Do I need an admin panel?
- [ ] Do I need server-side rendering?
- [ ] Is API documentation critical?
- [ ] Do I need ML/AI model serving?
- [ ] Is type safety important?

### Team Considerations

- [ ] What is the team's Python experience level?
- [ ] Does the team have async programming experience?
- [ ] What frameworks does the team already know?
- [ ] What is the maintenance timeline?

---

## Framework Evaluation Checklist

### Django Evaluation

**Choose Django if most of these are true:**

| Requirement | Check |
|-------------|-------|
| Need full-stack web application | [ ] |
| Need built-in admin panel | [ ] |
| Need built-in authentication | [ ] |
| Need ORM with migrations | [ ] |
| Team prefers "batteries-included" | [ ] |
| Security features are critical | [ ] |
| Need mature, stable framework | [ ] |
| Building CMS, e-commerce, or social platform | [ ] |
| Need server-side templates | [ ] |
| Rapid development is priority | [ ] |

**Django score:** ___/10

**Warning signs for Django:**
- [ ] Pure API with no admin needed
- [ ] High concurrency (10K+ concurrent connections)
- [ ] Microservices architecture
- [ ] Team wants maximum flexibility
- [ ] Need native async throughout

---

### FastAPI Evaluation

**Choose FastAPI if most of these are true:**

| Requirement | Check |
|-------------|-------|
| Building REST API or microservice | [ ] |
| High performance is critical | [ ] |
| Need native async support | [ ] |
| Need automatic API documentation | [ ] |
| Serving ML/AI models | [ ] |
| Need WebSocket support | [ ] |
| Type safety and validation important | [ ] |
| Building real-time application | [ ] |
| Team knows modern Python (3.8+) | [ ] |
| Microservices architecture | [ ] |

**FastAPI score:** ___/10

**Warning signs for FastAPI:**
- [ ] Need built-in admin panel
- [ ] Need server-side rendering
- [ ] Team lacks async experience
- [ ] Need mature, battle-tested ecosystem
- [ ] Building content-heavy website

---

### Flask Evaluation

**Choose Flask if most of these are true:**

| Requirement | Check |
|-------------|-------|
| Building small application | [ ] |
| Need maximum flexibility | [ ] |
| Building prototype or MVP | [ ] |
| Team is learning Python web | [ ] |
| Need custom architecture | [ ] |
| Building internal tool | [ ] |
| Simple API without complex needs | [ ] |
| Minimal dependencies preferred | [ ] |
| Control over all components | [ ] |
| Quick setup needed | [ ] |

**Flask score:** ___/10

**Warning signs for Flask:**
- [ ] Large-scale application
- [ ] Need lots of built-in features
- [ ] Team lacks security expertise
- [ ] High concurrency requirements
- [ ] Need real-time WebSockets

---

## Decision Matrix

After scoring, use this matrix:

| Highest Score | Recommendation |
|---------------|----------------|
| Django 7+ | Start with Django |
| FastAPI 7+ | Start with FastAPI |
| Flask 7+ | Start with Flask |
| Two tied | See "Tie-Breakers" below |
| All low (<5) | Consider hybrid approach |

### Tie-Breakers

**Django vs FastAPI tie:**
- Need admin panel? → Django
- Need high performance? → FastAPI
- Building full-stack? → Django
- Building API only? → FastAPI

**Django vs Flask tie:**
- Need quick setup? → Flask
- Need built-in features? → Django
- Building large app? → Django
- Building prototype? → Flask

**FastAPI vs Flask tie:**
- Need async? → FastAPI
- Need simplicity? → Flask
- Need auto-docs? → FastAPI
- Learning web dev? → Flask

---

## Project-Specific Checklists

### REST API Project

- [ ] Define expected RPS
- [ ] Define authentication method
- [ ] Define API versioning strategy
- [ ] Define documentation requirements
- [ ] Define rate limiting needs
- [ ] Define background task requirements

**Recommendation:** FastAPI (performance) or Django REST Framework (full-featured)

---

### Full-Stack Web Application

- [ ] Define admin panel requirements
- [ ] Define user authentication needs
- [ ] Define template/frontend strategy
- [ ] Define database requirements
- [ ] Define real-time features
- [ ] Define content management needs

**Recommendation:** Django

---

### Microservice

- [ ] Define service boundaries
- [ ] Define inter-service communication
- [ ] Define deployment strategy
- [ ] Define monitoring requirements
- [ ] Define scaling requirements
- [ ] Define database per service or shared

**Recommendation:** FastAPI

---

### ML Model Serving

- [ ] Define model loading strategy
- [ ] Define inference latency requirements
- [ ] Define batch vs real-time inference
- [ ] Define model versioning
- [ ] Define monitoring/logging
- [ ] Define scaling strategy

**Recommendation:** FastAPI

---

### Internal Tool

- [ ] Define user count
- [ ] Define security requirements
- [ ] Define admin features
- [ ] Define maintenance expectations
- [ ] Define integration requirements
- [ ] Define simplicity vs features tradeoff

**Recommendation:** Flask (simple) or Django (admin-heavy)

---

## Post-Selection Checklist

After choosing a framework:

### Django

- [ ] Set up project structure (apps, config)
- [ ] Configure settings (base, dev, prod)
- [ ] Set up database and migrations
- [ ] Configure authentication
- [ ] Set up admin customization
- [ ] Choose API approach (DRF, Ninja)
- [ ] Set up testing (pytest-django)
- [ ] Configure deployment (Gunicorn/Uvicorn)

### FastAPI

- [ ] Set up project structure (routers, schemas)
- [ ] Configure Pydantic settings
- [ ] Set up database (SQLAlchemy async)
- [ ] Configure dependency injection
- [ ] Set up authentication
- [ ] Configure OpenAPI documentation
- [ ] Set up testing (pytest, httpx)
- [ ] Configure deployment (Uvicorn)

### Flask

- [ ] Set up project structure (blueprints)
- [ ] Configure Flask settings
- [ ] Choose and configure extensions
- [ ] Set up database (SQLAlchemy)
- [ ] Configure authentication (Flask-Login)
- [ ] Set up API documentation (Flasgger)
- [ ] Set up testing (pytest)
- [ ] Configure deployment (Gunicorn)

---

## Red Flags Checklist

### Stop and Reconsider If:

- [ ] Choosing framework based on hype alone
- [ ] Team has no experience with chosen framework
- [ ] Framework doesn't match project requirements
- [ ] Ignoring scalability requirements
- [ ] Not considering maintenance burden
- [ ] Choosing based on single feature
- [ ] Not evaluating team velocity impact

---

## Final Decision Template

```
Project: _______________
Date: _______________
Decision Maker: _______________

Selected Framework: _______________

Scores:
- Django: ___/10
- FastAPI: ___/10
- Flask: ___/10

Key Reasons:
1. _______________
2. _______________
3. _______________

Risk Factors:
1. _______________
2. _______________

Mitigation Plan:
1. _______________
2. _______________

Approved By: _______________
```

---

## Quick Reference Cards

### When to Immediately Choose Django

- [ ] Need admin panel in < 1 week
- [ ] Building CMS or e-commerce
- [ ] Enterprise with security requirements
- [ ] Team knows Django already

### When to Immediately Choose FastAPI

- [ ] Building ML model serving API
- [ ] Need 3000+ RPS
- [ ] WebSocket-heavy application
- [ ] Microservices architecture

### When to Immediately Choose Flask

- [ ] Building in < 1 day
- [ ] Prototype or proof of concept
- [ ] Internal tool for < 10 users
- [ ] Learning Python web development

---

*Framework Selection Checklist v1.0*
*Part of Python Web Frameworks methodology*
