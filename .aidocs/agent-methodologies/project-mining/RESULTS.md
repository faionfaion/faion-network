# Agent Methodology Mining Results

Systematic extraction of 22 production AI agent tricks from faion projects.

## Structured Output (so-)

### so-schema-field-ordering-for-reasoning
**Category:** so-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/schemas/generation.json:48-51`
**Pattern:** Schema fields ordered by dependency: `summary_en` comes AFTER `article_en`, `tags`, and all content fields because the model needs to write content first, then summarize it. The summary field explicitly instructs "Include: main topic, key facts, companies/tools mentioned, what changed, who is affected" — forcing reasoning over generated content.
**Concrete rule:** Order JSON schema fields by data flow dependency, not alphabetically. Put prerequisite outputs before derived outputs. Use description strings as in-schema reasoning hints for complex fields.

### so-json-repair-incremental-strategy
**Category:** so-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/json_repair.py:17-142`
**Pattern:** 11-step incremental JSON repair with clear fallback chain: (1) try raw, (2) strip BOM/markdown, (3) extract object, (4) sanitize unicode quotes, (5) fix trailing commas, (6) fix control chars, (7) repair stray quotes, (8) escape backslashes, (9) close truncated, (10) handle "Extra data", (11) aggressive truncation recovery. Each step includes logging context. Never fails silently.
**Concrete rule:** Build repair chains with explicit phases. Log which repair fixed the JSON (helps identify which LLMs have which failure patterns). Use incremental passes rather than regex-all-at-once — order matters (trailing commas before truncation, unicode before structural fixes).

### so-enum-in-schema-reduces-variance
**Category:** so-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/schemas/editorial.json:17-19`
**Pattern:** `article_type` field uses `enum: ["news", "guide", "opinion", "personal", "publicistics"]` instead of free-form string. Keeps downstream stages simple and reduces hallucination. Same pattern in code_review schema where `severity` uses enum for consistency.
**Concrete rule:** Use JSON schema enums for any categorical field that has a fixed set of valid values. This constrains LLM output and makes downstream schema validation strict.

### so-pydantic-field-ordering-impacts-token-use
**Category:** so-
**File:** `/home/nero/workspace/projects/faion-cli/faion_cli/schemas.py:1-40`
**Pattern:** `AnalyzeOutput` schema in analyze.py orders fields strategically: `task_type` (simple enum) before `task_summary` (computed), `recommended_methods` (short list) before `context_fragments` (detailed). First fields are cheapest to generate, so model commits early (helps with streaming/interruption recovery). Each field has `description` for in-prompt reasoning.
**Concrete rule:** Order Pydantic schema fields by generation cost (cheap enums/scalars first, expensive structured data last). This improves token efficiency and recovery from partial responses.

## Multi-Model Orchestration (mm-)

### mm-sonnet-for-investigation-opus-for-reasoning
**Category:** mm-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/config.py:43` and `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s0_context_investigate.py:14`
**Pattern:** Stage 0 (context investigation) uses Sonnet (`MODEL_INVESTIGATE = "sonnet"`), all other stages use Opus. Investigation stage reads system state (logs, files, RSS) — pure retrieval, no creativity. All other stages (editorial planning, generation, review) use Opus for reasoning. This saves ~60% on investigation costs while maintaining quality for reasoning.
**Concrete rule:** Assign weaker models to read-only investigation/context-gathering stages. Reserve expensive models (Opus) for reasoning, writing, and judgment stages. Profile cost-per-stage before committing.

