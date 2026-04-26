# Structured Tool Errors with recoveryHint

## Summary

Tool errors are part of the prompt — they are the next thing the agent reads. Never bubble raw stack traces, HTTP error bodies, or upstream JSON. Return a structured object: `{code, message, recoveryHint, traceId, ...details}` where `recoveryHint` is a closed enum (`RETRY_LATER | CHECK_INPUT | TRY_ALTERNATIVE | REPORT_TO_USER | NEEDS_AUTH`). The hint is a direct instruction to the model's next reasoning step. The closed code lets the agent's loop decide retry vs escalate vs abort without re-reading the message.

## Why

LLM-friendly error design papers (SHIELDA, Kumaran's MCP error guide) consistently show that an unstructured error like `TypeError: NoneType has no attribute 'json' at line 42` causes the agent to either retry blindly (wasting tokens and risking duplicate side effects) or hallucinate an explanation ("the API is down, I will try again"). A structured error with a `recoveryHint` enum gives the loop a deterministic branch: `RETRY_LATER` → sleep + retry; `CHECK_INPUT` → reconsider arguments; `NEEDS_AUTH` → ask user; `REPORT_TO_USER` → stop. Same paper measured 30%+ reduction in dead-end loops on agent error benchmarks. The `traceId` is what the human reads when the agent escalates — never omit it.

## When To Use

- Every error path of every tool, including reads.
- Tools wrapping flaky upstreams (rate limits, auth tokens, transient 5xx).
- Tools where the agent retries automatically — the hint controls the retry policy.
- MCP servers — error structure is part of the public contract.

## When NOT To Use

- Don't fabricate `recoveryHint` when the failure is genuinely unrecoverable — emit `REPORT_TO_USER` and stop the loop instead of guessing `RETRY_LATER`.
- Don't add a hint to a successful response with warnings; warnings belong in a separate `warnings: []` field, not the error envelope.
- Don't expose internal stack traces inside `details` — they leak implementation, fill context, and don't help the agent.

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-envelope.xml` | The structured error shape and the recoveryHint enum. |
| `content/02-loop-policy.xml` | How the agent loop maps each hint to an action (retry / abort / ask). |

## Templates

| File | Purpose |
|------|---------|
| `templates/error_envelope.json` | Canonical JSON shape with all fields. |
| `templates/recovery_hints.txt` | Closed enum of hints with one-line semantics. |

## References

- https://medium.com/@kumaran.isk/llm-friendly-error-handling-designing-mcp-servers-for-ai-df427f6dfd2f
- https://arxiv.org/pdf/2508.07935
- https://www.arunbaby.com/ai-agents/0033-error-handling-recovery/
