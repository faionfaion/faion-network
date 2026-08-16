# Handoff Payload — ID + Minimal Metadata

## Summary

**One-sentence:** Constrains every multi-agent handoff to a typed `{task_id, target_agent, decision_metadata}` payload, with the receiving agent pulling state from a shared append-only store, preventing O(n²) context growth and enabling auditable replay.

**One-paragraph:** When agent A hands off to agent B in a multi-agent topology, the handoff payload is a structured `{task_id, target_agent, decision_metadata}` object — never the conversation history, never the raw input. Agent B reads task state from a shared store (file, queue, DB) keyed by `task_id`. The supervising router returns `SupervisorDecision` objects, not message threads. Each agent's context is sized to its job, not to the cumulative conversation.

**Ефективно для:** мульти-агентних мереж із спеціалізованими ролями (researcher → writer → editor; classifier → worker), де лінійний переказ всієї історії убиває контекст.

## Applies If (ALL must hold)

- Multi-agent topology with role-specialised agents.
- Supervisor/worker pattern where the supervisor routes.
- Pipeline length is more than 2 hops or each step has a small relevant subset of cumulative state.

## Skip If (ANY kills it)

- Single-agent loop — handoff is a no-op.
- Tightly-coupled co-reasoning where two agents must see each other's intermediate thoughts.
- Throwaway prototype where setting up a task store is more work than the agent.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Shared store | File queue, Redis, DB, or object store with `get/append_event/set_status` ops | Infrastructure |
| Agent role registry | `target_agent` enum | Application config |
| Initial task seed | Inserted into the store before first handoff | Trigger source |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `file-reference-passing` | Handoff payloads carry IDs, content lives in the store. |
| `idempotent-write-tools` | Append-only events make handoffs replayable. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules: payload shape, no-conversation-forward, store-first-action, supervisor-structured-output, append-only-events | ~1000 |
| `content/02-output-contract.xml` | essential | Handoff payload schema + SupervisorDecision schema | ~900 |
| `content/03-failure-modes.xml` | essential | Conversation forwarding, free-form routing, overwriting state | ~700 |
| `content/06-decision-tree.xml` | essential | Pick supervisor vs peer-to-peer vs hierarchical pattern | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate the payload | haiku | Pure structured output |
| Supervisor routing decision | sonnet | Requires understanding of role responsibilities |
| Design new agent mesh topology | opus | Architectural tradeoffs |

## Templates

| File | Purpose |
|------|---------|
| `templates/handoff.json` | JSON Schema for the handoff payload object |
| `templates/supervisor-decision.json` | JSON Schema for the supervisor router's structured output |
| `templates/_smoke-test.json` | Minimum valid handoff payload |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-handoff-id-payload.py` | Validates a handoff payload against the schema | Before passing any handoff to the next agent |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[file-reference-passing]]
- [[idempotent-write-tools]]
- [[discriminated-union-output]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the work map is supervisor-routed, peer-to-peer collaborative, or hierarchical teams. Branches route to one of three topology shapes with the matching handoff and store conventions.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/handoff.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "_header": {
    "_purpose": "JSON Schema for the handoff payload object",
    "_consumes": "agent A's output",
    "_produces": "validated handoff payload for agent B",
    "_depends_on": "content/02-output-contract.xml",
    "_token_budget_impact": "~80 tokens"
  },
  "title": "AgentHandoff",
  "type": "object",
  "required": [
    "task_id",
    "target_agent",
    "decision_metadata"
  ],
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string",
      "description": "Key into the shared task store. The receiving agent loads full state from store.get(task_id)."
    },
    "target_agent": {
      "type": "string",
      "description": "Role name of the receiving agent (must match a registered worker)."
    },
    "decision_metadata": {
      "type": "object",
      "description": "Small set of facts the target needs to plan its first action. NOT the input.",
      "properties": {
        "category": {
          "type": "string"
        },
        "lang": {
          "type": "string"
        },
        "priority": {
          "type": "string",
          "enum": [
            "low",
            "normal",
            "high"
          ]
        },
        "source_count": {
          "type": "integer"
        }
      }
    },
    "deadline": {
      "type": "string",
      "format": "date-time",
      "description": "Optional. Best-effort completion target."
    },
    "trace_id": {
      "type": "string",
      "description": "Optional. For OTel-style tracing across agent hops."
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "history"
        ]
      },
      {
        "required": [
          "messages"
        ]
      },
      {
        "required": [
          "raw_input"
        ]
      }
    ]
  }
}
```

### `templates/supervisor-decision.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "_header": {
    "_purpose": "JSON Schema for the supervisor router's structured output",
    "_consumes": "user task",
    "_produces": "validated SupervisorDecision object",
    "_depends_on": "content/02-output-contract.xml",
    "_token_budget_impact": "~80 tokens"
  },
  "title": "SupervisorDecision",
  "type": "object",
  "required": [
    "target_agent",
    "reason",
    "decision_metadata"
  ],
  "additionalProperties": false,
  "properties": {
    "target_agent": {
      "type": "string",
      "description": "Role name of the next worker. MUST be one of the registered roles; supervisor is responsible for picking a valid name."
    },
    "reason": {
      "type": "string",
      "maxLength": 200,
      "description": "One-line rationale for the routing decision. Audited, not consumed by the worker."
    },
    "decision_metadata": {
      "type": "object",
      "description": "The same shape as AgentHandoff.decision_metadata; passed directly into the handoff payload."
    },
    "fallback_agent": {
      "type": "string",
      "description": "Optional. Agent to retry with if target_agent fails or rejects."
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid handoff payload for the validator",
  "_consumes": "nothing",
  "_produces": "example handoff matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~50 tokens",
  "task_id": "t_8821",
  "target_agent": "neromedia_writer",
  "decision_metadata": {
    "category": "AI",
    "lang": "uk"
  }
}
```
