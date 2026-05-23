# purpose: Architecture style ADR.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a decision-tree-architecture-style artefact validating against scripts/validate-decision-tree-architecture-style.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: architecture-style-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
choice: <monolith|modular-monolith|microservices>
reversibility: <one_way_door_costly|partial_two_way>
---

## Context
- Team size: <N> (12mo: <M>)
- Deploy frequency target: <K/day or week>
- DevOps maturity (DORA): <elite|high|medium|low>
- Domain coupling: <tight|loose>
- Regulatory regime: <none|GDPR|HIPAA|PCI-DSS|SOC2>

## Decision
**<choice>** — because:
1. <reason>
2. <reason>

## Alternatives Rejected
| Option | Reason |
|--------|--------|
| ... | ... |

## Reversibility
- Tier: <as tagged above>
- Rollback path: <eng weeks + dollars>
