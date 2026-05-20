---
slug: inc-read-only-investigation-default
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The SRE agent boots with mode=read_only and is bound to a *-readonly Kubernetes / cloud RBAC role that grants only get/list/watch/log/describe.
content_id: "8f0c270b9b596906"
tags: [rbac, sre-agent, read-only, escalation, least-privilege]
---
# Read-Only Investigation Mode by Default

## Summary

**One-sentence:** The SRE agent boots with mode=read_only and is bound to a *-readonly Kubernetes / cloud RBAC role that grants only get/list/watch/log/describe.

**One-paragraph:** The SRE agent boots with mode=read_only and is bound to a *-readonly Kubernetes / cloud RBAC role that grants only get/list/watch/log/describe. To perform any mutation it must transition to mode=remediate, which requires (a) a human-issued /agent escalate-trust <incident_id> command, (b) a fresh MFA challenge against the on-caller, and (c) a time-boxed elevated role (default 60 minutes) that auto-revokes when the incident closes or the timer expires. The mode is enforced by RBAC, not by the prompt — a jailbroken or confused agent that "decides" to mutate cannot, because its credentials forbid it. This is the Azure SRE Agent / Causely pattern that became the consensus floor in 2026.

## Applies If (ALL must hold)

- First 6–12 months of any production agent rollout.
- Any environment where a misfired mutation costs more than a delayed remediation.
- Multi-tenant clusters where blast radius can cross customer boundaries.
- Compliance regimes that demand "least privilege by default" (SOC2 CC6.3, ISO 27001 A.9.2.3).

## Skip If (ANY kills it)

- Pre-production / sandbox clusters with no real data and full reset capability — friction without payoff.
- Mature setups where specific T1 actions (restart pod) have run thousands of times safely and graduate to always-on. T2 stays gated forever.
- Single-developer toolchains where there is no separation of duties to enforce.

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