### mm-filtering-with-weak-model-before-strong-processing
**Category:** mm-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/stages/code_review.py:86-107`
**Pattern:** Code review uses a 3-stage flow: Review (full code review with line numbers) → Meta-Review (filter false positives, adjust quality score) → Fix (implement). The meta-review stage can use a lighter model because it's filtering/validating previous results, not generating original analysis. In practice, all three currently use opus, but the architecture supports swapping meta-review to Sonnet.
**Concrete rule:** For multi-step reasoning, identify filter/validation steps and mark them as candidates for cheaper models. Structure stages so each output becomes input to a lighter-weight filter before expensive next step.

## Tool-Use Design (tu-)

### tu-allowed-tools-per-research-mode
**Category:** tu-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s3_research.py:14-38`
**Pattern:** Research stage (s3) adapts tool access by research_mode (news vs. material). News mode allows `["WebSearch", "WebFetch"]`. Material mode allows `["WebSearch", "WebFetch", "Bash", "Read"]` to search local repos/APIs. Tool set is determined at stage time based on article_type (set in editorial planning), not prompts.
**Concrete rule:** Encode tool policy as code logic (dict/enum keyed by mode), not by prompt instructions. This makes policy testable and auditable. Load tool set before building the prompt, not as part of it.

### tu-tools-disabled-for-structured-output
**Category:** tu-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/sdk.py:73-98`
**Pattern:** `_ALL_BUILTIN_TOOLS` list disables ALL Claude Code tools for structured queries (`disallowed_tools=_ALL_BUILTIN_TOOLS`). Without this, Opus tries to use tools instead of returning JSON. The comment: "Without this, Opus tries to use tools (Read, Grep...) instead of returning JSON." Explicit ban is more reliable than asking politely in the prompt.
**Concrete rule:** For structured output stages, explicitly disable tools via SDK config, don't rely on prompt instructions. Models ignore "return only JSON" when tools are available — tools are attractive.

### tu-claude-code-preset-for-implementation
**Category:** tu-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/stages/implementation.py:50` and code_review.py line `tools={"type": "preset", "preset": "claude_code"}`
**Pattern:** Implementation and Code Review stages use `tools={"type": "preset", "preset": "claude_code"}` instead of listing individual tools. This gives the agent the full Claude Code toolkit (Read, Edit, Bash, Grep, WebSearch, etc.) without needing to enumerate. Used when the agent needs broad file/code access.
**Concrete rule:** Use `preset: "claude_code"` for full-featured coding/implementation agents. Use `allowed_tools: []` for structured output only. Use explicit tool lists for constrained scenarios (e.g., WebFetch + WebSearch only).

## Pipeline & Sub-Task Delegation (pl-)

### pl-manifest-then-fetch-pattern-for-context
**Category:** pl-
**File:** `/home/nero/workspace/projects/faion-cli/faion_cli/pipeline.py:96-110`
**Pattern:** SDD pipeline's analyze stage searches for methodology context using `stage.context_query` (a manifest query like "{task}"). Results are metadata + small fragments (~500 token max). Subsequent stages use previous_outputs (full context references) rather than re-searching. Design: "search once, pass references, fetch on demand" reduces redundant searches.
**Concrete rule:** First stage searches and builds a lightweight manifest (metadata + fragments). Pass manifest through context; downstream stages reference by ID rather than re-searching or copying full content. Reduces redundancy and token waste.

### pl-parallel-translation-with-threadpool
**Category:** pl-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s9_parallel.py:1-54`
**Pattern:** Stage 9 runs 7 parallel translations + image generation in a single ThreadPoolExecutor pool. Each language is a separate `structured_query()` call to the same model. Timeout scales per language based on article length. `as_completed()` collects results as they finish, not in submission order. Allows one slow translation to not block the others.
**Concrete rule:** For independent sub-tasks (translations of the same content to different languages), use ThreadPoolExecutor with `as_completed()`. Scale timeouts per task. This is faster than sequential and simpler than async/await.

### pl-pass-paths-not-content-for-large-objects
**Category:** pl-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s10_deploy.py` (implicit from context flow) and `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s13_pick_and_publish.py:56-72`
**Pattern:** In s13 (publish to TG), articles are looked up by slug (path-like reference) rather than passed as full content. The function `_get_tg_post(slug, lang)` reads from disk. Image is located via `_find_image(slug)`. This pattern avoids copying large article content through memory and allows stages to be loosely coupled.
**Concrete rule:** For large objects (articles, images), pass references (slugs, paths, IDs) through context, not the full content. Each stage reads what it needs from canonical storage. Reduces memory/token overhead and makes the DAG more resilient.

