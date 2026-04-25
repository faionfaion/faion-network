# AGENT-04: Open-Source LLM Agents — Methodologies

Research subagent 4 of 10. Focus: Llama 3.x/4, Mistral/Mixtral/Codestral, Qwen2.5/3, DeepSeek V3/V3.2/R1, Groq/Together/Fireworks/Cerebras inference. April 2026.

Tag legend: `so-` structured output | `mm-` multi-model routing | `tu-` tool use | `pl-` planning | `lp-` loop control | `mem-` memory | `cli-` client/SDK | `eval-` evaluation | `cost-` cost | `mcp-` MCP

---

## 1. (so-, tu-) Force schema with grammar-constrained decoding (XGrammar > Outlines > LMFE)

**Rule.** When serving an open model that lacks first-class JSON mode (any local Llama/Qwen/Mistral via vLLM, SGLang, llama.cpp), wire `guided_json` / `--tool-call-parser hermes` plus a grammar backend. Default to **XGrammar** — it is the default backend in vLLM, SGLang, TensorRT-LLM, and MLC-LLM in 2026, with 3–10x faster mask construction than Outlines/LMFE and "near-zero" generation overhead. XGrammar-2 added 6x compile speedup specifically for tool-calling and explicitly supports OpenAI Harmony Response Format. Schema compliance = 100%; without grammar it's 70–95% depending on model.

**When to use.** Any production agent that needs typed JSON arguments, deterministic tool-call shape, or a strict enum-routed reply. Especially essential for sub-14B local models.

**When NOT to use.** Free-form prose generation (creative writing, summarization). Grammar locks the model into a regex/CFG and can degrade reasoning quality if the grammar is wider than necessary. Also avoid for models with a healthy native JSON mode (Mistral Large via API → use their `response_format: json_schema` instead).

**URLs.**
- https://github.com/mlc-ai/xgrammar
- https://github.com/dottxt-ai/outlines
- https://github.com/noamgat/lm-format-enforcer
- https://docs.vllm.ai/en/latest/features/structured_outputs.html
- https://arxiv.org/html/2601.04426 (XGrammar-2 paper)

---

## 2. (tu-, cli-) Use `--tool-call-parser hermes` for Qwen, `llama4_pythonic` for Llama 4, `llama3_json` for Llama 3.x

**Rule.** vLLM's auto tool-choice does NOT work without an explicit parser flag. Each open-model family emits tool calls in a different surface format: Qwen2.5/Qwen3/QwQ → Hermes XML-ish (`<tool_call>{...}</tool_call>`); Llama 3.1/3.3 → JSON-in-tags (`<|python_tag|>`); Llama 4 → Pythonic call literals (`[func(arg=val)]`); Mistral → JSON with `[TOOL_CALLS]`. Mismatch = vLLM returns the raw text in `content` and `tool_calls` stays empty, looking like the model "refused to call". Always set both `--enable-auto-tool-choice` and the matching `--tool-call-parser` plus a Jinja `--chat-template` override for tool-use cases.

**When to use.** Every self-hosted vLLM/SGLang deployment that exposes the OpenAI-compatible `/chat/completions` with tools. Always specify the parser even if the chat template "looks right" in tokenizer_config.json.

**When NOT to use.** Llama 3.2-1B/3B (smaller siblings emit no tool-call boundary tokens — vLLM docs flag this explicitly; use grammar-forced JSON output instead and parse manually). Skip native parser if you wrap the call with XGrammar tool-mode — they overlap.

**URLs.**
- https://docs.vllm.ai/en/latest/features/tool_calling/
- https://github.com/vllm-project/vllm/blob/main/docs/features/tool_calling.md
- https://qwen.readthedocs.io/en/latest/framework/function_call.html

---

## 3. (mm-, lp-, cost-) Route the inner loop to Groq/Cerebras, the planner to Together/Fireworks

**Rule.** Open-model agents win when you split the loop. **Inner loop (tight, few tokens, many calls — tool-arg formatting, classifier, route, validator)** → Groq (Llama-3.3-70B at 276 tok/s base, 1,665 tok/s with speculative decoding; TTFT 85–110ms) or Cerebras (~3,000 tok/s on Llama4Scout, 1,400 on Qwen3 235B, sub-second for entire turns). **Planner (long context, deeper reasoning)** → Together AI (broadest model catalog, cheaper than Fireworks on 55/101 shared models) or Fireworks (4x faster structured output vs vanilla vLLM, best DX/reliability). End-to-end agent latency drops 5–20x vs running everything on a single GPU-API provider.

**When to use.** Multi-step ReAct/AgentLoop with >5 LLM calls per task. Real-time UX (chat, voice). Dense token-budget pipelines (news/content workflows like neromedia).

