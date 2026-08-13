# Chaos-Eval — Fault Injection on Agent Tools

## Summary

**One-sentence:** Injects controlled tool faults (timeouts, 5xx, rate-limits, corrupted returns, MCP disconnects) into eval runs and grades the agent on recovery quality, not sunny-day success.

**One-paragraph:** Standard eval sets run with tools that always succeed; production tools fail. This methodology defines a chaos-eval config (fault classes, injection points, rates) layered on top of a regular eval, and a grading rubric that scores not "did it succeed?" but "did it recover, retry intelligently, escalate when blocked, or produce a confidently-wrong answer?". Output is one report per agent version with per-fault-class recovery scores.

**Ефективно для:** Команд, у яких production agent інколи дає «confidently wrong» відповідь, коли tool тимчасово впав — і eval показує 95%, а реальний uptime 60%; chaos-eval ловить цей клас bugs до релізу.

## Applies If (ALL must hold)

- Agent calls tools that can fail in production (HTTP, MCP, code execution).
- Replay harness exists (see [[agent-replay-harness-cookbook]]).
- Eval set ≥30 examples.
- Owner can run an extended eval cycle (chaos eval is 5-10× longer than normal).
- A grading rubric for recovery quality is available or can be authored.

## Skip If (ANY kills it)

- All tools are deterministic in-process (no network, no MCP).
- No replay harness — can't inject faults reliably.
- Eval already chaos-graded by upstream platform.
- Prototype with no SLA on reliability.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Replay harness | output of [[agent-replay-harness-cookbook]] | Eng |
| Eval set | jsonl ≥30 | QA |
| Tool fault catalogue | per-tool {fault_classes, default_rates} | Tool catalogue |
| Recovery rubric | rubric scoring 0..3 per outcome class | QA |
| Named owner | handle | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-replay-harness-cookbook/AGENTS.md` | Harness emits the trajectories chaos-eval mutates. |
| `geek/ai/ai-agents/agent-trajectory-eval-method/AGENTS.md` | Trajectory eval supplies the rubric chaos-eval extends. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: fault catalogue, injection points, grade recovery, baseline first | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the chaos-eval report | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: harness? → fault classes? → rubric? → run/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_fault_classes` | sonnet | Per-tool reasoning. |
| `grade_recovery` | sonnet | LLM-as-judge for recovery quality. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the report. |
| `templates/output.example.json` | Filled example. |
| `templates/chaos-config.json` | Skeleton chaos config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the report. | Before promotion gate. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-replay-harness-cookbook]], [[agent-trajectory-eval-method]].

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is a replay harness available? (2) are fault classes catalogued? (3) does a recovery rubric exist? Leaves point to "run chaos-eval", "build prerequisites first", or "escalate".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/chaos-eval-fault-injection/output.json",
  "title": "Chaos Eval Fault Injection Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "chaos-eval-fault-injection-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "chaos-eval-fault-injection@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Chaos Eval Fault Injection; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```

### `templates/chaos-config.json`

```json
{
  "_header": "purpose=chaos-eval config; consumes=tool inventory + production fault rates; produces=fault injection plan; depends-on=content/01-core-rules.xml; token-budget-impact=none (offline)",
  "name": "agent-chaos-config",
  "version": 1,
  "seed": 42,
  "scope": {
    "include_tools": [
      "*"
    ],
    "exclude_tools": [
      "log",
      "metric"
    ],
    "include_llm_calls": true
  },
  "faults": [
    {
      "type": "tool_timeout",
      "p": 0.1,
      "deadline_ms": 5000
    },
    {
      "type": "tool_error",
      "p": 0.05,
      "code": 500,
      "message": "internal server error"
    },
    {
      "type": "llm_rate_limit",
      "p": 0.02,
      "retry_after_s": 30
    },
    {
      "type": "tool_mutate",
      "p": 0.03,
      "strategy": "drop_field"
    },
    {
      "type": "service_disconnect",
      "p": 0.01,
      "midstream": true
    }
  ],
  "deterministic_injections": {
    "step_4": "tool_timeout",
    "step_7": "tool_mutate"
  },
  "grading": {
    "outcomes": [
      "recovered",
      "retried_intelligently",
      "escalated_correctly",
      "wrong_confident"
    ],
    "thresholds": {
      "wrong_confident_max": 0.0,
      "recovered_or_retried_min": 0.7,
      "escalated_correctly_min": 0.1
    }
  },
  "report": {
    "per_fault_breakdown": true,
    "per_tool_breakdown": true,
    "save_traces_for": [
      "wrong_confident"
    ]
  }
}
```
