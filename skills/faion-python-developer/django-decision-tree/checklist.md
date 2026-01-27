# Django Decision Checklist

Step-by-step checklists for making Django architecture decisions.

---

## 1. Framework Selection Checklist

### Should I Use Django?

- [ ] **Web application** - Building a website, not just CLI/background service
- [ ] **Database-driven** - Need ORM for data persistence
- [ ] **Admin interface** - Would benefit from Django admin
- [ ] **Authentication** - Need user accounts, permissions
- [ ] **Forms** - Complex form handling required
- [ ] **Templates** - Server-side rendering needed (even if also API)
- [ ] **Batteries included** - Value built-in features over assembling components

**Score: 5+ checks = Strong Django candidate**

### Django vs FastAPI Decision

| Factor | Choose Django | Choose FastAPI |
|--------|---------------|----------------|
| Admin panel needed | Yes | No |
| Server-side templates | Yes | No |
| API-only project | Consider Django Ninja | Yes |
| Async-first design | Django 5+ supports | Native |
| Team Django experience | Yes | No |
| Need ORM | Django ORM | SQLAlchemy |
| Rapid prototyping | Yes | Yes |
| Microservices | Possible | Better fit |

### When NOT to Use Django

- [ ] Real-time only (WebSocket-heavy) - Consider Channels or FastAPI
- [ ] Extremely high concurrency - Consider FastAPI/Starlette
- [ ] Minimal API (< 5 endpoints) - Consider FastAPI/Flask
- [ ] No database needed - Consider Flask/FastAPI
- [ ] Team has no Python experience - Consider their expertise

---

## 2. API Framework Checklist

### Django REST Framework vs Django Ninja

| Criterion | DRF | Django Ninja | Winner |
|-----------|-----|--------------|--------|
| Maturity | 13+ years | 4+ years | DRF |
| Performance | Good | Excellent | Ninja |
| Type hints | Optional | Native | Ninja |
| Auto docs | drf-spectacular | Built-in | Ninja |
| ViewSets | Native | Manual | DRF |
| Ecosystem | Extensive | Growing | DRF |
| Learning curve | Moderate | Low | Ninja |
| Async support | Limited | Native | Ninja |

### Choose DRF When

- [ ] Large existing DRF codebase
- [ ] Need ViewSets for CRUD
- [ ] Team experienced with DRF
- [ ] Need extensive third-party packages
- [ ] Complex nested serializers
- [ ] Browsable API important

### Choose Django Ninja When

- [ ] New project, no legacy
- [ ] Performance is priority
- [ ] Team likes type hints
- [ ] FastAPI-like DX preferred
- [ ] Auto OpenAPI docs required
- [ ] Simpler, flatter API structure

### Choose Raw Django Views When

- [ ] Very simple API (2-3 endpoints)
- [ ] Internal tool only
- [ ] Minimal serialization needed
- [ ] Want zero dependencies

---

## 3. Architecture Pattern Checklist

### Simple Architecture (Default)

Best for: Small projects, MVPs, prototypes

- [ ] < 5 Django apps
- [ ] < 10 models
- [ ] 1-2 developers
- [ ] Quick time to market
- [ ] Simple business logic

**Pattern:** Fat models, thin views, form validation

### Service Layer Architecture

Best for: Medium projects, growing teams

- [ ] 5-15 Django apps
- [ ] 10-50 models
- [ ] 3-10 developers
- [ ] Complex business logic
- [ ] Multiple entry points (API + web + CLI)

**Pattern:** Services for business logic, thin models/views

### Clean Architecture / DDD-Inspired

Best for: Large enterprise projects

- [ ] > 15 Django apps
- [ ] > 50 models
- [ ] > 10 developers
- [ ] Complex domain logic
- [ ] Multiple bounded contexts
- [ ] Long-term maintenance priority

**Pattern:** Domain layer, application layer, infrastructure layer

### Architecture Decision Flowchart

```
Start
|
v
Project size?
|
+-> Small (< 5 apps) --> Fat Models
|
+-> Medium (5-15 apps) --> Service Layer
|
+-> Large (> 15 apps) --> Clean Architecture
```

---

## 4. Database Selection Checklist

### PostgreSQL Checklist

Choose PostgreSQL when:

- [ ] Production environment
- [ ] Complex queries (CTEs, window functions)
- [ ] Full-text search needed
- [ ] JSON/JSONB fields required
- [ ] Geographic data (PostGIS)
- [ ] Array fields useful
- [ ] Advanced constraints needed
- [ ] High write concurrency

### SQLite Checklist

Choose SQLite when:

- [ ] Development/testing environment
- [ ] Read-heavy workload
- [ ] Single server deployment
- [ ] Side project / prototype
- [ ] Simplicity priority
- [ ] No concurrent writes
- [ ] Budget constraints

### MySQL Checklist

Choose MySQL when:

- [ ] Existing MySQL infrastructure
- [ ] Team MySQL expertise
- [ ] Simple queries sufficient
- [ ] Read replicas needed
- [ ] AWS RDS MySQL preferred

### Database Decision Matrix

| Need | PostgreSQL | MySQL | SQLite |
|------|------------|-------|--------|
| Production | Yes | Yes | Careful |
| Full-text search | Native | Plugin | Limited |
| JSON fields | Excellent | Good | Basic |
| Geographic | PostGIS | Limited | No |
| Simplicity | Medium | Medium | High |
| Scaling | Excellent | Good | Limited |
| Django support | Best | Good | Good |

