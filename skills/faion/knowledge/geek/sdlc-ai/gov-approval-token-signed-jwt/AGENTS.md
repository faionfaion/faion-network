---
slug: gov-approval-token-signed-jwt
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Whenever an agent needs human approval for a write/destructive action (deploy, rollback, kubectl delete, secret rotation, money movement), the approval is delivered as a cryptographically signed JWT, not a Slack thumbs-up.
content_id: "cbe68990a6a380a5"
tags: [governance, jwt, approval, audit, human-in-the-loop]
---
# Human Approval as a Signed, Scoped, Single-Use JWT

## Summary

**One-sentence:** Whenever an agent needs human approval for a write/destructive action (deploy, rollback, kubectl delete, secret rotation, money movement), the approval is delivered as a cryptographically signed JWT, not a Slack thumbs-up.

**One-paragraph:** Whenever an agent needs human approval for a write/destructive action (deploy, rollback, kubectl delete, secret rotation, money movement), the approval is delivered as a cryptographically signed JWT, not a Slack thumbs-up. The token carries sub (approver identity), scope (the exact tool + target tuple being approved), iat, a short exp (≤5 minutes), an aud for the calling agent, a jti for single-use, and the originating incident_id / task_id. The agent's tool layer verifies the signature, scope match, expiry, and replay flag at call time. Slack reactji can initiate the approval, but only the signed callback satisfies the gate.

## Applies If (ALL must hold)

- Any agent that can perform Tier 1+ (writes / destructive / money-moving) actions in production.
- Incident-response agents that propose remediations a human must authorize before the agent executes them.
- Deploy / rollback bots, kubectl operators, IAM-mutation agents, customer-data-export agents.
- Regulated environments (EU AI Act enforcement Aug 2026, SOC2 / GDPR audited orgs) where approval evidence is non-optional.

## Skip If (ANY kills it)

- Pure read-only agents — no write means no approval token is needed.
- Tier 0 actions inside a sandboxed dev environment with no production blast radius.
- Multi-step approvals with quorum and complex policy — escalate to a full IAM/policy engine (OPA, Cedar) instead of a hand-rolled JWT.
- One-off scratch scripts that are never reused — bootstrap cost dominates.

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
