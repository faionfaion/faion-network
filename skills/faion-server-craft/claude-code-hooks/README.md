# Claude Code Hooks

## Overview

Claude Code hooks are user-defined scripts that execute at specific points during Claude Code's operation. They enable automation such as formatting code after edits, running linters, saving tmux sessions, auto-staging git changes, running tests, and enforcing project conventions. Hooks are configured in `.claude/settings.json` and support command, prompt, and agent types.

**Target:** Developers using Claude Code on VPS or workstation who want to automate repetitive actions and enforce quality gates.

## When to Use

| Scenario | Fit |
|----------|-----|
| Auto-formatting code after Claude edits a file | Essential |
| Running linter before committing | Essential |
| Saving tmux session state during long agent runs | Recommended |
| Auto-running tests after code changes | Recommended |
| Enforcing coding standards on every edit | Recommended |
| Custom validation before tool execution | Good |
| Injecting context at session start | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Hook** | User script that runs at a specific event in Claude Code |
| **Event** | Trigger point: PreToolUse, PostToolUse, UserPromptSubmit, etc. |
| **Matcher** | Filter that restricts which tools/events trigger the hook |
| **Hook type** | command (shell), prompt (returns text), agent (creates sub-agent) |
| **Blocking** | Hooks run synchronously and block Claude until complete |
| **JSON output** | Hooks can return JSON to modify Claude's behavior |

## Hook Events

| Event | When it Fires | Common Use |
|-------|---------------|------------|
| `PreToolUse` | Before any tool call | Validate, block, modify params |
| `PostToolUse` | After any tool call | Format, lint, test, notify |
| `UserPromptSubmit` | When user sends a message | Inject context, validate input |
| `SubagentStart` | When a sub-agent is created | Save state, log |
| `Stop` | When Claude finishes a turn | Post-processing, cleanup |
| `SessionStart` | When a new session begins | Load context, set up env |
| `PreCompact` | Before context compaction | Save important state |
| `PostCompact` | After context compaction | Restore important state |

## Hook Types

### Command Hook

Runs a shell command. Receives event data on stdin, returns JSON on stdout.

```json
{
    "type": "command",
    "command": "bash /path/to/hook.sh"
}
```

### Prompt Hook

Returns text that gets injected into Claude's context.

```json
{
    "type": "prompt",
    "prompt": "Always use single quotes in TypeScript files."
}
```

### Agent Hook (Not Yet Available)

Creates a sub-agent that processes the event. Reserved for future use.

## settings.json Structure

### Location

```
~/.claude/settings.json           # Global settings (all projects)
{project}/.claude/settings.json   # Project-specific settings
```

### Hook Configuration Format

```json
{
    "hooks": {
        "EventName": [
            {
                "type": "command",
                "command": "command-to-run",
                "matcher": "optional-tool-name-pattern",
                "timeout": 30000
            }
        ]
    }
}
```

### Full settings.json Example

```json
{
    "hooks": {
        "PreToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/pre-tool-use.sh",
                "matcher": "Edit"
            }
        ],
        "PostToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-edit-format.sh",
                "matcher": "Edit"
            },
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-write-format.sh",
                "matcher": "Write"
            }
        ],
        "UserPromptSubmit": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh"
            }
        ],
        "SubagentStart": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh"
            }
        ],
        "Stop": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/on-stop.sh"
            }
        ]
    }
}
```

## Matchers

Matchers filter which tool calls trigger a hook. The matcher string is compared against the tool name.

| Matcher | Matches |
|---------|---------|
| `"Edit"` | Edit tool only |
| `"Write"` | Write tool only |
| `"Bash"` | Bash tool only |
| `"Read"` | Read tool only |
| (omitted) | All tools |

Multiple hooks for the same event are executed in order.

## Hook Input (stdin)

Hooks receive a JSON object on stdin with event-specific data.

### PreToolUse / PostToolUse Input

```json
{
    "event": "PostToolUse",
    "tool": "Edit",
    "parameters": {
        "file_path": "/home/nero/workspace/repos/nero-core/src/main.py",
        "old_string": "...",
        "new_string": "..."
    },
    "result": "OK"
}
```

### UserPromptSubmit Input

```json
{
    "event": "UserPromptSubmit",
    "prompt": "Fix the bug in the auth module"
}
```

## Hook Output (stdout)

Hooks can return JSON to influence Claude's behavior.

### PreToolUse Output Options

```json
{"action": "allow"}
{"action": "block", "reason": "File is read-only"}
{"action": "modify", "parameters": {"file_path": "/new/path.py"}}
```

### PostToolUse Output Options

