---
slug: tracker-jira-rovo-mcp-agents
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude Code, Cursor, Codex, third-party agents) and Jira plus Confluence plus Jira Service Management.
content_id: "778b44616450c89a"
tags: [jira, atlassian, mcp, audit-trail, permission-inheritance]
---
# Jira via Atlassian Rovo MCP, Permission-Inheriting

## Summary

**One-sentence:** Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude Code, Cursor, Codex, third-party agents) and Jira plus Confluence plus Jira Service Management.

**One-paragraph:** Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude Code, Cursor, Codex, third-party agents) and Jira plus Confluence plus Jira Service Management. The agent appears as a real Jira user, inherits the assignee's permissions, never exceeds project configuration, and writes every action to the native Jira audit trail.

## Applies If (ALL must hold)

- Enterprise Jira Cloud deployments where SOC2/audit-log inheritance is non-negotiable.
- Teams already on Jira plus JSM (incident queues, on-call data) who want one MCP for engineering and ITSM.
- Multi-tool agent stacks that must respect existing Atlassian permissions and never bypass project config.
- Workflow-embedded automation: drop the agent into a status transition (In Design → run designer agent) instead of a side webhook.

## Skip If (ANY kills it)

- Self-hosted Jira Data Center — Rovo MCP is Cloud-only; no on-prem fallback exists.
- Tight inner-loop tooling that needs lower-latency or lower-cost direct REST API access.
- Workflows that require the agent to bypass project configuration — impossible by design and should not be retrofitted.
- Single-author solo projects where the OAuth + workflow-embedding overhead exceeds the value.

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
