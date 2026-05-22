---
slug: django-quality-linting
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django code-quality stack spec (Ruff config, mypy + django-stubs, pre-commit hooks, CI gates including coverage 80%) for a Python 3.11+/Django 5.x repo.
content_id: "e909c74c03285659"
complexity: medium
produces: spec
est_tokens: 4000
tags: [django, ruff, mypy, django-stubs, pre-commit, ci]
---

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

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-quality-linting.py` | Validate the quality stack spec JSON. | After spec emission, before pyproject / pre-commit updates. |

## Related

- [[django-imports]] — ruff isort config consumed here.
- [[django-pytest-integration]] — coverage gate referenced.
- [[django-decision-tree]] — dep audit feeds pip-audit gate.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per gate: cheap (&lt; 1s on changed files) → pre-commit. Expensive (full diff / DB / network) → CI only. Pre-commit cumulative budget ≤ 10s, otherwise devs bypass.
