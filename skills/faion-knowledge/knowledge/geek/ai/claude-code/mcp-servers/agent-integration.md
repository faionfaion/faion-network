# Agent Integration — MCP Server Catalog

## When to use
- Agent needs to interact with an external service (GitHub, Slack, Notion, Stripe) without writing custom API code
- Standardizing tool interfaces across multiple agents — all agents use the same MCP tool, not ad-hoc curl calls
- Replacing fragile shell-script API wrappers with a typed, introspectable MCP interface
- Enabling Claude Code to read from or write to databases, CRMs, or project management tools mid-session

## When NOT to use
- The service has no MCP server and the task is one-off — use `WebFetch` + `Bash(curl:*)` directly
- The MCP server requires an OAuth flow that can't be completed non-interactively — authentication will block
- Security policy disallows external process spawning or network calls from within Claude Code
- The catalog server's tool count is very large (>50 tools) — it pollutes the model's tool namespace; filter or build a focused custom server instead

## Where it fails / limitations
- `npx -y` pulls the latest version on each Claude Code startup — breaking changes in upstream packages can silently break tools
- MCP servers run as subprocesses; crashes are not surfaced clearly to the agent — they produce "tool unavailable" errors
- `claude mcp add` writes to `~/.claude/settings.json`; changes are user-scoped and not committed with the project
- Tokens in env vars are stored in plaintext in settings.json — use a secrets manager or 1Password integration
- Multi-user projects where each developer has different API keys cannot share a single project-level MCP config
- Some servers (Twitter, Meta Ads) require complex OAuth flows — automation unfriendly; prefer service accounts with token auth

## Agentic workflow
Use a setup agent (Bash, Read) to check `claude mcp list`, detect missing servers, and add them via `claude mcp add`. A specialized task agent then uses the configured MCP tools directly (the tool names appear as `mcp__servername__toolname`). Keep server configuration in a documented `mcp-setup.sh` script committed to the project so it's reproducible across developers.

### Recommended subagents
- General-purpose Bash agent — runs `claude mcp add` commands and validates with `claude mcp list`
- `faion-pm-agent` — uses GitHub/Linear/Jira MCP tools for issue management
- `faion-research-agent` — uses memory MCP for persistent knowledge across sessions

### Prompt pattern
Checking and adding a server:
```bash
# In a setup script or agent Bash block:
claude mcp list | grep -q "github" || \
  claude mcp add github -s user -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -- npx -y @anthropic/github-mcp
```

Using an MCP tool in agent prompt:
```
Use the mcp__github__create_issue tool to file an issue titled "{title}" in repo "{repo}".
Set labels: ["bug"]. Body: {body}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude mcp add` | Register a server in user/project scope | Bundled with Claude Code |
| `claude mcp list` | List all registered servers and status | Bundled |
| `claude mcp remove` | Remove a server | Bundled |
| `npx @modelcontextprotocol/inspector` | Interactively test a server's tools/resources | `npx @modelcontextprotocol/inspector` |
| `fastmcp dev` | Dev mode for Python MCP servers with live reload | `pip install fastmcp` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub (`@anthropic/github-mcp`) | SaaS | Yes | Repos, PRs, issues; token auth |
| Notion (`@notionhq/notion-mcp-server`) | SaaS | Yes | Pages, databases; API key auth |
| Stripe (`@stripe/mcp`) | SaaS | Yes | Payments, subscriptions; API key |
| PostgreSQL (`@anthropic/postgres-mcp`) | OSS | Yes | Direct DB queries; connection string |
| Cloudflare (`@cloudflare/mcp-server-cloudflare`) | SaaS | Yes | DNS, Workers, KV, R2; API token |
| Slack (`@anthropic/slack-mcp`) | SaaS | Yes | Messages, channels; bot token |
| Linear (`@anthropic/linear-mcp`) | SaaS | Yes | Issues, cycles; API key |
| Figma (`@anthropic/figma-mcp`) | SaaS | Partial | Design-to-code; OAuth required |
| Memory (`@anthropic/memory-mcp`) | OSS | Yes | Persistent agent memory; local file |
| ElevenLabs (`elevenlabs-mcp`) | SaaS | Yes | TTS; API key |
| Hetzner (`mcp-hetzner`) | SaaS | Yes | Server management; API token |
| Playwright (`@anthropic/playwright-mcp`) | OSS | Yes | Browser automation; no auth |

## Templates & scripts
```bash
#!/usr/bin/env bash
# mcp-setup.sh — idempotent MCP server provisioning
# Run once per developer machine. Requires env vars set.

set -euo pipefail

setup_mcp() {
  local name=$1; shift
  if claude mcp list 2>/dev/null | grep -q "^$name"; then
    echo "MCP $name already registered, skipping."
    return
  fi
  claude mcp add "$name" "$@"
  echo "MCP $name registered."
}

setup_mcp github -s user -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -- npx -y @anthropic/github-mcp

setup_mcp postgres -s user -e DATABASE_URL="$DATABASE_URL" \
  -- npx -y @anthropic/postgres-mcp

setup_mcp memory -s user -- npx -y @anthropic/memory-mcp

echo "All MCP servers provisioned."
```

## Best practices
- Pin package versions: `npx -y @anthropic/github-mcp@1.2.3` — prevents silent breaking changes
- Store API keys in 1Password; inject via `op run -- claude mcp add ...` rather than hardcoding in settings
- Scope servers to user (`-s user`) for personal auth; use project scope (`-s project`) only for team-shared, non-secret config
- Audit enabled MCP tools periodically — unused servers add startup latency and expand attack surface
- For high-volume agent workflows, prefer direct API calls over MCP to avoid per-call process overhead
- Document required env vars for each server in `mcp-setup.sh` so onboarding is self-contained

## AI-agent gotchas
- MCP tool names use `mcp__servername__toolname` format — the agent must know the exact tool name; test with Inspector first
- If a server fails to start, the agent receives no error — it simply cannot see those tools; always verify with `claude mcp list`
- Servers with broad permissions (e.g., Postgres without read-only restriction) let agents run destructive queries — always scope permissions at the server level
- The `claude mcp add` command is interactive if run in a tty; in scripts use `--yes` or pipe /dev/null for non-interactive use
- Agents cannot dynamically add MCP servers mid-session — all servers must be registered before Claude Code starts

## References
- https://docs.anthropic.com/en/docs/claude-code/mcp
- https://github.com/wong2/awesome-mcp-servers
- https://github.com/modelcontextprotocol/servers
- https://www.npmjs.com/package/@modelcontextprotocol/inspector
