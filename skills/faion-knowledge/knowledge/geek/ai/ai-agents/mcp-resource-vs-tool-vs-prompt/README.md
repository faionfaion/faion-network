# MCP — Resource vs Tool vs Prompt: The Three-Question Test

**Category:** `mcp-` (Model Context Protocol)

## The Rule

When designing an MCP server, classify every capability as exactly one of:

- **Tool** — model invokes it to perform an action that has a side effect or returns dynamic computation
- **Resource** — content the model reads on demand; static or semi-static; deterministic per URI
- **Prompt** — a parameterized prompt template the user/host can invoke

Use the three-question test to pick:

1. Does the model need to **act** (mutate, fetch live, run)? → **Tool**
2. Is this **content the model reads** as if it were a file or web page? → **Resource**
3. Is this a **prompt the user invokes** (slash command shape)? → **Prompt**

Picking the wrong type is the most common MCP-server design mistake.

## Why It Works

The three primitives have different interaction contracts:

| Primitive | Triggered by | Returned to | Side effects? |
|-----------|--------------|-------------|---------------|
| Tool | Model decides during a turn | Model context | Allowed |
| Resource | Model decides during a turn (or host pre-injects) | Model context | None |
| Prompt | Host/user (slash menu) | Model context | None |

Misclassification consequences:
- "Tool that always returns the same large content" → bloats every turn the model decides to call it; should be a Resource
- "Resource that mutates state when accessed" → model can't reason about idempotency; should be a Tool
- "Tool meant to be invoked by the user" → never gets called by the model; should be a Prompt

## Decision Examples

| Capability | Right type | Why |
|------------|------------|-----|
| `search_docs(query)` | Tool | Dynamic; query parameterized; returns search results |
| `docs://api/auth` | Resource | Static page; deterministic by URI |
| `/onboard-new-engineer` (with args) | Prompt | User-invoked, parameterized template |
| `read_file(path)` | Tool | Dynamic; many possible paths |
| `file:///workspace/README.md` | Resource | One specific URI; deterministic |
| `apply_migration(name)` | Tool | Mutates state |
| `runbook://incident-database-down` | Resource | Static playbook content |

## When To Use Each

### Tool
- Live data fetch (DB query, API call, search)
- Mutating actions (write file, send message, deploy)
- Computation parameterized by user/model input
- Anything where args matter

### Resource
- Documentation pages, schemas, runbooks
- Codebase manifests, file contents
- Per-URI deterministic content
- Things the model should be ABLE to read but doesn't always need

### Prompt
- Slash commands the user wants to invoke
- Parameterized prompt templates ("Investigate ticket {ticket_id}")
- Onboarding wizards
- Multi-step interaction starters

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| `get_thing()` tool that always returns the same content | Convert to a Resource at a URI |
| `documentation` resource that requires server roundtrip per word | Bundle into a single resource or use search_docs Tool |
| Tools that the host expects users to invoke directly | Add a Prompt template that calls the Tool |
| Cramming three capabilities into one tool with a `mode` arg | Split into three tools (or tool + resource + prompt) |

## Composition

- + **tool-description-as-prompt**: each tool's description is the model's deciding factor
- + **subagent-as-context-firewall**: subagent might use Resources to load only what's needed
- + **prompt-cache-prefix-order**: tool definitions are part of the cached prefix; descriptions are amortized

## Cross-Runtime Parity

| Runtime | Tools | Resources | Prompts |
|---------|-------|-----------|---------|
| Anthropic MCP | ✅ | ✅ | ✅ |
| OpenAI Responses API + MCP | ✅ | ✅ (read-side) | partial |
| Vercel AI SDK 6 | ✅ | mapped via fetcher | mapped via system |
| LangChain MCP adapter | ✅ | ✅ | ✅ |

If you intend cross-runtime portability, design assuming all three exist; the runtime that doesn't support Prompts will collapse them to system messages.

## References

- [MCP Specification — primitives](https://modelcontextprotocol.io/docs/concepts/architecture)
- [Anthropic — Building MCP servers](https://docs.anthropic.com/claude/docs/mcp-servers)
- [Claude Code MCP integration](https://docs.anthropic.com/en/docs/claude-code/mcp)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
