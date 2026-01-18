# Hook Patterns Reference

Common patterns and solutions for Claude Code hooks.

---

## Security Patterns

### 1. File Protection

**Problem:** Prevent modifications to sensitive files.

```python
PROTECTED = [".env", ".git/", "secrets/", ".pem", ".key"]

file_path = tool_input.get("file_path", "")
if any(p in file_path for p in PROTECTED):
    print(f"Protected: {file_path}", file=sys.stderr)
    sys.exit(2)
```

### 2. Command Blocklist

**Problem:** Block dangerous shell commands.

```python
BLOCKED = [
    r"rm\s+-rf\s+/",
    r"sudo\s+rm",
    r"chmod\s+777",
    r">\s*/dev/sd",
]

command = tool_input.get("command", "")
for pattern in BLOCKED:
    if re.search(pattern, command):
        print(f"Blocked: {command}", file=sys.stderr)
        sys.exit(2)
```

### 3. Path Traversal Prevention

**Problem:** Block attempts to access files outside project.

```python
import os

file_path = tool_input.get("file_path", "")
project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")

# Resolve to absolute path
resolved = os.path.realpath(file_path)

# Check if within project
if not resolved.startswith(project_dir):
    print("Path traversal blocked", file=sys.stderr)
    sys.exit(2)
```

### 4. Secrets Detection

**Problem:** Prevent writing secrets to files.

```python
import re

SECRET_PATTERNS = [
    r"(?i)api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
    r"(?i)password\s*[:=]\s*['\"][^'\"]+['\"]",
    r"(?i)secret\s*[:=]\s*['\"][^'\"]+['\"]",
    r"(?i)token\s*[:=]\s*['\"][^'\"]+['\"]",
    r"AKIA[0-9A-Z]{16}",  # AWS Access Key
    r"sk-[a-zA-Z0-9]{48}",  # OpenAI API Key
]

content = tool_input.get("content", "") or tool_input.get("new_string", "")

for pattern in SECRET_PATTERNS:
    if re.search(pattern, content):
        print("Potential secret detected", file=sys.stderr)
        sys.exit(2)
```

---

## Automation Patterns

### 5. Auto-Approve Safe Operations

**Problem:** Skip permission prompts for safe operations.

```python
# Auto-approve documentation reads
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".txt", ".json")):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Documentation file"
            },
            "suppressOutput": True
        }
        print(json.dumps(output))
        sys.exit(0)
```

### 6. Auto-Format After Edit

**Problem:** Automatically format code after modifications.

```bash
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

case "$FILE_PATH" in
    *.ts|*.tsx|*.js|*.jsx|*.json)
        npx prettier --write "$FILE_PATH" 2>/dev/null || true
        ;;
    *.py)
        black "$FILE_PATH" 2>/dev/null || true
        ;;
    *.go)
        gofmt -w "$FILE_PATH" 2>/dev/null || true
        ;;
esac
```

### 7. Auto-Run Tests After Edit

**Problem:** Run related tests after file changes.

```python
import subprocess
from pathlib import Path

file_path = tool_input.get("file_path", "")
p = Path(file_path)

# Find related test file
test_patterns = [
    p.parent / f"{p.stem}.test{p.suffix}",
    p.parent / f"{p.stem}.spec{p.suffix}",
    p.parent / "__tests__" / f"{p.stem}.test{p.suffix}",
]

for test_file in test_patterns:
    if test_file.exists():
        subprocess.run(["npm", "test", "--", str(test_file)], capture_output=True)
        break
```

### 8. Command Modification

**Problem:** Modify commands before execution.

```python
command = tool_input.get("command", "")

# Always add --no-install flag to npm test
if command.startswith("npm test"):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": {
                "command": f"{command} --no-install"
            }
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

---

## Logging Patterns

### 9. Command Logging

**Problem:** Log all executed commands for audit.

```python
import os
from datetime import datetime

log_file = os.path.expanduser("~/.claude/command-log.txt")
timestamp = datetime.now().isoformat()
command = tool_input.get("command", "")
description = tool_input.get("description", "")

with open(log_file, "a") as f:
    f.write(f"{timestamp} | {command} | {description}\n")
```

### 10. File Change Tracking

**Problem:** Track all file modifications.

```python
import json
from datetime import datetime
from pathlib import Path

log_file = Path.home() / ".claude" / "file-changes.jsonl"

entry = {
    "timestamp": datetime.now().isoformat(),
    "tool": tool_name,
    "file": tool_input.get("file_path", ""),
    "session": data.get("session_id", ""),
}

with open(log_file, "a") as f:
    f.write(json.dumps(entry) + "\n")
```

---

## Context Patterns

### 11. Session Context Loading

**Problem:** Load project context at session start.

```bash
#!/bin/bash
set -euo pipefail

