# Poetry Project Setup

## Summary

Poetry is the standard for Python dependency management: deterministic builds via poetry.lock, isolated virtual environments, and streamlined PyPI publishing. Always commit poetry.lock; always use --sync in CI; never mix pip and poetry in the same project.

## Why

Without a lockfile, two agents on different machines resolve different dependency trees and produce non-reproducible builds. Poetry's solver generates a lockfile that pins every transitive dependency. The lock must be committed and treated as a reviewable artifact — the lockfile diff is the visible record of what changed.

## When To Use

- Starting any new Python project (service, library, CLI).
- Managing complex dependency trees requiring reproducible builds.
- Publishing packages to PyPI or private registries.
- Agent-managed repos where dependency changes must go through --dry-run + human approval.

## When NOT To Use

- Throwaway scripts or notebooks — uv pip install or pipx run is faster.
- Projects already standardized on pip-tools, uv, or pdm — don't migrate for novelty.
- Docker images built from requirements.txt with no solver runtime needed — export from Poetry at build time and use pip in the final stage.
- Monorepos with Pants/Bazel workspace tooling — Poetry has no first-class workspace concept.

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup-rules.xml` | Init commands, pyproject.toml structure, dependency management rules, lock file policy. |
| `content/02-docker-and-ci.xml` | Docker multi-stage build pattern, CI GitHub Actions workflow, publishing to PyPI. |
| `content/03-agent-gotchas.xml` | Known failure modes: dirty lockfile, poetry shell in CI, version-string mistakes, token leak. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | Full pyproject.toml with dependency groups, tool configs (ruff, mypy, pytest). |
| `templates/Dockerfile` | Multi-stage Docker build: poetry export in builder, pip install in final stage. |
