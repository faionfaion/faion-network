# AGENT-03: Google Gemini / Vertex AI Agent Builder Methodologies

**Focus:** Gemini 2.5/3.x function calling, controlled generation, Live API, ADK (Agent Development Kit), Vertex AI Agent Engine, 1M-2M context tricks. April 2026 state.

**Tag legend:** so=structured-output, mm=multi-modal, tu=tool-use, pl=planning, lp=long-context-prompting, mem=memory, cli=CLI/coding-agent, eval=evaluation, cost=cost-optimization, mcp=protocol/integration.

---

## M1. Dump the entire codebase as long-context "context refs", let Gemini pick which files to act on — replaces vector RAG below ~2M tokens

**Rule:** For codebases under ~60k LOC (or any corpus < 2M tokens), concatenate the full source tree into a single Gemini 2.5 Pro / 3 Pro prompt as the cached prefix, then ask the model to (a) name the relevant files and (b) propose edits. Skip embedding pipelines entirely.

**Why Gemini-specific:** Only Gemini ships a 1M-default / 2M-opt-in context with native long-doc attention quality. The "haystack" recall that lets this work is documented by Google Research and used in Gemini Code Assist Enterprise.

**When to use:** single-repo codebases, design-doc Q&A, long-form contract review, monorepo navigation agents, slow-changing knowledge bases (refresh daily).

**When NOT to use:** corpora with thousands of independent documents queried one at a time (cheaper with vector DB), strict per-query latency budgets under ~3s, regulated content where sources must be deterministically retrievable (use grounded retrieval API instead).

**Tags:** lp, cli, cost, mem
**URL:** https://medium.com/google-cloud/skip-the-rag-workflows-with-geminis-2m-context-window-and-the-context-cache-d9345730e3c0
**URL:** https://medium.com/google-cloud/level-up-your-codebase-with-geminis-long-context-window-in-vertex-ai-4653ad943fa3

---

## M2. Pin the long-context prefix into an explicit Context Cache, then reference it from every agent turn — locks 90% discount + sub-second TTFT

**Rule:** Use `cached_content.create()` (Gemini API) or `CachedContent` (Vertex AI) for any prefix > 2,048 tokens that you reuse 3+ times. Set `ttl` to match expected session length (default 1h). Invalidate on prefix change. Never rely on implicit caching alone for cost-critical agents — implicit hits are best-effort and break when the system prompt mutates.

