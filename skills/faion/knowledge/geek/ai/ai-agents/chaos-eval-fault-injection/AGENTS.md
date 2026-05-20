---
slug: chaos-eval-fault-injection
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A standard eval set runs tools that always succeed.
content_id: "3c55cc8024dfb4ec"
tags: [eval, fault-injection, reliability, testing]
---
# Chaos-Eval — Fault Injection on Agent Tools

## Summary

**One-sentence:** A standard eval set runs tools that always succeed.

**One-paragraph:** A standard eval set runs tools that always succeed. Production tools fail: timeouts, 5xx errors, rate limits, corrupted return values, MCP server disconnects. Chaos-eval injects each failure mode at random points along the agent's trajectory and grades not "did it succeed?" but "did it recover, retry intelligently, escalate when blocked, or produce a confidently-wrong answer?". Without it, your reported success rate is a sunny-day distribution that lies the moment the network blinks.

## Applies If (ALL must hold)

- Any agent past prototype that depends on external tools, web APIs, MCP servers, or remote LLMs.
- Pre-launch readiness gate alongside outcome and trajectory evals.
- Regression suite when retry / circuit-breaker / fallback logic changes.
- Building a "graceful degradation" story for SLAs and post-mortems.

## Skip If (ANY kills it)

- Air-gapped agents with only deterministic local tools (rare in practice).
- Pure prompt-only generators with zero tool use — there is nothing to fault-inject.
- Pre-prototype phase — wait until tool surface is stable before investing.
- Tools whose failure modes are already exercised by record/replay traces from production — chaos-eval is for failure modes you have not yet seen in prod.

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

- parent skill: `geek/ai/ai-agents/`
