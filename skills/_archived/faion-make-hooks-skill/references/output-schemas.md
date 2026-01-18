# Hook Output Schemas Reference

## Exit Codes

| Code | Type | Behavior |
|------|------|----------|
| **0** | Success | stdout parsed for JSON, or added as context |
| **2** | Blocking error | stderr shown to user, tool blocked (PreToolUse) |
| **1, 3+** | Non-blocking error | stderr shown in verbose mode only |

---

## PreToolUse Output

### Simple Block (Exit Code 2)

```bash
echo "Operation not allowed: dangerous command" >&2
exit 2
```

### Simple Allow (Exit Code 0)

```bash
exit 0
```

### JSON Output: Auto-Approve

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Documentation file auto-approved"
  },
  "suppressOutput": true
}
```

### JSON Output: Deny

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Protected file cannot be modified"
  }
}
```

### JSON Output: Ask User

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Sensitive operation requires confirmation"
  }
}
```

### JSON Output: Modify Input

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "npm test -- --coverage"
    }
  }
}
```

### JSON Output: Add Context

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Note: This file follows ESLint rules. Use 2-space indentation."
  }
}
```

### Full Schema

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string",
    "updatedInput": {},
    "additionalContext": "string"
  },
  "continue": true,
  "stopReason": "string",
  "suppressOutput": false,
  "systemMessage": "string"
}
```

---

## PostToolUse Output

### Simple Success

```bash
exit 0
```

### Block Further Processing

```json
{
  "decision": "block",
  "reason": "Linter found errors that must be fixed"
}
```

### Add Context

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "File formatted with Prettier"
  }
}
```

---

## PermissionRequest Output

### Allow

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "message": "Auto-approved by hook"
    }
  }
}
```

### Deny

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Operation blocked by security policy",
      "interrupt": false
    }
  }
}
```

### Allow with Modified Input

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm test --silent"
      }
    }
  }
}
```

---

## UserPromptSubmit Output

### Simple Context (Plain Text)

```bash
echo "Current branch: main"
echo "Last commit: abc123"
exit 0
```

### Block Prompt

```json
{
  "decision": "block",
  "reason": "Prompt contains potential secrets or sensitive information"
}
```

### Add Context (JSON)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "User is working on feature branch 'feature/auth'"
  }
}
```

---

## Stop / SubagentStop Output

### Allow Stop

```bash
exit 0
```

Or:

```json
{
  "decision": "allow"
}
```

### Block Stop (Continue Working)

```json
{
  "decision": "block",
  "reason": "Tests are still failing. Please fix the remaining errors."
}
```

### Block with System Message

```json
{
  "decision": "block",
  "reason": "Continue working on the task",
  "systemMessage": "Iteration 3/10 - Task not complete"
}
```

---

## SessionStart Output

### Add Context (Plain Text)

```bash
echo "Project: my-app"
echo "Environment: development"
echo "Node.js: $(node -v)"
exit 0
```

### Add Context (JSON)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "This is a TypeScript project using React 18 and Next.js 14"
  }
}
```

### Persist Environment Variables

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=true' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

---

## SessionEnd Output

### Simple Cleanup

```bash
# Log session end
echo "$(date): Session ended" >> ~/.claude/session-log.txt
exit 0
```

---

## Notification Output

### Custom Notification

```bash
# Send to system notification
notify-send "Claude Code" "Task requires attention"
exit 0
```

---

## PreCompact Output

### Simple Allow

```bash
exit 0
```

### Add Pre-Compaction Context

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreCompact",
    "additionalContext": "Important: Remember to complete the auth feature"
  }
}
```

---

## Prompt-Based Hook Output

For `type: "prompt"` hooks:

### Allow

```json
{
  "ok": true
}
```

### Block with Reason

```json
{
  "ok": false,
  "reason": "Tests are still failing. Continue debugging."
}
```

---

## Common Output Fields

All hooks can include these top-level fields:

```json
{
  "continue": true,
  "stopReason": "Message when continue=false",
  "suppressOutput": false,
  "systemMessage": "Warning message shown to user"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `continue` | boolean | `false` to stop Claude completely |
| `stopReason` | string | Message when stopping |
| `suppressOutput` | boolean | Hide stdout from transcript |
| `systemMessage` | string | Warning/info shown to user |

---

## Output in Different Languages

### Python

```python
import json
import sys

# Simple block
print("Error message", file=sys.stderr)
sys.exit(2)

# JSON output
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}
print(json.dumps(output))
sys.exit(0)
```

### Bash

```bash
# Simple block
echo "Error message" >&2
exit 2

# JSON output
jq -n '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  }
}'
exit 0
```

### Node.js

```javascript
// Simple block
console.error("Error message");
process.exit(2);

// JSON output
console.log(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "allow"
  }
}));
process.exit(0);
```
