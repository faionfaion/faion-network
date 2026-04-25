# AGENT-09 — MCP + Tool-Use Design Patterns

**Summary (2 lines):** MCP tools are not API wrappers — they are a typed prompt surface where the
schema, name, description, and error format collectively program the agent's loop. Naming, output
terseness, idempotency, and the right primitive choice (tool vs resource vs prompt) decide whether
the agent succeeds or thrashes.

Scope: April 2026 state of MCP (spec rev `2025-11-25`, protocol rev `2026-03-26`), Anthropic Claude
tool use, OpenAI Responses API hosted tools, and Vercel AI SDK 6. 10 methodologies, mapped to
`tu-` (tool-use) and `mcp-` (Model Context Protocol).

---

## tu-01 — Choose the right MCP primitive: tool vs resource vs prompt

**Rule:** If it has side effects → **tool** (model-controlled). If it is read-only background
context → **resource** (app-controlled). If it is a reusable workflow the user explicitly invokes →
**prompt** (user-controlled). Never expose `read_user_profile` as a tool when a `users://{id}`
resource already gives the host control over context injection.

**Cite:**
- https://modelcontextprotocol.io/specification/2025-11-25
- https://techcommunity.microsoft.com/blog/azuredevcommunityblog/mcp-demystified-tools-vs-resources-vs-prompts-explained-simply/4508057
- https://exotechnologies.xyz/research/mcp-tools-resources-prompts

**When to use:** Any new MCP server design. Apply the three-question test:
1. Side effects? → tool
2. Should the model decide when to invoke? → tool; if the host decides → resource
3. Should it surface as a slash command? → prompt

**When NOT to use:** Don't make everything a tool just because the SDK ships `@server.tool()` first.
Tools cost tokens in the schema list every turn; resources only cost tokens when read.

**Tiny example:**
```python
# FastMCP — three primitives, one server
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("github")

@mcp.resource("repo://{owner}/{name}/readme")  # read-only, host-controlled
def readme(owner: str, name: str) -> str: ...

@mcp.tool()  # side effect, model-controlled
def create_issue(repo: str, title: str, body: str) -> dict: ...

@mcp.prompt()  # user-controlled (slash command in Claude Desktop)
def review_pr(pr_url: str) -> list[Message]: ...
```

---

## tu-02 — Tool name = `verb_object`, prefixed by namespace

**Rule:** Tool names matter MORE than descriptions for selection accuracy. Use `verb_object`
(`create_issue`, `search_files`) and prefix with a service namespace (`asana_search_tasks`,
`jira_search_tickets`) when multiple servers expose similar verbs. Anthropic confirmed prefix
schemes meaningfully change selection accuracy and recommend tuning by eval.

**Cite:**
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools

**When to use:** Any tool catalog ≥ 5 tools, especially across multiple MCP servers. Always namespace
when running through an MCP gateway/aggregator (collisions are common).

**When NOT to use:** Single-server hobby projects where there's only ever one `search`. Don't
over-engineer with `acme_corp_internal_v2_search_documents_advanced`.

**Tiny example:**
```jsonc
// BAD — ambiguous, collides with other servers
{ "name": "search" }
{ "name": "manage" }   // does what?

// GOOD — verb_object, namespaced
{ "name": "github_search_issues" }
{ "name": "github_create_issue" }
{ "name": "github_close_issue" }
```

---

## tu-03 — Tool description IS the prompt (zero-shot teaching)

**Rule:** Treat the description like onboarding docs for a new hire. State (a) what the tool does,
(b) WHEN to use it vs sibling tools, (c) input format and edge cases, (d) example call. Anthropic's
SWE-bench SOTA jump came from description refinement, not model changes.

**Cite:**
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/engineering/advanced-tool-use

**When to use:** Every tool, every time. Re-run agent evals after each description tweak — small
edits produce outsized swings.

**When NOT to use:** No exceptions. Even a one-liner description should answer "what + when".

**Tiny example:**
```jsonc
// BAD
{ "description": "Searches files." }

// GOOD — what, when, input format, boundary
{ "description": "Search the user's repository for files whose CONTENTS match `query` (regex). Use this when the user asks 'where is X defined' or 'find all usages of Y'. Do NOT use to list directory contents — use `list_files` for that. `query` must be a valid Python regex; escape literal '.' as '\\.'. Returns up to 50 matches with file path, line number, and 2-line context. Example: query='def parse_url'." }
```

---

## tu-04 — Split tools by responsibility; use toolkits for grouping

**Rule:** One tool = one verb on one resource. Replace `manage_files(action, src, dst)` with
`copy_file`, `move_file`, `delete_file`. But: if the catalog blows past ~25 tools, group into
toolkits and load lazily — 35 schemas already burn 3k+ tokens per turn, and selection accuracy
collapses.

