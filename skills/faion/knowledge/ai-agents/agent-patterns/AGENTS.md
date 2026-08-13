# Agent Patterns

## Summary

**One-sentence:** Picks the right control-flow pattern (ReAct, Plan-and-Execute, Reflexion) for an autonomous agent task and locks it in with iteration caps and a termination signal.

**One-paragraph:** Different agent tasks require different control flow patterns. ReAct (Reason + Act) loops are general-purpose for tool-driven investigation. Plan-and-Execute creates a structured plan upfront for known multi-step projects. Reflexion wraps an inner agent with self-critique and retry for tasks where success is objectively checkable (code, math, structured extraction). This methodology produces a single decision record naming the chosen pattern, max iterations/attempts, the termination signal, and the rationale for not picking the other two patterns.

**Ефективно для:** Ситуацій, де агентний цикл ще не визначено, але є зрозуміла мета і набір інструментів — методологія за 10 хвилин обмежує простір рішень до однієї перевіреної архітектури плюс жорсткі ліміти, замість «спробуємо ReAct і подивимось».

## Applies If (ALL must hold)

- Task requires ≥2 tool calls or ≥2 reasoning steps (not a single-shot prompt).
- The task has either a verifiable success signal or a bounded scope of subtasks.
- Tool access is available (HTTP, filesystem, code execution, or MCP server).
- The owner can budget at least 5 LLM round-trips for the task.
- A human reviewer is named for the final output before it is acted upon.

## Skip If (ANY kills it)

- Single-step retrieval or classification — pattern overhead is wasted.
- Latency budget < 2 seconds end-to-end — patterns add round-trips.
- No verifiable success criterion exists (Reflexion has no termination signal).
- No tools accessible — ReAct collapses into plain chain-of-thought.
- Strict budget of < 5 LLM calls — patterns spend iterations.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task description | natural-language brief, ≤500 chars | Operator / parent agent |
| Tool inventory | JSON list of `{name, description, schema}` | Tool registry / MCP catalogue |
| Success criterion | Either a test command, a JSON schema, or a checklist | Owner of the downstream artefact |
| Budget caps | `max_iterations` + `max_attempts` (ints) | Operator (cost policy) |
| Pattern preference (optional) | one of `react|plan-and-execute|reflexion` | Operator override |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/autonomous-agents/AGENTS.md` | Provides the broader autonomous-agent vocabulary (planner/executor/critic). |
| `geek/ai/ai-agents/ai-agent-patterns/AGENTS.md` | Sibling overview — clarifies when CoT vs full agent loop is needed. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (caps, idempotent tools, terminal condition, model choice, observability, human-in-loop) | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (loops, plan staleness, runaway Reflexion, context overflow, fabricated tools) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify task → pick pattern → fix caps → wire signals → emit record | ~1100 |
| `content/05-examples.xml` | medium | Worked examples for each pattern (research / code-fix / build-feature) | ~1100 |
| `content/06-decision-tree.xml` | essential | Binary decision tree: success-signal? → bounded-subtasks? → ReAct/Plan/Reflexion leaf | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_shape` | haiku | Cheap structured classification of task vs tool inventory. |
| `pick_pattern` | sonnet | Per-instance judgment — applies decision tree to task features. |
| `author_decision_record` | sonnet | Composes the final JSON output with rationale. |
| `review_for_high_stakes` | opus | Used only when task is irreversible or production-facing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.json` | JSON Schema for `agent-patterns` output decision record. |
| `templates/decision-record.example.json` | Filled minimal valid example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-patterns.py` | Validate a decision-record file against the JSON Schema. | After subagent returns, before downstream agent reads it. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[ai-agent-patterns]] — overview of all named patterns including framework choices.
- peer: [[autonomous-agents]] — broader autonomous-agent operating context.

## Decision tree

See `content/06-decision-tree.xml`. The tree asks three observables in order: (1) is there a deterministic success signal? (2) are subtasks enumerable up-front? (3) is the action irreversible? Leaves point to ReAct, Plan-and-Execute, Reflexion, or `escalate-to-human`. Used when the operator hasn't pre-specified a pattern; never overrides an explicit operator choice.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-record.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/agent-patterns/decision-record.json",
  "title": "Agent-Patterns Decision Record",
  "description": "Output contract for the agent-patterns methodology. purpose=schema; consumes=task-brief+tool-inventory; produces=decision-record; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "task_id",
    "chosen_pattern",
    "caps",
    "terminal_condition",
    "rationale",
    "rejected_patterns",
    "actor_model",
    "human_gate_required",
    "version",
    "produced_at"
  ],
  "properties": {
    "task_id": {
      "type": "string",
      "minLength": 1
    },
    "chosen_pattern": {
      "type": "string",
      "enum": [
        "react",
        "plan-and-execute",
        "reflexion",
        "escalate-to-human"
      ]
    },
    "caps": {
      "type": "object",
      "properties": {
        "max_iterations": {
          "type": "integer",
          "minimum": 1,
          "maximum": 50
        },
        "max_steps": {
          "type": "integer",
          "minimum": 1,
          "maximum": 30
        },
        "max_attempts": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10
        },
        "max_iterations_per_step": {
          "type": "integer",
          "minimum": 1,
          "maximum": 20
        }
      },
      "additionalProperties": false
    },
    "terminal_condition": {
      "type": "string",
      "minLength": 5
    },
    "rationale": {
      "type": "string",
      "minLength": 40
    },
    "rejected_patterns": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "pattern",
          "reason"
        ],
        "properties": {
          "pattern": {
            "type": "string",
            "enum": [
              "react",
              "plan-and-execute",
              "reflexion"
            ]
          },
          "reason": {
            "type": "string",
            "minLength": 10
          }
        },
        "additionalProperties": false
      }
    },
    "actor_model": {
      "type": "string"
    },
    "critic_model": {
      "type": "string"
    },
    "human_gate_required": {
      "type": "boolean"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "chosen_pattern": {
            "const": "reflexion"
          }
        }
      },
      "then": {
        "required": [
          "critic_model"
        ]
      }
    }
  ]
}
```

### `templates/decision-record.example.json`

```json
{
  "task_id": "T-2026-05-22-001",
  "chosen_pattern": "reflexion",
  "caps": {
    "max_attempts": 3,
    "max_iterations": 8
  },
  "terminal_condition": "pytest tests/test_parser.py exits 0",
  "rationale": "Task is parser-fix with a deterministic success signal (test suite). Subtasks are not enumerable up-front because the model must discover failure modes through iteration. Action is reversible (local code edits in a feature branch).",
  "rejected_patterns": [
    {
      "pattern": "react",
      "reason": "no built-in retry; would loop once on failed test and stop"
    },
    {
      "pattern": "plan-and-execute",
      "reason": "subtasks unknown until model sees test output"
    }
  ],
  "actor_model": "claude-sonnet-4",
  "critic_model": "claude-haiku-4",
  "human_gate_required": false,
  "version": "1.0.0",
  "produced_at": "2026-05-22T10:14:00Z"
}
```
