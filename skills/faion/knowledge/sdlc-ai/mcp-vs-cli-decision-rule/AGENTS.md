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

## Related

- `mcp-resource-vs-tool-vs-prompt` — once MCP is the chosen route, what shape the thing should take.
- `mcp-transport-stdio-vs-http` — transport choice for a server this record decided to keep.
- `mcp-security` — credential handling for the first-party servers that survive R5.
- `context-file-cost-budget` — the other standing per-turn charge in an agent's context; audit both or you will fix one and keep paying the other.

## Dated facts

Assessed 2026-08-04. The 17.6k-55k token range is the measured tool-definition footprint of representative MCP server sets as gathered in the 2026 landscape review this methodology was written from, not a vendor-published figure — re-measure against your own connected set before quoting it. Protocol revision 2026-07-28 is stateless and deprecates Sampling, Roots and Logging under a twelve-month clock. The MCP registry has been in preview since 2025-09-08 and remains so at the time of writing.