**Cite:**
- https://composio.dev/blog/how-to-build-tools-for-ai-agents-a-field-guide
- https://medium.com/cloud-experts-hub/guide-to-agent-granularity-94e7e42ae23d

**When to use:** Default. Atomic tools debug better, fail more predictably, and produce cleaner
trajectories.

**When NOT to use:** When the underlying API only supports a transactional batch (e.g., a single
`update_record` that must atomically set 5 fields). In that case, expose ONE tool with
discriminated-union params — never a polymorphic action enum.

**Tiny example:**
```python
# BAD — agent must guess which fields each `action` needs
@tool
def manage_user(action: str, user_id: str, **kwargs) -> dict: ...

# GOOD — atomic, typed, self-documenting
@tool
def get_user(user_id: str) -> User: ...
@tool
def update_user_email(user_id: str, email: str) -> User: ...
@tool
def deactivate_user(user_id: str, reason: str) -> User: ...
```

---

## tu-05 — Idempotency keys + dry-run/apply pairs for any side effect

**Rule:** Every write tool must (a) accept an `idempotency_key`, (b) be safe to re-run with the same
key, and (c) ship as a `*_preview` + `*_apply` pair when the side effect is destructive or expensive.
Tools time out, networks flake, agents retry — un-keyed writes silently double-charge.

**Cite:**
- https://achan2013.medium.com/ai-agent-anti-patterns-part-2-tooling-observability-and-scale-traps-in-enterprise-agents-42a451ea84ec
- https://www.devx.com/technology/scalable-ai-agents-10-design-patterns-that-matter/
- https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/

**When to use:** Anything mutating, especially: payments, emails, file deletes, infra changes,
DB writes, external API POSTs.

**When NOT to use:** Pure reads (`get_*`, `search_*`, `list_*`). Don't bloat their schemas with
unused keys.

**Tiny example:**
```jsonc
// Preview returns the diff, no side effect
{ "name": "deploy_preview",
  "input": { "service": "nero-core", "ref": "main" },
  "output": { "diff": "+2 -1 services...", "estimated_cost_usd": 0.04 } }

// Apply requires the preview's hash + idempotency key
{ "name": "deploy_apply",
  "input": { "preview_hash": "sha256:abc...", "idempotency_key": "deploy-2026-04-25-001" } }
```

---

## tu-06 — Tool output: terse default, structured-on-demand

**Rule:** Default to compact, semantic output (Markdown table, summary line, count + IDs). Add a
`verbosity: "low"|"medium"|"high"` or `format: "summary"|"full"` param so the agent can opt into
detail when reasoning needs it. SkillReducer showed 48% description / 39% body compression
improved task quality 2.8% — verbose context is distraction.

**Cite:**
- https://medium.com/@shamsul.arefin/building-an-ai-agent-with-mcp-code-execution-from-confusion-to-clarity-6b13fccc8c4b
- https://arxiv.org/html/2603.29919v1
- https://www.harness.io/blog/agent-loop-new-os

**When to use:** Any tool that can return >500 tokens. Especially `list_*`, `search_*`, log queries.

**When NOT to use:** Tools where every field is load-bearing (e.g., `get_payment_invoice` for
audit). Make terseness opt-in only when accuracy survives compression.

**Tiny example:**
```python
@tool
def search_logs(query: str, limit: int = 20, format: Literal["summary","full"] = "summary"):
    rows = es.search(query, size=limit)
    if format == "summary":
        # 1 line per hit, ~30 tokens total
        return "\n".join(f"{r.ts} [{r.level}] {r.msg[:80]}" for r in rows)
    return [r.dict() for r in rows]  # full JSON only when asked
```

---

## tu-07 — Tool errors are prompts: semantic code + recoveryHint

**Rule:** Never bubble raw stack traces. Return a structured error: `{code, message, recoveryHint,
traceId}` where `recoveryHint` ∈ `RETRY_LATER | CHECK_INPUT | TRY_ALTERNATIVE | REPORT_TO_USER |
NEEDS_AUTH`. The hint is a direct instruction to the LLM's next reasoning step.

**Cite:**
- https://medium.com/@kumaran.isk/llm-friendly-error-handling-designing-mcp-servers-for-ai-df427f6dfd2f
- https://arxiv.org/pdf/2508.07935  (SHIELDA)
- https://www.arunbaby.com/ai-agents/0033-error-handling-recovery/

**When to use:** Every error path of every tool. Treat error messages as part of the prompt
contract.

**When NOT to use:** Don't fabricate `recoveryHint` when the failure is genuinely unrecoverable —
use `REPORT_TO_USER` and stop the loop.

