# Claude API

## Summary

**One-sentence:** Produces production code that calls Anthropic's Messages API via the official SDK with cached system prompts, MAX_TURNS-bounded tool-use loops, forced-tool structured output, Extended Thinking (Opus 4.7), streaming SSE handling, and Batch API submission/polling.

**One-paragraph:** Direct SDK use is the lowest-latency path to Claude and the only path that exposes every billing-reducing feature (Prompt Caching → 90% off input on cache hits; Batch API → 50% off for offline workloads) and every beta capability (Extended Thinking, interleaved thinking with tools) without proxy or framework overhead. This methodology ships the operational shape: enforce `MAX_TURNS` (default 10) on every agentic loop, cache the longest stable prefix first, use forced tool use for any JSON-shaped output, gate Extended Thinking by output-length payoff (skip if answer ≤200 tokens), and group requests by deadline (interactive never goes through Batch). It owns the runtime-code surface — model and tool selection are handled by `decision-framework` upstream.

**Ефективно для:**

- Агентних циклів зі своїми тулами, де потрібен повний контроль над масивом повідомлень і `stop_reason`-логікою (LangChain/LiteLLM ховають це).
- Великих стабільних системних промптів (≥1024 tokens) або тулових схем, що повторюються в кожному запиті — кешування дає 90% економії на input.
- Офлайн enrichment-пайплайнів на сотні-тисячі документів (summarization, tagging, embeddings prep) — Batch API ріже вартість навпіл за 24-годинне вікно.
- Складних reasoning-задач, де Extended Thinking на Opus 4.7 дає вимірюваний приріст точності (математика, контрактний аналіз, debugging).
- Production-сервісів, де SDK дає retry + SSE-парсинг + версійні заголовки безкоштовно; голий `requests` не варто.

## Applies If (ALL must hold)

- The codebase calls Anthropic's Claude directly (no LiteLLM / LangChain / proxy abstraction is already in production).
- A system prompt or large context block ≥1024 tokens repeats across requests, OR an agentic loop drives tools, OR an offline workload ≥100 requests can wait 24h.
- The team owns the Python or TypeScript runtime — direct SDK install is permitted (`pip install anthropic` / `npm install @anthropic-ai/sdk`).

## Skip If (ANY kills it)

