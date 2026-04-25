# Templates — MCP Resource vs Tool vs Prompt

## Python MCP SDK — all three primitives in one server

```python
from mcp.server import Server
from mcp.types import Tool, Resource, Prompt

server = Server("faion-mcp")

# --- Tool: dynamic action ---
@server.tool()
async def search_docs(query: str, max_results: int = 10) -> list[dict]:
    """
    Search the docs corpus for passages matching the query.

    Use this when the user asks a how-to or reference question.
    Do NOT use this for code search — use grep_repo instead.
    """
    return run_search(query, max_results)

# --- Resource: static-per-URI content ---
@server.resource("docs://{section}/{page}")
async def get_doc(section: str, page: str) -> str:
    return load_doc(section, page)

@server.list_resources()
async def list_resources():
    return [
        Resource(uri=f"docs://{s}/{p}", name=f"{s}/{p}", mime_type="text/markdown")
        for s, p in iter_doc_pages()
    ]

# --- Prompt: user-invoked template ---
@server.prompt()
async def onboard_engineer(seniority: str, focus_area: str) -> list[dict]:
    return [{
        "role": "user",
        "content": f"Onboard a {seniority} engineer focused on {focus_area}. "
                   "Read the architecture doc (docs://arch/overview), "
                   "list 5 starter tasks, and propose a 1-week plan."
    }]

if __name__ == "__main__":
    server.run()
```

## TypeScript MCP SDK

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";

const server = new Server({ name: "faion-mcp", version: "1.0.0" });

server.setRequestHandler("tools/call", async (req) => {
    if (req.params.name === "search_docs") {
        return { content: await searchDocs(req.params.arguments) };
    }
});

server.setRequestHandler("resources/read", async (req) => {
    return { contents: [{ uri: req.params.uri, text: await loadDoc(req.params.uri) }] };
});

server.setRequestHandler("prompts/get", async (req) => {
    if (req.params.name === "onboard_engineer") {
        return { messages: [{ role: "user", content: { type: "text", text: makeOnboardingPrompt(req.params.arguments) } }] };
    }
});
```

## Decision matrix template

```
| Capability         | Side effect? | Static-per-URI? | User invokes? | Type     |
|--------------------|--------------|-----------------|---------------|----------|
| search_docs(q)     | no           | no              | no            | Tool     |
| docs://api/auth    | no           | yes             | no            | Resource |
| /investigate(id)   | no           | no              | yes           | Prompt   |
| apply_migration()  | yes          | n/a             | no            | Tool     |
```

Run this on every capability before implementing.

## Pattern: Resource with content negotiation

```python
@server.resource("schema://{type}.{format}")
async def get_schema(type: str, format: str) -> tuple[str, str]:
    if format == "json":
        return (json.dumps(SCHEMAS[type]), "application/json")
    if format == "ts":
        return (to_typescript(SCHEMAS[type]), "text/typescript")
    raise ResourceNotFound()
```

## Pattern: Prompt that composes Tools and Resources

```python
@server.prompt()
async def review_pr(pr_number: int) -> list[dict]:
    return [
        {"role": "user", "content": (
            f"Review PR #{pr_number}.\n\n"
            f"1. Read the diff via `get_pr_diff(pr_number={pr_number})`.\n"
            f"2. Read the architecture doc at docs://arch/overview.\n"
            f"3. Output a structured review."
        )}
    ]
```

This is a Prompt, not a Tool — it's the user's slash command. It mentions Tools and Resources by name; the model takes it from there.
