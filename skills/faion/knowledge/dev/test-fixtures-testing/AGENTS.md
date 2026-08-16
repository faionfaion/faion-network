# Test Fixtures

## Summary

**One-sentence:** Produces a fixture-design config (Factory Boy + scope choices + rollback strategy + xdist isolation) for pytest/pytest-django suites.

**One-paragraph:** Poor fixture design causes the most persistent test-suite problems: Mystery Guest (data appearing from nowhere), God Fixture (one fixture creates everything), scope mismatches, and Sequence collisions under xdist. This methodology emits a fixture-design config that pins the Factory/Builder/Object-Mother choice per model, scope per fixture, transactional rollback wiring, and a worker-id-aware DB setup for parallel runs.

**Ефективно для:** Python backend whose pytest suite has 3+ "magic" autouse fixtures, where new contributors can't tell which fixture creates which row.

## Applies If (ALL must hold)

- Designing pytest fixtures for a new project or refactoring existing ones.
- Setting up Factory Boy for Django/SQLAlchemy model factories.
- Implementing transactional rollback isolation for database tests.
- Debugging scope-mismatch or fixture-teardown ordering issues.
- Identifying Mystery Guest / God Fixture anti-patterns in a suite.

## Skip If (ANY kills it)

- pytest-specific test patterns (parametrize, markers) → testing-pytest.
- E2E test data setup → e2e-testing.
- JavaScript test fixtures → testing-javascript.
- Decision is about mocking, not fixtures → mocking-strategies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `model-inventory.yaml` | list of {model, reuse_count, has_unique_fields, has_subobjects} | operator |
| `framework` | django / sqlalchemy / sqlmodel | repo |
| `xdist_workers` | integer | CI config |
| `conftest_path` | path | repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[testing-pytest]] | scope semantics and yield-fixture mechanics. |
| [[integration-testing]] | DB rollback discipline aligns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: scope must match state, yield not addfinalizer, no Mystery Guest, no God Fixture, factory uniqueness, xdist worker DB, autouse documented. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the fixture-design config artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: Mystery Guest, God Fixture, wide-scope+stateful, Sequence collisions, undocumented autouse. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: inventory models → pick pattern (Factory/Builder/Mother) → assign scope → wire rollback → emit conftest. | ~700 |
| `content/05-examples.xml` | recommended | Django Factory Boy + sqlalchemy rollback + xdist worker_id end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Factory vs Builder vs Object Mother; function vs module vs session scope; UUID vs Sequence. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_model_inventory` | haiku | Mechanical YAML→typed list. |
| `pick_pattern_per_model` | sonnet | Tradeoff between Factory simplicity and Builder/Mother semantic clarity. |
| `audit_existing_fixtures` | opus | Detecting Mystery Guest / God Fixture in existing conftest. |
| `emit_conftest` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/factory-boy-factory.py` | Factory Boy base factory with traits and sub-factories. |
| `templates/conftest-transactional.py` | Transactional rollback fixture for pytest-django. |
| `templates/_smoke-test.yaml` | Minimum model inventory. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-pytest]]
- [[integration-testing]]
- [[mocking-strategies]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `has_subobjects` (yes → SubFactory; no → continue), then on `has_many_optional_fields` (yes → Builder; no → continue), then on `domain_scenarios_named` (yes → Object Mother; no → plain Factory). Scope branches on `is_stateful` and `xdist_workers`. Each leaf cites a rule id.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/factory-boy-factory.py`

```python
"""
Factory Boy factories template.
Adapt models, fields, and subfactories to your domain.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

# from myapp.models import User, Profile, Product, Order

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Base user factory with sensible defaults."""

    class Meta:
        model = "auth.User"  # replace with your User model path
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.LazyAttribute(lambda obj: obj.email.split("@")[0])
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False

    # Traits — opt in with UserFactory(admin=True)
    class Params:
        admin = factory.Trait(is_staff=True, is_superuser=True)
        inactive = factory.Trait(is_active=False)


# class ProfileFactory(DjangoModelFactory):
#     class Meta:
#         model = Profile
#
#     user = factory.SubFactory(UserFactory)
#     bio = factory.Faker("paragraph", nb_sentences=2)
#     avatar = factory.django.ImageField(color="blue", width=100, height=100)


# class ProductFactory(DjangoModelFactory):
#     class Meta:
#         model = Product
#
#     name = factory.Faker("catch_phrase")
#     description = factory.Faker("text", max_nb_chars=200)
#     price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
#     owner = factory.SubFactory(UserFactory)
#     sku = factory.Sequence(lambda n: f"SKU-{n:06d}")


# class OrderFactory(DjangoModelFactory):
#     class Meta:
#         model = Order
#
#     user = factory.SubFactory(UserFactory)
#     status = "pending"
#     total = factory.LazyAttribute(lambda obj: sum(i.price for i in obj.items.all()))
#
#     @factory.post_generation
#     def items(self, create, extracted, **kwargs):
#         if not create:
#             return
#         if extracted:
#             for item in extracted:
#                 self.items.add(item)
#         else:
#             ProductFactory.create_batch(2)
```

### `templates/conftest-transactional.py`

```python
"""
Transactional rollback fixture for pytest-django.
Each test wraps DB changes in a transaction that is rolled back at the end.
This is faster than recreating the database or using truncation.

Usage: Place in tests/conftest.py and enable with the `transactional_db` fixture
or set `django_db_reset_sequences = True` if needed.
"""
import pytest


# ---- Standard pytest-django DB fixture (non-transactional, recommended default) ----

@pytest.fixture(autouse=True)
def db_access(db):
    """
    Allow DB access in all tests without @pytest.mark.django_db.
    Remove autouse=True if you prefer explicit opt-in per test.
    """
    pass


# ---- Transactional rollback fixture (SQLAlchemy) ----
# Wraps each test in a SAVEPOINT so the main transaction is never committed.

@pytest.fixture(scope="session")
def db_engine():
    """Session-scoped engine — created once for the entire test run."""
    from sqlalchemy import create_engine
    from myapp.db import Base, DATABASE_URL  # adapt to your project

    engine = create_engine(DATABASE_URL.replace("://", "+psycopg2://"))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    """
    Function-scoped DB session with rollback.
    Each test gets a clean slate via SAVEPOINT.
    """
    from sqlalchemy.orm import sessionmaker

    connection = db_engine.connect()
    outer_transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Nested transaction (SAVEPOINT)
    nested = connection.begin_nested()
    session.begin_nested()

    yield session

    session.close()
    nested.rollback()
    outer_transaction.rollback()
    connection.close()


# ---- Django: separate DB per xdist worker ----

# @pytest.fixture(scope="session")
# def django_db_setup(worker_id, django_test_environment, django_db_blocker):
#     from django.conf import settings
#     db_name = f"test_{settings.DATABASES['default']['NAME']}"
#     if worker_id != "master":
#         db_name = f"{db_name}_{worker_id}"
#     settings.DATABASES["default"]["TEST"] = {"NAME": db_name}
#     with django_db_blocker.unblock():
#         from django.test.utils import setup_databases
#         setup_databases(verbosity=0, interactive=False)
```

### `templates/_smoke-test.yaml`

```yaml
models:
  - model: User
    reuse_count: 12
    has_unique_fields: true
    has_subobjects: false
    has_many_optional_fields: false
    domain_scenarios_named: true

drivers:
  has_subobjects: false
  has_many_optional_fields: false
  domain_scenarios_named: true
  xdist_workers: 4

framework: django
conftest_path: tests/conftest.py
```
