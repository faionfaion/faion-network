# faion-claude-code Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-claude-code`

## When to Use

- Creating and managing Claude Code skills (SKILL.md)
- Setting up subagents with isolated contexts
- Creating slash commands
- Configuring lifecycle hooks
- Installing and configuring MCP servers
- IDE integrations (VS Code, JetBrains, Vim)
- Settings and permissions configuration
- Naming conventions for faion-network

## Overview

Claude Code configuration skill for creating and managing:
- Skills (SKILL.md files, references, automation)
- Agents (subagents with isolated context)
- Commands (slash commands with arguments)
- Hooks (lifecycle automation scripts)
- MCP servers (Model Context Protocol integrations)

<<<<<<< HEAD
Also covers settings, permissions, IDE integrations, and naming conventions.

---

## Directory Structure

```
faion-claude-code/
├── SKILL.md           # Main skill definition and routing
├── CLAUDE.md          # This navigation file
├── skills.md          # Skill creation guide (~346 lines)
├── agents.md          # Agent creation guide (~361 lines)
├── commands.md        # Command creation guide (~288 lines)
├── hooks.md           # Hook development guide (~484 lines)
├── mcp.md             # MCP server reference (~706 lines)
└── ref-CLAUDE.md      # Extended references
```

---

## Key Files

| File | Purpose | Size |
|------|---------|------|
| **SKILL.md** | Main entry point with routing table, naming conventions, settings reference, quick commands | ~276 lines |
| **skills.md** | SKILL.md creation, frontmatter fields, token economy, locations, troubleshooting | ~346 lines |
| **agents.md** | Agent files, tools whitelist, prompt writing, parallel execution patterns | ~361 lines |
| **commands.md** | Slash commands, argument syntax ($1, $ARGUMENTS), special syntax (!, @) | ~288 lines |
| **hooks.md** | Lifecycle events, input/output schemas, templates (Python/Bash), common patterns | ~484 lines |
| **mcp.md** | MCP server development (TS/Python), catalog of 40+ servers, configuration | ~706 lines |

---
=======
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
>>>>>>> claude

## Routing Logic

| Keywords | Reference Loaded |
|----------|-----------------|
| skill, SKILL.md | skills.md |
| agent, subagent | agents.md |
| command, /cmd, slash | commands.md |
| hook, PreToolUse, PostToolUse | hooks.md |
<<<<<<< HEAD
| MCP, server, install mcp | mcp.md |
| settings, config | Handled directly in SKILL.md |
=======
| MCP development, create mcp | mcp-basics.md |
| MCP catalog, install mcp | mcp-servers.md |
>>>>>>> claude

## Naming Conventions

### Global (faion-network)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
<<<<<<< HEAD
| Skill (role-based) | `faion-{role}` | `faion-software-developer`, `faion-ux-ui-designer` |
| Skill (process) | `faion-{process}` | `faion-sdd`, `faion-feature-executor` |
=======
| Skill (role-based) | `faion-{role}` | `faion-software-developer` |
| Skill (process) | `faion-{process}` | `faion-sdd` |
>>>>>>> claude
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
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-ml-engineer](../faion-ml-engineer/CLAUDE.md) | MCP servers for AI tools |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | CI/CD hooks integration |
