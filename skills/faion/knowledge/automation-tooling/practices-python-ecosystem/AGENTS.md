# Python Ecosystem Practices

## Summary

**One-sentence:** Produces a Python project baseline: pyproject.toml with ruff + mypy strict, uv/pip-tools lock, src/ layout, py.typed marker, pre-commit hooks, CI gate.

**One-paragraph:** Modern Python baseline: pyproject.toml (PEP 621) is the single source of truth; src/ layout to prevent accidental imports from the working dir; ruff for format + lint (replaces black + isort + flake8); mypy --strict for type checks; uv or pip-tools for deterministic lockfile; py.typed marker if shipping a typed library; pre-commit hooks running ruff + mypy on staged files; CI runs ruff check + mypy + pytest. The artefact is the project metadata; the validator checks the canonical fields are present.

**Ефективно для:**

- New Python project or library being scaffolded.
- Brownfield project migrating from setup.py to pyproject.toml.
- Adding ruff + mypy strict + pre-commit to a legacy repo.
- Wiring CI to enforce ruff check + mypy + pytest on every push.

## Applies If (ALL must hold)

- Python 3.10+ (PEP 604 union types + structural pattern matching available).
- Project ships a pyproject.toml as the build/config source of truth.
- Test runner is pytest.
- Lockfile manager is uv or pip-tools (no Poetry-specific behaviour required).

## Skip If (ANY kills it)

- Pure data-science notebooks with no installable package.
- Cython/extension-heavy projects requiring custom setup.py logic that pyproject can't express.
- Internal one-file scripts shipped via pipx without a project metadata file.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Python >= 3.10 | binary on PATH | developer machine |
| Project name + minimum supported Python version | string + version | task brief |
| Library or application? | lib | app | team decision |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[testing-django-pytest]] | shares pytest conventions; out-of-scope here |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `emit-pyproject` | haiku | render pyproject.toml from template + project name |
| `emit-ruff-config` | sonnet | select ruff rule groups based on project shape |
| `emit-pre-commit` | haiku | render .pre-commit-config.yaml from template |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | PEP 621 pyproject with ruff + mypy strict |
| `templates/.pre-commit-config.yaml` | Pre-commit hooks: ruff + mypy on staged files |
| `templates/ci.yml` | GitHub Actions workflow for Python |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-python-ecosystem.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-django-coding]]
- [[testing-django-pytest]]
- [[practices-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "T20"]
ignore = []

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
strict = true
python_version = "3.11"
disallow_untyped_defs = true
no_implicit_optional = true
warn_unreachable = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

### `templates/.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies: []
```

### `templates/ci.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install uv
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run mypy src
      - run: uv run pytest -q
```

### `templates/artefact.json`

```json
{
  "uses_pyproject": true,
  "src_layout": true,
  "ruff_configured": true,
  "mypy_strict": true,
  "lockfile_present": true,
  "pre_commit_present": true,
  "no_print_rule": true,
  "py_typed_marker": true,
  "python_min": "3.11"
}
```