- A multi-provider abstraction (LiteLLM, LangChain, Vercel AI SDK) is already in production — adding direct SDK calls fragments retry, logging, and cost tracking.
- The task fits Haiku 4.5 or a cheaper provider — model selection is owned by `decision-framework`; do not pick Claude before that gate.
- Latency budget is <200 ms p99 — even streaming carries SSE setup overhead; Batch is impossible.
- The product runs in a regulated context (HIPAA, FedRAMP) without an approved Anthropic BAA / contract addendum — defer to compliance review.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Selected Claude model id (haiku-4-5 / sonnet-4-6 / opus-4-7) | string | `decision-framework` output |
| System prompt + static context (≥1024 tokens if caching) | text | Product spec |
| Tool schema list (≤10 tools) | JSON Schema array | Tool registry |
| `ANTHROPIC_API_KEY` | env var | Secrets manager (1Password / Vault) |
| Output schema (if structured output required) | JSON Schema | API contract |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[decision-framework]] | Selects the model and the prompt-vs-RAG-vs-fine-tune axis before this code runs. |
| [[cost-optimization]] | Sets the budget envelope and caching/batching thresholds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules: max_tokens explicit, MAX_TURNS guard, forced tool use, cache prefix order, cached block ≥1024 tokens, ET output payoff gate, no hardcoded key, exponential backoff, Batch never for interactive | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the integration-record artefact: model id, max_tokens, cache_control flag, tool list, MAX_TURNS, retry policy, telemetry fields | 900 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: infinite tool loop, schema drift, side-effects without checkpoint, cache TTL expiry, cache prefix mismatch, silent thinking billing, ET on short output, hardcoded key, no retry on 429 | 1100 |
| `content/04-procedure.xml` | reference | 6-step build procedure: model select → system+tools assemble → cache markers → loop wrap → telemetry → batch fallback | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree: cacheable? agentic? offline-OK? thinking-payoff? → integration shape | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_request_shape` | haiku-4-5 | Cheap structured triage: agentic vs single-turn vs batch. |
| `generate_integration_code` | sonnet-4-6 | Balanced code generation with 1M context for repo-aware refactor. |
| `audit_existing_integration` | opus-4-7 + ET | Deep reasoning over a live codebase: cache-hit-rate analysis, MAX_TURNS placement, race-condition review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-caching-agent.py` | Cached system prompt + tool-use loop with MAX_TURNS guard and exponential-backoff retry. |
| `templates/tool-use-loop.py` | Complete tool-use skeleton with ToolExecutor, retry decorator, forced structured output. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-api.py` | Validate an integration-record JSON against the contract in `02-output-contract.xml`. | After codegen, before opening PR; in CI on the integration manifest file. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[decision-framework]] — selects model + approach before this methodology runs.
- [[cost-optimization]] — sets caching / batching policy this methodology implements.
- [[gemini-api]] — peer integration pattern; same shape, different provider features.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches first on whether the system prompt + static context ≥1024 tokens and repeats — if yes, caching is mandatory and the cache prefix must be the longest stable head. The second axis is agentic-vs-single-turn — agentic loops add the MAX_TURNS guard and the schema-validated tool dispatcher. The third axis is online-vs-offline — offline ≥100 requests routes to Batch API; otherwise streaming or sync. The fourth axis (Opus 4.7 only) gates Extended Thinking on expected output length and reasoning depth. Leaves emit one of: `cached-streaming-agent`, `cached-sync`, `batch-job`, or `opus-extended-thinking`, each referencing a rule id in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-caching-agent.py`

```python
# Cached system prompt + tool-use agent loop with MAX_TURNS guard
import random
import time

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

# System prompt must be >= 1024 tokens to qualify for caching
SYSTEM = [
    {
        "type": "text",
        "text": "You are a production assistant with access to tools. "
                "Always reason step-by-step before calling a tool. "
                "When you have enough information to answer, respond directly without calling more tools.",
        # NOTE: for real cache benefit this block must be >= 1024 tokens.
        # Append your large static context (retrieved documents, tool descriptions, domain rules) here.
        "cache_control": {"type": "ephemeral"},
    }
]

TOOLS = [
    {
        "name": "search",
        "description": "Search the knowledge base. Returns a list of relevant passages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"},
                "top_k": {"type": "integer", "description": "Number of results to return", "default": 5},
            },
            "required": ["query"],
        },
    },
]

MAX_TURNS = 10


def execute_tool(name: str, tool_input: dict) -> str:
    """Dispatch tool calls. Replace with real implementations."""
    if name == "search":
        return f"[search results for: {tool_input['query']}]"
    return f"[unknown tool: {name}]"


def call_with_retry(fn, max_retries: int = 5):
    """Exponential backoff with jitter for rate limits and 5xx errors."""
    for attempt in range(max_retries):
        try:
            return fn()
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = min(2 ** attempt + random.uniform(0, 1), 60)
            time.sleep(wait)
        except anthropic.APIError as e:
            if e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                wait = min(2 ** attempt + random.uniform(0, 1), 60)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Max retries exceeded")


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    cache_hits = 0

    for turn in range(MAX_TURNS):
        response = call_with_retry(
            lambda: client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=SYSTEM,
                tools=TOOLS,
                messages=messages,
            )
        )

        cache_hits += getattr(response.usage, "cache_read_input_tokens", 0)

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"Agent did not reach end_turn after {MAX_TURNS} turns")


if __name__ == "__main__":
    answer = run_agent("What is our refund policy for digital products?")
    print(answer)
```

### `templates/tool-use-loop.py`

