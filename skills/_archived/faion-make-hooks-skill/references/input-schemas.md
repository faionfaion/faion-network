# Hook Input Schemas Reference

## Common Fields (All Hooks)

Every hook receives these fields via stdin JSON:

```json
{
  "session_id": "string",
  "transcript_path": "/absolute/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse|PostToolUse|Stop|..."
}
```

---

## PreToolUse Input

### Bash Tool

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/sessions/abc123.jsonl",
  "cwd": "/home/user/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run unit tests",
    "timeout": 120000,
    "run_in_background": false
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Write Tool

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/absolute/path/to/file.ts",
    "content": "const hello = 'world';\nexport default hello;"
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Edit Tool

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/absolute/path/to/file.ts",
    "old_string": "const hello = 'world';",
    "new_string": "const greeting = 'hello world';",
    "replace_all": false
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Read Tool

```json
{
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/absolute/path/to/file.ts",
    "offset": 0,
    "limit": 2000
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Glob Tool

```json
{
  "tool_name": "Glob",
  "tool_input": {
    "pattern": "**/*.ts",
    "path": "/home/user/project/src"
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Grep Tool

```json
{
  "tool_name": "Grep",
  "tool_input": {
    "pattern": "function\\s+\\w+",
    "path": "/home/user/project/src",
    "glob": "*.ts",
    "output_mode": "content",
    "-n": true,
    "-C": 3
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Task Tool (Subagent)

```json
{
  "tool_name": "Task",
  "tool_input": {
    "description": "Research API patterns",
    "prompt": "Find all API endpoints in the codebase...",
    "subagent_type": "Explore",
    "model": "sonnet"
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### WebFetch Tool

```json
{
  "tool_name": "WebFetch",
  "tool_input": {
    "url": "https://example.com/api/docs",
    "prompt": "Extract API endpoints"
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### WebSearch Tool

```json
{
  "tool_name": "WebSearch",
  "tool_input": {
    "query": "React hooks best practices 2026",
    "allowed_domains": ["react.dev", "github.com"],
    "blocked_domains": []
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### MCP Tools

```json
{
  "tool_name": "mcp__memory__store",
  "tool_input": {
    "key": "user_preference",
    "value": "dark_mode"
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

---

## PostToolUse Input

Same as PreToolUse, plus `tool_response`:

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "..."
  },
  "tool_response": {
    "filePath": "/path/to/file.ts",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123XYZ"
}
```

### Common tool_response Formats

**Write/Edit:**
```json
{
  "filePath": "/path/to/file.ts",
  "success": true
}
```

**Read:**
```json
{
  "content": "file content...",
  "truncated": false
}
```

**Bash:**
```json
{
  "stdout": "command output",
  "stderr": "",
  "exitCode": 0
}
```

**Glob:**
```json
{
  "files": ["/path/file1.ts", "/path/file2.ts"]
}
```

---

## UserPromptSubmit Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Help me write a function that calculates fibonacci numbers"
}
```

---

## Stop / SubagentStop Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

`stop_hook_active`: `true` if already continuing from a previous Stop hook block.

---

## SessionStart Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

**Environment variable (SessionStart only):**
- `CLAUDE_ENV_FILE`: Path to file for persisting environment variables

---

## SessionEnd Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|other"
}
```

---

## Notification Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "hook_event_name": "Notification",
  "message": "Notification message",
  "type": "info|warning|error"
}
```

---

## PreCompact Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "hook_event_name": "PreCompact",
  "source": "manual|auto"
}
```

---

## PermissionRequest Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies"
  },
  "permission_type": "tool_use"
}
```

---

## Parsing Input in Scripts

### Python

```python
import json
import sys

data = json.load(sys.stdin)
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
```

### Bash

```bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
```

### Node.js

```javascript
const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
const { tool_name, tool_input } = data;
```
