---
slug: django-project-structure
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django project layout spec (apps/, core/, config/, tests/factories) with per-app file inventory and HackSoft-style services/selectors split.
content_id: "d6392c7bf921f2f9"
complexity: medium
produces: spec
est_tokens: 4000
tags: [django, project-structure, layering, services, selectors]
---

# Django Project Structure

## Summary

**One-sentence:** Produces a Django project layout spec naming the apps/ folder per domain, the shared core/ package, the config/ settings split, the central tests/factories/, and the per-app file inventory (models, services, selectors, apis, serializers, urls, constants, admin, tests).

**Ефективно для:** Teams that drift from flat `models.py + views.py` into N-app domain layouts and need one source of truth for "where does this file go" — before every PR re-debates it.

**One-paragraph:** Codifies the HackSoft + Two Scoops layout into one auditable spec. Output names the apps/ list, the per-app file inventory (services.py vs selectors.py vs apis.py vs admin.py), and the core/ + config/ + tests/ root packages. Forbids: scattered global views/ and models/ folders, circular `apps/ → core/` imports, mixing services and selectors in the same module, app folder names that aren't snake_case-plural.

## Applies If (ALL must hold)

- Django ≥ 5.0 project with ≥ 2 business domains (orders, accounts, billing, content, …).
- Project will grow past a few hundred lines (post-MVP).
- Team commits to apps/ + core/ + config/ split.
- Output drives `startapp` codegen + onboarding doc.
- A named owner accountable for the structure exists.

## Skip If (ANY kills it)

- Single-file Django scripts / management commands — full structure is overkill.
- Django CMS / Wagtail where the framework imposes its own conventions.
- Tiny utility app with one model and no business logic — add to core/.
- One-app prototype intended to remain one app.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| List of business domains | bullets | product doc / ERD |
| Django + Python versions | semver | pyproject.toml |
| Settings env list (dev / staging / prod) | bullets | platform team |
| Existing layout (if any) | tree | repo root |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-imports]]` | Cross-app alias convention that depends on the apps/ namespace. |
| `[[django-decision-tree]]` | Layering tier decided upstream. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: apps/ layout, per-app inventory, core/ no-imports-from-apps, config/ settings split, naming conventions | ~1000 |
| `content/02-output-contract.xml` | essential | JSON schema for the project structure spec | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: global models/views, core/ importing apps/, services+selectors in one module, app folder naming | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: enumerate apps → per-app inventory → core/ → config/ → tests/ | ~600 |
| `content/06-decision-tree.xml` | essential | Per concept: where does it live? | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `enumerate_apps` | haiku | Mechanical from domain list. |
| `emit_layout_spec` | sonnet | Bounded transformation. |

## Templates

| File | Purpose |
|---|---|
| `templates/layout-spec.json` | Reference output. |
| `templates/startapp-skeleton.tree` | Canonical per-app folder tree to copy. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-project-structure.py` | Validate a layout spec JSON. | After spec emission, before startapp/codegen. |

## Related

- [[django-imports]] — apps/ namespace consumed by alias rules.
- [[django-decision-tree]] — layering tier feeding into this spec.
- [[django-models]] — models.py consumed by each app.

## Decision tree

Lives at `content/06-decision-tree.xml`. Per concept (new model / new function / new shared base): does it belong to one business domain? → apps/&lt;domain&gt;/. Cross-domain shared base? → core/. Settings or wiring? → config/. Test factory? → tests/factories/.
