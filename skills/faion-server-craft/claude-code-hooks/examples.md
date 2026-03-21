# Claude Code Hooks Examples

## Example 1: NERO Hooks Configuration

Current hook setup on the NERO server for Claude Code development sessions.

### settings.json

```json
{
    "hooks": {
        "PostToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-edit-format.sh",
                "matcher": "Edit",
                "timeout": 10000
            },
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-write-format.sh",
                "matcher": "Write",
                "timeout": 10000
            }
        ],
        "UserPromptSubmit": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh",
                "timeout": 5000
            }
        ],
        "SubagentStart": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh",
                "timeout": 5000
            }
        ]
    }
}
```

### What This Achieves

1. Every time Claude edits a Python file, `ruff format` and `ruff check --fix` run automatically
2. Every time Claude writes a new file, the same formatting applies
3. Every time the user sends a prompt or a sub-agent starts, tmux pane content is captured
4. No manual formatting needed -- code is always clean

### Workflow in Practice

```
User: "Fix the import order in nero_core/tasks.py"

Claude: [Edit tool] → modifies nero_core/tasks.py
  ↓ PostToolUse hook fires
  ↓ post-edit-format.sh runs
  ↓ ruff format + ruff check --fix run on the file
  ↓ File is now formatted AND has import order fixed

User: "Create a new module nero_core/utils/retry.py"

Claude: [Write tool] → creates nero_core/utils/retry.py
  ↓ PostToolUse hook fires
  ↓ post-write-format.sh runs
  ↓ ruff format runs on the new file
  ↓ File is formatted from the start
```

## Example 2: Auto-Format Hook for Python (ruff)

### Hook Script

```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-format.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Only format Python files
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# Skip very large files
FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || echo 0)
if [ "$FILE_SIZE" -gt 1048576 ]; then
    exit 0
fi

# Run ruff (must be in PATH or use absolute path)
if command -v ruff &>/dev/null; then
    ruff format --quiet "$FILE_PATH" 2>/dev/null
    ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
fi

echo '{"status": "ok"}'
```

### Testing the Hook

```bash
# Create a badly formatted Python file
$ cat > /tmp/test_format.py << 'EOF'
import os
import sys
import json
from pathlib import Path
import  re

def foo(  x,y,z ):
    return x+y+z

def bar():
    unused_var = 42
    return "hello"
EOF

# Simulate PostToolUse event
$ echo '{"event":"PostToolUse","tool":"Edit","parameters":{"file_path":"/tmp/test_format.py"}}' | \
    bash ~/.claude/hooks/post-edit-format.sh
{"status": "ok"}

# Check the result
$ cat /tmp/test_format.py
import json
import os
import re
import sys
from pathlib import Path


def foo(x, y, z):
    return x + y + z


def bar():
    return "hello"

# ruff formatted: fixed spacing, sorted imports, removed unused variable
```

## Example 3: Git Safety Hook

Preventing destructive git operations during Claude Code sessions.

### Hook Script

```bash
#!/bin/bash
# ~/.claude/hooks/pre-bash-safety.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    echo '{"action": "allow"}'
    exit 0
fi

# Block force push to main/master
if echo "$COMMAND" | grep -qEi 'git\s+push\s+.*--force.*\b(main|master)\b'; then
    echo '{"action": "block", "reason": "Force push to main/master is blocked."}'
    exit 0
fi

# Block git reset --hard
if echo "$COMMAND" | grep -qE 'git\s+reset\s+--hard'; then
    echo '{"action": "block", "reason": "git reset --hard is blocked. Use git stash or git checkout -- file."}'
    exit 0
fi

# Block rm -rf on important directories
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/srv|/home|\$HOME|~/workspace)'; then
    echo '{"action": "block", "reason": "Refusing to rm -rf important directories."}'
    exit 0
fi

echo '{"action": "allow"}'
```

### In Action

```
User: "Push the changes to main"

Claude: [Bash] git push --force origin main
  ↓ PreToolUse hook fires
  ↓ pre-bash-safety.sh runs
  ↓ Returns: {"action": "block", "reason": "Force push to main/master is blocked."}
  ↓ Claude sees the block and adjusts

Claude: "The force push to main was blocked by a safety hook.
         I'll push normally instead."
Claude: [Bash] git push origin main
  ↓ PreToolUse hook fires
  ↓ pre-bash-safety.sh runs
  ↓ Returns: {"action": "allow"}
  ↓ Command executes normally
```

## Example 4: Tmux Save on Prompt

Capturing tmux pane content on every user prompt for debugging context.

### Hook Script

