---
slug: python-web-frameworks
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a one-line framework decision (Django|FastAPI|Flask) pinned in constitution.md plus the rationale matrix that justifies it.
content_id: "72a0ee0573b96669"
complexity: light
produces: decision-record
est_tokens: 3200
tags: [python, django, fastapi, flask, framework-selection, decision-record]
---
# Python Web Frameworks

## Summary

**One-sentence:** Picks Django vs FastAPI vs Flask once, locks it in `constitution.md`, and routes downstream methodology loading to the chosen framework.

**One-paragraph:** Produces a one-line framework decision (`framework = django|fastapi|flask`) plus the rationale matrix that justifies it. Lock the choice in `constitution.md` before writing any code — do not let downstream agents switch frameworks mid-feature. Use this methodology only for the framework decision; once made, load the framework-specific methodology (`django-models`, `python-fastapi`, etc.) and skip this one.

**Ефективно для:** greenfield Python-веб-проєкту, де ще не вибрано фреймворк, або плановий migration audit між Django ↔ FastAPI ↔ Flask.

## Applies If (ALL must hold)

- Project is a Python web service (HTTP, WebSocket, or hybrid) — not CLI / batch / notebook work.
- Framework choice is still open OR the team has an explicit re-platforming mandate.
- Decision is being captured in `constitution.md` (or equivalent ADR) and will be enforced by reviewers.
- Candidate frameworks are limited to Django, FastAPI, or Flask (this methodology does not cover Litestar, Sanic, Quart, Starlette).

## Skip If (ANY kills it)

- Codebase has already committed to one framework — load only that framework's specific methodology.
- Pure non-web Python work (ML batch, scripts, CLIs) — wrong abstraction layer.
- Hybrid stack with framework decisions already pinned per service.
- Performance-critical pure-async use case where FastAPI is already a foregone conclusion.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Functional brief | Markdown | product / SDD spec |
| Non-functional requirements | Markdown | NFR list (throughput, latency, admin, auth) |
| Team Python familiarity matrix | YAML/MD | team profile |
| Existing infra constraints (sync/async stack, container limits) | Markdown | infra notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | Baseline 2026 quality bar the framework must satisfy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 selection rules: when Django, when FastAPI, when Flask, async-discipline, switch-cost lock | ~1000 |
| `content/02-output-contract.xml` | essential | Schema for the decision-record output (framework, rationale, downstream methodologies to load) | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: mixed idioms, deprecated startup events, unsourced RPS claims, Flask-bloat, Flask-async-illusion | ~800 |
| `content/05-examples.xml` | medium | Three worked decisions (admin-heavy SaaS, async ML serving, internal tool) | ~400 |
| `content/06-decision-tree.xml` | essential | Concrete decision tree on observable inputs (admin needed? async? team size?) | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Run the decision tree against the brief | sonnet | Pure rule application — deterministic. |
| Draft the ADR / `constitution.md` framework section | sonnet | Templated writing. |
| Re-platforming impact estimate (when migrating) | opus | Needs judgement about hidden coupling. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pick-framework.sh` | Interactive picker that asks the decision-tree questions and prints `framework = …` plus the loaded-methodology list. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-web-frameworks.py` | Validates the decision-record JSON against `02-output-contract.xml` schema. | After the picker runs, before committing the ADR. |

## Related

- [[python-typing]] — type-checker baseline regardless of framework.
- [[django-models]] — load after `framework = django`.
- [[django-api]] — load after `framework = django` for the API layer.
- [[best-practices-2026]] — quality bar above the framework choice.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off four observables: needs built-in admin Y/N, native async needs Y/N, team size, and target throughput floor. Each leaf maps to one of `django | fastapi | flask` plus the set of downstream methodologies to load next.
