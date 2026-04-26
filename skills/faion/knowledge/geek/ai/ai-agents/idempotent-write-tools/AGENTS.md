# Idempotent Write Tools — Keys + Preview/Apply Pairs

## Summary

Every tool that mutates state must (a) accept an `idempotency_key` from the agent, (b) be safe to re-run with the same key (returns the same result without duplicating the side effect), and (c) ship as a `*_preview` + `*_apply` pair when the side effect is destructive or expensive. Tools time out, networks flake, agent loops retry on transient errors — un-keyed writes silently double-charge, double-deploy, double-email. Idempotency keys turn every retry into a no-op replay; preview/apply pairs let the agent show its work before committing.

## Why

Production agent runs fail mid-tool roughly an order of magnitude more often than human-issued API calls — long horizon = many tool calls = compounding flake rate. Without a key, the orchestrator cannot tell the difference between "the call succeeded but the response was lost" and "the call never happened", so it retries and the side effect runs twice. Stripe, AWS, GitHub, and every payment provider built idempotency keys for exactly this reason; agent tools inherit the same constraint, amplified by the agent's eagerness to retry on ambiguous errors. Preview/apply separates the model's reasoning step from the irreversible step, giving the human (or a guard agent) a chance to veto.

## When To Use

- Any tool that mutates external state: payments, emails, file deletes, infra changes, DB writes, external API POSTs.
- Tools whose side effect is destructive (delete) or expensive (deploy, send email, charge card) — split into `*_preview` + `*_apply`.
- When the agent runs in a loop with automatic retry on tool errors.
- When tools are exposed via MCP gateways with at-least-once delivery semantics.

## When NOT To Use

- Pure reads (`get_*`, `search_*`, `list_*`) — no side effect, no key needed; bloating the schema confuses the model.
- Append-only telemetry where duplicates are tolerable (metric emits, debug logs).
- Tools whose underlying API is already idempotent by content hash (e.g., S3 PUT with same body) — passing a key adds noise.

## Content

| File | What's inside |
|------|---------------|
| `content/01-idempotency-key.xml` | The key contract: what the agent sends, what the tool stores, replay semantics. |
| `content/02-preview-apply-pair.xml` | The two-tool pattern for destructive/expensive operations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idempotent_tool.py` | Reference Python implementation (Pydantic + key store) for a write tool. |

## References

- https://achan2013.medium.com/ai-agent-anti-patterns-part-2-tooling-observability-and-scale-traps-in-enterprise-agents-42a451ea84ec
- https://www.devx.com/technology/scalable-ai-agents-10-design-patterns-that-matter/
- https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/
