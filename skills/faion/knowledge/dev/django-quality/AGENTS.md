# Django Quality

## Summary

**One-sentence:** Produces a Django quality toolchain: ruff (format + lint), mypy + django-stubs (typing), bandit (security), pre-commit hooks; pyproject.toml only — no separate .flake8/setup.cfg, no black/isort alongside ruff.

**One-paragraph:** Produces a Django quality toolchain: ruff (format + lint), mypy + django-stubs (typing), bandit (security), pre-commit hooks; pyproject.toml only — no separate .flake8/setup.cfg, no black/isort alongside ruff. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project uses Django 5.x (or 4.2 LTS) with Python 3.12+.
- Code in question lives under `apps/<app>/` or `core/` per the django-coding-standards layout.
- A test runner is configured (`pytest + pytest-django`).
- The team has agreed to enforce service-layer logic separation.

## Skip If (ANY kills it)

- Project is not on Django (FastAPI, Flask, or other) — load the framework-specific methodology instead.
- Tiny throwaway tool with no growth horizon — overhead exceeds payoff.
- Codebase has not adopted the apps/core/config layout and refactoring it is out of scope right now.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| `apps/<app>/` layout | directory tree | repo source |
| Target Django version | string | `pyproject.toml` |
| Existing test runner config | TOML | `pyproject.toml` `[tool.pytest.ini_options]` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Type-checker baseline for Django code. |
| `free/dev/software-developer/django-coding-standards` | Layout standard that gates placement of files produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to django-quality | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold model/serializer/view/test from spec | sonnet | Mechanical code generation. |
| Design service-layer boundaries | opus | Needs domain judgement. |
| Audit existing code for layering violations | sonnet | Pattern matching with deterministic output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-commit-config.yaml` | Pre-commit pipeline: ruff format/check + mypy + bandit + djlint. |
| `templates/pyproject-ruff.toml` | pyproject.toml [tool.ruff] section preset for Django. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-quality.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-coding-standards]] — see methodology AGENTS.md for context.
- [[django-models]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pre-commit-config.yaml`

```yaml
# .pre-commit-config.yaml — modern Django project
# NO black, NO isort, NO flake8 — ruff covers all three.
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

### `templates/pyproject-ruff.toml`

```toml
# pyproject.toml — modern Django quality stack (ruff + mypy)
# Drop black, isort, flake8. This replaces all three.

[tool.ruff]
target-version = "py311"
line-length = 100
extend-exclude = ["migrations"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "DJ", "T20", "PT", "RUF", "S"]
ignore = ["E501", "S101"]  # E501 handled by formatter; S101 allows assert in tests

[tool.ruff.lint.per-file-ignores]
"**/tests/*.py" = ["S105", "S106"]
"**/settings/*.py" = ["S105"]

[tool.ruff.lint.isort]
known-first-party = ["apps", "core", "config"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.11"
plugins = ["mypy_django_plugin.main"]
strict = false
warn_unused_ignores = true
warn_redundant_casts = true

[tool.django-stubs]
django_settings_module = "config.settings.development"
```
