---
slug: direnv-mise-versions
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Per-project environment management on Ubuntu 24.
content_id: "b1d3f1ccef0242aa"
tags: [direnv, mise, python, environment, versioning]
---
# direnv + mise Version Management

## Summary

**One-sentence:** Per-project environment management on Ubuntu 24.

**One-paragraph:** Per-project environment management on Ubuntu 24.04 with direnv (auto-loads .envrc on directory entry) and mise (polyglot runtime manager replacing pyenv/nvm/asdf). Key pattern: `use mise` + `layout python-venv .venv` in .envrc auto-activates the correct Python version and virtualenv when entering a project directory. Shell integration order is critical: mise hook must come BEFORE direnv hook in .bashrc.

## Applies If (ALL must hold)

- Multiple Python/Node projects on the same server needing different runtime versions
- Automatically activating virtualenvs when entering project directories
- Loading project-specific .env variables securely without shell leakage
- Setting up a new development server with reproducible runtime environments

## Skip If (ANY kills it)

- Single-project servers where a single system Python or one venv is sufficient
- Managed platforms (Heroku, Railway) that provide runtime isolation at the container level
- When the project already uses Docker for isolation — runtime pinning is handled in the image
- Production systemd services — pin the venv path explicitly in ExecStart, don't rely on direnv

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/infra/server-craft/`
