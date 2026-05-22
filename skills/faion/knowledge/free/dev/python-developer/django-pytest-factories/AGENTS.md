---
slug: django-pytest-factories
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a pytest-factoryboy spec (factory classes, SubFactory graph, register list, mute_signals scope) for Django test data without manual setUp.
content_id: "49783ba20b7f14b0"
complexity: medium
produces: spec
est_tokens: 3600
tags: [django, pytest, factory-boy, pytest-factoryboy, testing]
---

# Django pytest Factories

## Summary

**One-sentence:** Produces a pytest-factoryboy spec listing every Django factory class, its SubFactory dependencies, the Faker fields, the post_generation hooks (M2M / passwords), and the `register()` calls that auto-create `user` / `user_factory` fixtures.

**Ефективно для:** Django test suites that drift toward 50-line setUp blocks creating User+Profile+Order graphs, where Faker drift makes assertions flaky, where signals fire surprise emails during unrelated tests.

**One-paragraph:** Codifies "where do test factories live and how are they registered?" into one spec. Forbids: parallel manual `@pytest.fixture def user` after `register(UserFactory)`, asserting on Faker-generated literal values, bulk_create-based factories when signals matter, missing `skip_postgeneration_save=True` on Django 4.2+ factories with post_generation hooks.

## Applies If (ALL must hold)

- Django ≥ 5.0 with pytest-django + factory_boy + pytest-factoryboy installed.
- Codebase has ≥ 3 domain models that need test data construction.
- Tests use Faker (not literal strings) for non-asserted fields.
- Team accepts that root conftest.py owns `register()` calls.
- Output drives codegen of tests/factories/ and conftest.py.

## Skip If (ANY kills it)

- Simple one-off test where a factory adds more complexity than value.
- Hard-coded value assertion path — pass literals to factory instead.
- Performance benchmarks where factory overhead matters — use bulk_create directly.
- Test suite already uses model_bakery / model_mommy — pick one.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| List of domain models | bullets | [[django-models]] output |
| Signal handlers list | bullets | grep models.signals |
| Existing conftest.py | code | repo |
| Test data realism requirements | text | QA / product |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-models]]` | Model fields + FK graph consumed by SubFactory. |
| `[[django-pytest-fixtures]]` | Per-test fixture scoping. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 3 testable rules: DjangoModelFactory + SubFactory + Faker, register-in-conftest, mute_signals scope | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the factories spec | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: manual override, Faker literal assertion, bulk_create skipping signals, missing skip_postgeneration_save | ~800 |
| `content/04-procedure.xml` | medium | 5 steps: enumerate models → declare factories → SubFactory graph → register → mute_signals scope | ~600 |
| `content/06-decision-tree.xml` | essential | Per model: factory needed? mute signals? skip_postgeneration_save? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_factories` | haiku | Mechanical: one factory per domain model. |
| `emit_factories_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/factories-spec.json` | Reference output document. |
| `templates/factories-conftest.py` | Reference root conftest with register() calls. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-factories.py` | Validate the factories spec JSON. | After spec emission. |

## Related

- [[django-pytest-fixtures]] — fixtures composed on top of the factories.
- [[django-pytest-mocking]] — when to mute signals vs mock them.
- [[django-models]] — model graph consumed here.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per model: does it have post_save signal handlers with external side effects? → mute_signals scope. Per factory with @post_generation: Django ≥ 4.2? → skip_postgeneration_save=True. Per relationship: FK → SubFactory; M2M → @post_generation.
