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
- Single-feature change inside an existing Django project — walk only the code-placement branch of the tree (rules r7-r12), not the bootstrap axes.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Team size + Python experience | text | hiring / team doc |
| Model count estimate + bounded contexts | int + list | product brief |
| Traffic profile (req/s, write/read ratio) | numbers | SLO doc |
| Deployment context (existing infra, regs) | text | platform team |
| Candidate third-party packages | list | tech-radar / spike |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[django-project-structure]]` | Layering choices materialise into folder structure. |
| `[[django-api]]` | DRF vs Ninja decision lands here. |
| `[[django-base-model]]` | Base model decisions consumed by the architecture record. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 12 testable rules: pick-framework, pick-api, pick-layering, pick-db, pick-deployment, audit-deps + code placement (views HTTP-only, services own side effects, utils pure, one-way dependency direction, tasks thin, integrations domain-free) | ~1900 |
| `content/02-output-contract.xml` | essential | JSON schema for the architecture decision-record | ~1100 |
| `content/03-failure-modes.xml` | essential | 10 antipatterns: oversize layering for MVP, undersize for enterprise, unmaintained dep, re-running tree without trigger, ORM in view, ORM in utils, logic in task, circular import, domain type in integration, multi-write without atomic | ~1300 |
| `content/04-procedure.xml` | deep | 8 steps walking the tree, ending with the placement policy | ~850 |
| `content/05-examples.xml` | deep | One worked example: faion-net-be architecture decision | ~700 |
| `content/06-decision-tree.xml` | essential | The actual decision tree + the per-unit code-placement branch | ~450 |

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
| `templates/arch-decision-record.md.j2` | Markdown skeleton for human-readable record. |
| `templates/arch-decision-record.md` | Markdown skeleton for human-readable record. Generated from `templates/arch-decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-django-decision-tree.py` | Validate the decision record JSON. | After tree walk, before architecture doc is published. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-api]] — API stack choice elaborated here.
- [[django-project-structure]] — layering choice elaborated here.
- [[django-base-model]] — base-model choice consumed by the layering decision.
- [[django-coding-standards]] — the apps/core/config layout the placement rules assume.
- [[python-typing]] — type-checker baseline for the layered code.

## Decision tree

Lives at `content/06-decision-tree.xml`. At bootstrap the tree walks: (1) Django at all? (2) DRF vs Ninja vs vanilla. (3) layering tier (simple/services/clean). (4) DB engine. (5) deployment target. (6) per-dep audit verdict. A separate branch answers the day-to-day question — where does THIS unit of code go? — routing on what the code does (HTTP / side effect / pure / async / vendor SDK) to one of rules r7-r12. Each leaf cites a rule id and consumes the recorded project signals.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/arch-decision-record.json`

```json
{
  "_purpose": "Reference architecture decision-record output.",
  "_consumes": "signals + candidate deps.",
  "_produces": "JSON for architecture doc + dep registry.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~200 tokens.",
  "artefact_id": "faion-net-be-arch",
  "owner": "ruslan@faion.net",
  "project": "faion-net-be",
  "signals": {
    "team_size": 1,
    "model_count": 12,
    "traffic_req_s": 5,
    "needs_admin": true,
    "needs_async": false,
    "bounded_contexts": 2
  },
  "decisions": {
    "framework": "django",
    "api_stack": "drf",
    "layering": "service-layer",
    "db": "postgres-managed",
    "deployment": "vps",
    "rationales": {
      "framework": "Solopreneur with admin-heavy product; needs ORM + admin + auth out of the box.",
      "api_stack": "Team familiarity with DRF + drf-spectacular requirement for the OpenAPI client.",
      "layering": "12 models with two bounded contexts; service layer keeps logic testable.",
      "db": "Managed PostgreSQL (Hetzner managed) for JSONB + full-text search.",
      "deployment": "Hetzner VPS with systemd; cost-efficient, no scale need for K8s yet."
    }
  },
  "dependencies": [
    {
      "name": "djangorestframework",
      "verdict": "adopt",
      "audit": {
        "recent_commits": true,
        "django_compat": true,
        "license_ok": true,
        "no_known_cves": true
      }
    },
    {
      "name": "djangorestframework-simplejwt",
      "verdict": "adopt",
      "audit": {
        "recent_commits": true,
        "django_compat": true,
        "license_ok": true,
        "no_known_cves": true
      }
    },
    {
      "name": "drf-spectacular",
      "verdict": "adopt",
      "audit": {
        "recent_commits": true,
        "django_compat": true,
        "license_ok": true,
        "no_known_cves": true
      }
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
