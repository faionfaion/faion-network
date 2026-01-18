# Hook Templates Reference

Ready-to-use templates for common hook scenarios.

---

## Python Templates

### PreToolUse: File Protection

```python
#!/usr/bin/env python3
"""Block modifications to protected files."""

import json
import sys

PROTECTED_PATTERNS = [
    ".env",
    ".git/",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "secrets/",
    "credentials",
    ".pem",
    ".key",
]

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    for pattern in PROTECTED_PATTERNS:
        if pattern in file_path:
            print(f"Protected file: {file_path}", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### PreToolUse: Auto-Approve Safe Operations

```python
#!/usr/bin/env python3
"""Auto-approve safe read operations."""

import json
import sys

SAFE_EXTENSIONS = [".md", ".txt", ".json", ".yaml", ".yml", ".toml"]

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name != "Read":
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    if any(file_path.endswith(ext) for ext in SAFE_EXTENSIONS):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": f"Auto-approved: safe file type"
            },
            "suppressOutput": True
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### PreToolUse: Command Validation

```python
#!/usr/bin/env python3
"""Validate bash commands for dangerous patterns."""

import json
import re
import sys

BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+~",
    r"rm\s+-rf\s+\*",
    r"sudo\s+rm",
    r"chmod\s+777",
    r">\s*/dev/sd",
    r"mkfs\.",
    r"dd\s+if=",
    r":(){:|:&};:",  # Fork bomb
]

WARNED_PATTERNS = [
    (r"\bgrep\b(?!.*\|)", "Consider using 'rg' instead of 'grep'"),
    (r"\bfind\s+\S+\s+-name\b", "Consider using 'fd' or 'rg --files'"),
    (r"\bcat\s+\S+\s*\|", "Consider reading file directly"),
]

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")

    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            print(f"Dangerous command blocked: {command}", file=sys.stderr)
            sys.exit(2)

    # Check warned patterns
    warnings = []
    for pattern, message in WARNED_PATTERNS:
        if re.search(pattern, command):
            warnings.append(message)

    if warnings:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": "Suggestions: " + "; ".join(warnings)
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### PostToolUse: Auto-Format Code

```python
#!/usr/bin/env python3
"""Auto-format files after editing."""

import json
import subprocess
import sys
from pathlib import Path

FORMATTERS = {
    ".ts": ["npx", "prettier", "--write"],
    ".tsx": ["npx", "prettier", "--write"],
    ".js": ["npx", "prettier", "--write"],
    ".jsx": ["npx", "prettier", "--write"],
    ".json": ["npx", "prettier", "--write"],
    ".py": ["black"],
    ".rs": ["rustfmt"],
    ".go": ["gofmt", "-w"],
}

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_response = data.get("tool_response", {})

    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    if not tool_response.get("success", False):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    suffix = Path(file_path).suffix

    if suffix in FORMATTERS:
        formatter = FORMATTERS[suffix] + [file_path]
        try:
            subprocess.run(formatter, capture_output=True, timeout=30)
        except Exception:
            pass  # Silently ignore formatting errors

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### UserPromptSubmit: Add Project Context

```python
#!/usr/bin/env python3
"""Add project context to prompts."""

import json
import os
import subprocess
import sys

def get_git_info():
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"Git branch: {branch}"
    except Exception:
        return None

def get_node_version():
    try:
        version = subprocess.check_output(
            ["node", "-v"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"Node.js: {version}"
    except Exception:
        return None

def main():
    context_parts = []

    # Project directory
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    context_parts.append(f"Project: {os.path.basename(project_dir)}")

    # Git info
    git_info = get_git_info()
    if git_info:
        context_parts.append(git_info)

    # Node version
    node_version = get_node_version()
    if node_version:
        context_parts.append(node_version)

    if context_parts:
        print("\n".join(context_parts))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Stop: Task Completion Check

```python
#!/usr/bin/env python3
"""Prevent premature exit if tasks incomplete."""

import json
import sys

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Check if already continuing from previous Stop
    if data.get("stop_hook_active", False):
        sys.exit(0)

    # Read transcript to check for incomplete tasks
    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    try:
        with open(transcript_path, 'r') as f:
            content = f.read()

        # Check for TODO markers or error indicators
        incomplete_markers = [
            "TODO:",
            "FIXME:",
            "Error:",
            "Failed:",
            "test failed",
        ]

        # Look in last 5000 characters
        recent = content[-5000:]
        for marker in incomplete_markers:
            if marker.lower() in recent.lower():
                output = {
                    "decision": "block",
                    "reason": f"Found incomplete work indicator: '{marker}'"
                }
                print(json.dumps(output))
                sys.exit(0)

    except Exception:
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Bash Templates

### PreToolUse: Simple Command Logger

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] $COMMAND" >> ~/.claude/command-log.txt
fi

exit 0
```

### PreToolUse: Block rm -rf

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" != "Bash" ]]; then
    exit 0
fi

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/|~|\*)'; then
    echo "Blocked: Dangerous rm command" >&2
    exit 2
fi

exit 0
```

### PostToolUse: Run Prettier

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx|json)$ ]]; then
    npx prettier --write "$FILE_PATH" 2>/dev/null || true
fi

exit 0
```

### SessionStart: Load Environment

```bash
#!/bin/bash
set -euo pipefail

# Print context (added to conversation)
echo "Project: $(basename "$CLAUDE_PROJECT_DIR")"
echo "Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')"
echo "Time: $(date '+%Y-%m-%d %H:%M')"

# Persist environment variables
if [[ -n "${CLAUDE_ENV_FILE:-}" ]]; then
    echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

### Notification: Desktop Alert

```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude needs attention"')

# Linux
if command -v notify-send &>/dev/null; then
    notify-send "Claude Code" "$MESSAGE"
# macOS
elif command -v osascript &>/dev/null; then
    osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\""
fi

exit 0
```

---

## Configuration Templates

### Full hooks.json for Plugin

```json
{
  "description": "My Custom Hooks Plugin",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-command.py",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/protect-files.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.py",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
            "timeout": 15
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all requested tasks are complete. Respond {\"ok\": true} to stop, or {\"ok\": false, \"reason\": \"explanation\"} to continue.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### settings.json Project Hooks

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-command.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} npx prettier --write {}"
          }
        ]
      }
    ]
  }
}
```

### Component Frontmatter (Skill/Agent)

```yaml
---
name: secure-developer
description: Development with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/protect-secrets.py"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
  Stop:
    - hooks:
        - type: prompt
          prompt: "Verify all security checks passed before stopping."
  once: true
---
```