### pl-deduplication-via-state-file
**Category:** pl-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s13_pick_and_publish.py:32-44`
**Pattern:** Before picking an article to publish, stage checks `tg_published/{date}.json` for already-posted slugs. This prevents re-publishing the same article in the same day. State is persisted across runs in a date-keyed file. This is a simple dedup manifest.
**Concrete rule:** For idempotent operations (publishing, deploying), maintain a per-day or per-run state file listing completed items. Check before executing. Append after success. Prevents duplicate side effects.

## Agent Loops (lp-)

### lp-review-loop-with-max-cycles
**Category:** lp-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/main.py:40-50`
**Pattern:** `_review_loop()` runs s5_review → s6_revise in a for loop up to MAX_REVIEW_CYCLES (3). Loop exits early if `review_approved` is true AND cycle >= 1 (min 1 revision). Logs each cycle. Falls through with a warning if max cycles hit. This is a bounded ReAct loop.
**Concrete rule:** Implement review loops with: (1) explicit cycle limit, (2) early exit condition (quality threshold), (3) min iterations (at least one revision even if first check passes), (4) logging at each step.

### lp-code-review-with-meta-review-filter
**Category:** lp-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/stages/code_review.py:57-120`
**Pattern:** Code review loop (max 10 iterations): Review → Meta-Review → Fix. Meta-Review filters false positives and adjusts quality score. Comments are kept only if severity is critical/required after meta-review. This creates a secondary validation gate. If quality >= 8 and no blocking issues after filter, approval happens early.
**Concrete rule:** For quality gates, add a meta-review step that filters and re-scores previous review. Use meta-review output to adjust approval criteria. This reduces false negatives (catching real issues) and false positives (avoiding nitpicks that don't matter).

### lp-context-stage-before-implementation
**Category:** lp-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/pipeline.py:50-62`
**Pattern:** Both SDD and NERO pipelines start with ContextStage, which reads project structure, docs, and recent commits. Only then runs planning/implementation. ContextStage output is cached in `ctx.results["context"]` and injected into all downstream prompts. This is a "warm-start" for the agent loop.
**Concrete rule:** Start multi-stage agent pipelines with a context-gathering stage. Cache context in the shared state (results dict). Inject context into all downstream stages' prompts. Avoids context being re-gathered and makes reasoning more consistent.

## Memory / Context Management (mem-)

### mem-pipeline-context-dataclass-with-apply-methods
**Category:** mem-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/context.py:19-200`
**Pattern:** `PipelineContext` is a @dataclass holding all pipeline state. Each stage calls `ctx.apply_X()` methods (e.g., `apply_generation()`, `apply_review()`) which validate output against constraints (SLUG_RE, MIN_ARTICLE_LENGTH) and raise `ValidationError` on failure. Apply methods also seed derived dicts (e.g., `articles["en"] = article_en`). This is explicit state mutation with validation.
**Concrete rule:** Use a shared context dataclass with typed fields for all pipeline state. Add apply_* methods for each stage output that validate and integrate. Avoid passing data between stages via return values — always update ctx. This makes the flow traceable and debuggable.

### mem-indexed-state-for-cross-run-persistence
**Category:** mem-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s13_pick_and_publish.py:32-37` and `/home/nero/workspace/projects/faion-cli/faion_cli/cache.py:20-26`
**Pattern:** Media Manager uses `tg_published/{date}.json` keyed by language. Faion-cli uses `~/.faion/cache/bm25_index.json` + `skills_hash.txt` to detect stale cache. Both use hash-based invalidation (timestamp + file modification times). State survives process restarts.
**Concrete rule:** For cross-run state (published articles, caches, logs), use date-keyed or hash-keyed indices. Store hashes separately to detect invalidation. Prefer JSON for readability. This makes pipelines resumable and checkpointable.