**When NOT to use.** Single-shot heavy reasoning (DeepSeek R1, long-form planning) — Groq's catalog skews to smaller/faster models; routing the planner there sacrifices quality. Also skip Groq for >128k context windows — KV-cache doesn't fit on LPU as readily as on H100/Blackwell GPU providers.

**URLs.**
- https://groq.com/blog/new-ai-inference-speed-benchmark-for-llama-3-3-70b-powered-by-groq
- https://artificialanalysis.ai/providers/groq
- https://www.cerebras.ai/blog/2026Insights
- https://pricepertoken.com/endpoints/compare/fireworks-vs-together
- https://fast.io/resources/best-inference-providers-ai-agents/

---

## 4. (so-, tu-) Repair JSON before retrying — `json_repair` is 10x cheaper than re-prompting

**Rule.** Even with grammar decoding, real-world failures happen: truncation at `max_tokens`, mid-stream OOM, mismatched chat-template patches. Wrap every JSON parse in a 3-layer defense: (1) `json.loads`, (2) `json_repair.loads()` from `mangiucugna/json_repair` (handles missing quotes/commas/brackets, stray prose, truncation), (3) only then re-prompt the model with the error. Repair fixes ~85% of malformed outputs at zero LLM cost. Re-prompting wastes a full request roundtrip and often produces the same broken pattern.

**When to use.** Any agent calling open models in production, especially Q4/Q5 quantized GGUFs where instruction-following degrades 10–20% on JSON edge cases.

**When NOT to use.** When schema must be cryptographically validated (financial tx args) — repair can silently change semantics. Use grammar decoding + strict pydantic validation, fail loud on mismatch.

**URLs.**
- https://github.com/mangiucugna/json_repair
- https://github.com/sigridjineth/agentjson
- https://huggingface.co/syntheticlab/fix-json

---

## 5. (cost-, mem-, lp-) Stick to SGLang for prefix-heavy agent loops — RadixAttention beats vLLM block-level caching

**Rule.** Agent loops repeat the system prompt + tool schema + few-shot examples every step. SGLang's RadixAttention (token-level radix tree LRU) hits 6.4x throughput vs vLLM block-level caching on prefix-heavy workloads, and 29% advantage even on H100 (16,200 vs 12,500 tok/s). Hit rate on stable agent prompts often exceeds 60%; teams report 20–40% compute savings just from prefix caching. For Together/Fireworks/DeepSeek API consumers — they all do server-side caching (DeepSeek V3.2 ships automatic KV cache hits at $0.014/1M cached tokens), so structure prompts as `[stable system+tools] ++ [variable user/state]` and never interleave variable bits early.

**When to use.** ReAct loops, multi-agent systems with shared system prompts, RAG pipelines, batch document classification with same instructions. Self-hosted: SGLang. Hosted: DeepSeek/Together/Fireworks all reward this layout.

