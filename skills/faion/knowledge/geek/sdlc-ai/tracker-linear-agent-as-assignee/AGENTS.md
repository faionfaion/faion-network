---
slug: tracker-linear-agent-as-assignee
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Treat AI coding agents (Cursor, Devin, Claude Code, Copilot) as first-class Linear assignees with their own user identity, not as a shared bot account.
content_id: "12bdfaa8d886ebce"
tags: [linear, agent-assignee, mcp, audit-trail, checkpoint-comments]
---
# Linear Agent as First-Class Assignee

## Summary

**One-sentence:** Treat AI coding agents (Cursor, Devin, Claude Code, Copilot) as first-class Linear assignees with their own user identity, not as a shared bot account.

**One-paragraph:** Treat AI coding agents (Cursor, Devin, Claude Code, Copilot) as first-class Linear assignees with their own user identity, not as a shared bot account. Assigning an issue to an agent triggers the delegation contract: the agent posts a task list, periodic checkpoints with elapsed time, and finally a PR link as comments back on the issue, while the human teammate remains the primary owner who clears spec/approval gates and merges. The integration runs over Linear's hosted MCP server (GA April 2026) so the agent inherits the user's project permissions and writes to the issue activity log under its own identity. The literal rule: every agent action against a Linear issue MUST be a comment, status change, or PR link tied to a real assignment event — never a silent background side-effect.

## Applies If (ALL must hold)

- Self-contained engineering tickets with concrete acceptance criteria written in the Linear issue body.
- Triage backlog with high-volume duplicate, label, or routing work where Linear's Triage Intelligence is the upstream stage.
- Bug fixes scoped to a single repo where Code Intelligence + the repo's MCP server can supply enough context.
- Teams already on Linear that want agent attribution in audit trails without standing up a separate identity service.

## Skip If (ANY kills it)

- Ambiguous discovery tickets with no acceptance criteria — the agent has nothing to anchor its checkpoints on and will fabricate intent.
- Cross-cutting refactors that touch architectural decisions or multiple repos — Linear-MCP is single-issue and single-repo per assignment.
- Tickets requiring live user interviews or non-codebase context the agent cannot fetch through MCP — the gap surfaces only after the agent ships a wrong-spec PR.
- Self-hosted-only environments — Linear's MCP and agent identity story is Linear-cloud only.

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
