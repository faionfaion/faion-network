# Django Decision Templates

Copy-paste templates for documenting Django architecture decisions.

---

## Architecture Decision Record (ADR) Template

Use this template to document significant architecture decisions.

```markdown
# ADR-{NUMBER}: {TITLE}

## Status

{Proposed | Accepted | Deprecated | Superseded by ADR-XXX}

## Context

{Describe the issue motivating this decision. What problem are we solving?}

## Decision

{Describe the decision and the approach chosen.}

## Alternatives Considered

### Option 1: {Name}

**Pros:**
- {Pro 1}
- {Pro 2}

**Cons:**
- {Con 1}
- {Con 2}

### Option 2: {Name}

**Pros:**
- {Pro 1}
- {Pro 2}

**Cons:**
- {Con 1}
- {Con 2}

## Consequences

### Positive

- {Positive consequence 1}
- {Positive consequence 2}

### Negative

- {Negative consequence 1}
- {Negative consequence 2}

## References

- {Link 1}
- {Link 2}
```

---

## Framework Selection ADR

```markdown
# ADR-001: Web Framework Selection

## Status

Accepted

## Context

We need to select a web framework for {PROJECT_NAME}. The project requires:
- {Requirement 1: e.g., Admin interface for content management}
- {Requirement 2: e.g., REST API for mobile apps}
- {Requirement 3: e.g., User authentication with social login}
- {Requirement 4: e.g., Background task processing}

Team expertise: {Django/FastAPI/Flask experience level}
Timeline: {X months to MVP}
Expected scale: {X users, X requests/second}

## Decision

We will use **Django** with **{DRF | Django Ninja | raw views}** for the following reasons:

1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

## Alternatives Considered

### FastAPI

**Pros:**
- Native async support
- Automatic OpenAPI docs
- High performance

**Cons:**
- No built-in admin
- Need to set up ORM separately
- Team has limited experience

### Flask

**Pros:**
- Lightweight
- Flexible

**Cons:**
- Need many extensions
- No built-in ORM
- More decisions required

## Consequences

### Positive

- Team can start immediately with familiar framework
- Django admin saves {X weeks} of development
- Rich ecosystem of packages available

### Negative

- Slightly lower performance than FastAPI for API-only use cases
- Some boilerplate for simple endpoints
```

---

## API Framework Selection ADR

```markdown
# ADR-002: API Framework Selection

## Status

Accepted

## Context

We need to build a REST API for {PROJECT_NAME}. Requirements:
- {Requirement 1: e.g., Complex nested resources}
- {Requirement 2: e.g., OpenAPI documentation}
- {Requirement 3: e.g., High throughput endpoints}
- {Requirement 4: e.g., Type safety}

## Decision

We will use **{Django REST Framework | Django Ninja}**.

### DRF Selection Reasoning

1. Need ViewSets for standard CRUD operations
2. Complex serialization with nested relationships
3. Team experienced with DRF
4. Need browsable API for debugging

### Django Ninja Selection Reasoning

1. Type hints catch errors at development time
2. Auto-generated OpenAPI docs required
3. Performance is critical
4. Simpler mental model for our API structure

## Alternatives Considered

### Django REST Framework

| Aspect | Rating |
|--------|--------|
| Maturity | Excellent |
| Performance | Good |
| Type Safety | Optional |
| Documentation | Needs drf-spectacular |
| Learning Curve | Moderate |

### Django Ninja

| Aspect | Rating |
|--------|--------|
| Maturity | Good |
| Performance | Excellent |
| Type Safety | Native |
| Documentation | Built-in |
| Learning Curve | Low |

### Raw Django Views

| Aspect | Rating |
|--------|--------|
| Simplicity | High |
| Features | Limited |
| Best For | Very simple APIs |

## Consequences

{Describe implications of the choice}
```

---

## Database Selection ADR

```markdown
# ADR-003: Database Selection

## Status

Accepted

## Context

We need to select a database for {PROJECT_NAME}. Considerations:
- Data model complexity: {Simple | Medium | Complex}
- Query patterns: {Read-heavy | Write-heavy | Balanced}
- Special requirements: {Full-text search | JSON | Geographic | Arrays}
- Scale expectations: {X GB data, X queries/second}
- Team expertise: {PostgreSQL | MySQL | SQLite experience}
- Budget: {Managed DB budget | Self-hosted}

## Decision

We will use **{PostgreSQL | MySQL | SQLite}** because:

1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

### PostgreSQL Selection Reasoning

- Need advanced features: {JSONB, full-text search, CTEs}
- Production-ready with excellent Django support
- Best feature compatibility with Django ORM

### SQLite Selection Reasoning

- Development/prototype phase
- Read-heavy workload with single server
- Simplicity and zero configuration priority
- Will migrate to PostgreSQL when needed

### MySQL Selection Reasoning

- Existing MySQL infrastructure
- Team expertise
- Adequate for our query patterns

## Migration Path

If starting with SQLite:
1. Development: SQLite
2. Staging: PostgreSQL (to catch compatibility issues)
3. Production: PostgreSQL

## Consequences

### Positive

- {Positive 1}
- {Positive 2}

### Negative

- {Negative 1}
- {Negative 2}
```

