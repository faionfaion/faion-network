# Agent Trajectory Eval Method

## Summary

**One-sentence:** Evaluation method that scores not just an agent's final answer but the full tool-call trajectory — right tools, right order, redundancy, recovery — and produces a per-run report with trajectory metrics.

**One-paragraph:** Output-only evals miss the half of agent quality that lives in the trajectory: did the agent pick the right tools, in a sensible order, without redundancy, and recover gracefully from tool errors? This methodology defines a three-layer score (system efficiency: latency + tokens + tool calls; session: trajectory exact-match / precision / recall; node: per-tool selection and parameter accuracy) and emits a per-run report that gates promotion. Required for any agent feature that survived first-week sunny-day testing and now needs an honest production readiness signal.

**Ефективно для:** Команд, у яких pass-rate на golden set ≥80%, але в проді агент іноді робить дивне і ніхто не знає чому; метрики траєкторії показують конкретні misselect-tool / redundant-call / no-recovery випадки, які output-only-евали ховають.

## Applies If (ALL must hold)

- Agent is past initial-prototype stage (has ≥1 deployed version).
- Trajectory logs (per-tool call + args + return) are persisted.
- A golden set of ≥30 expected-trajectory examples exists or can be assembled.
- Owner is willing to gate GA promotion on trajectory metrics, not only final-answer metrics.
- An eval harness can replay or fresh-run trajectories (see [[agent-replay-harness-cookbook]]).

## Skip If (ANY kills it)