**When NOT to use.** One-shot generation, cold-start eval runs (cache won't have time to warm), workloads with random seeds in the system prompt (cache key changes every call).

**URLs.**
- https://docs.vllm.ai/en/latest/design/prefix_caching/
- https://medium.com/byte-sized-ai/prefix-caching-sglang-vs-vllm-token-level-radix-tree-vs-block-level-hashing-b99ece9977a1
- https://blog.squeezebits.com/guided-decoding-performance-vllm-sglang
- https://api-docs.deepseek.com/guides/thinking_mode

---

## 6. (cost-, lp-) Speculative decoding with a 1B–3B draft beats raising your API budget

**Rule.** For self-hosted Llama 3.3 70B, pair it with Llama 3.2 1B as the draft model — NVIDIA TensorRT-LLM measures 3.55x throughput; Cerebras/Groq specdec hit 1,665 tok/s on Groq Llama-3.3-70B-Specdec (6x base). End-to-end agentic tasks like SWE-Bench finish 1.8–4.5x faster. The 1B draft fits on the same GPU; verifier acceptance rate of ~2.94 tokens/call is typical. Snowflake Arctic Inference packages this as a drop-in vLLM plugin in 2026.

**When to use.** Any 70B+ self-hosted deployment with stable agent traffic. Especially valuable when single-step latency dominates (interactive agents, voice).

**When NOT to use.** Highly diverse outputs (creative writing, code with novel API calls) — acceptance rate plummets and overhead becomes net negative. Do NOT pair a 1B draft with a smaller verifier (8B) — the speedup is marginal because the verifier is already fast.

**URLs.**
- https://developer.nvidia.com/blog/boost-llama-3-3-70b-inference-throughput-3x-with-nvidia-tensorrt-llm-speculative-decoding/
- https://groq.com/blog/groq-first-generation-14nm-chip-just-got-a-6x-speed-boost-introducing-llama-3-1-70b-speculative-decoding-on-groqcloud
- https://www.snowflake.com/en/engineering-blog/fast-speculative-decoding-vllm-arctic/
- https://developers.redhat.com/articles/2025/11/19/speculators-standardized-production-ready-speculative-decoding

---

## 7. (tu-, eval-) Pick fine-tuned tool-use variants over general-instruct for 8B/13B agents

**Rule.** General-instruct sub-14B models are weak at tool selection. Use specialist variants: `Groq/Llama-3-Groq-8B-Tool-Use` (89.06% BFCL — top open-source 8B), `meetkai/functionary-medium-v3.x`, NousResearch `Hermes-3-Llama-3.1-70B`. They are full-FT + DPO on tool-use datasets. The accuracy gap vs vanilla Llama-3.1-8B-Instruct is ~15–20 BFCL points, which is the difference between a usable production agent and one that hallucinates 1-in-5 tool calls. For Qwen, qwen-agent ships its own Hermes-format default parser that beats prompt-only ReAct on the same model.

**When to use.** Any local/self-hosted agent under 14B parameters. Edge deployment on Mac M-series or single GPU. When you have a fixed tool catalog (≤32 tools).

**When NOT to use.** When you need >32 tools (Llama API caps at 32; specialist FTs often regress beyond their training distribution). When you need multilingual content+tools — many specialist FTs lose non-English ability.

**URLs.**
- https://groq.com/blog/introducing-llama-3-groq-tool-use-models
- https://huggingface.co/Groq/Llama-3-Groq-70B-Tool-Use
- https://gorilla.cs.berkeley.edu/leaderboard.html
- https://github.com/QwenLM/Qwen-Agent

---

## 8. (so-, cost-) Q5_K_M is the floor for agent quantization — Q4 silently breaks tool calling

**Rule.** Quantize down to Q5_K_M (or Q6_K) for local deployment, never below. Q4_K_M loses 15–20% on instruction-following benchmarks (C-Eval, MMLU-style retrieval) and tool-argument shape compliance degrades much faster than overall perplexity numbers suggest. Q5_K_M retains ~95–99% of BF16 quality with substantial memory savings. If you must go to Q4, mandatory pair with grammar-constrained decoding (methodology #1) — XGrammar masks compensate for the model's degraded structure prior. AWQ-INT4 is acceptable for ≥70B models because the redundancy absorbs more loss; for 7B–14B agents, stick to Q5_K_M minimum.

**When to use.** Local agent deployment (Mac, single 24/48GB GPU), edge devices, cost-sensitive self-hosting.

**When NOT to use.** Server-class deployment with H100/Blackwell — full BF16 / FP8 is faster on modern hardware than CPU-bound GGUF Q-anything. API consumers — quantization is provider's problem, focus on prompt instead.

**URLs.**
- https://willitrunai.com/blog/quantization-guide-gguf-explained
- https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i
- https://www.knightli.com/en/2026/04/11/llama-gguf-quantization-selection/
- https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks

---

## 9. (tu-, cli-) Mistral: set `tool_choice="any"` to force a call; default `auto` regresses to prose

**Rule.** Mistral Small/Large/Codestral via the official API support `tool_choice` with values `auto` (default), `any` (force any tool), `none`, or a specific tool name. Mistral's `auto` is more conservative than OpenAI's — on borderline prompts it often replies in prose with the tool args described inline. For agent steps where you KNOW a tool must be called (router stage, action executor), explicitly send `tool_choice="any"`. Bonus: it saves ~33 tokens of "you may call a tool" boilerplate vs `auto`. `tool_call_id` became mandatory in `tool` role messages in 2025; missing it now 400s.

**When to use.** Action steps in a planner→executor split, schema-routed dispatch, every step where prose output is a bug.

**When NOT to use.** Multi-step reasoning where the model legitimately should sometimes answer directly. Conversational agents where a forced tool call disrupts UX.

**URLs.**
- https://docs.mistral.ai/capabilities/function_calling
- https://docs.mistral.ai/capabilities/structured_output/json_mode
- https://docs.mistral.ai/getting-started/changelog/

---

## 10. (pl-, lp-) DeepSeek V3.2 thinking-mode tool calling — separate plan from execute, never mix

**Rule.** DeepSeek V3.2 introduced thinking-mode tool calling (V3.2 release Dec 2025). The model emits a chain-of-thought block before each tool decision. R1-0528 hits Tau-Bench Airline 53.5 / Retail 63.9 — competitive with proprietary 7-figure-budget agents. But: keep the thinking block server-side. Truncate before returning to downstream tools or you'll pollute their context with reasoning chatter and 2x your token cost. Use V3.2 for the planner; V3.2-non-thinking (or Llama 3.3 70B on Groq) for the executor — splitting saves ~40% on output tokens vs running everything in thinking mode.

**When to use.** Complex multi-step agents (5+ tools, branching plans). Tau-Bench-style customer service / API orchestration. Anywhere a smaller model gets stuck in tool-loop deadlocks.

**When NOT to use.** Simple route-and-call agents (use Llama-3-Groq-Tool-Use or Mistral Small instead — same accuracy, 5x cheaper). Real-time chat (thinking-mode adds 1–3s latency for the CoT block).

**URLs.**
- https://api-docs.deepseek.com/guides/thinking_mode
- https://api-docs.deepseek.com/news/news251201
- https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond
- https://magazine.sebastianraschka.com/p/technical-deepseek

---

## 11. (eval-) Test agents on BFCL V4 + tau²-bench, not on your own held-out set

**Rule.** Berkeley Function Calling Leaderboard V4 ships a holistic agentic eval (multi-turn, parallel calls, REST/Java/JS tool catalogs); tau²-bench (tau-cubed) covers retail/airline/banking with simulated user dialogues. Both are pip-installable (`bfcl-eval`, `tau2-bench`). Run them in CI before swapping a model in your agent pipeline. Public 2026 numbers: best open-source (Llama 3.1 405B) = 0.885 BFCL; specialist 8B FTs ~0.89 on simple, ~0.65 on multi-turn. Your custom eval will overfit to your prompt style; BFCL/tau-bench surface failure modes (parallel-call hallucination, multi-turn state drift) that you can't detect from tooling alone.

**When to use.** Before any model swap in production. As a smoke gate in CI when modifying chat templates or tool parsers. When picking among 8B-class specialists.

**When NOT to use.** As the only eval — open-source models score 2-5x worse than GPT-4-class on AgentBench multi-turn, but may still be perfect for your narrow domain. Always pair with a domain-specific eval (50–100 hand-labeled traces).

**URLs.**
- https://gorilla.cs.berkeley.edu/leaderboard.html
- https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard
- https://github.com/sierra-research/tau2-bench
- https://github.com/THUDM/AgentBench
- https://github.com/philschmid/ai-agent-benchmark-compendium

---

## 12. (mcp-, tu-) For local Llama/Qwen with MCP, generate the GBNF grammar from the MCP tool list at startup

**Rule.** llama.cpp ships a JSON-Schema → GBNF converter and llama-server's `--jinja` flag activates tool-use templates with auto-generated grammar. Workflow: at agent boot, list MCP tools → convert each `inputSchema` to GBNF → union them into one root grammar → pass via `grammar=` in every llama.cpp request. This eliminates the #1 failure mode of local-model MCP agents: malformed `tools/call` arguments. `llama-cpp-agent` library automates this for nested objects/enums/dicts. For vLLM/SGLang serving, the same effect via `guided_json` with the union schema.

**When to use.** Any local-LLM-driven MCP client. Edge agents that can't call hosted APIs. Privacy-sensitive deployments where the MCP server runs on the same machine.

**When NOT to use.** Hosted-model MCP (Claude/Anthropic, OpenAI) — they already enforce structured tool args server-side. Highly dynamic tool catalogs (tools change per request) — re-compiling GBNF every request adds 10–50ms; cache compiled grammars by tool-set hash.

**URLs.**
- https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
- https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- https://pypi.org/project/llama-cpp-agent/
- https://deepwiki.com/qualcomm/llama.cpp/8-structured-output-and-function-calling

---

## Summary

12 production-grade methodologies for open-source LLM agents in April 2026, covering grammar-forced structured output (XGrammar/Outlines/LMFE/GBNF), per-family tool-call parsers (Hermes/llama4_pythonic/llama3_json), inference-provider routing (Groq/Cerebras/Together/Fireworks tradeoffs), JSON repair before retry, prefix-cache-aware prompt layout (SGLang RadixAttention), speculative decoding, specialist tool-use fine-tunes, quantization floor (Q5_K_M), Mistral `tool_choice=any`, DeepSeek V3.2 thinking-mode planner/executor split, BFCL V4 / tau²-bench evaluation, and GBNF generation for local MCP agents. Each rule has paired when-to-use / when-NOT-to-use guidance and cites primary sources from huggingface.co, mistral.ai, groq.com, vllm.ai, mlc-ai, sglang, and Berkeley Gorilla.
