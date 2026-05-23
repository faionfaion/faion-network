# purpose: C4 diagram-pack spec.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a c4-model artefact validating against scripts/validate-c4-model.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: c4-pack-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
toolchain: <structurizr|mermaid|plantuml>
---

## Level 1 — System Context

- Path: `docs/architecture/c4/01-context.<ext>`
- Audience: non-technical stakeholders, leadership.
- Includes: system, users, external systems.

## Level 2 — Containers

- Path: `docs/architecture/c4/02-containers.<ext>`
- Audience: engineers, ops.
- Includes: deployable units + their technology stack + relationships.

## Level 3 — Components (per container)

- Path: `docs/architecture/c4/03-components-<container>.<ext>`
- Audience: engineers working on this container.
- Includes: components inside one container + relationships.

## Sync policy

- Diagrams live in `docs/architecture/c4/` and ship in every PR that adds/removes a container or external system.
- CI lint compares container list in L2 against the deploy manifest; mismatch blocks merge.
