# Agent Integration — Claude Code Agents (Subagents)

## When to use
- Parallelizing independent tasks that don't share state (e.g., three modules implemented simultaneously)
- Context isolation — preventing unrelated research from polluting the primary agent's context window
- Role specialization — a reviewer agent that only reads, a coder agent that only writes
- Long-running background work (research, web scraping, report generation) dispatched from an orchestrator
- Sequential pipeline stages where each stage needs a clean context (spec → design → implement → test)

## When NOT to use
- Simple single-step tasks that complete in one tool call — agent overhead is not justified
- The subtask requires interactive user input mid-execution — agents run autonomously
- Real-time streaming output is required — Task tool is async; results return on completion
- Task needs to share mutable in-memory state with the parent — agents are isolated, use files as IPC

## Where it fails / limitations
- Each agent instance consumes a full context window — spawning 10 agents in parallel is costly
- Agent descriptions drive auto-delegation; weak descriptions cause the wrong agent to be selected
- `bypassPermissions` mode in agents runs without guardrails — dangerous in automated pipelines
- Isolated context means agents cannot see the parent's conversation history unless explicitly passed
- No built-in retry on agent failure — orchestrator must handle errors from the Task tool return value
- Agent files in `.claude/agents/` are loaded at Claude Code startup; changes require session restart
- Circular delegation (agent A spawns agent B which spawns agent A) causes infinite loops

## Agentic workflow
An orchestrator agent (Task tool, Read-only tools) breaks work into focused subtasks and dispatches them to specialized agents via the Task tool. Each subagent returns structured output (JSON). The orchestrator aggregates results and writes the final artifact. For multi-stage pipelines, each stage's output file is the next stage's input — file system is the coordination layer.

### Recommended subagents
- `faion-pm-agent` — project management, issue creation, backlog grooming
- `faion-ba-agent` — requirements analysis, spec drafting
- `faion-spec-reviewer-agent` — validates spec/design documents against quality rubric
- `faion-task-YOLO-executor-opus-agent` — executes implementation tasks with maximum autonomy
- `faion-idea-generator-agent` — generates options/alternatives for architectural decisions
- Built-in `Explore` subagent (subagent_type) — fast read-only codebase search

### Prompt pattern
Orchestrator dispatching:
```
Use the Task tool to spawn a research agent:
- subagent_type: "general-purpose"
- prompt: "Read {files}, extract {information}, write findings to {output_path} as JSON."
Then spawn an implementation agent with the findings as input.
```

Agent system prompt structure:
```markdown
---
name: faion-{role}-agent
description: {Action verb} + {object} + {when to use this agent}
model: sonnet
tools: [Read, Glob, Grep]
---
You are a {role}. Your input is {input}. Your output is {output path and format}.
## Workflow
1. {step}
## Rules
- Output ONLY to {path}, never edit source files
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` CLI | Launch Claude Code, list agents, invoke `/agent-name` | Bundled |
| `gh` | GitHub CLI used inside agents for PR/issue operations | cli.github.com |
| `jq` | Parse JSON output from agents in shell scripts | System package |
| `flock` | Serialize concurrent agent writes to shared files | Part of `util-linux` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code (local/remote) | OSS/SaaS | Native | Agents are a first-class Claude Code primitive |
| Anthropic Agent SDK | OSS | Yes | Alternative for programmatic agent orchestration |
| GitHub Actions | SaaS | Yes | Agents can push commits, create PRs via `gh` |
| Linear | SaaS | Yes | Agents create/update issues via Linear API |

## Templates & scripts
See `templates.md` for full agent file templates (research, implementation, reviewer, orchestrator roles).

Minimal research agent:
```markdown
---
name: faion-research-agent
description: Researches codebase patterns. Use when you need to understand code structure.
model: haiku
tools: [Read, Glob, Grep, WebFetch]
---
Research the codebase for: {topic}
Write structured findings to the path provided in your prompt.
Use Grep to find patterns, Glob to find files. Be exhaustive.
```

## Best practices
- One clear goal per agent — agents that "research AND implement AND test" fail at all three
- Whitelist only tools the agent actually needs (least privilege); avoids accidental side effects
- Write agent output to files, not stdout — the orchestrator reads files; stdout is discarded after Task completes
- Use `model: haiku` for read-only research agents; reserve `opus` for architecture and spec writing
- Put shared context (project constraints, conventions) in the agent's system prompt, not the Task prompt
- Prefer `permissionMode: acceptEdits` over `bypassPermissions` for file-writing agents
- Name agents with action verbs in `description` — "Analyzes X", "Implements Y", "Reviews Z" — drives auto-delegation accuracy

## AI-agent gotchas
- Agent descriptions are used by Claude to decide when to auto-delegate — test descriptions by asking "would I use this agent if I saw this description?"
- Agents spawned via Task tool cannot ask the user questions (`AskUserQuestion` blocks the async call) — design agents to be fully autonomous or return a structured "needs_input" response
- If an agent writes to a file that another concurrent agent also writes to, the last write wins — use unique output paths per agent or `flock`
- Context passed to a subagent via the Task prompt counts against the subagent's context limit — keep prompts concise, reference files rather than inlining content
- An agent with `Bash` tool and `bypassPermissions` can delete files, push to remote, send network requests — audit before granting
- The `skills` frontmatter field loads skills into the agent's context; loading too many skills inflates context and degrades instruction-following

## References
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://docs.anthropic.com/en/docs/claude-code/skills
- https://docs.anthropic.com/en/docs/claude-code/slash-commands
