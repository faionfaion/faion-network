# Multi-Agent Orchestration Decision Tree

## Summary

**One-sentence:** Produces a multi-agent orchestration decision record — topology pick, hand-off protocol, judge-actor justification, measurable rollback trigger.

**One-paragraph:** Multi-agent systems are popular and almost always wrong by default. This methodology produces a typed decision record naming: the topology (single+tools / hierarchical / collaborative / conversational), the hand-off protocol (task_id + scoped context + success criteria + escalation), whether a judge-actor split is empirically justified (quality_lift_pp ≥ 2 at acceptable cost_multiplier), and a rollback trigger (latency, cost, quality vs single-agent baseline). Without this, teams ship multi-agent for "separation of concerns" and pay 30-100% extra latency for no measurable quality lift.

**Ефективно для:** ML-engineer, що дебатує "agent vs orchestrator" і хоче явну, ревьюваємо decision з measurable rollback — а не фанбойство.

## Applies If (ALL must hold)

- Considering splitting a single-agent + tools setup into multiple agents.
- A current baseline (single-agent + tools) exists or can be reconstructed.
- An eval that can measure quality lift at the relevant task is available.
- A named owner can run the periodic re-evaluation.

## Skip If (ANY kills it)

- Single-task workflow with no hand-off — multi-agent adds overhead for zero gain.
- Prototype where neither quality nor cost has been measured yet — build single-agent first.
- Regulatory / compliance overrides force a specific topology.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current single-agent baseline (latency, cost, quality) | report | observability |
| Eval suite measuring task quality | JSONL | eval repo |
| List of distinct subtasks | doc | architecture |
| Cost-multiplier budget for multi-agent | YAML | finops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/ml-engineer/multi-agent-design-patterns` | Provides topology vocabulary. |
| `geek/ai/ml-engineer/multi-agent-systems` | Production patterns reference. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: single-agent default, topology fit, hand-off protocol, judge-actor justified, rollback trigger. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the orchestration decision record. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: split-for-separation, chat-history hand-off, cargo-cult judge, no rollback, no rebaseline. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes from baseline + subtask count + measured quality lift. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-topology-pick` | sonnet | Pattern matching against the four topologies. |
| `decide-judge-actor-roi` | opus | Cost vs quality reasoning. |
| `audit-rollback-trigger` | haiku | Schema-presence check. |

## Templates

| File | Purpose |
|---|---|
| `templates/orchestration-decision.json` | JSON schema for the output. |
| `templates/orchestration-decision.md` | Markdown skeleton with required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-multi-agent-orchestration-decision-tree.py` | Enforce contract: topology valid, hand-off protocol fields present, judge-actor measured, rollback trigger present. | After subagent return. |

## Related

- [[ai-agent-patterns]]
- [[multi-agent-design-patterns]]
- [[agents-react-pattern]]

## Decision tree

The tree at `content/06-decision-tree.xml` triages: is single-agent + tools the baseline? → measure quality lift at the proposed multi-agent topology → adopt only if lift_pp ≥ 2 AND cost_multiplier within budget. Walk it before refactoring a working single-agent into a multi-agent debate club.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/orchestration-decision.json`

```json
{
  "_purpose": "JSON Schema for the Multi-Agent Orchestration decision record.",
  "_consumes": "decision-record.json from subagent",
  "_produces": "validation report for validate-multi-agent-orchestration-decision-tree.py",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/multi-agent-orchestration-decision",
  "type": "object",
  "required": [
    "subtasks",
    "topology_pick",
    "handoff_protocol",
    "judge_actor_used",
    "rollback_trigger",
    "owner"
  ],
  "properties": {
    "subtasks": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "topology_pick": {
      "enum": [
        "single",
        "hierarchical",
        "collaborative",
        "conversational"
      ]
    },
    "handoff_protocol": {
      "type": "object",
      "required": [
        "task_id",
        "scoped_context",
        "success_criteria",
        "escalation"
      ],
      "properties": {
        "task_id": {
          "type": "string"
        },
        "scoped_context": {
          "type": "string"
        },
        "success_criteria": {
          "type": "string"
        },
        "escalation": {
          "type": "string"
        }
      }
    },
    "judge_actor_used": {
      "type": "object",
      "required": [
        "used",
        "quality_lift_pp",
        "cost_multiplier"
      ],
      "properties": {
        "used": {
          "type": "boolean"
        },
        "quality_lift_pp": {
          "type": "number"
        },
        "cost_multiplier": {
          "type": "number"
        }
      }
    },
    "rollback_trigger": {
      "type": "object",
      "required": [
        "latency_threshold_ms",
        "cost_threshold_multiplier",
        "quality_threshold_pp"
      ],
      "properties": {
        "latency_threshold_ms": {
          "type": "integer"
        },
        "cost_threshold_multiplier": {
          "type": "number"
        },
        "quality_threshold_pp": {
          "type": "number"
        }
      }
    },
    "owner": {
      "type": "string",
      "minLength": 2,
      "not": {
        "pattern": "(?i)^(team|we|us|engineering|the (team|squad|group))$"
      }
    }
  }
}
```
