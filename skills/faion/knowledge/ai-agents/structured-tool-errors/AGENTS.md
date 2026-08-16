# Structured Tool Errors with recoveryHint

## Summary

**One-sentence:** Tool errors are part of the prompt — return a structured `{code, message, recoveryHint, traceId, …}` envelope so the agent loop can branch deterministically.

**One-paragraph:** Produces an error envelope returned by every tool error path with required fields `code` (UPPER_SNAKE), `message` (one human sentence, no stack trace), `recoveryHint` (closed enum `RETRY_LATER | CHECK_INPUT | TRY_ALTERNATIVE | REPORT_TO_USER | NEEDS_AUTH`), `traceId` (correlation ID), and optional `retry_after_seconds` + sanitised `details`. The closed-enum hint maps to one and only one runner action; the agent loop never re-interprets it. Studies (SHIELDA, Kumaran MCP error guide) report 30%+ reduction in dead-end retry loops vs free-form errors.

**Ефективно для:** будь-якого tool / MCP сервера, де агент в циклі retry-ить запити (rate-limits, auth, transient 5xx) і блукає в free-form error-повідомленнях замість дискретного "RETRY_LATER / CHECK_INPUT".

## Applies If (ALL must hold)

- Tool is invoked from an agent loop where the model may retry on its own.
- Tool wraps a flaky upstream (rate-limits, auth, transient 5xx) OR is an MCP server with a public error contract.
- The agent runner has (or will gain) a hint → action dispatcher.
- Errors are returned as JSON bodies the model can read.

## Skip If (ANY kills it)

- Failures are genuinely unrecoverable AND the tool is invoked by deterministic code that never retries.
- Tool is invoked synchronously by a human user only (errors go to a UI, not a model loop).
- Tool emits warnings on a successful path; warnings belong in a separate `warnings: []` field, not the error envelope.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool definition | JSON Schema / Anthropic tool spec / MCP manifest | tool source repo |
| Upstream failure taxonomy | enumerated list | runbook |
| Agent runner hint-dispatch map | YAML | `runner/policy.yml` |
| Existing error responses | sample HTTP bodies | logs / traces |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/idempotent-write-tools` | Retries are only safe on idempotent tools; this companion methodology guarantees the precondition. |
| `geek/ai/ai-agents/headless-cli-four-guards` | Bounds the retry loop with `--max-turns`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: envelope shape, closed recoveryHint enum, no raw stack traces, runner hint→action map, traceId mandatory | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tool error envelope (already present in templates as `error_envelope.json`) | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: HTTP-code-as-error-code, stack-trace-in-details, missing-traceId, freeform-hint-prose, fabricated-RETRY_LATER | ~700 |
| `content/04-procedure.xml` | medium | Migrate a tool: identify error paths → assign codes → assign hints → wire dispatcher → smoke test | ~800 |
| `content/06-decision-tree.xml` | essential | Picks `recoveryHint` value per failure category | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Inventory existing tool error paths | sonnet | Mechanical AST walk. |
| Assign `recoveryHint` per failure | opus | Risk judgement; opus weighs retry vs escalate. |
| Wire runner hint → action map | sonnet | Boilerplate plumbing. |
| Generate the OpenAPI / MCP error schema | sonnet | Schema translation, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error_envelope.json` | JSON Schema for the tool error envelope — copy into tool / MCP server contract. |
| `templates/recovery_hints.txt` | Closed enum of recovery hints with a one-line semantic for each value. |
| `templates/runner_policy.yaml` | YAML map from `recoveryHint` to runner action with retry budgets and timeouts. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-tool-errors.py` | Validates a sample tool-error JSON body against `02-output-contract.xml` / `error_envelope.json`. | Pre-commit hook on tool definitions; runtime smoke test in tool's test suite. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[idempotent-write-tools]] — `RETRY_LATER` is only safe when the tool is idempotent.
- [[headless-cli-four-guards]] — `--max-turns` bounds the retry loop in CLI invocations.
- [[stream-json-orchestration]] — orchestrator observes error envelopes via `tool_result` events.
- [[verb-object-tool-naming]] — tool naming companion; both improve agent error handling.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the `recoveryHint` value from the failure category: rate-limit / transient 5xx → `RETRY_LATER`; 4xx with bad arguments → `CHECK_INPUT`; auth missing/expired → `NEEDS_AUTH`; unrecoverable / 5xx with no retry budget → `REPORT_TO_USER`; resource missing but a peer tool exists → `TRY_ALTERNATIVE`. Use it whenever the question is "which hint do I emit for THIS failure".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/error_envelope.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$comment": "purpose: tool error envelope schema enforcing closed recoveryHint enum\nconsumes: per-tool failure category + upstream status\nproduces: JSON body the agent runner can dispatch on without parsing prose\ndepends-on: agent runner with hint->action map (templates/runner_policy.yaml)\ntoken-budget-impact: ~250 tokens to render in agent context",
  "title": "ToolError",
  "type": "object",
  "required": [
    "error"
  ],
  "properties": {
    "error": {
      "type": "object",
      "required": [
        "code",
        "message",
        "recoveryHint",
        "traceId"
      ],
      "properties": {
        "code": {
          "type": "string",
          "pattern": "^[A-Z][A-Z0-9_]+$",
          "description": "Semantic UPPER_SNAKE code, e.g. UPSTREAM_RATE_LIMITED."
        },
        "message": {
          "type": "string",
          "maxLength": 240,
          "description": "One human sentence. No stack trace."
        },
        "recoveryHint": {
          "type": "string",
          "enum": [
            "RETRY_LATER",
            "CHECK_INPUT",
            "TRY_ALTERNATIVE",
            "REPORT_TO_USER",
            "NEEDS_AUTH"
          ]
        },
        "retry_after_seconds": {
          "type": "integer",
          "minimum": 0,
          "maximum": 3600
        },
        "traceId": {
          "type": "string",
          "minLength": 8
        },
        "details": {
          "type": "object",
          "description": "Sanitised key-value details. Never raw stack frames."
        }
      },
      "additionalProperties": false
    }
  }
}
```

