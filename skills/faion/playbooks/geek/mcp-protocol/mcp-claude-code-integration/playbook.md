---
name: mcp-claude-code-integration
description: Register an existing MCP server in Claude Code via stdio or HTTP transport, verify the connection, and invoke tools in an agent session.
tier: geek
group: mcp-protocol
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have one or more MCP servers registered in Claude Code — either at user scope (`~/.claude/claude.json`) or project scope (`.claude/claude.json`) — and you will be able to invoke their tools from any Claude Code session. This playbook covers the consumer side: connecting to MCP servers you did not build. For building your own server, see `mcp-server-build`.

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code` or via the Anthropic installer).
- An MCP server available locally or remotely:
  - **stdio**: an executable on PATH (e.g. `npx @linear/mcp-server`, `uvx mcp-server-filesystem`).
  - **HTTP**: a running server URL (e.g. `http://127.0.0.1:3100/mcp`).
- For third-party servers: their npm / PyPI package name or binary path. See the MCP server catalog at `knowledge/geek/ai/claude-code/mcp-servers`.
- Optional: API keys or tokens the server requires (Linear API key, GitHub PAT, etc.).

## Steps

### Register a stdio server with `claude mcp add`

1. Open a terminal and confirm Claude Code is on your PATH.

```bash
claude --version
```

2. Add a server at **user scope** (available in every project on this machine).

```bash
# Linear project management MCP server
claude mcp add --scope user linear-mcp \
  -- npx -y @linear/mcp-server
```

The `--` separator passes all remaining tokens as the command + args to spawn the subprocess. Claude Code stores the entry in `~/.claude/claude.json` under `mcpServers`.

3. Add a server that requires an environment variable (e.g. a GitHub PAT).

```bash
claude mcp add --scope user github-mcp \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_yourpat \
  -- npx -y @modelcontextprotocol/server-github
```

`-e KEY=VALUE` injects the variable only into the server subprocess, not the shell.

4. Add a local filesystem server at **project scope** (checked into `.claude/claude.json`).

```bash
# From inside the project root:
claude mcp add --scope project filesystem-mcp \
  -- uvx mcp-server-filesystem /home/nero/workspace/projects/my-project/
```

Project-scope entries live in `.claude/claude.json` relative to the git root. They are committed and shared with teammates.

### Register an HTTP server with `claude mcp add-json`

5. Use `add-json` when the server speaks Streamable HTTP instead of stdio.

```bash
claude mcp add-json --scope user remote-mcp '{
  "type": "http",
  "url": "http://127.0.0.1:3100/mcp"
}'
```

For an authenticated HTTP server (Bearer token):

```bash
claude mcp add-json --scope user remote-mcp-auth '{
  "type": "http",
  "url": "https://mcp.internal.myorg.com/mcp",
  "headers": {
    "Authorization": "Bearer eyJ..."
  }
}'
```

6. Confirm the raw JSON entry was written correctly.

```bash
cat ~/.claude/claude.json | python3 -m json.tool | grep -A8 '"remote-mcp'
```

### Verify registration and connection

7. Inside a Claude Code session, run the `/mcp` slash command.

```
/mcp
```

Expected output (truncated example):

```
MCP Servers (2 connected):

linear-mcp (stdio)
  Status: connected
  Tools: linear_search_issues, linear_create_issue, linear_list_teams, ...

filesystem-mcp (stdio)
  Status: connected
  Tools: read_file, write_file, list_directory, ...
```

If a server shows `error` or `disconnected`, proceed to Troubleshooting.

### Invoke an MCP tool in a session

8. Ask Claude to use a registered tool by natural language — no special syntax needed.

For Linear:

```
Search Linear for open bugs assigned to me in the faion-network project
```

For the filesystem server:

```
List all .md files under /home/nero/workspace/projects/faion-net/faion-network/skills/faion/playbooks/
```

Claude dispatches the matching tool automatically. The tool name and JSON input are visible in the session as a tool-use block before the result.

### Manage registered servers

9. List all registered servers and their scopes.

```bash
claude mcp list
```

10. Remove a server by name.

```bash
claude mcp remove linear-mcp --scope user
```

11. To edit a server config (change args, env vars, URL), remove and re-add it. Direct JSON editing of `~/.claude/claude.json` also works — changes take effect on the next session start.

## Verify

Inside a Claude Code session run `/mcp`. Every registered server must appear with `Status: connected`. Then issue a natural language request that requires a tool from one of them:

```
Use the filesystem server to read the file /home/nero/workspace/projects/faion-net/faion-network/CHANGELOG.md
```

Claude should invoke `read_file` and print the file contents. If it responds without calling a tool, the server is not connected or no tool matched the request — check `/mcp` output again.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/mcp` shows `error: spawn ENOENT` | Command not found when Claude Code spawned the subprocess | Use the absolute path: `which npx` then replace `npx` with the full path, e.g. `/usr/local/bin/npx` |
| `/mcp` shows `error: spawn ENOENT` for uvx | `uvx` not installed or not on PATH at Claude Code startup time | Install via `pip install uv` then verify `which uvx`; use absolute path in the `claude mcp add` command |
| Server connects but `/mcp` lists 0 tools | Server started successfully but returned empty tool list | Run the server binary manually and check stderr: `npx -y @linear/mcp-server 2>&1` |
| `linear_search_issues` fails with 401 | API key not set or wrong env var name | Re-run `claude mcp add` with the correct `-e` key; verify with `printenv GITHUB_PERSONAL_ACCESS_TOKEN` outside of Claude |
| HTTP server shows `connection refused` | Server not running on the expected port | Start the server process first; confirm with `curl http://127.0.0.1:3100/mcp` before registering |
| Project-scope server not visible to teammates | `.claude/claude.json` not committed | `git add .claude/claude.json && git commit` — env vars with secrets should be in `.env`, not in the JSON |
| `add-json` rejects the payload | JSON syntax error in the shell-quoted string | Write the JSON to a temp file and pipe: `claude mcp add-json --scope user myserver "$(cat /tmp/mcp.json)"` |
| `/mcp` server disappears after restart | Scope mismatch: added with `--scope project` but running outside that project | Run Claude Code from inside the project root, or re-add with `--scope user` |

## Next

- `mcp-server-build` — build your own MCP server in TypeScript or Python to expose an internal API or database as typed tools.
- Read `knowledge/geek/ai/claude-code/mcp-servers` for a catalog of 40+ production MCP servers (Linear, GitHub, Notion, Postgres, filesystem, browser) with recommended scopes and env var names.
- `context-window-packing` — optimize large MCP tool outputs (e.g. filesystem reads, issue lists) before they fill the context window.

## References

- [knowledge/geek/ai/claude-code/mcp-servers](../../../knowledge/geek/ai/claude-code/mcp-servers) — authoritative catalog of MCP server packages with their install commands and required env vars; backs the `npx @linear/mcp-server` and `uvx mcp-server-filesystem` examples in Steps 2–4.
- [knowledge/geek/ai/claude-code/mcp-basics](../../../knowledge/geek/ai/claude-code/mcp-basics) — explains the stdio vs. HTTP transport contract and how Claude Code spawns server subprocesses; directly backs the ENOENT troubleshooting row and the `--` separator in Step 2.
- [knowledge/geek/ai/claude-code/mcp](../../../knowledge/geek/ai/claude-code/mcp) — schema design patterns for tool input and the security boundary model (read-only vs. write-capable); backs the env-var injection pattern in Step 3 and the project-scope commit guidance in Step 4.