---

## 5. Deployment Checklist

### PaaS vs VPS Decision

| Factor | PaaS | VPS |
|--------|------|-----|
| Simplicity | High | Low |
| Control | Low | High |
| Cost (small) | Higher | Lower |
| Cost (scale) | Higher | Lower |
| Maintenance | Managed | Manual |
| Learning curve | Low | High |

### PaaS Selection Checklist

- [ ] **Render** - Simple, generous free tier
- [ ] **Fly.io** - Edge deployment, Docker-based
- [ ] **Railway** - Developer-friendly, GitHub integration
- [ ] **Heroku** - Battle-tested, extensive add-ons
- [ ] **DigitalOcean App Platform** - Good balance

### VPS Provider Checklist

- [ ] **DigitalOcean** - Simple, good docs
- [ ] **Hetzner** - Best price/performance
- [ ] **Linode** - Reliable, good support
- [ ] **Vultr** - Many locations
- [ ] **AWS EC2** - Enterprise, complex

### Kubernetes Checklist

Consider Kubernetes when:

- [ ] Need horizontal scaling
- [ ] Multiple services/microservices
- [ ] Zero-downtime deployments required
- [ ] Team has K8s experience
- [ ] Cloud-native architecture
- [ ] High availability required

### Serverless Checklist

Consider serverless when:

- [ ] Highly variable traffic
- [ ] Cost optimization priority
- [ ] Cold start acceptable
- [ ] Stateless application
- [ ] Event-driven architecture

---

## 6. Third-Party Package Evaluation

### Package Quality Checklist

Before adding a package, verify:

- [ ] **Active maintenance** - Commits within 6 months
- [ ] **Django compatibility** - Supports Django 5.x
- [ ] **Python compatibility** - Supports Python 3.11+
- [ ] **Documentation** - Clear, comprehensive docs
- [ ] **Test coverage** - CI passing, good coverage
- [ ] **Community** - GitHub stars, PyPI downloads
- [ ] **Security** - No known vulnerabilities
- [ ] **License** - Compatible with your project
- [ ] **Alternatives** - Compared to other options
- [ ] **Necessity** - Can't be done with Django built-ins

### Essential Packages Checklist (2025)

| Category | Package | Purpose |
|----------|---------|---------|
| API | django-rest-framework | REST API |
| API | django-ninja | FastAPI-like API |
| Debug | django-debug-toolbar | Debug panel |
| Auth | django-allauth | Authentication |
| CORS | django-cors-headers | CORS handling |
| Filter | django-filter | Query filtering |
| Tasks | celery | Background tasks |
| Extensions | django-extensions | Dev utilities |
| Environment | django-environ | Environment vars |
| Storage | django-storages | Cloud storage |

### Package Risk Assessment

| Risk Level | Indicators |
|------------|------------|
| Low | > 5k stars, active, documented |
| Medium | 1-5k stars, maintained |
| High | < 1k stars, no recent commits |
| Critical | Abandoned, security issues |

---

## 7. Code Placement Checklist

### Function Placement Decision

For each new function, answer:

1. **Does it write to database?**
   - [ ] Yes -> `services/`
   - [ ] No -> Continue

2. **Does it call external API?**
   - [ ] Yes -> `services/` or `integrations/`
   - [ ] No -> Continue

3. **Is it a pure function (no side effects)?**
   - [ ] Yes -> `utils/`
   - [ ] No -> Continue

4. **Does it handle HTTP request/response?**
   - [ ] Yes -> `views/`
   - [ ] No -> Continue

5. **Does it define data structure?**
   - [ ] Yes -> `models/`
   - [ ] No -> Continue

6. **Does it validate input data?**
   - [ ] Yes -> `serializers/` or `forms/`
   - [ ] No -> Continue

7. **Is it a background task?**
   - [ ] Yes -> `tasks/`
   - [ ] No -> Continue

8. **Is it reusable across apps?**
   - [ ] Yes -> `core/` or `common/`
   - [ ] No -> Place in relevant app

### Layer Dependencies

Correct dependency direction:

```
views/ -> services/ -> utils/
         -> models/
         -> integrations/

serializers/ -> models/

tasks/ -> services/
```

Never:
- [ ] utils/ importing from services/
- [ ] models/ importing from views/
- [ ] services/ importing from views/

---

## 8. Pre-Project Decision Summary

Complete before starting new Django project:

### Framework

- [ ] Django is the right choice (see checklist 1)
- [ ] API framework selected: [ ] DRF / [ ] Ninja / [ ] Views only
- [ ] Architecture pattern selected: [ ] Simple / [ ] Service / [ ] Clean

### Database

- [ ] Database selected: [ ] PostgreSQL / [ ] MySQL / [ ] SQLite
- [ ] Migration strategy defined
- [ ] Backup strategy defined

### Deployment

- [ ] Platform selected: [ ] PaaS / [ ] VPS / [ ] Kubernetes
- [ ] Provider selected: _____________
- [ ] CI/CD approach defined

### Packages

- [ ] Essential packages identified
- [ ] All packages evaluated against checklist
- [ ] No unnecessary dependencies

### Documentation

- [ ] Architecture decision records (ADRs) created
- [ ] Development setup documented
- [ ] Deployment process documented

---

*Use these checklists as living documents. Revisit decisions as project evolves.*
