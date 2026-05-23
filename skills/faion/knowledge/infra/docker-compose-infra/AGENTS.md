# Docker Compose (Infrastructure)

## Summary

**One-sentence:** Generates a production-grade Compose stack — internal networks for DB tier, deploy.resources caps, restart unless-stopped, modern compose.yaml filename, named volumes.

**One-paragraph:** Generates a production-grade Compose stack — internal networks for DB tier, deploy.resources caps, restart unless-stopped, modern compose.yaml filename, named volumes.

**Ефективно для:**

- Solo team provisioning a VPS with shared infra (PG + Redis + RMQ).
- Single-host staging or small prod (≤10 services).
- Orchestrated restarts with healthcheck-gated ordering.

## Applies If (ALL must hold)

- Defining multi-container application stacks (app + DB + cache + worker).
- Provisioning shared infrastructure services on a VPS.
- Setting up isolated per-project stacks with own networks, volumes, and resource limits.
- Rolling out infrastructure updates requiring orchestrated service restarts.

## Skip If (ANY kills it)

- Single-container deployments — docker run + systemd is simpler.
- Production at scale requiring multi-host orchestration.
- Zero-downtime blue-green deploys — Compose lacks traffic shifting.
- Stateless functions or serverless workloads.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service tier map | yaml | which services are app / db / cache |
| Resource caps | yaml | cpu + mem per service |
| Network topology | yaml | internal vs external networks |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| docker-compose-devops | Base Compose V2 rules. |
| server-init-bootstrap | Hardened host. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-internal-network-for-db, r2-resource-limits, r3-restart-unless-stopped, r4-modern-filename, r5-named-volumes-only | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Docker Compose (Infrastructure) artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: flat-network-leak, no-resource-limits, legacy-filename | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-docker-compose` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-docker-compose` | sonnet | Bounded structural check against the output contract. |
| `review-docker-compose` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/docker-compose.json` | JSON skeleton matching the output contract. |
| `templates/docker-compose.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-compose.py` | Validate Docker Compose (Infrastructure) output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[docker-compose-devops]]
- [[docker-compose-cicd]]
- [[server-init-bootstrap]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
