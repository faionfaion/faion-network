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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-api.py` | Validate an integration-record JSON against the contract in `02-output-contract.xml`. | After codegen, before opening PR; in CI on the integration manifest file. |

## Related

- [[decision-framework]] — selects model + approach before this methodology runs.
- [[cost-optimization]] — sets caching / batching policy this methodology implements.
- [[gemini-api]] — peer integration pattern; same shape, different provider features.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches first on whether the system prompt + static context ≥1024 tokens and repeats — if yes, caching is mandatory and the cache prefix must be the longest stable head. The second axis is agentic-vs-single-turn — agentic loops add the MAX_TURNS guard and the schema-validated tool dispatcher. The third axis is online-vs-offline — offline ≥100 requests routes to Batch API; otherwise streaming or sync. The fourth axis (Opus 4.7 only) gates Extended Thinking on expected output length and reasoning depth. Leaves emit one of: `cached-streaming-agent`, `cached-sync`, `batch-job`, or `opus-extended-thinking`, each referencing a rule id in `01-core-rules.xml`.
