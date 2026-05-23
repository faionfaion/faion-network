# Jira via Atlassian Rovo MCP, Permission-Inheriting

## Summary

**One-sentence:** Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude, Cursor, Codex) and Jira/Confluence/JSM, with permission inheritance and native audit-trail writes.

**One-paragraph:** Use Atlassian's Rovo Remote MCP server (GA April 2026) as the single authenticated bridge between every AI client (Claude Code, Cursor, Codex, third-party agents) and Jira plus Confluence plus Jira Service Management. The agent appears as a real Jira user, inherits the assignee's permissions, never exceeds project configuration, and writes every action to the native Jira audit trail.

**Ефективно для:**

- Atlassian Cloud orgs з Rovo seat-licensed.
- Multi-client AI fleet (Claude + Cursor + Codex), один bridge.
- Compliance audit: native Jira audit trail per action.
- Permission inheritance: agent не може exceed assignee scope.

## Applies If (ALL must hold)

- Org runs Atlassian Cloud (Jira / Confluence / JSM) with Rovo enabled.
- Multiple AI clients (Claude, Cursor, Codex) need Jira access.
- Permission inheritance from real users is a hard compliance requirement.

## Skip If (ANY kills it)

- Self-managed / DC Jira where Rovo MCP is not yet GA.
- Single-client setup where direct OAuth is simpler.
- Compliance team forbids any AI write access to Jira (read-only only).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Atlassian Cloud subscription with Rovo | license | billing |
| AI client supporting MCP | Claude / Cursor / etc. | client setup |
| Jira service account with audit-event writeback enabled | config | Jira admin |

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
| `templates/duo-flow.yaml` | Rovo MCP installation + client registration YAML (scope, audit, single-install). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-jira-rovo-mcp-agents.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[tracker-linear-agent-as-assignee]]
- [[tracker-github-copilot-workspace]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
