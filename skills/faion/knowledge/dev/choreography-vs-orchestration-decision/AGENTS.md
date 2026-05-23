# Choreography vs Orchestration Decision

## Summary

**One-sentence:** Produces a versioned ADR choosing choreography (event-driven, no central coordinator) vs orchestration (central saga coordinator) for a specific cross-service workflow, with operational ownership named.

**One-paragraph:** When event-driven-architecture mentions sagas but does not decide choreography vs orchestration, this methodology produces the decision. Operational ownership is the determining factor: choreography spreads ownership (and debugging cost) across emitters; orchestration concentrates it on the coordinator service. The ADR names the chosen pattern, the workflow it covers, and a single accountable owner.

**Ефективно для:**

- Saga рішення — choreography чи orchestration на конкретному flow.
- Operational ownership: хто володіє debug + retry + DLQ.
- ADR форм у git-store, versioned + reviewable.
- Anti-debate-club: рішення в артефакті, не на стенду.

## Applies If (ALL must hold)

- Task is an instance of role-software-architect/Microservice extraction safety gate OR adjacent.
- Operator has the workflow definition + service map available.
- Output will be consumed downstream (not discarded).
- Tier == pro or higher.

## Skip If (ANY kills it)

- Team already maintains a working ADR for this workflow.
- Greenfield prototype with no production users.
- Single-service workflow — no saga, no decision.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow definition (steps + branches) | diagram or BPMN | team |
| Service map (owners + emit/consume events) | Markdown table | platform |
| Operational SLOs (debug latency, retry policy) | doc | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[microservices-design]] | Service boundaries are the precondition for the saga split |

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
| `draft-inputs-summary` | haiku | Mechanical capture of workflow + services. |
| `synthesize-decision` | sonnet | Per-workflow judgment on ownership vs latency trade-off. |
| `review-for-compliance` | opus | Cross-team synthesis when ownership is contested. |

## Templates

| File | Purpose |
|------|---------|
| `templates/choreography-vs-orchestration-decision.json` | JSON skeleton matching the output contract. |
| `templates/choreography-vs-orchestration-decision.md` | Markdown skeleton with both options + trade-offs. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-choreography-vs-orchestration-decision.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-choreography-vs-orchestration-decision.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[cap-pacelc-walkthrough]]
- [[microservices-design]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates on workflow size and natural ownership distribution; orchestration is the default unless ownership is already distributed.