```json
{"status": "ok"}
{"status": "error", "message": "Formatting failed"}
```

### No Output

If a hook produces no JSON output, it is treated as successful.

## Common Hook Patterns

### 1. Auto-Format After Edit

```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-format.sh
# Formats files after Claude edits them

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

EXTENSION="${FILE_PATH##*.}"

case "$EXTENSION" in
    py)
        ruff format "$FILE_PATH" 2>/dev/null
        ruff check --fix "$FILE_PATH" 2>/dev/null
        ;;
    ts|tsx|js|jsx)
        npx prettier --write "$FILE_PATH" 2>/dev/null
        ;;
    json)
        npx prettier --write "$FILE_PATH" 2>/dev/null
        ;;
    *)
        # No formatter for this extension
        ;;
esac

echo '{"status": "ok"}'
```

### 2. Tmux Session Save

```bash
#!/bin/bash
# ~/.claude/hooks/tmux-save.sh
# Saves tmux session layout on user prompt and subagent start

if [ -n "$TMUX" ]; then
    tmux capture-pane -t . -p > /tmp/tmux-claude-last-pane.txt 2>/dev/null
fi

echo '{"status": "ok"}'
```

### 3. Pre-Commit Validation

```bash
#!/bin/bash
# ~/.claude/hooks/pre-bash-validate.sh
# Blocks dangerous git commands

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // empty')

# Block force push to main
if echo "$COMMAND" | grep -qE 'git push.*--force.*main|git push.*-f.*main'; then
    echo '{"action": "block", "reason": "Force push to main is not allowed"}'
    exit 0
fi

# Block reset --hard without confirmation
if echo "$COMMAND" | grep -qE 'git reset --hard'; then
    echo '{"action": "block", "reason": "git reset --hard requires explicit user confirmation"}'
    exit 0
fi

echo '{"action": "allow"}'
```

### 4. Auto-Run Tests After Edit

```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-test.sh
# Runs relevant tests after editing Python files

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty')

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Only for Python files
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# Find corresponding test file
DIR=$(dirname "$FILE_PATH")
BASENAME=$(basename "$FILE_PATH" .py)
TEST_FILE="$DIR/test_${BASENAME}.py"

if [ -f "$TEST_FILE" ]; then
    python -m pytest "$TEST_FILE" -x -q 2>&1 | tail -5
fi

echo '{"status": "ok"}'
```

### 5. Session Start Context

```bash
#!/bin/bash
# ~/.claude/hooks/session-start.sh
# Injects context at session start

echo '{"status": "ok"}'

# Or inject useful context:
# echo '{"context": "Server: Hetzner CX53, Ubuntu 24.04, 16 CPUs, 30GB RAM"}'
```

### 6. Git Auto-Stage After Write

```bash
#!/bin/bash
# ~/.claude/hooks/post-write-stage.sh
# Auto-stages newly created files

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Check if file is in a git repo
if git -C "$(dirname "$FILE_PATH")" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "$(dirname "$FILE_PATH")" add "$FILE_PATH" 2>/dev/null
fi

echo '{"status": "ok"}'
```

## Performance Considerations

| Factor | Recommendation |
|--------|---------------|
| Hook execution time | Keep under 5 seconds |
| Timeout | Default is 30s, set lower for frequent hooks |
| Blocking nature | Hooks block Claude, keep them fast |
| External calls | Avoid network calls in hooks |
| Error handling | Always exit 0, log errors separately |
| Large files | Skip formatting for files > 1MB |

## Debugging Hooks

### Testing a Hook Manually

```bash
# Simulate PostToolUse event
echo '{"event":"PostToolUse","tool":"Edit","parameters":{"file_path":"/tmp/test.py"}}' | \
    bash ~/.claude/hooks/post-edit-format.sh

# Check exit code
echo $?
```

### Logging

```bash
# Add logging to hooks for debugging
LOG_FILE="/tmp/claude-hooks.log"
echo "$(date) - $0 - $(cat)" >> "$LOG_FILE"
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Hook not firing | Wrong matcher | Check tool name spelling |
| Hook timeout | Command too slow | Optimize or increase timeout |
| Permission denied | Script not executable | `chmod +x hook.sh` |
| jq not found | jq not installed | `sudo apt install jq` |
| JSON parse error | Invalid JSON output | Validate with `jq .` |

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [dotfiles-management](../dotfiles-management/) | Store hooks in dotfiles repo |
| [deploy-scripts](../deploy-scripts/) | Hooks can trigger deploy validation |
| [secrets-management](../secrets-management/) | Hooks should not contain secrets |
