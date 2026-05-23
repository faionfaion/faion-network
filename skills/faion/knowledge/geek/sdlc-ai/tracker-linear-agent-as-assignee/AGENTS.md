---
slug: tracker-linear-agent-as-assignee
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an agent-identity + delegation-contract config so coding agents (Cursor, Devin, Claude, Copilot) appear as distinct Linear assignees with checkpoint comments, never as shared bot accounts.
content_id: "fe40f81a74ec8d25"
complexity: medium
produces: config
est_tokens: 4200
tags: [linear, agent-assignee, mcp, audit-trail, checkpoint-comments]
---
# Linear Agent as First-Class Assignee

## Summary

**One-sentence:** Treat AI coding agents as first-class Linear assignees with their own user identity; on assignment the agent posts a task list, periodic checkpoints, and a PR link as comments, via Linear's hosted MCP (GA April 2026).

**One-paragraph:** Treat AI coding agents (Cursor, Devin, Claude Code, Copilot) as first-class Linear assignees with their own user identity, not as a shared bot account. Assigning an issue to an agent triggers the delegation contract: the agent posts a task list, periodic checkpoints with elapsed time, and finally a PR link as comments back on the issue, while the human teammate remains the primary owner who clears spec/approval gates and merges. The integration runs over Linear's hosted MCP server (GA April 2026) so the agent inherits the user's project permissions and writes to the issue activity log under its own identity. The literal rule: every agent action against a Linear issue MUST be a comment, status change, or PR link tied to a real assignment event — never a silent background side-effect.

**Ефективно для:**

- Linear orgs з multi-agent fleet (Cursor / Devin / Claude / Copilot).
- Audit-driven teams: action log per agent identity.
- Delegation flow: human owner + agent assignee, clean handoff.
- Checkpoint cadence keеps humans оrientated by elapsed time.

## Applies If (ALL must hold)

- Org tracks work in Linear with assignment-driven workflow.
- Multiple coding agents (Cursor / Devin / Claude / Copilot) are in use.
- Linear MCP server is reachable and licensed.

## Skip If (ANY kills it)

- Tracker is not Linear (Jira/Asana/Notion) — use the matching tracker methodology.
- Org wants one shared bot account (anti-pattern, but explicit choice).
- Linear MCP not yet enabled on the org plan.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Linear org with MCP enabled | Linear setting | admin |
| Coding agent supports Linear MCP | client docs | Cursor / Devin / Claude / Copilot |
| Issue assignment policy | Markdown | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-identity.yaml` | Per-vendor Linear user setup (display name, avatar, scope). |
| `templates/checkpoint-comment.md` | Checkpoint comment template (elapsed time + current step). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-linear-agent-as-assignee.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[tracker-jira-rovo-mcp-agents]]
- [[tracker-github-copilot-workspace]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
