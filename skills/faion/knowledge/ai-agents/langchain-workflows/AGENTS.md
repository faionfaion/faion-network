# Langchain Workflows

## Summary

**One-sentence:** Designs a LangGraph state machine (typed state, nodes, conditional edges, interrupts, subgraphs) and emits a workflow-spec decision-record.

**One-paragraph:** LangGraph workflows fail from nested state, missing interrupts on destructive nodes, and uncompacted accumulating fields. This methodology converts a workflow profile (steps, branches, HITL points, parallelism) into a deterministic LangGraph spec: TypedDict state, node list, edge graph, interrupt_before set, subgraph composition.

**Ефективно для:** solopreneur orchestrating a multi-step AI workflow with human approval gates.

## Applies If (ALL must hold)

- Workflow has ≥3 steps with branching logic.
- ≥1 step is destructive or needs human approval.
- State must persist across pauses/restarts.
- LangGraph (or LangChain) is the chosen framework.
- You can build and run a checkpointer (in-mem for dev, sqlite/postgres for prod).

## Skip If (ANY kills it)

- Workflow is a linear chain — plain LCEL is enough.
- No state to persist — stateless functions suffice.
- Framework is Anthropic SDK / OpenAI Agents SDK — use their native workflow primitives.
- Steps run only once — orchestrate with a job runner, not LangGraph.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `workflow-profile.yaml` | YAML: steps, branches, hitl_points, parallel_branches, persistence_target | author writes |
| `Node implementations` | Python module with one function per node | developer authoring |
| `Checkpointer config` | env vars for SQLite/Postgres | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[langchain-basics]] | Runnable + LCEL. |
| [[langchain-memory]] | Workflow state ≈ memory; same persistence rules. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Migrated rules for flat state, partial updates, conditional edges, interrupt_before, subgraphs. | ~1000 |
| `content/02-output-contract.xml` | essential | workflow-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Nested state, missing interrupt, uncompacted accumulator, in-memory checkpoint in prod. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step design procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/workflow-profile.yaml` | Input contract. |
| `templates/workflow-spec.md.j2` | Output skeleton. |
| `templates/workflow-spec.md` | Output skeleton. Generated from `templates/workflow-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/graph.py` | Working StateGraph wiring. |
| `templates/_smoke-test.yaml` | Minimum profile. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-langchain-workflows.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[langchain-memory]]
- [[map-reduce-send-fanout]]
- [[max-turns-circuit-breaker]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on hitl_points (≥1 → interrupt_before required), then on parallel_branches (>0 → Send/fan-out), then on persistence_target (in-mem dev, sqlite/postgres prod). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/workflow-profile.yaml`

```yaml
steps: TODO          # fill with concrete value per the driver definition
branches: TODO          # fill with concrete value per the driver definition
hitl_points: TODO          # fill with concrete value per the driver definition
parallel_branches: TODO          # fill with concrete value per the driver definition
persistence_target: TODO          # fill with concrete value per the driver definition
```

### `templates/graph.py`

```python
"""Reference artefact for langchain-workflows. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "langchain-workflows", "version": "2.0.0"})
    return 0 if out["slug"] == "langchain-workflows" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
steps: low
branches: low
hitl_points: low
parallel_branches: low
persistence_target: low
```