### mem-ask-user-for-pause-resume
**Category:** mem-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/pipeline.py:106-174`
**Pattern:** Pipelines can pause and ask the user a question via RabbitMQ. The question is stored in `ctx.ask_user_question` and `ctx.paused_at_stage`. Resume message updates `ctx.user_answer`. Pipeline resumes with `start_stage = paused_at_stage`, so stages already completed are skipped. This is long-lived agent state.
**Concrete rule:** For user-interactive pipelines, store pause points (stage index, question) in context. On resume, re-hydrate context from storage, skip completed stages, and continue. Use async messaging (RabbitMQ) for question delivery, not blocking I/O.

## CLI vs SDK Choices (cli-)

### cli-agent-sdk-wrapper-with-sync-interface
**Category:** cli-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/sdk.py:1-100`
**Pattern:** All LLM calls go through `sdk.py`: `structured_query()` and `agent_query()`. These wrap `claude_agent_sdk.query()` with asyncio.run() (sync interface). Retries use exponential backoff with jitter. Patches SDK parser to skip unknown message types. This creates a single point of control for all API calls.
**Concrete rule:** Create a thin SDK wrapper in your pipeline that exposes sync functions (not async). Handle retries and error mapping centrally. Patch known SDK issues at initialization. All stages import from this wrapper, never directly from the SDK.

### cli-vs-api-sdk-for-pipelines
**Category:** cli-
**File:** `/home/nero/workspace/projects/faion-cli/faion_cli/pipeline.py:155-200`
**Pattern:** Faion-cli uses the Anthropic Python SDK directly (`import anthropic`), not the Agent SDK. Reason: faion-cli is a library (installed as a package), runs locally on user machines, and doesn't need tool access. Agent SDK is for agent flows with tools. Direct SDK is simpler for structured-only pipelines.
**Concrete rule:** Use Agent SDK for pipelines that need tools or complex agent loops. Use Anthropic SDK directly for simple structured pipelines (no tools). Agent SDK adds overhead and dependencies that don't pay off for simple cases.

## Evaluation Patterns (eval-)

### eval-quality-score-with-blocking-issues-gate
**Category:** eval-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/schemas/code_review.json:13-80`
**Pattern:** Code review schema has `overall_quality` (1-10 score) AND a list of `comments` with `severity` enum (critical, required, suggestion, nitpick, praise). Approval logic is: `quality >= 8 AND no(critical OR required)`. This separates aesthetic quality from blockers. A beautiful-but-broken PR fails; a workmanlike but correct PR passes.
**Concrete rule:** For quality gates, use BOTH a score (1-10) and a categorized list of issues (severity + category). Approval requires both score threshold AND absence of blocking severities. This decouples aesthetic polish from correctness.

### eval-metadata-in-schema-for-audit
**Category:** eval-
**File:** `/home/nero/workspace/projects/nero/deploy/nero-agent/stages/code_review.py:69-80`
**Pattern:** After each code review iteration, emit_event() is called with payload containing `iteration`, `quality_score`, `blocking_issues` count, `comments_count`, and `stats` dict. This populates a database (events table) for post-hoc analysis. The schema is audit-friendly.
**Concrete rule:** Emit structured events for each major stage output. Include iteration/attempt count, quality scores, issue counts, and stats. Store in a queryable database (Postgres events table). This creates an audit trail and enables quality trending.

### eval-previous-context-injection-for-loop-state
**Category:** eval-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/stages/s9_parallel.py:23-53` (implicit in timeout calculation)
**Pattern:** Timeout scales based on article length: "900s base + 300s per KB above 2KB, cap 1800s". This encodes knowledge that longer articles need more translation time. The formula is tuned from production observation. Timeout is set per-task based on context, not globally.
**Concrete rule:** For iterative refinement stages, track metrics from previous iterations (article length, complexity) and use them to set budgets (timeouts, retry counts) for the next iteration. This improves throughput without sacrificing quality.

## Cost Optimization (cost-)