**Why Gemini-specific:** Explicit cache is the ONLY way to get a guaranteed 90% input-token discount on Gemini 2.5+ (75% on 2.0). Implicit caching exists but is opportunistic — system-prompt drift kills hit rates (see python-genai issue #1880).

**Minimum write thresholds (April 2026):** 1,024 tokens for 2.5 Flash, 2,048 tokens for 2.5 Pro. Below that, cache write is rejected.

**When to use:** multi-turn agents with stable system prompt + tool list + long doc context, RAG pipelines with shared corpus prefix, ADK agents in a chat session.

**When NOT to use:** prompts < 2k tokens (won't write), one-shot batch jobs (use Batch Mode 50% discount instead), prefixes that change every turn.

**Tags:** cost, mem, lp
**URL:** https://ai.google.dev/gemini-api/docs/caching
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
**URL:** https://github.com/googleapis/python-genai/issues/1880

---

## M3. Order `response_schema` fields so dependent fields come AFTER their inputs — Gemini emits keys in schema order, exploiting it = chain-of-thought for free

**Rule:** Gemini's controlled generation respects schema property order at decode time. Place `reasoning` / `analysis` / `evidence` BEFORE `decision` / `final_answer`. The model's emitted JSON literally constructs reasoning tokens that condition the answer tokens — a free, schema-enforced CoT with zero parsing fragility.

**Why Gemini-specific:** OpenAI's structured output also preserves order, but Gemini's docs explicitly guarantee it via "implicit property ordering" (see Google blog). Anthropic JSON mode does not enforce decode order.

**Concrete pattern:**
```json
{
  "type": "object",
  "properties": {
    "extracted_facts": {"type": "array", "items": {"type": "string"}},
    "reasoning": {"type": "string"},
    "confidence": {"type": "number"},
    "decision": {"type": "string", "enum": ["approve", "reject", "escalate"]}
  },
  "propertyOrdering": ["extracted_facts", "reasoning", "confidence", "decision"]
}
```

**When to use:** classifiers, extractors, agentic tool-routers where you want both rationale and final action, eval judges.

**When NOT to use:** UI-facing JSON (users see reasoning streaming first — surprising), high-volume Flash-Lite calls where extra reasoning tokens dominate cost.

**Tags:** so, pl, eval
**URL:** https://blog.google/technology/developers/gemini-api-structured-outputs/
**URL:** https://ai.google.dev/gemini-api/docs/structured-output

---

## M4. Use `text/x.enum` (not JSON enum) for routers and classifiers — single-token decision, ~100x cheaper than free-form

**Rule:** When the agent's only job is to pick from a fixed label set (intent classification, route-to-subagent, severity tag), set `response_mime_type="text/x.enum"` and `response_schema=Enum`. The model emits exactly one enum value with no JSON wrapper, no quotes, no whitespace.

**Why Gemini-specific:** This MIME type is unique to Gemini's controlled generation. Constrained decoding guarantees the output is one of the listed values — no parsing, no retries, no "decision: 'approve' " whitespace bugs.

**When to use:** ADK router agents that delegate to sub-agents, content moderation labels, ticket triage, multi-arm bandit selectors, A/B routing in agent pipelines.

**When NOT to use:** when you also need rationale (use JSON schema with reasoning field per M3), enum sets > ~500 values (token-budget issues — see python-genai #950), free-form classification.

**Tags:** so, tu, pl, cost
**URL:** https://ai.google.dev/gemini-api/docs/structured-output
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-controlled-generation-response-schema-7

---

## M5. Live API — declare ALL tools at session setup; tool-result events MUST precede the next model turn or the model hallucinates over its own pending call

**Rule:** Gemini Live API's `BidiGenerateContentSetup` requires `tools` declared upfront — you cannot add tools mid-session. When a `toolCall` event fires, your client MUST execute the tool and send `toolResponse` BEFORE sending any new user input. If you re-prompt before responding, the model treats the unanswered call as resolved-with-nothing and confabulates.

**Why Gemini-specific:** Unlike `generateContent`, Live API does NOT auto-handle tool round-trips. You manage the event loop. Out-of-order events break the audio/text stream's coherence model.

**Concrete pattern:** four independent async jobs — (1) audio in, (2) audio out, (3) toolCall executor, (4) toolResponse sender. The toolCall executor MUST signal job (4) before job (1) accepts the next user utterance.

**When to use:** real-time voice agents, multimodal screen-sharing copilots, low-latency assistants on LiveKit/WebRTC, kiosk agents.

**When NOT to use:** turn-based chatbots (use `generateContent` — auto tool-handling), batch processing, anything where >300ms latency is acceptable (Live API is overkill and 5x more expensive).

**Tags:** mm, tu, mcp
**URL:** https://ai.google.dev/gemini-api/docs/live-api/tools
**URL:** https://github.com/google-gemini/gemini-live-api-examples
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api

---

## M6. ADK workflow agents (Sequential / Parallel / Loop) — encode determinism in the orchestrator, leave reasoning to LlmAgent leaves

**Rule:** Don't ask one big LlmAgent to plan a 7-step workflow. Compose a `SequentialAgent` (or `ParallelAgent` for fan-out, `LoopAgent` for refine-until-good) of small LlmAgents, each with a single tool list and tight system prompt. Workflow agents are pure code — zero LLM calls for routing — so the topology is auditable and replayable.

**Why Gemini-specific:** ADK's three workflow primitives are first-class agent types, not patterns layered on top. State flows via `session.state` (deterministic), not via re-prompting. This is structurally different from LangGraph where the supergraph itself is an LLM.

**Concrete pattern:** `LoopAgent(sub_agents=[GeneratorAgent, CritiqueAgent, RefinerAgent], max_iterations=3, escalation_key="approved")` runs the trio until critique sets state["approved"]=True or 3 iters elapse.

**When to use:** known-DAG pipelines (extract → enrich → score → write), self-refine loops, fan-out research aggregators.

**When NOT to use:** open-ended tasks where the plan IS the work (use a single LlmAgent with planning), workflows requiring runtime topology changes.

**Tags:** pl, tu, eval
**URL:** https://google.github.io/adk-docs/agents/workflow-agents/
**URL:** https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/

---

## M7. ADK `before_model_callback` short-circuit — return `LlmResponse` from the callback to skip the LLM entirely (request-level cache + guardrail)

**Rule:** Wire a `before_model_callback` on every production LlmAgent. Three jobs in priority order: (1) check a request-level cache keyed on `(prompt_hash, tool_state_hash)` — return cached `LlmResponse` to skip the call; (2) run input guardrails (PII scrub, jailbreak detection) — return a refusal `LlmResponse` if blocked; (3) inject dynamic few-shots from `session.state`. Mirror with `after_model_callback` for output sanitization.

**Why Gemini-specific:** ADK's callback contract — return-None continues, return-LlmResponse short-circuits — is unique. No LangChain hook lets you replace the model output mid-flow this cleanly.

**When to use:** every production agent, especially regulated domains (health, finance), high-traffic agents where 30%+ of requests are repeats.

**When NOT to use:** prototype/eval agents where every callback adds latency you can't measure against, agents where you actively want non-determinism.

**Tags:** mcp, eval, cost, so
**URL:** https://google.github.io/adk-docs/callbacks/types-of-callbacks/
**URL:** https://google.github.io/adk-docs/safety/

---

## M8. Vertex AI Agent Engine sessions — let the runtime own conversation persistence; never roll your own DB for chat history

**Rule:** Deploy ADK agents to Vertex AI Agent Engine and use the built-in `create_session` / `get_session` / `list_sessions` API. State (per-conversation, ephemeral) and Memory (cross-session, per-user, persistent) are separate primitives — wire `PreloadMemoryTool` for long-term recall. Don't shove chat history into your own Postgres just because that's the LangChain default.

**Why Gemini-specific:** Agent Engine session storage is a managed Spanner-backed service that survives agent restarts, scales horizontally, and is billed per stored event — not per agent instance. Memory Engine is a separate vector-backed product specifically for cross-session personalization. No equivalent in OpenAI Assistants API at this scale.

**When to use:** any production-deployed ADK agent, multi-instance horizontal scale, conversational agents needing user-level memory across sessions.

**When NOT to use:** local dev (use `InMemorySessionService`), agents you'll deploy on Cloud Run/GKE without Agent Engine (then DIY persistence is unavoidable), one-shot stateless agents.

**Tags:** mem, mcp
**URL:** https://docs.cloud.google.com/agent-builder/agent-engine/sessions/manage-sessions-adk
**URL:** https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview

---

## M9. Combine built-in tools (Google Search + Maps + Code Execution) WITH custom function declarations in a single `tools=[...]` array — context circulation lets Gemini chain them

**Rule:** As of March 2026, Gemini 3 supports mixing native tools and user functions in one request. Pattern: user asks "find the closest open Italian restaurant with > 4.5 rating and book a table"; Gemini calls `google_maps_search` (native) → reads result → calls `google_search` (native) for ratings → calls `book_table(restaurant_id)` (your function). Each parallel tool call gets a unique `id` for cross-result mapping.

**Why Gemini-specific:** Only Gemini exposes Google Search + Maps as first-party native tools (cheaper, faster, with native grounding metadata) AND lets you mix them with custom functions in one tool list. Anthropic web search is custom-tool-only; OpenAI's web search is opaque.

**Always check `groundingMetadata`:** the response includes `webSearchQueries`, `groundingChunks`, `groundingSupports` — surface citations back to users (compliance + trust).

**When to use:** local-discovery agents, real-time-news assistants, fact-grounded research bots, anything where Google's index beats your scraped corpus.

**When NOT to use:** air-gapped enterprise (Google native tools call Google services), use-cases where you must own retrieval (compliance), domain-specific search where Google indexes are too noisy.

**Tags:** tu, mcp, lp, eval
**URL:** https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tooling-updates/
**URL:** https://www.marktechpost.com/2026/04/07/how-to-combine-google-search-google-maps-and-custom-functions-in-a-single-gemini-api-call-with-context-circulation-parallel-tool-ids-and-multi-step-agentic-chains/

---

## M10. Tune `thinking_level` per agent role — `minimal` for routers, `high` for planners, `medium` is wrong default for cost-sensitive workloads

**Rule:** Gemini 3 replaced the integer `thinking_budget` with a 4-tier `thinking_level` (minimal / low / medium / high). Match level to role: `minimal` for ADK routers and classifiers (single-token decisions), `low` for tool-callers, `medium` for end-user chat, `high` for SDD planners and code-fix agents. Each step up multiplies thinking-token cost; default `medium` overspends on simple tasks.

**Why Gemini-specific:** Gemini bills you for thinking tokens generated under the hood AND charges output rates. Anthropic's extended thinking is similar in concept but has different cost dynamics. On Gemini 2.5 you still use integer `thinking_budget` (set to 0 to disable on Flash for routers).

**When to use:** any multi-agent system where roles have different reasoning needs, cost-sensitive workloads at scale, latency-sensitive endpoints (lower level = faster).

**When NOT to use:** unknown task complexity (let `auto` decide), reasoning-critical single-shot tasks (use `high` and don't optimize), Gemini 3 Pro tasks where thinking is mandatory and not configurable.

**Tags:** cost, pl, eval
**URL:** https://ai.google.dev/gemini-api/docs/thinking
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking
**URL:** https://ai.google.dev/gemini-api/docs/gemini-3

---

## M11. Batch Mode — bundle every non-interactive agent eval / backfill into one job, get 50% off + implicit caching → effective 12.5% of synchronous cost

**Rule:** Any agent task that doesn't need a sub-second response — eval suites, dataset labeling, document backfill, nightly re-summarization, SDD memory consolidation — goes through Batch Mode (`batches.create()`). The 24h SLA is a cost contract: you trade latency for 50% discount. Combine larger batches (200k requests in one job, not 1000 jobs of 200) for better throughput and higher implicit-cache hit rates.

**Why Gemini-specific:** 50% batch discount stacks with implicit caching (which works inside batches). Effective cost on repeat-prefix workloads: ~12.5% of synchronous Gemini Pro pricing. OpenAI's batch is also 50% off but does not stack with prompt caching.

**When to use:** eval harnesses (Vertex AI Gen AI Eval), nightly re-classification of news/content pipelines, large-scale dataset transformation, SDD pattern-mining over committed code.

**When NOT to use:** anything user-facing, sub-24h SLA tasks, agent loops with interactive feedback, when you need per-call streaming.

**Tags:** cost, eval, mem
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini
**URL:** https://developers.googleblog.com/en/scale-your-ai-workloads-batch-mode-gemini-api/

---

## M12. Use Vertex AI Gen AI Eval Service with `Adaptive Rubrics` + `Tool Use Quality` metrics for agent evaluation — Gemini-as-judge with per-prompt rubric generation

**Rule:** For agent eval, don't write static rubrics — Vertex AI's "adaptive rubrics" generate a unique pass/fail criteria PER prompt, then a Gemini judge model scores against them. Pair with the `Tool Use Quality` metric, which evaluates: (a) tool selection correctness, (b) parameter accuracy, (c) call sequence adherence. Both run inside Batch Mode for cheap eval at scale.

**Why Gemini-specific:** The adaptive-rubrics + tool-use-quality combination is unique to Vertex AI Gen AI Eval. The judge defaults to `gemini-2.0-flash` (cheap) but is swappable. Integration with Agent Engine means you can evaluate deployed agents against production traces, not just offline datasets.

**When to use:** every production agent before promotion, regression testing on prompt changes, multi-agent system validation, comparing model versions (2.5 → 3) for migration.

**When NOT to use:** when you need ground-truth deterministic metrics (use BLEU/ROUGE/exact-match), heavily subjective tasks where human eval is irreplaceable.

**Tags:** eval, tu
**URL:** https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview
**URL:** https://codelabs.developers.google.com/codelabs/production-ready-ai-roadshow/2-evaluating-multi-agent-systems/evaluating-multi-agent-systems
**URL:** https://googlecloudplatform.github.io/applied-ai-engineering-samples/genai-on-vertex-ai/gemini/evals_playbook/notebooks/1_gemini_evals_playbook_evaluate/

---

## M13. Files API + GCS URI registration — upload large multimodal assets ONCE, reference by URI across thousands of agent calls

**Rule:** Any file > 100MB total request size MUST go through Files API (`files.upload()`) — inline base64 in prompts is rejected. For files needed beyond Files API's 48h expiry, register a Google Cloud Storage URI with the Gemini API: `gs://bucket/object` becomes a never-expiring reference. Use this for agent corpora, training-doc libraries, video archives.

**Why Gemini-specific:** Files API supports 2GB per file, 20GB per project. GCS URI registration (added 2026) bypasses the 48h TTL — your bucket IS the storage. External URL fetching also works (100MB cap, fetched at request time). No equivalent unified file-API across modalities elsewhere.

**When to use:** video-understanding agents, multi-document analyzer agents, bills/contracts processing pipelines, anything where the same large asset is referenced repeatedly.

**When NOT to use:** small files inline (< 20MB — base64 is fine and saves a round-trip), files only used once (just pass the bytes), strict data-residency where GCS isn't available.

**Tags:** mm, mem, cost, mcp
**URL:** https://ai.google.dev/gemini-api/docs/files
**URL:** https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-new-file-limits/
**URL:** https://ai.google.dev/gemini-api/docs/file-input-methods

---

## Summary of Tag Coverage

| Tag | Methodologies |
|-----|---------------|
| so (structured-output) | M3, M4, M7 |
| mm (multi-modal) | M5, M13 |
| tu (tool-use) | M4, M5, M6, M7, M9, M12 |
| pl (planning) | M3, M4, M6, M9, M10 |
| lp (long-context) | M1, M2, M9 |
| mem (memory) | M1, M2, M8, M11, M13 |
| cli (coding-agent) | M1 |
| eval (evaluation) | M3, M6, M7, M9, M10, M11, M12 |
| cost (cost-optimization) | M1, M2, M4, M7, M10, M11, M13 |
| mcp (protocol/integration) | M5, M7, M8, M9, M13 |
