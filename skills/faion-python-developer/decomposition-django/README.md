# Django Decomposition Patterns

LLM-friendly code organization for Django projects.

---

## When to Decompose

| Signal | Action |
|--------|--------|
| `models.py` > 300 lines | Split into `models/` package |
| `views.py` > 200 lines | Split into `views/` package |
| Business logic in views | Extract to `services/` |
| Complex queries repeated | Extract to `selectors/` |
| 3+ apps share logic | Create `core/` app |
| Fat models with side effects | Move logic to services |

---

## Django-Specific Decomposition Patterns

### The HackSoft Pattern (Services + Selectors)

The most widely adopted pattern for Django projects. Core principles:

| Layer | Purpose | Contains |
|-------|---------|----------|
| **Services** | Write operations | Business logic, mutations, side effects |
| **Selectors** | Read operations | Queries, filters, aggregations |
| **Models** | Data definition | Fields, properties, validation |
| **Views** | HTTP handling | Request/response, serialization |

```
app/
├── models/           # Data layer (thin)
├── services/         # Write operations
├── selectors/        # Read operations
├── serializers/      # API I/O
├── views/            # HTTP layer (thin)
└── tests/
```

### Clean Architecture Pattern

Framework-agnostic business logic:

```
project/
├── domain/           # Core entities (no Django imports)
├── application/      # Use cases (services)
├── infrastructure/   # Django ORM, external APIs
└── interface/        # Views, serializers
```

**When to use:** Large teams, potential framework migration, complex domain logic.

### Domain-Driven Design (DDD)

Organize by business domain, not technical layer:

```
project/
├── users/            # User bounded context
├── orders/           # Order bounded context
├── payments/         # Payment bounded context
└── shared/           # Cross-domain utilities
```

---

## LLM Context Considerations

### File Size Guidelines

LLM coding agents work best with focused, single-purpose files:

| File Type | Target Lines | Max Lines | Why |
|-----------|--------------|-----------|-----|
| Model | 50-80 | 150 | One model per file |
| Service | 80-120 | 200 | One domain per file |
| Selector | 40-60 | 100 | Related queries |
| View | 60-80 | 150 | One resource |
| Serializer | 60-80 | 120 | One model/response |
| Test | 100-150 | 300 | One module |

### Context Window Optimization

**For Claude Code (200k tokens):**
- Can analyze entire Django app at once
- Use `CLAUDE.md` files in each app for context
- Hierarchical rules: root `CLAUDE.md` + app-specific

**For Cursor/Copilot:**
- Use `.cursor/rules/` for Django conventions
- Index entire project for multi-file edits
- Break large migrations into smaller files

### File Organization for AI Tools

```
myproject/
├── CLAUDE.md               # Project-wide Django conventions
├── apps/
│   ├── users/
│   │   ├── CLAUDE.md       # User app specifics
│   │   ├── models/
│   │   ├── services/
│   │   └── ...
│   └── orders/
│       ├── CLAUDE.md       # Order app specifics
│       └── ...
└── .cursor/
    └── rules/
        └── django.mdc      # Cursor Django rules
```

---

## Django REST Framework Patterns

### ViewSet Decomposition

**Anti-pattern:** Monolithic ViewSet with 500+ lines

**Pattern:** Split by action type

```
views/
├── __init__.py
├── user_crud_views.py      # list, create, retrieve, update, destroy
├── user_action_views.py    # @action methods (activate, deactivate)
└── user_nested_views.py    # Nested resources (/users/{id}/orders)
```

### Serializer Organization

```
serializers/
├── __init__.py
├── user_read.py            # UserListSerializer, UserDetailSerializer
├── user_write.py           # UserCreateSerializer, UserUpdateSerializer
└── user_nested.py          # UserOrderSerializer, UserProfileSerializer
```

### Permission Modularization

```python
# permissions.py (~30-50 lines)
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
```

---

## Django Extensions Tips

### django-extensions

```bash
# Visualize model relationships (helps LLM understand structure)
python manage.py graph_models -a -o models.png

# Show URL patterns (context for LLM)
python manage.py show_urls

# Generate model diagram as text
python manage.py show_models
```

### django-debug-toolbar

Profile queries before/after decomposition:

```python
# settings/development.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
```

---

## Key Principles

1. **Service Layer** - Business logic extracted from views
2. **Selectors** - Read-only query methods
3. **Thin Models** - Only ORM-specific logic
4. **Thin Views** - Only HTTP request/response handling
5. **Dataclasses** - Explicit input/output contracts

---

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
- [Django Documentation](https://docs.djangoproject.com/) - Official Django docs
- [Django REST Framework](https://www.django-rest-framework.org/) - DRF official docs

### Best Practices Guides
- [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide) - Services/selectors pattern
- [HackSoft Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example) - Working example
- [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x) - Comprehensive best practices

### Architecture Patterns
- [Clean Architecture in Django](https://medium.com/21buttons-tech/clean-architecture-in-django-d326a4ab86a9) - 21 Buttons approach
- [Architecture Patterns with Python](https://www.cosmicpython.com/) - Clean architecture book
- [Django Clean Architecture Template](https://github.com/sdediego/django-clean-architecture) - Project template
- [DRF Clean Architecture Template](https://github.com/onlythompson/drf_api_project_template) - DDD + Clean Architecture

### LLM Coding Workflows
- [Addy Osmani - LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/) - AI coding best practices
- [Project Structure for AI Tools](https://developertoolkit.ai/en/shared-workflows/context-management/file-organization/) - File organization for AI
- [Django + LLMs Guide](https://medium.com/@mhkocaoglan/django-and-large-language-models-a-comprehensive-guide-9391eb52e6f2) - Integrating LLMs with Django

### Tools
- [drf-service-layer](https://github.com/qu3vipon/drf-service-layer) - Service layer package for DRF
- [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django) - Production-ready Django template

---

## Related

- [checklist.md](checklist.md) - Step-by-step decomposition checklist
- [examples.md](examples.md) - Real-world decomposition examples
- [templates.md](templates.md) - Code templates and snippets
- [llm-prompts.md](llm-prompts.md) - Effective prompts for Django development
- [../django-services.md](../django-services.md) - Django service layer details
- [../django-coding-standards.md](../django-coding-standards.md) - Django coding standards
