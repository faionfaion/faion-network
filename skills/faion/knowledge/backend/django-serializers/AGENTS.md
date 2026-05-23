# Django DRF Serializer Conventions

## Summary

**One-sentence:** Produce two serializers per endpoint — `EntityCreateRequest` / `EntityUpdateRequest` for input and `EntityResponse` / `EntityListResponse` for output — both subclassing `serializers.Serializer` with explicit fields and zero business logic.

**One-paragraph:** A single shared `ModelSerializer` accidentally exposes sensitive fields (password, is_staff, internal IDs) in responses and silently accepts them on input. The fix: separate Input and Output serializers, both `serializers.Serializer` (not ModelSerializer), with every field declared explicitly. Validation is shape-only — `validate_*()` and `validate()` may check format and cross-field consistency but MUST NOT query the database or call services. Nested serializers consume pre-fetched data from a selector (no own queries). Views pass `request.data` through Input, call a service, return a model wrapped in Output.

**Ефективно для:** any new DRF endpoint, any audit that fixes a "password in response" leak, any refactor moving validation out of view methods.

## Applies If (ALL must hold)

- Any Django REST Framework API endpoint that accepts input data.
- Any API endpoint that returns model data as JSON.
- Views that need to validate request payload before passing to a service.
- Endpoints with nested related data that must be serialized efficiently.

## Skip If (ANY kills it)

- Internal utility functions that manipulate data in Python — no HTTP boundary.
- Admin-only views using Django admin's built-in forms — ModelAdmin handles that.
- Django Ninja or FastAPI projects — use Pydantic schemas (see [[python-fastapi]]).

## Prerequisites

| Artifact | Format | Source |
|----------|--------|--------|
| Django model | Python | `apps/<app>/models.py` |
| Service function (write) | Python | `apps/<app>/services.py` |
| Selector function (read) | Python | `apps/<app>/selectors.py` |
| DRF installed (`djangorestframework`) | dep | repo manifest |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `django-service-layer` | serializers call services for writes |
| `django-selectors` | nested serializers consume selector output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: input/output split, no business logic, explicit fields, write_only, nested-selector | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the serializer-class spec produced + signature examples | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: identify endpoint → input → output → wire view → test | ~400 |
| `content/05-examples.xml` | optional | worked example: user-create endpoint with Input+Output serializers | ~400 |
| `content/06-decision-tree.xml` | essential | route through "modelserializer or serializer?" and "input or output?" | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Input field design | sonnet | shape and type, deterministic |
| Output field selection (PII guard) | opus | judgement on which model fields are safe to expose |
| Nested serializer wiring | sonnet | follow selector pattern |
| validate() / validate_<field> design | opus | format vs business-logic boundary needs care |

## Templates

| File | Purpose |
|------|---------|
| `templates/serializer_input.py` | Input serializer skeleton (Create + Update) |
| `templates/serializer_output.py` | Output serializer skeleton (Detail + List) |
| `templates/view_with_serializers.py` | view skeleton chaining Input → service → Output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-serializers.py` | AST check: no `ModelSerializer` with `fields="__all__"`, no `validate_*` containing ORM calls, explicit fields | pre-commit / CI |

## Related

- [[django-service-layer]] — writes happen in services, not serializers
- [[django-selectors]] — reads happen in selectors, not serializer methods
- [[django-quality-security]] — input validation is the methodology's security baseline

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is the data crossing the HTTP boundary?" through "is this input or output?" to one of: write a `Serializer` Input pair, write a `Serializer` Output pair, or skip-this-methodology (internal helper, no API). The "must use Serializer, not ModelSerializer" branch keeps PII exposure low; the "validate() format only" branch enforces the service-layer split.
