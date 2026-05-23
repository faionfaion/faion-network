# CAP / PACELC Walkthrough

## Summary

**One-sentence:** Produces a CAP/PACELC decision record for a specific microservice-extraction or datastore choice, naming AP vs CP under partition and the EL vs EC trade-off otherwise.

**One-paragraph:** When extracting state across services or picking AP vs CP datastores, this methodology walks the architect through CAP (under partition: pick Availability OR Consistency) and PACELC (Else: Latency vs Consistency) for the specific split. Output: a versioned decision record naming the chosen mode, the rationale citing measured RPO/RTO + read/write workload, and a single accountable owner.

**Ефективно для:**

- Microservice extraction — який бік CAP кожен сервіс обирає.
- Datastore selection — AP (Dynamo, Cassandra) чи CP (Spanner, etcd).
- PACELC: latency-vs-consistency коли мережа здорова — теж рішення.
- Versioned ADR з owner — потрібен для post-mortem traceability.

## Applies If (ALL must hold)

- Task is an instance of role-software-architect/Microservice extraction safety gate OR closely-adjacent.
- Operator has Prerequisites available before starting.
- Output will be consumed by a downstream agent or human reviewer.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Team already maintains a working ADR for this split.
- Greenfield prototype with no production users.
- Regulatory context overrides any in-methodology guidance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| RPO/RTO targets | policy doc | service owner |
| Read/write workload split | metrics | observability |
| Network partition exposure | infra map | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-design]] | Service-boundary doc that justifies the split being analysed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-split judgment on AP vs CP and EL vs EC. |
| `review-for-compliance` | opus | Cross-service synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cap-pacelc-walkthrough.json` | JSON skeleton matching the output contract. |
| `templates/cap-pacelc-walkthrough.md` | Markdown skeleton naming both axes. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cap-pacelc-walkthrough.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-cap-pacelc-walkthrough.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[microservices-design]]
- [[choreography-vs-orchestration-decision]]

## Decision tree

See `content/06-decision-tree.xml`. Tree separates the two CAP/PACELC axes and routes the decision to AP vs CP first, then EL vs EC; both must be named.
