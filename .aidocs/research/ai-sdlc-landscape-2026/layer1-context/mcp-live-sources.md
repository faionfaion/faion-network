# MCP as the live-sources layer
**Layer:** 1 — Context · **Verdict:** 🟡 take the idea, not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
The Model Context Protocol (MCP) is a JSON-RPC-based wire protocol that lets an agent call tools and read resources exposed by an external server, over stdio or HTTP. Anthropic released it in November 2024 and contributed it to the Linux Foundation's Agentic AI Foundation on 2025-12-09. As of 2026-07-28 the protocol underwent its largest rewrite since launch: it became **stateless**, dropped the `initialize` handshake and `Mcp-Session-Id`, added a mandatory `server/discover` RPC, and deprecated Roots, Sampling and Logging. In practice MCP is the transport for connecting an agent to systems that hold live state — issue trackers, databases, monitoring, payments — as opposed to files a human pastes or commits.

## Current state
| Fact | Value | Date |
|------|-------|------|
| Current spec revision | **2026-07-28** — final, shipped | 2026-07-28 |
| Previous revision | 2025-11-25 | 2025-11-25 |
| Release candidate locked | 2026-05-21, 10-week validation window before final | 2026-05-21 |
| Tier-1 SDKs at GA | TypeScript, Python, Go, C# ship day-one support; Rust in beta | 2026-07-28 |
| Governance | AAIF / Linux Foundation; changes via Spec Enhancement Proposals (SEPs) as markdown files in `seps/`, PR-derived numbering | since 2025-12-09 |
| Deprecation policy | New: Active / Deprecated / Removed states, **minimum 12-month deprecation window** (SEP-2596) | 2026-07-28 |
| Registry | `registry.modelcontextprotocol.io` — **still in preview** since 2025-09-08; "does not provide data durability guarantees"; breaking changes and data resets possible before GA; no GA date announced | 2026-08-03 |
| Ecosystem size | "more than 10,000 published MCP servers" (LF); ~110M+ monthly SDK downloads cited April 2026 | 2025-12-09 / 2026-04 |
| Price | free / open standard; cost is entirely token overhead + your own hosting | 2026-08-03 |

## Mechanics

### What changed on 2026-07-28 (verbatim from the official changelog)

Major changes, quoted from `modelcontextprotocol.io/specification/2026-07-28/changelog`:

1. *"Remove protocol-level sessions and the `Mcp-Session-Id` header from the Streamable HTTP transport. List endpoints (`tools/list`, `resources/list`, `prompts/list`) no longer vary per-connection. Servers that need cross-call state use explicit, server-minted handles passed as ordinary tool arguments"* (SEP-2567).
2. *"Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake. Every request now carries its protocol version and client capabilities in `_meta`"* — keys `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities`, `io.modelcontextprotocol/clientInfo`, and server identity back in each result's `_meta` as `io.modelcontextprotocol/serverInfo`. Mismatch → `UnsupportedProtocolVersionError` (SEP-2575).
3. *"Add `server/discover`: servers MUST implement this RPC to advertise their supported protocol versions, capabilities, and identity."*
4. HTTP GET endpoint and `resources/subscribe`/`unsubscribe` replaced by **`subscriptions/listen`** — one long-lived POST-response stream; clients opt into `toolsListChanged`, `promptsListChanged`, `resourcesListChanged`, `resourceSubscriptions`; notifications tagged with `io.modelcontextprotocol/subscriptionId`.
5. **`ping`, `logging/setLevel`, `notifications/roots/list_changed` removed.** Log level is now per-request via `io.modelcontextprotocol/logLevel` in `_meta`.
6. Tasks moved out of core into extension `io.modelcontextprotocol/tasks`; `tasks/result` replaced by polling `tasks/get`, plus `tasks/update`; `tasks/list` removed.
7. **Multi Round-Trip Requests (MRTR)** replaces all server-initiated requests (`roots/list`, `sampling/createMessage`, `elicitation/create`). The server returns `resultType: "input_required"` with an `inputRequests` field; the client retries the original request carrying `inputResponses`.
8. Every result now carries a required `resultType`: `"complete"` or `"input_required"`.
9. SSE resumability removed — no `Last-Event-ID`, no event IDs. A broken stream loses the in-flight request; the client MUST re-issue with a new request ID.

