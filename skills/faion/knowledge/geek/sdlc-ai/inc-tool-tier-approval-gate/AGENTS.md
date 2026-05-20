---
slug: inc-tool-tier-approval-gate
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Classify every tool the SRE agent can invoke into three fixed tiers and enforce the policy at the tool-execution layer (MCP server / wrapper), never at the prompt: T0 read-only (free), T1 safe mutation (auto with mandatory audit), T2 destructive (always requires a signed human approval token).
content_id: "3121cda3afe88742"
tags: [incident-response, approval-gate, tool-safety, sre-agent, governance]
---
# Tool-Tier Approval Gate (T0/T1/T2)

## Summary

**One-sentence:** Classify every tool the SRE agent can invoke into three fixed tiers and enforce the policy at the tool-execution layer (MCP server / wrapper), never at the prompt: T0 read-only (free), T1 safe mutation (auto with mandatory audit), T2 destructive (always requires a signed human approval token).

**One-paragraph:** Classify every tool the SRE agent can invoke into three fixed tiers and enforce the policy at the tool-execution layer (MCP server / wrapper), never at the prompt: T0 read-only (free), T1 safe mutation (auto with mandatory audit), T2 destructive (always requires a signed human approval token). Each tool ships with a tier label in a registry; the executor refuses any T2 call that lacks a verified approval token bound to the same `(tool, target, incident_id)` and TTL ≤ 5 minutes. Unknown tools default to T2.

## Applies If (ALL must hold)

- Always, for any production agent that can call any side-effecting tool (kubectl, cloud APIs, databases, deploy systems).
- Designing or reviewing an MCP server that exposes infrastructure tools.
- Adopting Microsoft's Agent Governance Toolkit, OpenAI Agents SDK, or building a custom tool registry.
- Preparing for SOC2 or EU AI Act compliance reviews of agentic workflows.

## Skip If (ANY kills it)

- Pure read-only agents that hold no write credentials anywhere — the gate is unnecessary scaffolding.
- Single-developer experiments running locally against throwaway resources — overhead exceeds value.
- Pre-production environments with no real data — adopt as you near customer traffic, not before.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
