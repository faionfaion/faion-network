# AI Agent Patterns

## Summary

**One-sentence:** Picks one of six control-flow patterns (CoT / ReAct / Tool Use / Plan-and-Execute / Reflection / Tree-of-Thoughts) and a matching framework (raw SDK / LangGraph / AutoGen / CrewAI / OpenAI Agents SDK) for a new agent task.

**One-paragraph:** Single prompt-response is insufficient for any non-trivial agent task; choosing the right control-flow pattern matters more than upgrading the underlying model. This methodology classifies the task on three axes (needs-tools, step-count, branching), maps to CoT / ReAct / Plan-and-Execute / Tool Use, and then maps the chosen pattern to a framework that fits team experience and dependency budget. Output is one decision record committed alongside the agent code.

**Ефективно для:** Команд, які тиждень обговорюють «який фреймворк взяти» замість «яка форма агента нам потрібна»; за годину дає named pattern + framework з обґрунтуванням, прив'язаним до конкретних характеристик задачі.

## Applies If (ALL must hold)

- New agent feature being scoped (no pattern committed yet).
- Task is non-trivial — at least one of: needs tools, has multi-step plan, requires iteration.
- Team is willing to commit to a single pattern for the feature (no parallel experiments).
- Latency budget allows ≥2 LLM round-trips.
- Owner can review the chosen framework's dependency cost.

## Skip If (ANY kills it)

- Task is solvable in one LLM call (no tools, single-shot output).
- Hard real-time SLA < 500ms — multi-iteration patterns are too slow.
- One-off script where framework dependency cost exceeds project lifetime.
- Creative generation where strict control flow degrades quality.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task brief | natural language ≤500 chars | Operator |
| Tool inventory | JSON list `{name, description, schema}` | Tool registry |
| Latency budget | seconds | SLA owner |
| Framework experience matrix | team handles → familiar frameworks | Tech lead |
| Named owner | handle | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-patterns/AGENTS.md` | Sibling — pattern selection logic; this methodology extends it with framework choice. |
| `geek/ai/ai-agents/agent-shape-decision-frame/AGENTS.md` | Shape selection runs first; pattern runs inside chosen shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: classified-in-writing, comment-pattern-at-top, framework-pinned, schema-tools, max-steps-guard, default-ReAct, Plan-Execute at depth ≥5, Reflection for self-correction, ToT only when branching | ~1500 |
| `content/02-output-contract.xml` | essential | JSON Schema for the pattern+framework decision record | ~700 |
| `content/03-failure-modes.xml` | essential | 10 antipatterns (no classification, framework first, no max-steps, vague tool desc, no tracing, ToT cargo-cult, over-deep ReAct, missing Reflection, multi-agent for breadth, verbal decision) | ~1500 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify → pick pattern → pick framework → define tools → ship behind flag | ~1000 |
| `content/05-examples.xml` | medium | Three worked examples (CoT, ReAct, Plan-and-Execute) | ~1000 |
| `content/06-decision-tree.xml` | essential | Pattern tree + framework tree | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task` | haiku | Three-question classification. |
| `pick_pattern_and_framework` | sonnet | Per-instance judgment. |
| `author_decision_record` | sonnet | Final composition. |
| `executive_review` | opus | For multi-agent / framework-with-runtime-cost decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the decision record. |
| `templates/decision-record.example.json` | Filled minimal valid example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision record. | After subagent emits record. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-patterns]] — narrower scope, three patterns only.
- peer: [[plan-execute-vs-react]] — deeper on Plan-and-Execute vs ReAct trade-off.

## Decision tree

See `content/06-decision-tree.xml`. First tree: pattern selection on three axes (needs-tools, step-count, branching). Second tree: framework selection given chosen pattern + team experience + dependency budget.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ai-agent-patterns/record.json",
  "title": "AI Agent Patterns Decision Record",
  "description": "purpose=schema; consumes=task-brief+tool-inventory+experience-matrix; produces=pattern+framework-decision; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "task_id",
    "classification",
    "chosen_pattern",
    "chosen_framework",
    "framework_pin",
    "caps",
    "tools",
    "rationale",
    "rejected",
    "owner",
    "version",
    "produced_at"
  ],
  "properties": {
    "task_id": {
      "type": "string"
    },
    "classification": {
      "type": "object",
      "required": [
        "needs_tools",
        "step_count",
        "branching"
      ],
      "properties": {
        "needs_tools": {
          "type": "boolean"
        },
        "step_count": {
          "type": "integer",
          "minimum": 1
        },
        "branching": {
          "type": "boolean"
        }
      }
    },
    "chosen_pattern": {
      "type": "string",
      "enum": [
        "cot",
        "react",
        "plan-and-execute",
        "tool-use"
      ]
    },
    "chosen_framework": {
      "type": "string",
      "enum": [
        "raw-sdk",
        "langgraph",
        "autogen",
        "crewai",
        "openai-agents-sdk",
        "claude-code"
      ]
    },
    "framework_pin": {
      "type": "string",
      "pattern": "==\\d+\\.\\d+(\\.\\d+)?"
    },
    "caps": {
      "type": "object",
      "required": [
        "max_steps",
        "loop_detect"
      ],
      "properties": {
        "max_steps": {
          "type": "integer",
          "minimum": 1,
          "maximum": 50
        },
        "loop_detect": {
          "type": "boolean"
        }
      }
    },
    "tools": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "description"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "description": {
            "type": "string",
            "minLength": 30
          },
          "schema_ref": {
            "type": "string"
          }
        }
      }
    },
    "rationale": {
      "type": "string",
      "minLength": 40
    },
    "rejected": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "pattern",
          "framework",
          "reason"
        ]
      }
    },
    "owner": {
      "type": "string"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

### `templates/decision-record.example.json`

```json
{
  "task_id": "T-research-001",
  "classification": {
    "needs_tools": true,
    "step_count": 4,
    "branching": false
  },
  "chosen_pattern": "react",
  "chosen_framework": "raw-sdk",
  "framework_pin": "anthropic==0.39.0",
  "caps": {
    "max_steps": 15,
    "loop_detect": true
  },
  "tools": [
    {
      "name": "web_search",
      "description": "Full-text web search via SearXNG, returns top 10 results",
      "schema_ref": "schemas/web_search.json"
    }
  ],
  "rationale": "Task needs tools (research) but step count is small (4) and no branching \u2014 ReAct on raw SDK is the smallest fit.",
  "rejected": [
    {
      "pattern": "plan-and-execute",
      "framework": "langgraph",
      "reason": "step count too small to justify graph"
    }
  ],
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "produced_at": "2026-05-22T16:00:00Z"
}
```