```python
# Complete tool-use skeleton: ToolExecutor + retry + forced structured output
import json
import random
import time
from typing import Any, Callable

import anthropic

client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

class ToolExecutor:
    """Register tools and dispatch Claude's tool_use blocks."""

    def __init__(self):
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable[..., Any]] = {}

    def register(self, tool: dict, handler: Callable[..., Any]) -> None:
        self._tools[tool["name"]] = tool
        self._handlers[tool["name"]] = handler

    @property
    def tools(self) -> list[dict]:
        return list(self._tools.values())

    def execute(self, name: str, inputs: dict) -> tuple[str, bool]:
        """Execute a tool. Returns (content_str, is_error)."""
        if name not in self._handlers:
            return json.dumps({"error": f"Unknown tool: {name}"}), True
        try:
            result = self._handlers[name](**inputs)
            return json.dumps({"result": result}), False
        except Exception as exc:
            return json.dumps({"error": str(exc)}), True


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------

def _with_backoff(fn: Callable, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return fn()
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
        except anthropic.APIError as e:
            if e.status_code < 500 or attempt == max_retries - 1:
                raise
        wait = min(2 ** attempt + random.uniform(0, 1), 60)
        time.sleep(wait)
    raise RuntimeError("Max retries exceeded")


# ---------------------------------------------------------------------------
# Standard tool-use loop
# ---------------------------------------------------------------------------

def run_with_tools(
    prompt: str,
    executor: ToolExecutor,
    model: str = "claude-sonnet-4-20250514",
    system: str | None = None,
    max_tokens: int = 4096,
    max_turns: int = 10,
) -> str:
    """Run a tool-use conversation. Returns final text response."""
    messages: list[dict] = [{"role": "user", "content": prompt}]

    for turn in range(max_turns):
        create_kwargs: dict[str, Any] = dict(
            model=model,
            max_tokens=max_tokens,
            tools=executor.tools,
            messages=messages,
        )
        if system:
            create_kwargs["system"] = system

        response = _with_backoff(lambda: client.messages.create(**create_kwargs))

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason != "tool_use":
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                content, is_error = executor.execute(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content,
                    "is_error": is_error,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError(f"Tool loop exceeded {max_turns} turns without reaching end_turn")


# ---------------------------------------------------------------------------
# Forced structured output (use a tool schema to guarantee JSON shape)
# ---------------------------------------------------------------------------

OUTPUT_SCHEMA: dict = {
    "name": "structured_output",
    "description": "Return the final structured result. Always call this tool to respond.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "sources": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["summary", "confidence", "sources"],
    },
}


def extract_structured(
    prompt: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
) -> dict:
    """Force Claude to return a structured dict matching OUTPUT_SCHEMA."""
    response = _with_backoff(lambda: client.messages.create(
        model=model,
        max_tokens=max_tokens,
        tools=[OUTPUT_SCHEMA],
        tool_choice={"type": "tool", "name": OUTPUT_SCHEMA["name"]},
        messages=[{"role": "user", "content": prompt}],
    ))
    for block in response.content:
        if block.type == "tool_use" and block.name == OUTPUT_SCHEMA["name"]:
            return block.input
    raise RuntimeError("Structured output tool was not called")


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    executor = ToolExecutor()

    # Register a sample tool
    executor.register(
        {
            "name": "lookup_policy",
            "description": "Look up a company policy by topic.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Policy topic, e.g. 'refunds'"}
                },
                "required": ["topic"],
            },
        },
        handler=lambda topic: f"Policy for '{topic}': 30-day full refund for unopened items.",
    )

    # Standard tool-use loop
    answer = run_with_tools(
        prompt="What is the refund policy for unopened items?",
        executor=executor,
        system="You are a helpful customer service agent.",
    )
    print("Answer:", answer)

    # Forced structured output
    result = extract_structured(
        "Summarize: Claude is an AI assistant by Anthropic focused on safety and helpfulness."
    )
    print("Structured:", result)
```