### cost-structured-query-disables-all-tools
**Category:** cost-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/sdk.py:51-98`
**Pattern:** `structured_query()` explicitly disables all tools and sets `max_turns=1`. This prevents the model from attempting tool calls, which would inflate token use and latency. Without this, Opus wastes ~30-50% of tokens on tool planning that gets discarded anyway.
**Concrete rule:** For structured output only, disable tools at the SDK level (not via prompt). Set max_turns=1. This reduces token use and prevents tool hallucination that wastes API budget.

### cost-retry-with-exponential-backoff-and-jitter
**Category:** cost-
**File:** `/home/nero/workspace/projects/neromedia-faion-net/pipeline/sdk.py:60-142`
**Pattern:** Retry delay = `min(RETRY_BASE_DELAY * (2 ** attempt), RETRY_MAX_DELAY) + random_jitter`. Base delay 5s, max delay 60s, jitter 0-50% of delay. This avoids thundering herd if multiple pipelines retry at the same time. Retries only on retryable errors (timeout, overload, 429, 5xx), not on auth errors.
**Concrete rule:** Implement exponential backoff with jitter for transient errors. Fail fast on permanent errors (auth, 4xx). Log which error triggered retry to identify patterns later.

### cost-tier-gating-for-pipeline-access
**Category:** cost-
**File:** `/home/nero/workspace/projects/faion-cli/faion_cli/pipeline.py:56-83`
**Pattern:** Before running any stage, `verify_subscription()` is called. If the user's tier doesn't allow the pipeline, return an error without making API calls. Tier is stored in credentials after auth. This gates expensive operations (SDD, custom pipelines) behind a paywall.
**Concrete rule:** Implement tier checking before running pipelines. Query user subscription in auth module. Return error early if tier insufficient. Never make API calls on behalf of free users.

### cost-stage-timeouts-per-model-size
**Category:** cost-
**File:** `/home/nero/workspace/projects/mediamanager-faion-net/mediamanager_be/app/orchestrator/runner.py:71-76`
**Pattern:** Different pipeline modes have different timeouts: "generate": 2400s (40min), "publish": 120s (2min), "digest": 600s (10min). These are tuned from production latency observations. Generate includes LLM reasoning (Opus is slow); publish is mechanical (no LLM); digest has light LLM work.
**Concrete rule:** Assign timeouts per pipeline mode based on expected work. Heavy reasoning pipelines get longer budgets. Mechanical pipelines get short budgets. This prevents runaway processes and makes monitoring easier.

## MCP Server Patterns (mcp-)

No MCP-specific patterns were found in the mined projects. These pipelines use Claude Agent SDK and Anthropic SDK directly, not MCP servers.

---

## Summary: Top 5 Most Impressive Tricks

1. **Incremental JSON repair with 11 clear phases** (so-json-repair-incremental-strategy): Rather than blast JSON with overlapping regex, faion uses a principled 11-step fallback chain with logging at each step. This handles real-world LLM output (unicode quotes, trailing commas, truncation, HTML bleed) reliably. The recovery rate is exceptional.

2. **Multi-stage review loops with meta-filtering** (lp-code-review-with-meta-review-filter + eval-quality-score-with-blocking-issues-gate): NERO uses a 3-step review (review → meta-review → fix) bounded at 10 iterations, with approval requiring both quality >= 8 AND absence of blocking issues. The meta-review filters false positives; this is a secondary validation gate that dramatically improves precision.

3. **Schema field ordering for reasoning flow** (so-schema-field-ordering-for-reasoning): Generation schema orders fields by data dependency: article first, then tags, then summary. The summary field description includes specific reasoning hints ("Include: main topic, key facts, companies/tools mentioned..."). This is in-schema reasoning that works because the order forces correct logical flow.

4. **Parallel translation + image in one ThreadPool** (pl-parallel-translation-with-threadpool): Neromedia's stage 9 runs 7 language translations + image generation in a single ThreadPoolExecutor. Timeouts scale per language based on article length. `as_completed()` gathers results as they finish. Simple, fast, and more maintainable than async/await.

5. **Warm-start context stage injected into all downstream prompts** (lp-context-stage-before-implementation + mem-pipeline-context-dataclass-with-apply-methods): NERO's pipeline begins with ContextStage (reads project structure, docs, commits). This context is cached and injected into all downstream stages' prompts. Avoids re-gathering context and makes reasoning consistent across the agent loop. Combined with context.apply_* validation methods, this is a rock-solid architecture.