Deprecated (still functional, ≥12 months): **Roots, Sampling, Logging** (SEP-2577), with stated migrations — *"pass directories or files via tool parameters, resource URIs, or server configuration instead of Roots; integrate directly with LLM provider APIs instead of Sampling; log to `stderr` (stdio) or use OpenTelemetry instead of Logging."* Also deprecated: HTTP+SSE transport, `includeContext` values `"thisServer"`/`"allServers"`, and OAuth 2.0 Dynamic Client Registration (RFC 7591) in favour of Client ID Metadata Documents.

Minor changes that matter for cost: *"Servers SHOULD return tools from `tools/list` in a deterministic order to enable client-side caching and improve LLM prompt cache hit rates"*, and a new `CacheableResult` interface requiring `ttlMs` and `cacheScope` (`"public"`/`"private"`) on all list/read results.

### Client surface as a solopreneur actually meets it (Claude Code, docs fetched 2026-08-03)

```bash
# remote HTTP server
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"

# local stdio server — everything after `--` is passed through untouched
claude mcp add --env AIRTABLE_API_KEY=KEY --transport stdio airtable -- npx -y airtable-mcp-server

# raw JSON
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'
```

Scopes via `-s/--scope`: `local` (this project, just you) · `project` (`.mcp.json` at repo root, committed, requires per-user approval prompt; reset with `claude mcp reset-project-choices`) · `user` (`~/.claude.json`, all projects). `.mcp.json` supports `${VAR}` expansion. `type` accepts `streamable-http` as an alias for `http`. WebSocket (`type: "ws"`) is config-only, header auth only, no OAuth. Per-server `"timeout"` in ms overrides `MCP_TOOL_TIMEOUT`. Output is capped: warning above 10,000 tokens, hard limit 25,000, raised with `MAX_MCP_OUTPUT_TOKENS`.

### The token tax, and the mitigation

Tool definitions are loaded into context before any work happens. Measured figures, all 2026 and all secondary/community (no vendor publishes this):
- GitHub's MCP server: **~17,600 tokens** of core tool definitions; **~42,000** with a full toolset; **~55,000** across all 93 tools.
- On a 200k window that is **8–27% of capacity** consumed before the first prompt.
- Typical per-tool schema cost: 500–1,400 tokens. 5–10 servers installed ≈ 50,000–67,000 tokens at session start.

Anthropic's fix, from the Claude Code MCP docs (fetched 2026-08-03): **tool search is enabled by default.** *"Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them. Only tool names and server instructions load at session start."* Controlled by `ENABLE_TOOL_SEARCH`:

| Value | Behaviour |
|-------|-----------|
| (unset) | all MCP tools deferred, loaded on demand |
| `true` | force deferral, send the beta header everywhere |
| `auto` | threshold mode — load upfront if definitions fit within 10% of the context window, defer the overflow |
| `false` | upfront loading |

