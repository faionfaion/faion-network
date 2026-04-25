# Agent Integration — Claude Code Commands (Slash Commands)

## When to use
- Exposing a repeatable action to developers with a predictable interface (`/deploy`, `/commit`, `/review`)
- Wrapping a complex Bash + context injection sequence that would be tedious to type every session
- Creating lightweight project-specific shortcuts that don't need the overhead of a full skill/agent
- Injecting live context (current branch, diff, env) at invocation time via `!`-prefix bash execution

## When NOT to use
- Workflow requires multiple sequential agents, memory between steps, or parallel subtasks → use a skill or agent instead
- Action must run automatically (not via manual `/invoke`) → use hooks
- Logic exceeds ~250 lines — split into a skill with SKILL.md
- Command is project-private and the team doesn't use faion-network → store locally, gitignore it

## Where it fails / limitations
- Commands share the main agent's context window — heavy `!`-bash output inflates context fast
- No built-in state persistence between invocations; each `/cmd` is a fresh call
- `argument-hint` is cosmetic only — the model sees raw `$ARGUMENTS`, no parsing or validation
- `allowed-tools: Bash(git:*)` uses prefix matching; typo in prefix silently grants no permission
- SlashCommand → Skill tool rename (Jan 2026): permissions referencing `SlashCommand` must be updated to `Skill`
- Model field selects the model for the command's primary turn but subagent calls within still use their own model

## Agentic workflow
A command-creation agent reads the user's intent, checks existing `.claude/commands/` for duplicates, drafts the frontmatter (tools, model, args) and body, then writes the file. A separate review pass validates token economy (no tables where lists work, English only, under 200 lines). No human checkpoint needed for simple commands; complex workflows generating agent files should pause for review.

### Recommended subagents
- General-purpose implementer (Write, Edit, Read) — creates the command file from a description
- `faion-spec-reviewer-agent` — validates the command against naming convention and token economy rules

### Prompt pattern
```
Create a Claude Code slash command for: {task_description}
- Location: {.claude/commands/name.md or ~/.claude/commands/name.md}
- Arguments: {$1 = X, $2 = Y or $ARGUMENTS}
- Tools needed: {list}
- Keep under 150 lines. English. No tables where lists work.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` CLI | `claude mcp add`, `claude /help`, list/run commands | Bundled with Claude Code |
| `jq` | Parse JSON frontmatter or hook input in `!`-bash blocks | System package |
| `gh` | GitHub CLI — common in commands for PR/issue ops | `brew install gh` / cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | OSS/SaaS | Native | Commands are native; no external service needed |
| GitHub Actions | SaaS | Yes | Commands can trigger via `gh workflow run` |
| Linear | SaaS | Yes | Commands wrapping `gh`+Linear API for issue ops |

## Templates & scripts
See `templates.md` in this directory.

Minimal command template:
```markdown
---
description: {what it does}
argument-hint: [{arg}]
allowed-tools: Bash(git:*), Read
model: claude-sonnet-4-20250514
---

Branch: !`git branch --show-current`
Diff: !`git diff --stat HEAD`

{Instructions using $ARGUMENTS}
```

## Best practices
- Keep commands stateless — no file writes, no side effects unless the name implies it (`/deploy`, `/commit`)
- Use `model: haiku` for mechanical tasks (lint, format check); saves cost on high-frequency commands
- Put shared helper scripts in `~/.claude/scripts/` and call them via Bash; don't inline 50-line scripts in commands
- Namespace project-specific commands: `.claude/commands/{project}-{action}.md` + gitignore at parent level
- Test `!`-bash prefix separately in terminal before embedding; errors produce silent empty strings
- The `disable-model-invocation: true` flag prevents auto-delegation — use for commands that must only run manually

## AI-agent gotchas
- Commands invoked by an agent (via Skill tool) run in the agent's context window — `!`-bash output is injected verbatim; keep it short
- If a command writes files, it bypasses the agent's permission system unless Write is in `allowed-tools`
- `$ARGUMENTS` passes the full argument string unparsed — agent-generated arguments may contain newlines or quotes that break shell interpolation in `!`-bash blocks
- Auto-delegation: Claude selects commands based on the `description` field; vague descriptions cause wrong command invocation
- Avoid `allowed-tools: Bash` (no prefix) in shared commands — grants unrestricted shell access to any agent using the command

## References
- https://docs.anthropic.com/en/docs/claude-code/slash-commands
- https://docs.anthropic.com/en/docs/claude-code/skills
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