---

## Deployment Architecture ADR

```markdown
# ADR-004: Deployment Architecture

## Status

Accepted

## Context

We need to determine the deployment strategy for {PROJECT_NAME}. Factors:
- Team DevOps expertise: {None | Basic | Advanced}
- Budget: {$ | $$ | $$$}
- Scale requirements: {Fixed | Variable | Unpredictable}
- Compliance: {None | SOC2 | HIPAA | PCI}
- Release frequency: {Weekly | Daily | Continuous}

## Decision

We will deploy on **{PaaS Platform | VPS | Kubernetes}**.

### PaaS Selection (Render/Fly.io/Railway)

**Reasoning:**
- Team lacks DevOps expertise
- Need to focus on product, not infrastructure
- Acceptable cost for current scale
- Easy preview environments

**Provider: {Render | Fly.io | Railway | Heroku}**

### VPS Selection (DigitalOcean/Hetzner)

**Reasoning:**
- Cost optimization priority
- Need full control
- Team has Linux experience
- Static traffic patterns

**Provider: {DigitalOcean | Hetzner | Linode}**

### Kubernetes Selection

**Reasoning:**
- Enterprise requirements
- Multiple services to orchestrate
- Auto-scaling required
- Company already has K8s infrastructure

## Architecture Diagram

```
{Include ASCII or link to diagram}
```

## Consequences

### Operational

- {Ops consequence 1}
- {Ops consequence 2}

### Cost

- Estimated monthly cost: ${X}
- Cost drivers: {Compute | Database | Bandwidth}

### Maintenance

- {Maintenance requirement 1}
- {Maintenance requirement 2}
```

---

## Architecture Pattern ADR

```markdown
# ADR-005: Application Architecture Pattern

## Status

Accepted

## Context

We need to establish the code organization pattern for {PROJECT_NAME}. Factors:
- Project size: {Small | Medium | Large} ({X apps, X models})
- Team size: {X developers}
- Domain complexity: {Simple | Complex}
- Expected growth: {Stable | Growing | Rapid}
- Testing requirements: {Basic | Comprehensive}

## Decision

We will use **{Simple/Fat Models | Service Layer | Clean Architecture}**.

### Simple Architecture (Fat Models)

```
app/
  models.py      # Business logic in models
  views.py       # Thin views
  forms.py       # Validation
```

**Best for:**
- Small projects (< 5 apps)
- 1-2 developers
- Simple business logic
- Quick prototypes

### Service Layer Architecture

```
app/
  models.py       # Data structure only
  services.py     # Business logic
  views.py        # HTTP handling
  serializers.py  # Input/output
```

**Best for:**
- Medium projects (5-15 apps)
- 3-10 developers
- Complex business logic
- Multiple entry points

### Clean Architecture

```
app/
  domain/
    entities.py
    value_objects.py
  application/
    services.py
    interfaces.py
  infrastructure/
    repositories.py
    gateways.py
  api/
    endpoints.py
```

**Best for:**
- Large projects (> 15 apps)
- Enterprise requirements
- Complex domain logic
- Long-term maintenance priority

## Layer Responsibilities

| Layer | Responsibility | Dependencies |
|-------|----------------|--------------|
| views/ | HTTP handling | services, serializers |
| services/ | Business logic | models, utils |
| utils/ | Pure functions | None |
| models/ | Data structure | Django ORM |

## Consequences

### Code Organization

- {Organization consequence 1}
- {Organization consequence 2}

### Testing

- {Testing consequence 1}
- {Testing consequence 2}

### Onboarding

- {Onboarding consequence 1}
```

---

## Package Evaluation Template

```markdown
# Package Evaluation: {PACKAGE_NAME}

## Purpose

{What problem does this package solve?}

## Evaluation Criteria

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Maintenance | | Last commit: {date} |
| Django Compatibility | | Supports Django {version} |
| Python Compatibility | | Supports Python {version} |
| Documentation | | |
| Test Coverage | | |
| Community | | {X} GitHub stars, {Y} PyPI downloads/month |
| Security | | Known vulnerabilities: {Yes/No} |
| License | | {License type} |

## Alternatives Compared

| Package | Pros | Cons |
|---------|------|------|
| {Package 1} | | |
| {Package 2} | | |
| {Package 3} | | |

## Decision

**{Include | Exclude}** this package because:

1. {Reason 1}
2. {Reason 2}

## Integration Notes

```python
# Installation
pip install {package-name}

# settings.py
INSTALLED_APPS = [
    ...
    '{package_app}',
]

