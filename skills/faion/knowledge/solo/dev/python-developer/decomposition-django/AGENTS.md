# Decomposition (Django)

## Summary

The HackSoft services+selectors decomposition pattern for Django: business logic lives in `services/` (write operations, `@transaction.atomic`, keyword-only args), read queries in `selectors/` (return QuerySets, no mutations), models stay thin (ORM fields + validators, no business logic), views stay thin (parse → call service → serialize). Trigger decomposition when `models.py` exceeds 300 lines or `views.py` exceeds 200 lines. Execute one bounded context at a time with `pytest` green at every step.

## Why

Fat views and fat models mix HTTP concerns, business logic, and ORM queries, making each layer untestable in isolation and incomprehensible to LLM agents. The services+selectors split creates predictable, single-purpose files that agents can read and modify without loading the entire app. Keyword-only service args (`def user_create(*, email, password)`) prevent positional-argument drift as signatures evolve. `import-linter` enforces the layer boundary so agents cannot accidentally call views from services.

## When To Use

- Django app where `models.py` exceeds ~300 lines or `views.py` exceeds ~200 lines
- Migrating a fat-model codebase to services + selectors layout
- Splitting a monolithic Django project by bounded context (DDD per-domain apps)
- Preparing a codebase for AI-assisted refactoring — small focused files improve reliability
- Onboarding a new team where views mix auth, queries, business logic, and serialization

## When NOT To Use

- One-shot scripts, admin command tools, or proof-of-concept apps
- Apps with a single model and 5 or fewer endpoints — premature decomposition adds friction
- Codebases in maintenance-only mode where churn risk outweighs clarity gain
- Teams without test coverage to validate the refactor — break-and-freeze is the result

## Content

| File | What's inside |
|------|---------------|
| `content/01-layer-rules.xml` | Service/selector/model/view rules, file-size thresholds, layer boundary enforcement |
| `content/02-migration-procedure.xml` | Phased decomposition order, circular-import prevention, migration safety, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/user_service.py` | Full UserService with dataclass inputs, @transaction.atomic, keyword-only args |
| `templates/user_selectors.py` | User selector functions with QuerySet returns and eager loading |
| `templates/importlinter.ini` | import-linter config enforcing services-cannot-import-views boundary |
