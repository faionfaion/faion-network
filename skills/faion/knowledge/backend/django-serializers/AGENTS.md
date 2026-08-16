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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-serializers.py` | AST check: no `ModelSerializer` with `fields="__all__"`, no `validate_*` containing ORM calls, explicit fields | pre-commit / CI |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-service-layer]] — writes happen in services, not serializers
- [[django-selectors]] — reads happen in selectors, not serializer methods
- [[django-quality-security]] — input validation is the methodology's security baseline

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is the data crossing the HTTP boundary?" through "is this input or output?" to one of: write a `Serializer` Input pair, write a `Serializer` Output pair, or skip-this-methodology (internal helper, no API). The "must use Serializer, not ModelSerializer" branch keeps PII exposure low; the "validate() format only" branch enforces the service-layer split.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/serializer_input.py`

```python
from rest_framework import serializers


class <Entity>CreateRequest(serializers.Serializer):
    """Input contract for creating a <Entity>."""

    name = serializers.CharField(required=True, allow_blank=False, max_length=120)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(required=False, default=True)
    # secret-like inputs MUST be write_only so accidental nesting cannot leak them
    password = serializers.CharField(required=True, min_length=12, write_only=True)

    def validate_name(self, value: str) -> str:
        # SHAPE-ONLY validation. No DB, no service calls.
        if value.strip() != value:
            raise serializers.ValidationError("must not contain leading/trailing whitespace")
        return value


class <Entity>UpdateRequest(serializers.Serializer):
    """Input contract for partial updates (PATCH)."""

    name = serializers.CharField(required=False, allow_blank=False, max_length=120)
    email = serializers.EmailField(required=False)
    is_active = serializers.BooleanField(required=False)
```

### `templates/serializer_output.py`

```python
from rest_framework import serializers


class <Entity>Response(serializers.Serializer):
    """Output contract for a single <Entity>. Lists exposed fields explicitly."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    # DO NOT add password / token / secret / is_staff / mfa_secret


class <Entity>ListItem(serializers.Serializer):
    """Compact representation for list endpoints — fewer fields than detail."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class <Entity>ListResponse(serializers.Serializer):
    """List wrapper with pagination metadata."""

    count = serializers.IntegerField(read_only=True)
    next = serializers.URLField(read_only=True, allow_null=True)
    previous = serializers.URLField(read_only=True, allow_null=True)
    results = <Entity>ListItem(many=True, read_only=True)
```