# Configuration
{PACKAGE}_SETTING = {
    'option': 'value',
}
```

## Risks

- {Risk 1}
- {Risk 2}

## Mitigation

- {Mitigation 1}
- {Mitigation 2}
```

---

## Code Placement Decision Template

```markdown
# Code Placement Decision

## Function/Class

```python
def {function_name}({params}):
    """
    {Description}
    """
    ...
```

## Decision Checklist

- [ ] Writes to database? -> services/
- [ ] Calls external API? -> services/ or integrations/
- [ ] Pure function? -> utils/
- [ ] Handles HTTP? -> views/
- [ ] Defines data? -> models/
- [ ] Validates input? -> serializers/
- [ ] Background task? -> tasks/
- [ ] Reusable? -> core/

## Placement Decision

**Location:** `{app}/{layer}/{file}.py`

**Reasoning:**
{Why this location is appropriate}

## Example

```python
# {path}

{code}
```
```

---

## Project Setup Template

```markdown
# {PROJECT_NAME} Technical Decisions

## Framework Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | Django {version} | |
| API | {DRF | Ninja | Views} | |
| Database | {PostgreSQL | MySQL | SQLite} | |
| Cache | {Redis | Memcached | None} | |
| Task Queue | {Celery | Django-Q | None} | |
| Search | {Elasticsearch | PostgreSQL FTS | None} | |

## Architecture

**Pattern:** {Simple | Service Layer | Clean}

**Project Structure:**
```
{project}/
  apps/
    {app1}/
    {app2}/
  core/
  config/
```

## Packages

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| {package} | {version} | {purpose} |

### Development Only

| Package | Version | Purpose |
|---------|---------|---------|
| django-debug-toolbar | {version} | Debugging |
| pytest-django | {version} | Testing |

## Deployment

| Environment | Platform | Database |
|-------------|----------|----------|
| Development | Local | SQLite |
| Staging | {Platform} | {DB} |
| Production | {Platform} | {DB} |

## ADRs

1. [ADR-001: Framework Selection](docs/adr/001-framework.md)
2. [ADR-002: API Framework](docs/adr/002-api-framework.md)
3. [ADR-003: Database](docs/adr/003-database.md)
4. [ADR-004: Deployment](docs/adr/004-deployment.md)
5. [ADR-005: Architecture](docs/adr/005-architecture.md)
```

---

## Service Function Template

```python
# {app}/services.py
"""
Business logic for {domain}.

All functions that:
- Write to database
- Orchestrate multiple operations
- Call external services
- Contain business rules
"""
from django.db import transaction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import {Model}


@transaction.atomic
def create_{entity}(
    # Required parameters
    {param1}: {type1},
    {param2}: {type2},
    *,
    # Optional parameters (keyword-only)
    {param3}: {type3} | None = None,
) -> "{Model}":
    """
    Create a new {entity}.

    Args:
        {param1}: {description}
        {param2}: {description}
        {param3}: {description}

    Returns:
        Created {Model} instance.

    Raises:
        ValidationError: If {condition}.
    """
    from .models import {Model}

    # Validation
    if not {condition}:
        raise ValidationError("{message}")

    # Create
    instance = {Model}.objects.create(
        {field1}={param1},
        {field2}={param2},
    )

    # Side effects
    {side_effect_function}(instance)

    return instance
```

---

## Utils Function Template

```python
# {app}/utils.py
"""
Pure utility functions for {domain}.

All functions that:
- Have no side effects
- Don't access database
- Don't call external services
- Are deterministic
"""
from decimal import Decimal


def calculate_{thing}(
    {param1}: {type1},
    {param2}: {type2},
    *,
    {param3}: {type3} = {default},
) -> {return_type}:
    """
    Calculate {thing}.

    Pure function - no side effects, no database access.

    Args:
        {param1}: {description}
        {param2}: {description}
        {param3}: {description}

    Returns:
        {description}

    Examples:
        >>> calculate_{thing}({example_input})
        {example_output}
    """
    # Implementation
    result = {calculation}

    return result
```

---

## Django Ninja Endpoint Template

```python
# {app}/api.py
from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from .schemas import {Entity}In, {Entity}Out
from . import services


router = Router(tags=["{domain}"])


@router.post("/", response={201: {Entity}Out})
def create_{entity}(request, payload: {Entity}In):
    """Create a new {entity}."""
    instance = services.create_{entity}(**payload.dict())
    return 201, instance


@router.get("/{id}", response={Entity}Out)
def get_{entity}(request, id: int):
    """Get {entity} by ID."""
    from .models import {Model}
    return get_object_or_404({Model}, id=id)


@router.get("/", response=List[{Entity}Out])
def list_{entities}(request, limit: int = 100, offset: int = 0):
    """List all {entities}."""
    from .models import {Model}
    return {Model}.objects.all()[offset:offset + limit]
```

---

*Use these templates as starting points. Adapt to your project's needs.*