**Tiny example:**
```jsonc
// BAD
{ "error": "TypeError: NoneType has no attribute 'json' at line 42" }

// GOOD
{ "error": {
    "code": "UPSTREAM_RATE_LIMITED",
    "message": "GitHub API returned 429.",
    "recoveryHint": "RETRY_LATER",
    "retry_after_seconds": 60,
    "traceId": "01HX9...QF"
} }
```

---

## mcp-01 — Transport choice: stdio local, Streamable HTTP remote, SSE deprecated

**Rule:** Use **stdio** for local subprocess MCP servers (IDE, desktop). Use **Streamable HTTP**
(single endpoint, OAuth 2.1, resumable) for remote/multi-tenant. Treat **SSE** as deprecated
(removed-in-favor-of streamable HTTP since protocol rev 2026-03-26) — only support it when you must
back-compat an old client.

**Cite:**
- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- https://brightdata.com/blog/ai/sse-vs-streamable-http
- https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/

**When to use stdio:** Local-only, single-user, fast launch (Claude Desktop, Claude Code,
Cursor plugins).
**When to use Streamable HTTP:** Multi-user, hosted, behind an LB, needs OAuth, needs resumable
streams.

**When NOT to use stdio:** Any production multi-user deployment — stdio cannot horizontally scale.
**When NOT to use SSE:** Greenfield. Period.

**Tiny example:**
```python
# Local stdio
mcp.run(transport="stdio")

# Remote streamable HTTP (single endpoint /mcp, supports POST + SSE upgrade)
mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
```

---

## mcp-02 — MCP composition: gateway / virtual server / federation

**Rule:** When you have >5 MCP servers, put a gateway in front. Patterns: (a) **virtual server** —
gateway exposes a curated subset as one logical server; (b) **federation** — gateways consume
gateways in a tree; (c) **per-client visibility** — gateway filters tool list by user/role. IBM
ContextForge and similar (see Lunar/Maxim/TrueFoundry round-ups) are the 2026 production picks.

**Cite:**
- https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- https://www.heyitworks.tech/blog/mcp-aggregation-gateway-proxy-tools-q1-2026
- https://www.lunar.dev/post/the-best-open-source-mcp-gateways-in-2026

**When to use:** Enterprise / multi-tenant / multi-team setups. Gateways centralize auth, rate
limiting, audit, and namespace collision resolution.

**When NOT to use:** Solo dev or a single agent with 1–3 servers. The gateway is overhead, not value.

**Tiny example:**
```yaml
# ContextForge virtual server config — bundle 3 backends as one
virtual_servers:
  - name: dev_workspace
    expose:
      - github.create_issue
      - github.search_issues
      - linear.create_ticket
      - sentry.search_events
    deny: ["github.delete_*"]   # gateway-level safety
```

---

## mcp-03 — Multi-runtime parity: Anthropic, OpenAI Responses, Vercel AI SDK

**Rule:** Design tools as a single source of truth (Zod / Pydantic schema), then export adapters for
each runtime. The shapes are converging but NOT identical:
- **Anthropic Claude tool use** — `name`, `description`, `input_schema` (JSON Schema). Native MCP
  client in Claude Code / Claude Desktop / API.
- **OpenAI Responses API** — replaces Assistants (sunset 2026-08-26). Hosted tools (`web_search`,
  `file_search`, `computer_use`) are first-class; custom tools via `function` type. Native MCP
  support in Responses API.
- **Vercel AI SDK 6** — `tool({ description, inputSchema, execute })`; `ToolLoopAgent` runs the loop
  up to 20 steps; **strict mode** opt-in per tool guarantees schema-conformant inputs;
  human-in-the-loop approval is built in.

**Cite:**
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- https://openai.com/index/new-tools-for-building-agents/
- https://developers.openai.com/api/docs/guides/tools
- https://vercel.com/blog/ai-sdk-6
- https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling

**When to use:** Any cross-vendor codebase. Assume you'll need to swap providers; bake the abstraction
in early.

**When NOT to use:** Single-provider lock-in projects where the abstraction tax exceeds the
swap-out probability.

**Tiny example:**
```ts
// One schema, three exports
import { z } from "zod";
const SearchInput = z.object({ query: z.string(), limit: z.number().int().max(50).default(20) });

// Vercel AI SDK
export const searchTool = tool({
  description: "Search the user's notes. Use when the user asks 'find my note about X'.",
  inputSchema: SearchInput,
  execute: async ({ query, limit }) => searchNotes(query, limit),
});

// Anthropic / OpenAI: emit JSON Schema from the same Zod source
export const searchToolSchema = {
  name: "search_notes",
  description: searchTool.description,
  input_schema: zodToJsonSchema(SearchInput),
};
```

---

## tu-08 — Strict mode + schema validation at the runtime boundary

