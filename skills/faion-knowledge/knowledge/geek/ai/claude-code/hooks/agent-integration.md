# Agent Integration — Claude Code Hooks

## When to use
- Enforcing security policy: block dangerous commands (rm -rf, DROP TABLE) before they execute
- Auto-approval of known-safe operations to reduce permission prompts in automated pipelines
- Post-edit formatting: run prettier/ruff/eslint automatically after every Write or Edit
- Injecting session context (git branch, project name, env) at session start so agents don't have to ask
- Preventing premature agent exit when tasks are still incomplete (Stop hook)
- Audit logging: record every Bash command for compliance or debugging

## When NOT to use
- Hook logic is complex enough to warrant a standalone agent — hooks are synchronous, blocking, and have a 60s default timeout
- You need to modify the model's response rather than the tool execution — hooks operate on tool calls, not text output
- The action should be user-triggered (on demand), not automatic — use a command or agent instead
- Hook script has side effects that must be reversible — hooks run before confirmation dialogs

## Where it fails / limitations
- Exit code 2 blocks the tool — if your hook crashes unexpectedly (Python exception), it exits non-zero and blocks silently
- Hooks run synchronously; a slow hook (API call, heavy computation) adds latency to every tool call it matches
- `suppressOutput: true` in the hook JSON response hides the permission prompt — accidentally suppressing all output makes debugging hard
- Regex matchers in `matcher` field must be valid JavaScript regex; PCRE syntax doesn't work
- Hooks defined in component frontmatter (skills/agents) run only while that component is active — not globally
- The `CLAUDE_ENV_FILE` trick (persist env vars) only works in `SessionStart` hooks; other hooks cannot persist env between calls

## Agentic workflow
Design hooks as thin guards, not business logic: a PreToolUse hook reads stdin JSON, checks one condition, exits 0 or 2. A PostToolUse hook runs a formatter and exits 0. Keep them under 30 lines. An agent can write new hook scripts to the filesystem and update `settings.json` — but the new hooks only activate after a session restart. For dynamic hook behavior, use a dispatcher hook that delegates to a script selected by env var.

### Recommended subagents
- General-purpose implementer (Write, Edit, Bash) — writes hook scripts and updates settings.json
- `faion-spec-reviewer-agent` — validates hook logic against security checklist before deployment
- Bash testing agent — runs hook manually against sample inputs: `echo '{...}' | python hook.py`

### Prompt pattern
```
Write a PreToolUse hook (Python) that:
- Blocks any Bash command matching: {pattern_list}
- Allows all other Bash commands
- Exits 2 with message "{message}" on block
- Exits 0 silently on allow
Install to ~/.claude/scripts/hooks/{name}-hook.py and register in ~/.claude/settings.json.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude /hooks` | List all registered hooks in current session | Bundled |
| `claude --debug` | Show hook execution output and errors | Bundled |
| `jq` | Parse hook stdin JSON in bash hooks | System package |
| `python3` | Recommended for hook scripts (safer than bash for JSON parsing) | System |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code hooks system | OSS | Native | Built-in; no external service |
| GitHub Actions | SaaS | Indirect | PostToolUse hooks can trigger `gh` CLI calls |
| Datadog / Grafana | SaaS | Yes | Logging hooks can push metrics via curl |
| Sentry | SaaS | Yes | Error hooks can send hook failures to Sentry |

## Templates & scripts
See `templates.md` for full Python and Bash hook templates.

Production-ready security hook (blocks dangerous patterns):
```python
#!/usr/bin/env python3
"""PreToolUse security guard — blocks high-risk bash patterns."""
import json, sys, re

BLOCKED = [
    r"rm\s+-rf\s+/",
    r"git\s+push\s+.*--force.*main",
    r"DROP\s+TABLE",
    r"truncate\s+/",
    r"> /dev/sd",
]

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # malformed input — allow and let Claude handle

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    for pattern in BLOCKED:
        if re.search(pattern, command, re.IGNORECASE):
            print(f"Blocked: matches dangerous pattern '{pattern}'", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Best practices
- Write hooks in Python, not bash — Python's `json.load(sys.stdin)` is safer than `jq` in shell scripts
- Always handle `json.JSONDecodeError` — malformed input should default to allowing (exit 0), not blocking
- Use the `matcher` field to scope hooks narrowly: `"Bash"` not `".*"` unless you need all tools
- Test hooks manually before registering: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python hook.py`
- Keep hooks idempotent — PostToolUse formatters should produce the same result if run twice
- Log blocked commands to a file (not just stderr) for audit: `echo "BLOCKED: $command" >> ~/.claude/hook-audit.log`
- Set `"timeout": 10` for hooks that do I/O — never leave it at the 60s default for simple checks

## AI-agent gotchas
- An agent that writes hook scripts and registers them cannot use them in the same session — hooks load at startup only
- If a PreToolUse hook blocks a tool the agent considers essential, the agent may enter a retry loop — design hooks to provide actionable error messages explaining what alternative to use
- Hooks with `permissionDecision: "allow"` bypass the normal permission prompt — this is powerful but means the user has no visibility into what was auto-approved; log these approvals
- The `updatedInput` field in PreToolUse output lets a hook rewrite the command Claude executes — powerful but can cause unexpected behavior if the agent doesn't know the command was modified
- Stop hooks that return `{"decision": "block"}` prevent the agent from completing — always include a `"reason"` so the agent knows why it was blocked and what to do next
- UserPromptSubmit hooks run before Claude sees the prompt — a hook that blocks here silently drops the user's message; always show a reason in `stopReason`

## References
- https://docs.anthropic.com/en/docs/claude-code/hooks