### `templates/recovery_hints.txt`

```text
recoveryHint enum — closed vocabulary
=====================================

RETRY_LATER       Transient upstream issue. Runner sleeps `retry_after_seconds`
                  (clamped 1-300) and retries up to per-tool retry budget.

CHECK_INPUT       Argument-level problem (validation failure, missing ID,
                  malformed query). Runner returns envelope to the model so
                  it can reconsider — NO automatic retry.

TRY_ALTERNATIVE   This tool cannot serve the request (wrong scope, missing
                  permission, feature not enabled). Runner returns envelope
                  to the model and prompts it to pick a different tool.

REPORT_TO_USER    Irrecoverable for the agent (data inconsistency, business
                  rule violation, hard limit). Runner HALTS the loop and
                  surfaces the envelope to the user.

NEEDS_AUTH        Credentials missing, expired, or insufficient. Runner
                  HALTS the loop and triggers the user-facing auth flow.

Picking the hint
================
- 401/403          → NEEDS_AUTH
- 400 / schema bad → CHECK_INPUT
- 404 / wrong tool → TRY_ALTERNATIVE
- 429 / 503        → RETRY_LATER (with retry_after_seconds)
- 409 / conflict   → REPORT_TO_USER (data state needs human decision)
- unknown 500      → RETRY_LATER on first try, REPORT_TO_USER after budget
```

### `templates/runner_policy.yaml`

```yaml
policy_version: "1.1.0"
default_retry_budget_per_tool: 3
retry_after_seconds_clamp:
  min: 1
  max: 300

dispatch:
  RETRY_LATER:
    action: wait_and_retry
    use_retry_after_seconds: true
    fallback_seconds: 10
    counts_against_retry_budget: true
  CHECK_INPUT:
    action: return_to_model
    counts_against_retry_budget: false
  TRY_ALTERNATIVE:
    action: return_to_model
    suggest_different_tool: true
    counts_against_retry_budget: false
  REPORT_TO_USER:
    action: halt_loop
    surface_envelope_to_user: true
  NEEDS_AUTH:
    action: halt_loop
    trigger_auth_flow: true

# Per-tool overrides (example)
overrides:
  github_api:
    default_retry_budget_per_tool: 5
  payment_gateway:
    dispatch:
      RETRY_LATER:
        action: halt_loop   # never auto-retry payment side-effects
        surface_envelope_to_user: true
```