Requires a model supporting `tool_reference` blocks: Sonnet 4.5, Haiku 4.5, Opus 4.5 and later. Disabled automatically on Google Cloud Agent Platform, on a non-first-party `ANTHROPIC_BASE_URL`, and rejected server-side on Azure-hosted Microsoft Foundry. `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` kills it and `ENABLE_TOOL_SEARCH` cannot override that. Tool descriptions and server instructions are **truncated at 2KB each**.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | MCP spec 2026-07-28 — Key Changes (changelog) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | The 9 major changes, 12 minor, 4 deprecations, feature-lifecycle policy, SEP numbers | 2026-08-03 |
| 2 | MCP blog — The 2026-07-28 Specification | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | GA date 2026-07-28; Tier-1 SDK availability; 12-month deprecation guarantee; migration cost acknowledged for session-id users | 2026-08-03 |
| 3 | Introducing the MCP Registry | https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/ + https://modelcontextprotocol.io/registry/about | Preview since 2025-09-08; no durability guarantee; breaking changes/data resets possible; built for sub-registries, not end users | 2026-08-03 |
| 4 | Claude Code — Connect Claude Code to tools via MCP | https://code.claude.com/docs/en/mcp | All `claude mcp` commands, transports, scopes, `.mcp.json` shape, OAuth flow, `headersHelper`, output limits, **tool search + `ENABLE_TOOL_SEARCH`** | 2026-08-03 |
| 5 | LF press: AAIF formation | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Dated 2025-12-09; MCP released Nov 2024; "more than 10,000 published MCP servers" | 2026-08-03 |
| 6 | Unit 42 — prompt injection via MCP Sampling | https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/ | Attack vectors through the (now-deprecated) Sampling feature | 2026-08-03 |
| 7 | UpGuard — Six MCP security incidents | https://www.upguard.com/blog/mcp-security-incidents | Invariant Labs GitHub-MCP exfiltration (May 2025); 2026-01-20 exploit chain against Anthropic's official Git MCP server, 3 CVEs (path traversal, argument injection, repo-scoping bypass), RCE via prompt injection alone; 2026-04-03 `@azure-devops/mcp` missing auth layer | 2026-08-03 |
| 8 | Practical DevSecOps — MCP security statistics 2026 | https://www.practical-devsecops.com/mcp-security-statistics-2026-report/ | 30–82% of public MCP servers carry exploitable flaws; only 8.5% use OAuth; Trend Micro: 492 servers internet-exposed with no auth; HackerOne +540% prompt-injection reports | 2026-08-03 |
| 9 | StackOne / getunblocked / community token measurements | https://www.stackone.com/blog/mcp-token-optimization/ · https://getunblocked.com/blog/github-mcp-token-cost/ | GitHub MCP 17.6k / 42k / 55k tokens depending on toolsets; 500–1,400 tokens per tool schema | 2026-08-03 |

## Adjudication of claim 4

**Claim — "MCP = the thing that separates a real context layer from imitation (connected sources vs files you paste by hand)."**

🔴 **Refuted as stated.** The claim conflates a *transport* with a *context layer*, and for a solopreneur it inverts the cost/benefit. Specifically:

1. **The dichotomy is false.** The alternative to MCP is not "files you paste by hand" — it is a CLI the agent already runs with a Bash tool. `gh issue view`, `psql -c`, `stripe logs tail`, `curl` are all *connected live sources* with **zero** upfront token cost, no protocol version to track, no OAuth loop, and credentials already on the machine. Claude Code's own tool-search design concedes the point: it hides MCP definitions until needed precisely because the definitions themselves are the problem.
2. **MCP has a floor cost that scales with servers, not with usage.** Every installed server pays rent in the context window on every request, whether used or not. 17.6k tokens is GitHub's *core* toolset. Tool search reduces this materially but does not remove it (names + server instructions still load), and it silently falls back to upfront loading on several hosting configurations.
3. **The protocol just broke.** 2026-07-28 removed the handshake, session IDs, `ping`, SSE resumability, and moved every server-initiated interaction to a new MRTR pattern. Sampling, Roots and Logging are deprecated. Every third-party server written before mid-2026 is now on a migration clock. A solopreneur adopting MCP broadly in 2026 is adopting a maintenance obligation.
4. **The discovery layer is not production infrastructure.** The registry has been "preview" since 2025-09-08 with explicit "no durability guarantees, breaking changes and data resets may occur" — nearly 11 months, no GA date.
5. **The security profile is bad for a one-person operation with no security team.** Independent scans put 30–82% of public servers as carrying exploitable flaws and only 8.5% using OAuth; Anthropic's *own* official Git MCP server took three CVEs and RCE-via-prompt-injection on 2026-01-20. A solopreneur cannot audit a server before installing it.

