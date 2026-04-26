# Templates — Tool Description as Prompt

## Anthropic tool definition

```python
tools = [
    {
        "name": "search_docs",
        "description": (
            "Search the indexed documentation for passages matching a query. "
            "Use this when the user asks a how-to or reference question and you don't already have the answer. "
            "Do NOT use this for code search — use `grep_repo` instead. "
            "Returns up to 10 passages ranked by relevance; each includes title, path, and a 200-char excerpt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language question."},
                "max_results": {"type": "integer", "default": 10, "description": "1-50."},
            },
            "required": ["query"],
        },
    },
]
```

## OpenAI tool definition

```python
tools = [{
    "type": "function",
    "function": {
        "name": "create_pr",
        "description": (
            "Create a pull request from the current working branch. "
            "Use this when the user has finalized changes and wants them on the remote. "
            "Do NOT use this if the working tree is dirty (run `git_status` first). "
            "Side effect: pushes branch and opens a PR on GitHub. Returns the PR URL."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["title"],
        },
    },
}]
```

## MCP tool description

```python
@mcp.tool()
def query_warehouse(sql: str) -> list[dict]:
    """
    Execute a read-only SQL query against the warehouse.

    Use this when the user asks for analytics that require SQL.
    Do NOT use this for transactional or write operations.
    Returns up to 1000 rows; truncate with LIMIT if larger sets are needed.

    Side effect: none (read-only, sandboxed read-replica).
    Latency: 1-30s depending on query.
    """
    ...
```

The docstring becomes the tool description. Keep human-doc and LLM-doc aligned.

## Pattern: tool family with anti-triggers

```python
read_file = {
    "name": "read_file",
    "description": (
        "Read a file's contents from the local repo. "
        "Use this when you need to inspect specific code/text. "
        "Do NOT use this for searching across files — use `grep_repo`. "
        "Do NOT use this on files larger than 50KB without `offset`/`limit`."
    ),
}

grep_repo = {
    "name": "grep_repo",
    "description": (
        "Search the repository for a regex pattern. "
        "Use this when you need to find where something appears across many files. "
        "Do NOT use this if you already know the file path — use `read_file`. "
        "Returns matches grouped by file, max 200 lines."
    ),
}
```

The mutual `do NOT use this when` lines collapse the misuse rate to ~zero.

## Pattern: side-effect tools

```python
{
    "name": "apply_patch",
    "description": (
        "MUTATING: Apply a unified-diff patch to the repo. "
        "Use this AFTER you have validated the patch with `dry_run_patch`. "
        "Do NOT use this on a dirty working tree. "
        "Returns: {applied: bool, conflicts: list[str]}."
    ),
}
```

## Pattern: pagination

```python
{
    "name": "list_issues",
    "description": (
        "List GitHub issues in the current repo. "
        "Use this to find context for a bug fix or feature. "
        "Returns 30 per page; pass `cursor` from the previous response to paginate. "
        "Do NOT loop more than 5 pages — narrow the query if you need more."
    ),
}
```
