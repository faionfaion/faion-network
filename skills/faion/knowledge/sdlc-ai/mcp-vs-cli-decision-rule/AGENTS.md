# MCP vs CLI Decision Rule

## Summary

**One-sentence:** Produces a Source Routing Record that routes each live source an agent needs to CLI, MCP or neither — defaulting to the CLI, because a binary the agent already shells out to has no standing cost while an MCP server charges for its tool definitions on every single request.

**One-paragraph:** Every MCP server an agent connects to inserts its tool definitions into the context of every request, before any work happens — a footprint that runs from roughly 17.6k to 55k tokens for representative server sets, paid again on each turn whether the tools are used or not. A CLI the agent invokes costs nothing until the moment it is invoked, and then costs only its output. That asymmetry is the whole decision: MCP is worth its standing charge for the narrow set of things a one-shot command genuinely cannot do — a session that must persist across calls, access brokered through an OAuth flow the agent cannot perform itself, a subscription that pushes updates. Everything else routes to the CLI. Two dated facts sharpen this further. The 2026-07-28 protocol revision went stateless and deprecated Sampling, Roots and Logging, which puts a clock on servers built against the older revision. And the registry has been in preview since 2025-09-08, so it confers no trust — third-party servers receive no credentials, first-party OAuth only.

**Ефективно для:**

- Anyone whose agent config has accumulated MCP servers and whose sessions have quietly got more expensive.
- Wiring a new data source into an agent, where "is there an MCP for this" is the reflex question.
- Deciding whether to publish an MCP server for your own tool when a CLI already exists.
- Servers pinned to a pre-2026-07-28 revision that depend on Sampling, Roots or Logging.

## Applies If (ALL must hold)

- An agent needs access to a source it does not already have — data, a service, a tool.
- The agent can execute commands, so a CLI route is actually available to it.
- Someone pays per-request inference cost for this agent's sessions.

## Skip If (ANY kills it)

- The agent cannot shell out at all — the comparison is moot, route what you must through MCP and cap the count.
- You are implementing a server rather than choosing one — see the `mcp-server-implementation` and `mcp-architecture` material.
- The source is already reachable through a first-party integration that is neither MCP nor CLI; this rule has nothing to add.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 states the cost asymmetry, R2 sets the default, R3 the closed list of exceptions. |
| `content/02-output-contract.xml` | The Source Routing Record: per-source routing, the server cap, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from what a source actually requires to CLI / MCP / neither. |
| `scripts/validate-mcp-vs-cli-decision-rule.py` | Validates a record; enforces the CLI default, the closed justification list, the server cap and the spec-revision clock. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/source-routing-record.yaml` | Fill-in record for an agent with a mixed source set; ships valid against the contract. |
| `templates/source-routing-record-cli-only.yaml` | The common outcome — every source routes to a CLI and no server is connected at all. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `mcp-resource-vs-tool-vs-prompt` — once MCP is the chosen route, what shape the thing should take.
- `mcp-transport-stdio-vs-http` — transport choice for a server this record decided to keep.
- `mcp-security` — credential handling for the first-party servers that survive R5.
- `context-file-cost-budget` — the other standing per-turn charge in an agent's context; audit both or you will fix one and keep paying the other.

## Dated facts

Assessed 2026-08-04. The 17.6k-55k token range is the measured tool-definition footprint of representative MCP server sets as gathered in the 2026 landscape review this methodology was written from, not a vendor-published figure — re-measure against your own connected set before quoting it. Protocol revision 2026-07-28 is stateless and deprecates Sampling, Roots and Logging under a twelve-month clock. The MCP registry has been in preview since 2025-09-08 and remains so at the time of writing.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/source-routing-record.yaml`

```yaml
#
# If every source routes to a CLI, use source-routing-record-cli-only.yaml instead.
# Validate:  validate-mcp-vs-cli-decision-rule.py source-routing-record.yaml

agent: "the repo coding agent, running with shell access"

# --- The standing charge (r1, r4). Cap first, then fit the set to it. ---
server_cap: 2
definition_footprint_tokens: 21400
standing_cost_per_session: "USD 0.09 per session at our current turn count"
deferred_tool_loading: true
deferred_fallback: >
  On a miss the agent re-runs tool discovery once and, if still absent, reports the
  gap in its final message instead of declining silently. Misses are logged.

sources:
  - name: "GitHub"
    capability: "read issues and PRs, push branches"
    cli_available: true
    cli_binary: "gh"
    route: cli          # authenticated, already installed, zero standing cost

  - name: "production Postgres"
    capability: "ad-hoc read queries during investigation"
    cli_available: true
    cli_binary: "psql"
    route: cli

  - name: "the design tool"
    capability: "read a file's component tree and export assets"
    cli_available: false
    route: mcp
    mcp_justification: oauth-brokered   # stateful-session|oauth-brokered|push-subscription|no-cli-exists
    first_party: true
    credential_scope: "read-only on two named project files; no org-wide scope"
    spec_revision: "2026-07-28"

  - name: "the ticketing system"
    capability: "watch for status changes and react"
    cli_available: true
    cli_binary: "tkt"
    route: mcp
    cli_insufficient_reason: >
      The command answers questions; it cannot receive a push. The requirement is a
      subscription that wakes the agent, which no one-shot invocation expresses.
    mcp_justification: push-subscription
    first_party: true
    credential_scope: "one project, issue read plus comment write; no admin"
    spec_revision: "2026-03-26"
    migration_deadline: "2027-07-28"   # earlier revision; twelve-month clock recorded

  - name: "an internal analytics warehouse"
    capability: "aggregate queries for weekly summaries"
    cli_available: false
    route: neither
    reason: >
      Only a community-published server exists and it would hold a warehouse
      credential. Waiting for a first-party path; the weekly summary stays manual.
```

### `templates/source-routing-record-cli-only.yaml`

```yaml
#
# The cheapest outcome and a common one: no standing charge, no widened trust
# boundary, no protocol revision to track. Do not add mcp_justification or
# credential_scope keys below - server_cap 0 forbids an MCP route (r4).
# Validate:  validate-mcp-vs-cli-decision-rule.py source-routing-record-cli-only.yaml

agent: "solo developer's coding agent, shell access enabled"

server_cap: 0
definition_footprint_tokens: 0
standing_cost_per_session: "USD 0.00 - no server connected"
deferred_tool_loading: false

sources:
  - name: "GitHub"
    capability: "issues, PRs, releases"
    cli_available: true
    cli_binary: "gh"
    route: cli

  - name: "the app database"
    capability: "read queries while debugging"
    cli_available: true
    cli_binary: "psql"
    route: cli

  - name: "cloud infrastructure"
    capability: "inspect and restart services"
    cli_available: true
    cli_binary: "hcloud"
    route: cli

  - name: "the password vault"
    capability: "fetch a credential for a deploy"
    cli_available: true
    cli_binary: "op"
    route: cli

  - name: "the analytics dashboard"
    capability: "weekly traffic numbers"
    cli_available: false
    route: neither
    reason: >
      No first-party command-line path and no first-party server. Connecting a
      third-party one would put a stranger inside the credential path for a number
      that is read once a week by a human anyway.
```