# Project info
echo "=== Project Context ==="
echo "Directory: $CLAUDE_PROJECT_DIR"
echo "Name: $(basename "$CLAUDE_PROJECT_DIR")"

# Git info
if [ -d .git ]; then
    echo "Branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --format='%s' 2>/dev/null || echo 'N/A')"
fi

# Package info
if [ -f package.json ]; then
    echo "Node project: $(jq -r '.name // "unnamed"' package.json)"
fi

# Environment
echo "Node: $(node -v 2>/dev/null || echo 'N/A')"
echo "Python: $(python3 --version 2>/dev/null || echo 'N/A')"
```

### 12. Prompt Context Injection

**Problem:** Add context to user prompts.

```python
context_parts = []

# Time context
from datetime import datetime
context_parts.append(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Git context
import subprocess
try:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        stderr=subprocess.DEVNULL
    ).decode().strip()
    context_parts.append(f"Git branch: {branch}")
except:
    pass

# Output context (added to prompt)
print("\n".join(context_parts))
sys.exit(0)
```

---

## Flow Control Patterns

### 13. Prevent Premature Exit

**Problem:** Ensure Claude completes all tasks before stopping.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Before stopping, verify:\n1. All requested tasks completed\n2. No errors remain\n3. Code compiles/runs\n\nRespond {\"ok\": true} to stop, or {\"ok\": false, \"reason\": \"...\"} to continue."
          }
        ]
      }
    ]
  }
}
```

### 14. Iteration Loop (Ralph Loop Pattern)

**Problem:** Keep Claude working through iterations.

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
STATE_FILE=".claude/loop-state.json"

if [[ ! -f "$STATE_FILE" ]]; then
    exit 0  # No active loop
fi

ITERATION=$(jq -r '.iteration' "$STATE_FILE")
MAX=$(jq -r '.max_iterations' "$STATE_FILE")

if [[ $ITERATION -ge $MAX ]]; then
    rm "$STATE_FILE"
    exit 0  # Loop complete
fi

# Continue loop
NEW_ITERATION=$((ITERATION + 1))
jq ".iteration = $NEW_ITERATION" "$STATE_FILE" > "$STATE_FILE.tmp"
mv "$STATE_FILE.tmp" "$STATE_FILE"

PROMPT=$(jq -r '.prompt' "$STATE_FILE")

jq -n \
    --arg prompt "$PROMPT" \
    --arg msg "Iteration $NEW_ITERATION/$MAX" \
    '{
        "decision": "block",
        "reason": $prompt,
        "systemMessage": $msg
    }'
```

---

## MCP Tool Patterns

### 15. MCP Operation Logging

**Problem:** Log all MCP tool operations.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"MCP: \\(.tool_name)\"' >> ~/.claude/mcp-operations.log"
          }
        ]
      }
    ]
  }
}
```

### 16. MCP Write Protection

**Problem:** Validate MCP write operations.

```python
tool_name = data.get("tool_name", "")

if tool_name.startswith("mcp__") and "write" in tool_name.lower():
    # Require confirmation for MCP writes
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "MCP write operation requires confirmation"
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

---

## Validation Patterns

### 17. JSON Validation

**Problem:** Validate JSON files before writing.

```python
import json

if tool_name == "Write" and file_path.endswith(".json"):
    content = tool_input.get("content", "")
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
```

### 18. TypeScript Validation

**Problem:** Type-check TypeScript before allowing edits.

```bash
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$FILE_PATH" =~ \.tsx?$ ]]; then
    # Run type check (non-blocking warning)
    npx tsc --noEmit "$FILE_PATH" 2>&1 || true
fi

exit 0
```

---

## Notification Patterns

### 19. Desktop Notifications

**Problem:** Alert user when Claude needs attention.

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude needs attention"')

# Cross-platform notification
if command -v notify-send &>/dev/null; then
    # Linux
    notify-send "Claude Code" "$MESSAGE"
elif command -v osascript &>/dev/null; then
    # macOS
    osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\""
elif command -v powershell.exe &>/dev/null; then
    # Windows (WSL)
    powershell.exe -Command "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > \$null; \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText01); \$template.GetElementsByTagName('text').Item(0).AppendChild(\$template.CreateTextNode('$MESSAGE')); [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show([Windows.UI.Notifications.ToastNotification]::new(\$template))"
fi

exit 0
```

### 20. Slack Notification

**Problem:** Send notifications to Slack.

```python
import json
import os
import urllib.request

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "")

if SLACK_WEBHOOK:
    message = data.get("message", "Claude Code notification")
    payload = json.dumps({"text": f":robot_face: {message}"})

    req = urllib.request.Request(
        SLACK_WEBHOOK,
        data=payload.encode(),
        headers={"Content-Type": "application/json"}
    )

    try:
        urllib.request.urlopen(req, timeout=5)
    except:
        pass
```
