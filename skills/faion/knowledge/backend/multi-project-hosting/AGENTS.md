# Multi-Project Hosting on One VPS

## Summary

**One-sentence:** Pattern for hosting 2-5 web projects on a single VPS: port allocation by 100-range convention (8000-8099 project A, 8100-8199 project B), shared nginx reverse proxy, per-project user, /srv/<project> isolation, port registry.

**One-paragraph:** Shoehorning multiple sites onto one VPS is the cheapest way to ship N indie projects, but port collisions and shared-service confusion (which project owns the Redis instance?) kill the operator within a year. This methodology codifies the conventions: port ranges by 100, /srv/<project>/ isolation, /srv/port-registry.txt as the source of truth, shared nginx as the only public-facing service.

## Applies If (ALL must hold)

- Operator hosts ≥2 web projects on the same VPS.
- Each project has its own service / process / DB.
- nginx is the only public entry point (80/443).

## Skip If (ANY kills it)

- Single-project deploy — convention is overkill.
- Container orchestration (k8s, Nomad) — port allocation handled there.
- Public-port-per-project model (different IPs / hostnames) — different topology.

**Ефективно для:**

- Solo VPS-фаундери з 3-5 indie projects на одному хості.
- Port-collision incidents коли два проєкти хочуть :8000.
- Onboard новий проєкт за 10 хвилин: алокуй range, додай nginx vhost.
- Audit: який сервіс власник якого порту.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/nginx-reverse-proxy` | Shared nginx is the entry point. |
| `solo/infra/server-craft/systemd-user-services` | Per-project user with systemd-user. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Multi-project audit listing port ranges + isolation + vhost coverage. |
| `templates/_smoke-test.md` | Minimum viable filled-in multi-project audit. |
| `templates/port-registry.txt` | Plain-text source of truth for port allocations per project. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-project-hosting.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[nginx-reverse-proxy]]
- [[systemd-user-services]]
- [[firewall-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
