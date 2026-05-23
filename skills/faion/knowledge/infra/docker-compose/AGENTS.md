# Docker Compose (DevOps)

## Summary

**One-sentence:** Generates a Docker Compose V2 stack — healthchecks on every depends_on target, named volumes, 127.0.0.1 port bindings to bypass UFW, no legacy version: field.

**One-paragraph:** Generates a Docker Compose V2 stack — healthchecks on every depends_on target, named volumes, 127.0.0.1 port bindings to bypass UFW, no legacy version: field.

**Ефективно для:**

- Solo team running a local dev stack (app + db + cache + broker).
- Single-host staging or small prod (≤10 services).
- Prototyping microservice topology before Kubernetes.

## Applies If (ALL must hold)

- Stack has ≥2 services with depends_on relationships.
- Host is a single VPS (no orchestrator).
- UFW or another host firewall is active.
- Persistent data exists (database, queues, blob).

## Skip If (ANY kills it)

- Multi-host production at scale — use Kubernetes or Docker Swarm.
- Rolling-update zero-downtime — Compose restarts, does not roll.
- Helm/K8s manifests already exist — dual maintenance burden.
- Enterprise secrets — Compose secrets limited; use Vault.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | list | service list with images + roles |
| Host firewall config | yaml | ufw status |
| Persistent data paths | yaml | volume names per service |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| server-init-bootstrap | Hardened host baseline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-no-version-field, r2-healthcheck-on-depended, r3-port-bind-localhost, r4-named-volumes, r5-restart-policy | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Docker Compose (DevOps) artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: ufw-bypass, missing-healthcheck, data-loss-on-reset | 800 |
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
| `scripts/validate-docker-compose.py` | Validate Docker Compose (DevOps) output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[docker-compose-cicd]]
- [[docker-compose-infrastructure]]
- [[server-init-bootstrap]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
