# Linear Agent as First-Class Assignee

## Summary

Treat AI coding agents (Cursor, Devin, Claude Code, Copilot) as first-class Linear assignees with their own user identity, not as a shared bot account. Assigning an issue to an agent triggers the delegation contract: the agent posts a task list, periodic checkpoints with elapsed time, and finally a PR link as comments back on the issue, while the human teammate remains the primary owner who clears spec/approval gates and merges. The integration runs over Linear's hosted MCP server (GA April 2026) so the agent inherits the user's project permissions and writes to the issue activity log under its own identity. The literal rule: every agent action against a Linear issue MUST be a comment, status change, or PR link tied to a real assignment event — never a silent background side-effect.

## Why

Linear's own engineering team and the April 2026 product docs converge on the same loop: the issue is the durable artefact, the agent is a thread on the issue, and the human reviewer's first signal is the agent's checkpoint comment. This produces three measurable wins versus shared-bot patterns: (a) the audit trail attributes each action to the specific agent identity (not "system"), satisfying SOC2-style review; (b) the issue's "assignee" semantics extend cleanly — Linear's existing notification, SLA, and triage rules apply unchanged; (c) checkpoint comments give the human a cheap rollback handle (react with thumbs-down) before the agent burns a PR review cycle. The empirical anchor is Linear's published in-house workflow ("CX → Linear → Triage Intelligence → assigned coding agent → human merges") plus the Code Intelligence + repo MCP context surface that ships with the integration.

## When To Use

- Self-contained engineering tickets with concrete acceptance criteria written in the Linear issue body.
- Triage backlog with high-volume duplicate, label, or routing work where Linear's Triage Intelligence is the upstream stage.
- Bug fixes scoped to a single repo where Code Intelligence + the repo's MCP server can supply enough context.
- Teams already on Linear that want agent attribution in audit trails without standing up a separate identity service.

## When NOT To Use

- Ambiguous discovery tickets with no acceptance criteria — the agent has nothing to anchor its checkpoints on and will fabricate intent.
- Cross-cutting refactors that touch architectural decisions or multiple repos — Linear-MCP is single-issue and single-repo per assignment.
- Tickets requiring live user interviews or non-codebase context the agent cannot fetch through MCP — the gap surfaces only after the agent ships a wrong-spec PR.
- Self-hosted-only environments — Linear's MCP and agent identity story is Linear-cloud only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-assignment-contract.xml` | The required shape of the assignment-to-PR loop: agent identity, checkpoint comment cadence, PR-link-as-final-comment rule. |
| `content/02-mcp-permission-inheritance.xml` | How the agent inherits the assignee user's Linear permissions via MCP, and why the agent must never run with a higher-scoped identity than the assigning human. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-identity.yaml` | Linear user record + scope declaration for one agent (name, email, allowed actions, prohibited actions). |
| `templates/checkpoint-comment.md` | Markdown skeleton the agent posts at each checkpoint (task list, elapsed time, next step, blockers). |
