# Agent Integration — Claude Code Hooks

## When to use
- Setting up a new Claude Code project environment and need auto-formatting, linting, or test execution after edits
- Enforcing coding standards across a team or solo workflow (block dangerous git commands, enforce file conventions)
- Long-running agentic sessions where context compaction is expected and state must be preserved
- When Claude subagents are spawned frequently and each needs consistent environment setup at start
- Debugging hook configurations — testing stdin/stdout JSON contracts for existing hook scripts

## When NOT to use
- For logic that should be in CI/CD pipelines — hooks run locally and do not replace remote quality gates
- When the required action takes more than 10 seconds — blocking hooks make the entire Claude session unresponsive
- For network-dependent validation (external API calls, remote test runners) — latency is unpredictable and will block Claude
- For operations that require human judgment — hooks are automatic and cannot pause for confirmation mid-execution
- When the environment doesn't have `jq` installed — most hook patterns depend on it for JSON parsing

## Where it fails / limitations
- Hooks run synchronously and block Claude Code entirely until they complete; a slow hook degrades the whole session
- PreToolUse `block` action prevents tool execution but cannot prevent Claude from planning the blocked action again
- Agent hook type (sub-agent creation) is reserved for future use and not yet available as of 2025
- Hooks do not have access to the full conversation context — they only receive event-specific JSON on stdin
- Settings.json hook changes do not take effect until Claude Code is restarted or the session reloads
- On Windows (WSL), path handling in hook scripts requires explicit WSL path normalization

## Agentic workflow
Claude subagents can write, test, and install hook scripts end-to-end: generate the hook shell script with correct stdin JSON parsing, create the settings.json fragment, test the hook by piping sample event JSON, and update the global or project settings.json. The `update-config` skill handles settings.json modifications safely. Human review is required before deploying hooks that block tool execution (PreToolUse with `block` action) since incorrect matchers can silently prevent legitimate operations.

### Recommended subagents
- `update-config` — modify settings.json with new hook entries safely
- general Bash subagent — test hooks manually by piping JSON event payloads

### Prompt pattern
```
Write a PostToolUse hook script for the Edit tool that:
1. Reads file_path from stdin JSON
2. Runs ruff format + ruff check --fix if .py extension
3. Runs prettier --write if .ts/.js/.json extension
4. Exits 0 always, logs errors to /tmp/claude-hooks.log
5. Returns {"status": "ok"}
Output only the bash script, no explanation.
```

```
Add this hook to my ~/.claude/settings.json:
Event: PostToolUse, Matcher: Edit
Command: bash ~/.claude/hooks/post-edit-format.sh
Preserve all existing hook entries.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Parse stdin JSON in hook scripts | `apt install jq` / https://jqlang.github.io/jq/ |
| `ruff` | Python formatter/linter called from hooks | `pip install ruff` / https://docs.astral.sh/ruff/ |
| `prettier` | JS/TS/JSON formatter called from hooks | `npm i -g prettier` / https://prettier.io/ |
| `tmux` | Session state capture in SubagentStart/UserPromptSubmit hooks | system package |
| `bash` | Hook script runtime — all hook commands run as shell | system package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | SaaS/local CLI | Native | Hooks are a native Claude Code feature; no external integration needed |
| GitHub Actions | SaaS | No | Hooks are local-only; cannot trigger remote CI directly from hooks |
| tmux | OSS | Yes | Hooks can interact with tmux sessions for state capture and logging |

## Templates & scripts
See `templates.md` for full hook script library.

Minimal PostToolUse formatter hook (suitable for direct use):
```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-format.sh
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.parameters.file_path // empty')
[ -z "$FILE" ] || [ ! -f "$FILE" ] && exit 0

EXT="${FILE##*.}"
case "$EXT" in
  py)
    ruff format "$FILE" 2>>/tmp/claude-hooks.log
    ruff check --fix --silent "$FILE" 2>>/tmp/claude-hooks.log
    ;;
  ts|tsx|js|jsx|json)
    npx prettier --write "$FILE" 2>>/tmp/claude-hooks.log
    ;;
esac
echo '{"status":"ok"}'
```

PreToolUse safety hook — blocks force-push to main:
```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.parameters.command // empty')
if echo "$CMD" | grep -qE 'git push.*(--force|-f).*(main|master)'; then
  echo '{"action":"block","reason":"Force push to main/master is not allowed"}'
  exit 0
fi
echo '{"action":"allow"}'
```

## Best practices
- Always read stdin fully with `INPUT=$(cat)` even if the hook doesn't use event data — unread stdin can cause pipe errors
- Return `{"status":"ok"}` or `{"action":"allow"}` explicitly rather than producing no output — silent hooks are harder to debug
- Log errors to a dedicated file (`/tmp/claude-hooks.log`) rather than stderr — stderr output appears in Claude's context as noise
- Set timeouts explicitly for any hook that calls external tools: `"timeout": 10000` (10 seconds) prevents hanging sessions
- Use matchers to scope hooks narrowly — a PostToolUse hook without a matcher runs on every tool call including Read and Glob
- Test every hook by piping a realistic event payload before adding it to settings.json
- Store hook scripts in a dotfiles repo and symlink to `~/.claude/hooks/` for version control and portability

## AI-agent gotchas
- Agents writing hook scripts must include `INPUT=$(cat)` as the first command — hooks that ignore stdin will block waiting for EOF in some environments
- A hook that returns invalid JSON (e.g., a trailing newline with text) causes Claude Code to surface an error in the conversation; agents must validate JSON output before writing hook scripts
- `PreToolUse` hooks with `"action":"block"` prevent the tool from running but do NOT tell Claude why without the `reason` field — always include `reason` to avoid Claude retrying indefinitely
- Agents that modify settings.json directly may corrupt the file if they append without validating existing JSON structure — use the `update-config` skill which merges safely
- Hook execution order within an event is deterministic (array order) but agents often generate hooks without considering ordering dependencies — linters must run after formatters, not before

## References
- https://docs.anthropic.com/en/docs/claude-code/hooks — Claude Code hooks official documentation
- https://jqlang.github.io/jq/manual/ — jq manual for JSON processing in hooks
- https://docs.astral.sh/ruff/ — ruff formatter/linter documentation
- https://prettier.io/docs/en/ — Prettier formatter documentation
