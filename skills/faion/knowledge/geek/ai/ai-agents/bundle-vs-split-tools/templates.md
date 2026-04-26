# Templates — Bundle vs Split Tools

## Split (default, <25 tools)

```python
tools = [
    {"name": "search_docs", "description": "...", "input_schema": {...}},
    {"name": "read_file",   "description": "...", "input_schema": {...}},
    {"name": "grep_repo",   "description": "...", "input_schema": {...}},
    {"name": "apply_patch", "description": "...", "input_schema": {...}},
    {"name": "run_tests",   "description": "...", "input_schema": {...}},
]
```

## Bundle by audience (when > 25 split tools)

```python
{
    "name": "file_ops",
    "description": (
        "File system operations on the workspace. "
        "Use mode='list' to enumerate, 'read' to fetch, 'write' to create/update, 'delete' to remove. "
        "ALL modes take `path` (relative to repo root). 'write' also takes `content`."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "mode": {"type": "string", "enum": ["list", "read", "write", "delete"]},
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["mode", "path"],
    }
}
```

## Bundle with per-mode descriptions

```python
{
    "name": "git_ops",
    "description": (
        "Git operations on the local repo.\n\n"
        "modes:\n"
        "  status       — show working tree status (no args)\n"
        "  diff         — show unstaged diff (optional `path`)\n"
        "  log          — show recent commits (optional `n`, default 10)\n"
        "  branch_list  — list local branches\n"
        "Do NOT use this for remote operations — use github_ops."
    ),
    "input_schema": {...}
}
```

## Anti-template — too-broad bundle

```python
# BAD — different audiences in one tool
{
    "name": "exec",
    "input_schema": {
        "properties": {
            "mode": {"enum": ["git", "npm", "docker", "http", "filesystem"]},
            "subcommand": {"type": "string"},
            "args": {"type": "array"}
        }
    }
}
```

The model has to mentally split this 5-way every call. Symptom: tool-selection latency rises; arg-fill errors rise.

Fix: split into 5 tools.

## Pattern: Resource for read-only bundles

If your bundle is mostly read-only:

```python
# Don't:
file_ops(mode="read", path="docs/api.md")

# Do:
@server.resource("file:///workspace/{path}")
async def read_file(path): ...
```

The model loads it as a Resource, freeing a tool slot.

## Pattern: explicit "mode" enum vs inferred

```python
# GOOD — enum makes valid values explicit
"mode": {"type": "string", "enum": ["list", "read", "write", "delete"]}

# BAD — model can invent invalid modes
"mode": {"type": "string"}
```

## Decision matrix

```
| Tool group       | Audience    | Shared args? | Bundle? |
|------------------|-------------|--------------|---------|
| {list, read, write, delete} files | filesystem | path | yes |
| {git_status, git_diff, git_log} | git | none | yes (still small audience) |
| {http_get, db_query, redis_get} | mixed | none | NO — split |
```
