---
slug: django-decision-tree
tier: free
group: dev
domain: python-developer
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django architecture decision-record (framework, API stack, layering, DB, deployment, dep audit) at project bootstrap or major-refactor checkpoint.
content_id: "6d6aa84a58801b9e"
complexity: deep
produces: decision-record
est_tokens: 4500
tags: [django, architecture, decision-tree, deployment, dependency-audit]
---

# Django Decision Tree

## Summary

**One-sentence:** Produces an architecture decision-record at Django project bootstrap (or major refactor checkpoint) — framework choice (Django vs FastAPI), API stack (DRF vs Ninja), layering tier (simple vs services vs clean-arch), DB engine, deployment target, and per-dependency audit verdict.

**Ефективно для:** Teams committing to a Django stack who need one auditable record naming every architectural choice so onboarding, postmortems, and refactor reviews can all reference the same source of truth.

**One-paragraph:** Codifies the recurring "do we even want Django? DRF or Ninja? service layer yet? Postgres? VPS or Render?" decisions into one decision-record. The output names the choice for each axis, cites the project signals (team size, model count, traffic profile) that drove it, and lists every third-party package with a maintenance verdict. Forbids: re-running the full tree without trigger, choosing FastAPI for an admin-heavy product, choosing clean-arch for a 3-model MVP, adding unmaintained packages without a sunset plan.

## Applies If (ALL must hold)

- Starting a new Django project OR major refactor checkpoint (every ~12 months / 50 models / team scaling).
- The team has Python experience and wants Django on the table.
- A named owner accountable for the architectural choices is available.
- Project signals (team size, model count, traffic, deployment context) are known.
- Output drives onboarding doc + dependency review + deployment plan.

## Skip If (ANY kills it)

- After spec sign-off with deployment already chosen — don't re-run the full tree.
- The choice is constrained by infrastructure / team policy / regulatory rules.
- Tiny scripts, ETL jobs, single-page admin tools — Django is overkill.
- Greenfield project where the bottleneck is product-market fit, not architecture.
- Single-feature change inside an existing Django project — use code-placement guidance only.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Team size + Python experience | text | hiring / team doc |
| Model count estimate + bounded contexts | int + list | product brief |
| Traffic profile (req/s, write/read ratio) | numbers | SLO doc |
| Deployment context (existing infra, regs) | text | platform team |
| Candidate third-party packages | list | tech-radar / spike |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[django-project-structure]]` | Layering choices materialise into folder structure. |
| `[[django-api]]` | DRF vs Ninja decision lands here. |
| `[[django-base-model]]` | Base model decisions consumed by the architecture record. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: pick-framework, pick-api, pick-layering, pick-db, pick-deployment, audit-deps | ~1300 |
| `content/02-output-contract.xml` | essential | JSON schema for the architecture decision-record | ~1100 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: oversize layering for MVP, undersize for enterprise, unmaintained dep, re-running tree without trigger | ~800 |
| `content/04-procedure.xml` | deep | 7 steps walking the tree | ~700 |
| `content/05-examples.xml` | deep | One worked example: faion-net-be architecture decision | ~700 |
| `content/06-decision-tree.xml` | essential | The actual decision tree | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `collect_signals` | haiku | Mechanical fill of input signals. |
| `walk_tree` | sonnet | Per-axis decision with rationale. |
| `audit_deps` | opus | Cross-checks maintenance / security / licence. |

## Templates

| File | Purpose |
|---|---|
| `templates/arch-decision-record.json` | Reference output. |
| `templates/arch-decision-record.md` | Markdown skeleton for human-readable record. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-decision-tree.py` | Validate the decision record JSON. | After tree walk, before architecture doc is published. |

## Related

- [[django-api]] — API stack choice elaborated here.
- [[django-project-structure]] — layering choice elaborated here.
- [[django-base-model]] — base-model choice consumed by the layering decision.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree walks: (1) Django at all? (2) DRF vs Ninja vs vanilla. (3) layering tier (simple/services/clean). (4) DB engine. (5) deployment target. (6) per-dep audit verdict. Each leaf cites a rule id and consumes the recorded project signals.