**The defensible version of the claim:** a real context layer needs *live* state, not only committed files. MCP is one way to get it, and the right way for a small number of high-value first-party hosted servers with OAuth (Sentry, Stripe, Notion, GitHub). It is the wrong default for everything else. For a non-technical solopreneur it is the wrong choice almost everywhere — the setup surface alone (transports, scopes, PATs, `.mcp.json`, approval prompts, OAuth callbacks, `headersHelper`) is a technical product.

## What to borrow for faion
1. **The distinction, restated correctly:** committed files (slow-changing truth) vs live sources (fast-changing state) vs on-demand knowledge (methodologies). Faion sells the third and should be explicit about the first two.
2. **A decision rule, not an endorsement.** "Use a CLI unless the source has no CLI, or auth is only available over OAuth, or you need the agent to react to pushed events." That rule is short, defensible and nobody is publishing it.
3. **The token-budget accounting.** Tool definitions are a *fixed* per-request cost; tool calls are variable. Teach the fixed cost first — it is the part people miss.
4. **`ENABLE_TOOL_SEARCH` as an operational default**, with the exact fallback conditions where it silently turns off (non-first-party `ANTHROPIC_BASE_URL`, GCP Agent Platform, Azure Foundry, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`). That last one is a real trap: it disables tool search and `ENABLE_TOOL_SEARCH` cannot override it.
5. **The 2026-07-28 migration checklist** as a geek-tier artefact: session-id → server-minted handles in tool args; `initialize` → `_meta` + `server/discover`; server-initiated requests → MRTR `resultType: "input_required"`; `logging/setLevel` → `_meta` `logLevel`; SSE resumability → re-issue with a new request ID. This is the single most concrete, most perishable, most valuable MCP content available right now.
6. **A hard security rule for the audience we serve:** first-party hosted servers with OAuth only; never `npx`-run a third-party stdio server against production credentials. Back it with the 2026-01-20 Anthropic Git-MCP CVE chain and the 2026-04-03 `@azure-devops/mcp` missing-auth finding — dated, specific, and it lands.

## What NOT to borrow — and why
- **MCP as the default answer to "how do I give the agent context."** It is the answer to "how do I give the agent a live *system*", which is a much narrower question and rarely the solopreneur's actual bottleneck.
- **Sampling, Roots, Logging.** Deprecated 2026-07-28. Any faion content that teaches building on them is teaching a dead API. Note: the Unit 42 attack-vector research is *about* Sampling — the deprecation partially closes that class.
- **Session-oriented MCP server designs.** Removed. Any tutorial recommending `Mcp-Session-Id` is now wrong.
- **The registry as a discovery recommendation.** Preview since 2025-09-08, explicitly not built for end-user browsing, no GA. Do not point buyers at it.
- **Any "install these 10 MCP servers" listicle pattern.** It is exactly the behaviour that burns 50–67k tokens at session start and maximises supply-chain exposure.
- **MCP for our own product.** `faion search` / `faion get-content` are local, sealed, and have no runtime dependency. Exposing them over MCP would trade a zero-token local Go binary for a per-request tool-definition tax and a protocol we would have to chase. If we ever want editor integration, ship a plugin/skill that shells out to the binary.

## Mapping to our corpus
Verified against `skills/faion/knowledge/*/INDEX.xml` on 2026-08-03. Every MCP methodology we own is **geek** tier:

| Slug | Domain | Tier |
|------|--------|------|
| `mcp` | claude-code | geek |
| `mcp-basics` | claude-code | geek |
| `mcp-servers` | claude-code | geek |
| `mcp-transport-stdio-vs-http` | ai-agents | geek |
| `mcp-resource-vs-tool-vs-prompt` | ai-agents | geek |
| `mcp-gateway-composition` | ai-agents | geek |
| `mcp-architecture` | ml-engineering | geek |
| `mcp-server-implementation` | ml-engineering | geek |
| `mcp-client-integration` | ml-engineering | geek |
| `mcp-security` | ml-engineering | geek |
| `mcp-dev-prompts` | ml-engineering | geek |
| `tracker-jira-rovo-mcp-agents` | sdlc-ai | geek |

**⚠️ Staleness finding — act on this.** Grepping the corpus shows the MCP methodologies are pinned to the **2025-11-25** revision. Files carrying that version string:
- `ml-engineering/mcp-architecture/` — `meta.json`, `AGENTS.md`, `content/01-core-rules.xml`, `content/02-output-contract.xml`, `content/05-examples.xml`, `scripts/validate-mcp-architecture.py`
- `ai-agents/mcp-transport-stdio-vs-http/content/01-core-rules.xml`
- (plus `.bak` copies in `mcp-client-integration`, `mcp-security`, `mcp-dev-prompts`)

`mcp-architecture`'s validator script encodes the old revision, so it will pass servers that are non-conformant under 2026-07-28 and vice versa. This is content we sell. It is wrong as of 2026-07-28.

Proposed changes:
1. **Refresh, do not create:** `mcp-architecture`, `mcp-server-implementation`, `mcp-client-integration`, `mcp-transport-stdio-vs-http`, `mcp-resource-vs-tool-vs-prompt` → repin to 2026-07-28, remove Sampling/Roots/Logging guidance, add MRTR, `server/discover`, `_meta` capability carriage, `CacheableResult`. Update `validate-mcp-architecture.py`.
2. **New: `mcp-2026-07-28-migration`** — domain `ai-agents`, tier **geek**. Breaking-change-by-breaking-change migration with the SEP numbers and the 12-month deprecation clock.
3. **New: `mcp-vs-cli-decision-rule`** — domain `sdlc-ai`, tier **solo**. The one thing our corpus has no home for: *when not to use MCP*. Token floor, CLI alternative, `ENABLE_TOOL_SEARCH` fallbacks, first-party-OAuth-only security rule. This is the piece that serves a solopreneur, and it is the only MCP content that belongs below geek tier.
4. **`mcp-security` needs the 2026 incident record** — the 2026-01-20 Anthropic Git MCP CVE chain and the 2026-04-03 Azure DevOps package, plus the "8.5% use OAuth" scan data. Currently likely reasoned rather than evidenced.

No new methodology needed for "what is MCP" — covered by `claude-code/mcp-basics`.

## Open questions / staleness risk
- **The spec is 6 days old at time of writing.** SDK-level and server-ecosystem breakage will surface over the next quarter. Anything we publish now about real-world migration state will age fast; publish the *spec deltas* (stable, sourced from the changelog) and avoid claims about ecosystem readiness.
- **The 12-month deprecation clock started 2026-07-28**, so Roots/Sampling/Logging are removable no earlier than **2026-07-28 + 12 months**. Do not state a removal date more precisely than that.
- **Registry GA is unannounced.** If it GAs, the "don't rely on the registry" guidance changes. Re-check.
- **Token-cost figures are all community-measured.** No vendor publishes tool-definition token counts. The 17.6k / 42k / 55k spread reflects different toolset configurations, not disagreement — but we must present them as configuration-dependent measurements with a source and date, never as "the" number.
- **Tool search moves the goalposts.** Once deferral is universal, the "MCP is expensive" argument weakens considerably. It is currently default-on in Claude Code but absent or disabled on Bedrock, GCP Agent Platform, Azure Foundry, proxies, and pre-Sonnet-4.5 models. Our claim must be scoped: *expensive where deferral is unavailable, cheap where it is*.
- **`server/discover` is a MUST for servers.** Whether it is universally implemented in practice is unverified; I found no conformance data.