**Rule:** Turn on provider-native strict mode (OpenAI `strict: true`, Vercel AI SDK 6 per-tool
strict, Anthropic `disable_parallel_tool_use` + JSON Schema validation). The model literally cannot
emit invalid args. Catch the few schemas that strict can't express (open-ended objects, recursive
types) and validate them on the server side.

**Cite:**
- https://vercel.com/blog/ai-sdk-6
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use
- https://developers.openai.com/api/docs/guides/tools

**When to use:** Production tools that mutate state, anything where a malformed arg causes a
hard-to-debug downstream error.

**When NOT to use:** Highly recursive / open-shape inputs (e.g., a `query_dsl: any` for an internal
search DSL). Use a JSON Schema with `additionalProperties: true` and post-validate.

**Tiny example:**
```ts
// Vercel AI SDK 6 — opt-in strict per tool
const deleteFile = tool({
  description: "Permanently delete a file. ALWAYS confirm with user first.",
  inputSchema: z.object({ path: z.string(), idempotency_key: z.string() }),
  strict: true,           // provider-side validation
  execute: async (args) => fs.unlink(args.path),
});
```

---

## Summary table

| ID     | Methodology                                          | Primary cite |
|--------|------------------------------------------------------|--------------|
| tu-01  | Tool vs resource vs prompt — three-question test     | modelcontextprotocol.io |
| tu-02  | `verb_object` + namespace prefix                     | anthropic.com/engineering/writing-tools-for-agents |
| tu-03  | Description = zero-shot teaching                     | anthropic.com/engineering/advanced-tool-use |
| tu-04  | Split atomic tools, group via toolkits ≥ 25          | composio.dev field guide |
| tu-05  | Idempotency keys + preview/apply pair                | promptengineering.org 2026 playbook |
| tu-06  | Terse-default output, opt-in verbosity               | SkillReducer (arxiv 2603.29919) |
| tu-07  | Structured errors with `recoveryHint`                | medium kumaran.isk LLM-friendly errors |
| mcp-01 | stdio local / Streamable HTTP remote / SSE dead      | spec 2025-11-25 |
| mcp-02 | Gateway, virtual server, federation                  | blog.modelcontextprotocol.io 2026 roadmap |
| mcp-03 | Cross-runtime parity (Anthropic / OpenAI / Vercel)   | vercel.com/blog/ai-sdk-6 |
| tu-08  | Strict-mode validation at the runtime boundary       | ai-sdk.dev tools-and-tool-calling |

---

## Sources

- [MCP Spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [Writing effective tools for AI agents — Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Advanced tool use — Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- [Effective context engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building effective agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [Define tools — Claude API docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Implement tool use — Claude API docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
- [OpenAI new tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- [OpenAI using tools guide](https://developers.openai.com/api/docs/guides/tools)
- [OpenAI Responses API migration](https://platform.openai.com/docs/guides/migrate-to-responses)
- [Vercel AI SDK 6](https://vercel.com/blog/ai-sdk-6)
- [AI SDK Core: Tool Calling](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling)
- [MCP Demystified: Tools vs Resources vs Prompts (Microsoft)](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/mcp-demystified-tools-vs-resources-vs-prompts-explained-simply/4508057)
- [MCP Tools vs Resources vs Prompts (Exo)](https://exotechnologies.xyz/research/mcp-tools-resources-prompts)
- [SSE vs Streamable HTTP (Bright Data)](https://brightdata.com/blog/ai/sse-vs-streamable-http)
- [MCP Transport Protocols (MCPcat)](https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/)
- [MCP Aggregation, Gateway, Proxy Q1 2026](https://www.heyitworks.tech/blog/mcp-aggregation-gateway-proxy-tools-q1-2026)
- [Best open-source MCP gateways 2026 (Lunar)](https://www.lunar.dev/post/the-best-open-source-mcp-gateways-in-2026)
- [LLM-friendly error handling for MCP](https://medium.com/@kumaran.isk/llm-friendly-error-handling-designing-mcp-servers-for-ai-df427f6dfd2f)
- [SHIELDA — Structured exception handling for agents (arxiv)](https://arxiv.org/pdf/2508.07935)
- [SkillReducer — token efficiency (arxiv)](https://arxiv.org/html/2603.29919v1)
- [How to build great tools for AI agents (Composio)](https://composio.dev/blog/how-to-build-tools-for-ai-agents-a-field-guide)
- [Agent anti-patterns part 2 (Allen Chan)](https://achan2013.medium.com/ai-agent-anti-patterns-part-2-tooling-observability-and-scale-traps-in-enterprise-agents-42a451ea84ec)
- [2026 playbook for reliable agentic workflows](https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/)
- [MCP code execution token reduction](https://medium.com/@shamsul.arefin/building-an-ai-agent-with-mcp-code-execution-from-confusion-to-clarity-6b13fccc8c4b)