```bash
#!/bin/bash
# ~/.claude/hooks/tmux-save.sh

if [ -z "${TMUX:-}" ]; then
    exit 0
fi

SAVE_DIR="$HOME/.claude/tmux-captures"
mkdir -p "$SAVE_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tmux capture-pane -t "$TMUX_PANE" -p > "$SAVE_DIR/capture_${TIMESTAMP}.txt" 2>/dev/null

# Cleanup: keep only last 10
ls -t "$SAVE_DIR"/capture_*.txt 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null

echo '{"status": "ok"}'
```

### Result

```bash
$ ls ~/.claude/tmux-captures/
capture_20260321_100000.txt
capture_20260321_100145.txt
capture_20260321_100312.txt
capture_20260321_100500.txt

$ head -5 ~/.claude/tmux-captures/capture_20260321_100500.txt
nero@nero-hetzner:~/workspace/repos/nero-core$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Example 5: Pre-Commit Validation Hook

Hook that validates code before Claude creates a commit.

### Hook Script

```bash
#!/bin/bash
# ~/.claude/hooks/pre-commit-validate.sh
# Matcher: "Bash" - triggers on any Bash command
# Validates before git commit commands

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // empty' 2>/dev/null)

# Only intercept git commit commands
if ! echo "$COMMAND" | grep -qE 'git\s+commit'; then
    echo '{"action": "allow"}'
    exit 0
fi

# Find the git repo root
# The command might specify a directory, but default to cwd
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo '{"action": "allow"}'
    exit 0
fi

ISSUES=""

# Check for .env files in staging
STAGED_ENV=$(git -C "$REPO_ROOT" diff --cached --name-only | grep -E '\.env$|\.env\.' | grep -v '\.example$' | grep -v '\.tpl$')
if [ -n "$STAGED_ENV" ]; then
    ISSUES="${ISSUES}Staged .env files detected: $STAGED_ENV. "
fi

# Check for large files (>5MB)
LARGE_FILES=$(git -C "$REPO_ROOT" diff --cached --name-only | while read f; do
    if [ -f "$REPO_ROOT/$f" ]; then
        SIZE=$(stat -c%s "$REPO_ROOT/$f" 2>/dev/null || echo 0)
        if [ "$SIZE" -gt 5242880 ]; then
            echo "$f ($(($SIZE / 1048576))MB)"
        fi
    fi
done)
if [ -n "$LARGE_FILES" ]; then
    ISSUES="${ISSUES}Large files staged: $LARGE_FILES. "
fi

if [ -n "$ISSUES" ]; then
    echo "{\"action\": \"block\", \"reason\": \"Pre-commit validation failed: $ISSUES\"}"
else
    echo '{"action": "allow"}'
fi
```

## Example 6: Debugging a Broken Hook

Hook is not firing or producing errors.

### Symptom: Hook Not Running

```bash
# Check settings.json is valid JSON
$ jq . ~/.claude/settings.json
# If this errors, fix the JSON syntax

# Check hook file exists and is executable
$ ls -la ~/.claude/hooks/post-edit-format.sh
-rwxr-xr-x 1 nero nero 500 Mar 21 post-edit-format.sh

# Check matcher is correct (case-sensitive)
# "Edit" (correct) vs "edit" (wrong) vs "EDIT" (wrong)
```

### Symptom: Hook Errors

```bash
# Add logging to diagnose
$ cat > /tmp/debug-hook.sh << 'HOOK'
#!/bin/bash
INPUT=$(cat)
echo "$(date) HOOK INPUT: $INPUT" >> /tmp/hook-debug.log
echo '{"status": "ok"}'
HOOK
$ chmod +x /tmp/debug-hook.sh

# Temporarily point settings.json to debug hook
# Then trigger an edit and check the log
$ cat /tmp/hook-debug.log
2026-03-21 10:00:00 HOOK INPUT: {"event":"PostToolUse","tool":"Edit","parameters":{"file_path":"/home/nero/test.py","old_string":"foo","new_string":"bar"}}
```

### Symptom: jq Not Found

```bash
# Hook scripts depend on jq for JSON parsing
$ which jq
# Nothing returned

$ sudo apt install -y jq
$ which jq
/usr/bin/jq

# Hooks should now work
```

### Symptom: Hook Takes Too Long

```bash
# Check timeout in settings.json
# Default: 30000 (30s), reduce for frequent hooks
{
    "type": "command",
    "command": "bash ~/.claude/hooks/post-edit-format.sh",
    "matcher": "Edit",
    "timeout": 10000  # 10s should be plenty for formatting
}

# If formatter is slow on large files, add size check:
FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || echo 0)
if [ "$FILE_SIZE" -gt 1048576 ]; then
    # Skip files larger than 1MB
    exit 0
fi
```
