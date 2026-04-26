# Tool-Tier Approval Gate (T0/T1/T2)

## Summary

Classify every tool the SRE agent can invoke into three fixed tiers and enforce the policy at the tool-execution layer (MCP server / wrapper), never at the prompt: T0 read-only (free), T1 safe mutation (auto with mandatory audit), T2 destructive (always requires a signed human approval token). Each tool ships with a tier label in a registry; the executor refuses any T2 call that lacks a verified approval token bound to the same `(tool, target, incident_id)` and TTL ≤ 5 minutes. Unknown tools default to T2.

## Why

Prompt-level instructions like "do not delete data without asking" are not safety — they are suggestions a sufficiently confused agent ignores, as the AWS Kiro production-deletion incident showed in 2025. Moving the gate into the executor makes the safety property structural: the agent cannot delete a PVC even if it is jailbroken, because the call refuses without the cryptographic token. The three-tier split is the consensus pattern across PagerDuty, incident.io, FireHydrant, Microsoft Agent Governance Toolkit, and the EU AI Act high-risk classification (Aug 2026 deadline). It also creates a clean audit story: T1 calls log themselves, T2 calls log + token, T0 calls are cheap and free.

## When To Use

- Always, for any production agent that can call any side-effecting tool (kubectl, cloud APIs, databases, deploy systems).
- Designing or reviewing an MCP server that exposes infrastructure tools.
- Adopting Microsoft's Agent Governance Toolkit, OpenAI Agents SDK, or building a custom tool registry.
- Preparing for SOC2 or EU AI Act compliance reviews of agentic workflows.

## When NOT To Use

- Pure read-only agents that hold no write credentials anywhere — the gate is unnecessary scaffolding.
- Single-developer experiments running locally against throwaway resources — overhead exceeds value.
- Pre-production environments with no real data — adopt as you near customer traffic, not before.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-tier-rule.xml` | The closed T0/T1/T2 vocabulary, default to T2, tool-layer enforcement. |
| `content/02-approval-token-binding.xml` | Token must be a signed JWT bound to `(tool, target, incident, sub)` with TTL ≤ 5 min, single-use. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool_registry.py` | Reference Python tool registry with tier enum, dispatcher, and approval verifier. |
| `templates/approval_jwt_claims.json` | Canonical JWT claim set the executor must validate. |
