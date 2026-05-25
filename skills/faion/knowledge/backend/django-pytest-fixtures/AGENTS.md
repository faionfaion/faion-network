# Django pytest Fixtures

## Summary

**One-sentence:** Produces a pytest-django fixtures spec naming each fixture with its scope (function / module / session), db vs transactional_db semantics, conftest.py placement, test settings overrides (MD5 hasher, locmem email, eager Celery), and pytest-xdist config.

**Ефективно для:** Test suites that take 10+ minutes locally, where flaky tests depend on transaction semantics, and where MEDIA_ROOT leaks pollute the repo between runs.

**One-paragraph:** Codifies fixture composition + scoping + test settings into one spec. Forbids: using `db` when transaction.on_commit hooks are asserted, session-scoped mutable fixtures, overriding settings without the pytest-django `settings` fixture, MEDIA_ROOT pointing at real disk, --reuse-db racing on cold start.

## Applies If (ALL must hold)

- Django ≥ 5.0 with pytest-django installed.
- Test suite has ≥ 50 tests where fixture scope matters.
- The team commits to pytest-django's `db` / `transactional_db` fixture model.
- A test settings file exists or can be added.
- Output drives conftest.py + tests/factories/ + test settings codegen.

## Skip If (ANY kills it)

- Pure unit test of helpers / pure functions with no Django dep — plain pytest is faster.
- One-off scripts or ad-hoc manage.py shell exploration.
- Legacy `manage.py test` CI gate that you cannot remove.
- Test suite already standardised on Django TestCase + unittest.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Model + signal + Celery inventory | bullets | [[django-models]] + grep |
| Existing conftest.py + test settings | code | repo |
| Estimated test count + slow-test list | numbers | pytest --durations=20 |
| CI runtime budget | minutes | platform team |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-pytest-factories]]` | Factories produce the data each fixture wraps. |
| `[[django-models]]` | Signal handler list informs db vs transactional_db. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: db marker, scope rules, API clients, composition, conftest hierarchy, test settings, xdist, tests/ layout | ~1400 |
| `content/02-output-contract.xml` | essential | JSON schema for the fixtures spec | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: db-vs-transactional confusion, mutable session-scope, xdist racing, override_settings drift, MEDIA_ROOT pollution | ~900 |
| `content/04-procedure.xml` | medium | 5 steps: declare fixtures → scope → settings → xdist → validate | ~600 |
| `content/06-decision-tree.xml` | essential | Per fixture: db or transactional_db? scope choice? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_fixtures` | haiku | Mechanical from test list. |
| `emit_fixtures_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/fixtures-spec.json` | Reference output. |
| `templates/conftest-root.py` | Root conftest with api_client + authenticated_client + admin_client. |
| `templates/test_settings.py` | Test settings override file (in-memory SQLite, MD5 hasher, locmem email). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-pytest-fixtures.py` | Validate the fixtures spec JSON. | After spec emission. |

## Related

- [[django-pytest-factories]] — factories feeding the fixtures.
- [[django-pytest-integration]] — integration-test layer built on these fixtures.
- [[django-pytest-mocking]] — mock fixtures that compose with these.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per fixture: does the test assert on transaction.on_commit / signals / select_for_update? → transactional_db. Else → db. Per scope: data mutable? → function. Read-only static reference data? → session.
