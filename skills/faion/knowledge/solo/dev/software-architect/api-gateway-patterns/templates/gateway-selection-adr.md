# purpose: ADR template documenting gateway pattern + product selection.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a api-gateway-patterns artefact validating against scripts/validate-api-gateway-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: api-gateway-patterns-<client>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
pattern: <edge|bff|per-service|none>
product: <kong|traefik|envoy|aws-apigw|apollo-router>
---

## Context

<one paragraph: workload + clients + cross-cutting concerns to consolidate>

## Decision

Use the **<pattern>** pattern with **<product>** as the gateway.

## Alternatives Rejected

| Option | Reason rejected |
|--------|-----------------|
| <option> | <reason> |

## Consequences

- <trade-off accepted>
- <operational cost>

## Rollback path

<how we'd revert if the choice is wrong within 6 months>
