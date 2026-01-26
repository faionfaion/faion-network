# Claude Code

> **Entry point:** `/faion-net` — invoke for automatic routing.

Claude Code configuration: skills, agents, commands, hooks, MCP servers, IDE integrations.

## When to Use

- Creating and managing Claude Code skills (SKILL.md)
- Setting up subagents with isolated contexts
- Creating slash commands
- Configuring lifecycle hooks
- Installing and configuring MCP servers
- IDE integrations (VS Code, JetBrains, Vim)
- Settings and permissions configuration

## Files

| File | Purpose | Size |
|------|---------|------|
| [SKILL.md](SKILL.md) | Main entry with decision tree, routing | ~320 lines |
| [skills.md](skills.md) | SKILL.md creation, troubleshooting | ~346 lines |
| [agents.md](agents.md) | Agent files, tools whitelist | ~361 lines |
| [commands.md](commands.md) | Slash commands, argument syntax | ~288 lines |
| [hooks.md](hooks.md) | Lifecycle events, templates | ~484 lines |
| [mcp-basics.md](mcp-basics.md) | MCP server development | ~370 lines |
| [mcp-servers.md](mcp-servers.md) | MCP server catalog (40+ servers) | ~250 lines |
| [ref-CLAUDE.md](ref-CLAUDE.md) | Extended references | - |

## Routing Logic

| Keywords | Reference Loaded |
|----------|-----------------|
| skill, SKILL.md | skills.md |
| agent, subagent | agents.md |
| command, /cmd, slash | commands.md |
| hook, PreToolUse, PostToolUse | hooks.md |
| MCP development, create mcp | mcp-basics.md |
| MCP catalog, install mcp | mcp-servers.md |

## Naming Conventions

### Global (faion-network)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
| Skill (role-based) | `faion-{role}` | `faion-software-developer` |
| Skill (process) | `faion-{process}` | `faion-sdd` |
| Agent | `faion-{name}-agent` | `faion-task-YOLO-executor-opus-agent` |
| Command | `{verb}` | `commit`, `deploy` |
| Hook | `faion-{event}-{purpose}-hook.{ext}` | `faion-pre-bash-security-hook.py` |

### Project-specific (gitignored)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill | `{project}-{name}` | `myapp-auth` |
| Agent | `{project}-{name}-agent` | `myapp-deploy-agent` |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md) | MCP servers for AI tools |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | CI/CD hooks integration |
