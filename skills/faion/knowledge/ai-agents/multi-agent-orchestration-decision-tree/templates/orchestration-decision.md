<!--
purpose: Markdown skeleton for an authored Multi-Agent Orchestration decision record.
consumes: subtask list + baseline metrics + eval result + cost budget + owner
produces: filled-in record matching the JSON schema sibling file
depends-on: content/02-output-contract.xml
token-budget-impact: 0 — template
variables:
  - name: slug
    type: string
    required: true
    description: Kebab-case id naming the workflow this decision binds - "invoice-triage-orchestration". One workflow per record; a repo-wide topology decision is how every stage ends up paying for a judge.
  - name: owner
    type: string
    required: true
    description: One named handle accountable for the topology. When the cost multiplier is questioned at month end, this is who answers.
  - name: topology
    type: enum
    required: true
    options: [single, hierarchical, collaborative, conversational]
    description: Which topology you are committing to. single is the default and needs no defence; the other three each add a hand-off, and every hand-off is a place context is lost and tokens are spent again.
  - name: scoped_context
    type: text
    required: true
    description: Exactly which subset of context crosses each hand-off. The failure mode is passing everything - cost multiplies and the sub-agent starts answering the parent's question instead of its own.
  - name: success_criteria
    type: text
    required: true
    description: How a sub-agent knows it is finished, stated so a machine could check it. "A good summary" is not a criterion; "JSON validates against schema X and cites at least two source ids" is.
  - name: rationale
    type: text
    required: true
    description: Two sentences citing the measured single-agent baseline and why it is not enough. Single agent is the default - this field is where you overturn it, with numbers you actually ran.
-->

# Multi-Agent Orchestration Decision — `{{slug}}`

- **Owner:** `{{owner}}`
- **Topology pick:** `{{topology}}`

## Subtasks

- [distinct subtask 1]
- [distinct subtask 2]

## Hand-off protocol

| Field | Value |
|---|---|
| task_id | `[id schema]` |
| scoped_context | {{scoped_context}} |
| success_criteria | {{success_criteria}} |
| escalation | `[who or what handles failure]` |

## Judge–actor (only if used)

| Metric | Value |
|---|---|
| quality_lift_pp | `[>= 2 required]` |
| cost_multiplier | `[within budget]` |

## Rollback trigger

| Metric | Threshold |
|---|---|
| latency_threshold_ms | `[value]` |
| cost_threshold_multiplier | `[value]` |
| quality_threshold_pp | `[value]` |

## Rationale

{{rationale}}
