# Jira via Atlassian Rovo MCP, Permission-Inheriting

## Summary

Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude Code, Cursor, Codex, third-party agents) and Jira plus Confluence plus Jira Service Management. The agent appears as a real Jira user, inherits the assignee's permissions, never exceeds project configuration, and writes every action to the native Jira audit trail. Workflow embeddings (auto-trigger an agent on `status: "In Design"`) are the canonical extension point — no custom webhooks, no shared bot tokens, no out-of-band approval channels. Self-hosted Jira Data Center is unsupported by design.

## Why

April 2026 enterprises that already pay for SOC2 audit-log inheritance through Atlassian get it transparently when their agents speak MCP via Rovo. The mechanism is the OAuth handshake plus a permission-inheritance contract: Atlassian explicitly states agents respect the user's permissions, project configurations, workflows, and audit trails — privilege escalation is impossible because the agent operates as the assignee. This collapses the bot-account anti-pattern (one shared key with admin scope) into the same identity layer Jira already enforces for humans, and removes the need for a parallel approval system because Jira's existing transition rules already encode "who can move this to Done".

## When To Use

- Enterprise Jira Cloud deployments where SOC2/audit-log inheritance is non-negotiable.
- Teams already on Jira plus JSM (incident queues, on-call data) who want one MCP for engineering and ITSM.
- Multi-tool agent stacks that must respect existing Atlassian permissions and never bypass project config.
- Workflow-embedded automation: drop the agent into a status transition (`In Design` → run designer agent) instead of a side webhook.

## When NOT To Use

- Self-hosted Jira Data Center — Rovo MCP is Cloud-only; no on-prem fallback exists.
- Tight inner-loop tooling that needs lower-latency or lower-cost direct REST API access.
- Workflows that require the agent to bypass project configuration — impossible by design and should not be retrofitted.
- Single-author solo projects where the OAuth + workflow-embedding overhead exceeds the value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rovo-mcp-as-bridge.xml` | Rovo MCP is the only allowed Jira/Confluence/JSM bridge; agent identity, OAuth, audit inheritance. |
| `content/02-workflow-embedded-trigger.xml` | Embedding agents at workflow status transitions, with permission inheritance and human gate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/duo-flow.yaml` | Workflow-status embedding example: agent on `In Design` enter, inherit permissions, human-gate the next transition. |

## Related

- https://www.atlassian.com/platform/remote-mcp-server
- https://www.atlassian.com/blog/announcements/ai-agents-in-jira
- https://github.com/atlassian/atlassian-mcp-server