- Agent is a single-tool wrapper (no trajectory to score).
- Trajectory logs are unavailable and cannot be added (closed harness).
- Final-answer quality alone meets the team's bar and trajectory variation does not affect outcomes.
- Production cost ceiling cannot accommodate the eval run cost.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Golden trajectory set | jsonl `[{task, expected_tools, expected_order}]` ≥30 entries | QA |
| Live trajectory logs | jsonl from observability stack | Datadog / Langfuse / LangSmith |
| Tool registry | JSON name+schema | Tool catalogue |
| Cost ceiling | $ per eval run | Finance |
| Named owner | handle | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-replay-harness-cookbook/AGENTS.md` | Harness emits the trajectories this evaluator consumes. |
| `geek/ai/ai-agents/chaos-eval-fault-injection/AGENTS.md` | Chaos-eval extends this with deliberate fault injection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: golden frozen, three-layer scoring, CI reported, judge calibrated, cost capped | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the trajectory-eval report | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (output-only, judge drift, cherry-picked traces, etc.) | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: build golden → score per-layer → aggregate → CI → report | ~1000 |
| `content/05-examples.xml` | medium | Worked example: trajectory report for a code-fixer agent | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: logs available? → golden set? → cost ok? → run/build/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_traces` | haiku | Structured extraction. |
| `score_trajectory` | sonnet | LLM-as-judge for trajectory quality where rule-based fails. |
| `aggregate_report` | sonnet | Compose final report. |
| `review_regression` | opus | Cross-version drift diagnosis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the trajectory-eval report. |
| `templates/report.example.json` | Filled minimal valid example. |
| `templates/golden-trajectory.jsonl` | Skeleton golden-set with two example entries. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the report against the schema. | After subagent emits report, before promotion gate. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-replay-harness-cookbook]] — replay produces the input traces.
- peer: [[chaos-eval-fault-injection]] — extends trajectory eval with fault injection.
- external: TRACE (arXiv:2602.21230); Vertex AI trajectory_exact_match / precision / recall.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) are trajectory logs available? (2) is a golden set ≥30 examples ready? (3) does cost fit ceiling? Leaves point to "run eval", "build prerequisites first", or "escalate".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/agent-trajectory-eval-method/report.json",
  "title": "Trajectory Eval Report",
  "description": "purpose=schema; consumes=traces+golden-set; produces=trajectory-eval-report; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "report_id",
    "golden_set_version",
    "n_examples",
    "agent_version",
    "system_efficiency",
    "session_quality",
    "node_precision",
    "judge_calibration_date",
    "cost_usd",
    "owner",
    "version",
    "produced_at"
  ],
  "$defs": {
    "metric": {
      "type": "object",
      "required": [
        "mean",
        "ci_low",
        "ci_high"
      ],
      "properties": {
        "mean": {
          "type": "number"
        },
        "ci_low": {
          "type": "number"
        },
        "ci_high": {
          "type": "number"
        }
      }
    }
  },
  "properties": {
    "report_id": {
      "type": "string"
    },
    "golden_set_version": {
      "type": "string"
    },
    "n_examples": {
      "type": "integer",
      "minimum": 30
    },
    "agent_version": {
      "type": "string"
    },
    "system_efficiency": {
      "type": "object",
      "required": [
        "latency_ms",
        "tokens",
        "tool_calls"
      ],
      "properties": {
        "latency_ms": {
          "$ref": "#/$defs/metric"
        },
        "tokens": {
          "$ref": "#/$defs/metric"
        },
        "tool_calls": {
          "$ref": "#/$defs/metric"
        }
      }
    },
    "session_quality": {
      "type": "object",
      "required": [
        "trajectory_exact_match",
        "trajectory_precision",
        "trajectory_recall"
      ],
      "properties": {
        "trajectory_exact_match": {
          "$ref": "#/$defs/metric"
        },
        "trajectory_precision": {
          "$ref": "#/$defs/metric"
        },
        "trajectory_recall": {
          "$ref": "#/$defs/metric"
        }
      }
    },
    "node_precision": {
      "type": "object",
      "required": [
        "tool_selection_accuracy",
        "param_accuracy"
      ],
      "properties": {
        "tool_selection_accuracy": {
          "$ref": "#/$defs/metric"
        },
        "param_accuracy": {
          "$ref": "#/$defs/metric"
        }
      }
    },
    "judge_calibration_date": {
      "type": "string",
      "format": "date"
    },
    "cost_usd": {
      "type": "number",
      "minimum": 0
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

### `templates/report.example.json`

```json
{
  "report_id": "traj-eval-support-v3.1.0",
  "golden_set_version": "golden-trajectory-v3-frozen-2026-05-15",
  "n_examples": 120,
  "agent_version": "support-agent@3.1.0",
  "system_efficiency": {
    "latency_ms": {
      "mean": 4200,
      "ci_low": 3900,
      "ci_high": 4500
    },
    "tokens": {
      "mean": 8200,
      "ci_low": 7600,
      "ci_high": 8800
    },
    "tool_calls": {
      "mean": 3.8,
      "ci_low": 3.3,
      "ci_high": 4.3
    }
  },
  "session_quality": {
    "trajectory_exact_match": {
      "mean": 0.61,
      "ci_low": 0.54,
      "ci_high": 0.68
    },
    "trajectory_precision": {
      "mean": 0.84,
      "ci_low": 0.8,
      "ci_high": 0.88
    },
    "trajectory_recall": {
      "mean": 0.79,
      "ci_low": 0.74,
      "ci_high": 0.84
    }
  },
  "node_precision": {
    "tool_selection_accuracy": {
      "mean": 0.92,
      "ci_low": 0.89,
      "ci_high": 0.95
    },
    "param_accuracy": {
      "mean": 0.87,
      "ci_low": 0.83,
      "ci_high": 0.91
    }
  },
  "judge_calibration_date": "2026-04-15",
  "cost_usd": 4.2,
  "owner": "qa@faion.net",
  "version": "1.0.0",
  "produced_at": "2026-05-22T14:00:00Z"
}
```

### `templates/golden-trajectory.jsonl`

```json
{"task_id":"fix-parser-001","task":"Fix tests/test_parser.py — three failing tests","expected_tools":["read_file","grep","edit_file","run_pytest"],"expected_order":["read_file","grep","edit_file","run_pytest"],"allowed_alternatives":[["read_file","edit_file","run_pytest"]]}
{"task_id":"add-endpoint-002","task":"Add POST /v1/widgets endpoint with validation","expected_tools":["list_dir","read_file","edit_file","run_pytest"],"expected_order":["list_dir","read_file","edit_file","run_pytest"],"allowed_alternatives":[]}
```
