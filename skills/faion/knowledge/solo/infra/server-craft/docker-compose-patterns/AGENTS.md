---
slug: docker-compose-patterns
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Docker Compose V2 patterns for stateful infra (Postgres, Redis, RabbitMQ) on a single VPS alongside systemd services: bind-to-127.0.0.1 (UFW bypass guard), healthchecks, depends_on with condition, named volumes, restart policy."
content_id: "e974483129e23915"
complexity: medium
produces: report
est_tokens: 6000
tags: [docker, docker-compose, infrastructure, vps, postgres]
---
# Docker Compose Patterns for Solo VPS

## Summary

**One-sentence:** Docker Compose V2 patterns for stateful infra (Postgres, Redis, RabbitMQ) on a single VPS alongside systemd services: bind-to-127.0.0.1 (UFW bypass guard), healthchecks, depends_on with condition, named volumes, restart policy.

**One-paragraph:** Docker Compose on a single-VPS solo stack is a natural fit but has three traps: ports binding to 0.0.0.0 bypass UFW, `depends_on` without `condition: service_healthy` races the parent service against unready dependencies, and unnamed volumes accumulate as untracked anonymous mounts. This methodology produces a verified compose file with all three controls: 127.0.0.1 binds, condition-gated depends_on, named volumes per service.

## Applies If (ALL must hold)

- Operator runs ≥1 stateful service in Docker on a single VPS.
- Application services connect to those containers from systemd (not Docker).
- Operator uses UFW or other host firewall.

## Skip If (ANY kills it)

- Full stack runs in Docker (including app) — use docker compose only.
- Kubernetes / Nomad / Swarm — compose is dev-only there.
- Single ephemeral container — `docker run` is simpler.

**Ефективно для:**

- Solo SaaS з Postgres + Redis у Docker, додатком на systemd.
- Setups де UFW deny-by-default але Docker слив порти.
- Команди що мігрують з docker run на compose.
- Аудит compose-файлу перед прод-релізом.

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
| `solo/infra/server-craft/firewall-management` | 127.0.0.1 binds depend on UFW deny-by-default. |
| `solo/infra/server-craft/health-checks-autoheal` | healthcheck patterns shared. |

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
| `templates/skeleton.md` | Compose audit report listing bind / healthcheck / depends_on / volumes. |
| `templates/_smoke-test.md` | Minimum viable filled-in compose audit. |
| `templates/docker-compose.yml` | Compose template with 127.0.0.1 binds + healthchecks + named volumes. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-compose-patterns.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[firewall-management]]
- [[health-checks-autoheal]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
