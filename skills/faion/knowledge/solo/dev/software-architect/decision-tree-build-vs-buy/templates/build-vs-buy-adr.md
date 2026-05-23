# purpose: Build vs Buy ADR template.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a decision-tree-build-vs-buy artefact validating against scripts/validate-decision-tree-build-vs-buy.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: build-vs-buy-<capability>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
adr_id: NNN
capability: <name>
choice: <build|buy|adopt-oss>
reversibility: <partial_two_way|one_way_door_costly|one_way_door_irrevocable>
---

## Context
<one paragraph: what the capability does, who uses it, why now>

## Scoring

| Axis | Build | Buy | Adopt OSS |
|------|-------|-----|-----------|
| Strategic differentiation | 1-5 | 1-5 | 1-5 |
| 3-yr TCO | $ | $ | $ |
| Time-to-value | weeks | weeks | weeks |
| Vendor lock-in risk | low | high | low |

## Decision
**<choice>** — because:
1. <reason 1>
2. <reason 2>

## Alternatives Rejected
| Option | Reason rejected |
|--------|-----------------|
| ... | ... |

## Reversibility
- Tier: <as tagged above>
- Rollback path: <eng weeks + dollars + customer impact>
