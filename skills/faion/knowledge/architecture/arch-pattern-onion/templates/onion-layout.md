# purpose: Onion Architecture layout spec.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a arch-pattern-onion artefact validating against scripts/validate-arch-pattern-onion.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: onion-layout-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Layer 1 — Domain Model
Modules: `Domain/Model`
- Entities, value objects, aggregates.

## Layer 2 — Domain Services
Modules: `Domain/Services`
- Behaviour spanning aggregates.
- Depends on: Domain Model only.

## Layer 3 — Application Services
Modules: `Application/Services`
- Orchestrates domain services for use cases.
- Depends on: Domain Services + Domain Model.

## Layer 4 — Infrastructure / UI / Tests
Modules: `Infrastructure/`, `UI/`, `Tests/`
- DB, HTTP, framework wiring, integration tests.
- Depends on: Application Services + Domain.

## Lint contract
- Tool: importlinter / ArchUnit
- Inner layers MUST NOT import from outer layers.
