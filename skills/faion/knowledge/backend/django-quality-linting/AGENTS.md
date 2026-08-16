# Django Linting and Static Analysis Stack

## Summary

**One-sentence:** Produces a quality-stack spec — Ruff config (rule groups + per-file ignores), mypy + django-stubs config, pre-commit hooks (under 10s budget), and CI gate list (ruff / mypy / manage.py check --deploy / pip-audit / coverage ≥ 80%).

**Ефективно для:** Django projects where pre-commit hooks balloon past 30s and devs `--no-verify`, where mypy `--strict` was enabled on day one and was immediately disabled because of 800 errors, where prints leak into production logs.

**One-paragraph:** Codifies the complete code-quality stack for a Django repo into one spec the platform team and CI can both consume. Output names the Ruff rule groups + line length + per-file ignores, the mypy strict-file list, the pre-commit hook list with the 10s-budget commitment, and the CI gate set. Forbids: bare `# type: ignore`, repo-wide mypy --strict day-one, mypy_django_plugin without django_settings_module, T20 without per-file-ignore for management commands, MegaLinter as a pre-commit hook.

## Applies If (ALL must hold)

- Django ≥ 5.0 + Python ≥ 3.11.
- New project OR existing project ready for a quality-tool refactor.
- Team owns the .pre-commit-config.yaml and CI config.
- A named owner for the migration to strict mypy is identified.
- Output drives pyproject.toml + .pre-commit-config.yaml + CI YAML codegen.

## Skip If (ANY kills it)

- Throwaway prototype — Ruff alone is enough.
- Codebase on Django &lt; 4.2 — django-stubs examples don't apply cleanly.
- Legacy project under feature freeze — ROI on quality tooling is low.
- Repository already has a complete stack that the team is happy with.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Python + Django versions | semver | pyproject.toml |
| Existing pre-commit config (if any) | YAML | repo |
| Existing CI config | YAML | .github/workflows or similar |
| Current `mypy --strict` error count baseline | int | tooling pass |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[django-imports]]` | ruff `I` config consumed here. |
| `[[django-pytest-integration]]` | coverage gate referenced. |
| `[[typescript-strict-mode]]` | analogous strict-flag migration pattern (cross-stack). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 4 testable rules: ruff config, mypy + django-stubs config, pre-commit hooks under 10s, CI gate set + coverage ≥ 80% | ~1200 |
| `content/02-output-contract.xml` | essential | JSON schema for the quality stack spec | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: bare ignore, day-one strict, missing settings_module, T20 without ignore, MegaLinter in hooks | ~900 |
| `content/04-procedure.xml` | medium | 5 steps: ruff → mypy → pre-commit → CI → validate | ~600 |
| `content/06-decision-tree.xml` | essential | Per gate: pre-commit (fast) vs CI (heavy)? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_existing_tools` | haiku | Mechanical inventory. |
| `emit_quality_spec` | sonnet | Bounded transformation. |
| `audit_for_speed` | opus | Cross-checks pre-commit time budget vs hook list. |

## Templates

| File | Purpose |
|---|---|
| `templates/quality-spec.json` | Reference output. |
| `templates/pyproject.toml.ruff-mypy.toml` | pyproject.toml ruff + mypy + django-stubs snippet. |
| `templates/.pre-commit-config.yaml` | pre-commit hook list. |
| `templates/ci-quality.yml` | GitHub Actions snippet for the quality job. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-quality-linting.py` | Validate the quality stack spec JSON. | After spec emission, before pyproject / pre-commit updates. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-imports]] — ruff isort config consumed here.
- [[django-pytest-integration]] — coverage gate referenced.
- [[django-decision-tree]] — dep audit feeds pip-audit gate.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per gate: cheap (&lt; 1s on changed files) → pre-commit. Expensive (full diff / DB / network) → CI only. Pre-commit cumulative budget ≤ 10s, otherwise devs bypass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/quality-spec.json`

```json
{
  "_purpose": "Reference Django quality stack spec output.",
  "_consumes": "Python/Django versions + existing tool config.",
  "_produces": "JSON for pyproject + pre-commit + CI codegen.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~220 tokens.",
  "artefact_id": "billing-quality-stack",
  "owner": "ruslan@faion.net",
  "django_version": "5.2.1",
  "python_version": "3.12",
  "ruff": {
    "rule_groups": [
      "E",
      "W",
      "F",
      "I",
      "B",
      "C4",
      "UP",
      "SIM",
      "DJ",
      "T20"
    ],
    "line_length": 100,
    "exclude_migrations": true,
    "per_file_ignores": {
      "apps/*/management/commands/*.py": [
        "T20"
      ]
    }
  },
  "mypy": {
    "django_settings_module": "config.settings.test",
    "strict_files": [
      "apps/billing/services.py",
      "apps/billing/selectors.py",
      "apps/accounts/services.py"
    ],
    "check_untyped_defs": true,
    "warn_unused_ignores": true
  },
  "pre_commit_hooks": [
    {
      "name": "ruff",
      "stage": "commit",
      "fast": true
    },
    {
      "name": "ruff-format",
      "stage": "commit",
      "fast": true
    },
    {
      "name": "mypy",
      "stage": "commit",
      "fast": true
    },
    {
      "name": "manage.py check",
      "stage": "commit",
      "fast": true
    },
    {
      "name": "pytest",
      "stage": "push",
      "fast": false
    }
  ],
  "ci_gates": [
    "ruff check --no-fix",
    "ruff format --check",
    "mypy --strict apps/",
    "manage.py check --deploy --fail-level WARNING",
    "manage.py makemigrations --check --dry-run",
    "pip-audit --strict",
    "coverage-gate"
  ],
  "coverage_threshold": 80,
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/pyproject.toml.ruff-mypy.toml`

```toml
[tool.ruff]
target-version = "py312"
line-length = 100
extend-exclude = [
    "migrations",
    ".venv",
    "build",
]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM", "DJ", "T20"]

[tool.ruff.lint.per-file-ignores]
"apps/*/management/commands/*.py" = ["T20"]  # self.stdout.write is the canonical alternative
"tests/**/*.py" = ["S101"]                   # assert is normal in tests

[tool.ruff.lint.isort]
known-first-party = ["apps", "config", "core"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.12"
check_untyped_defs = true
warn_unused_ignores = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
plugins = ["mypy_django_plugin.main"]

[[tool.mypy.overrides]]
module = ["apps.billing.services", "apps.billing.selectors", "apps.accounts.services"]
strict = true

[tool.django-stubs]
django_settings_module = "config.settings.test"
```

### `templates/.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs[compatible-mypy]
          - djangorestframework-stubs[compatible-mypy]
        # Only run on changed files at commit time — keeps the gate < 1s.
        files: ^apps/

  - repo: local
    hooks:
      - id: django-system-checks
        name: django-system-checks
        entry: python manage.py check
        language: system
        pass_filenames: false
        types: [python]

      - id: pytest
        name: pytest
        entry: pytest -n auto
        language: system
        pass_filenames: false
        stages: [pre-push]
```

### `templates/ci-quality.yml`

```yaml
name: quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    env:
      DJANGO_SETTINGS_MODULE: config.settings.test

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: ruff check . --no-fix
      - run: ruff format --check .
      - run: mypy --strict apps/
      - run: python manage.py check --deploy --fail-level WARNING
      - run: python manage.py makemigrations --check --dry-run
      - run: pip-audit --strict
      - run: pytest -n auto --cov=apps --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```
