# AGENT-07: Multi-Model Orchestration

**Summary:** Production agents in 2026 are not single-model — they are mesh of cheap-fast classifiers/extractors/rerankers feeding a strong reasoner, with cost-aware routers, fallback chains, and role-specialized model assignment.
Headline finding: well-tuned cascades and routers reproduce 95-98% of GPT-4-class quality at 25-50% of the cost; getting there requires explicit per-step model choices, not "one model rules all."

---

## mm-01 — Cascade with confidence-thresholded escalation (FrugalGPT)

**Rule:** Run the cheapest model first. Only escalate to the next model in the chain if a confidence/scoring head says the cheap answer is below threshold. Tune thresholds against a held-out eval set.

**URL:** https://arxiv.org/abs/2305.05176 (FrugalGPT, Chen/Zaharia/Zou 2023, TMLR 2024) — "match performance of best individual LLM with up to 98% cost reduction."

**When to use:** High-volume, query-mix workload where a known fraction of queries are easy (FAQ, classification, short summaries). Stable task type so thresholds generalize.
**When NOT to use:** Adversarial/safety-critical pipelines where a wrong-but-confident cheap answer is unacceptable; tasks where the cheap model's confidence is poorly calibrated.

**Tiny example:**
```
1. Haiku answers + emits self-score 0..1
2. If self-score < 0.7  → escalate to Sonnet
3. If Sonnet self-score < 0.6 → escalate to Opus
Only 8% of traffic hits Opus. Avg cost per query ↓ 73%.
```

---

## mm-02 — Preference-trained router (RouteLLM)

**Rule:** Train a small router (matrix factorization, BERT classifier, or similarity ranker) on Chatbot-Arena-style preference data to pick "weak vs strong model" per prompt before any inference happens. No cascade, single-shot routing decision.

**URL:** https://arxiv.org/abs/2406.18665 / https://github.com/lm-sys/RouteLLM — "95% of GPT-4 perf using only 26% GPT-4 calls, ~48% cheaper than random baseline."

**When to use:** You have telemetry to fine-tune the router on your own traffic. Latency-sensitive (cascade adds a round-trip; routing doesn't).
**When NOT to use:** Cold-start with no preference data; rapidly drifting distribution where the router goes stale.

**Tiny example:**
```python
from routellm.controller import Controller
client = Controller(routers=["mf"], strong_model="gpt-4", weak_model="mixtral-8x7b")
client.chat.completions.create(model="router-mf-0.11593", messages=...)
# 0.11593 = cost-quality knob
```

---

## mm-03 — Role-specialized models per agent step (Opus plans, Sonnet codes, Haiku parses)

**Rule:** Assign different models to different cognitive roles, not different "subtasks." The split that works empirically: **plan/review = strongest**, **execute/generate = mid**, **classify/extract/format = smallest**. In Claude Code subagents, set `model:` per agent definition.

**URL:** https://www.mindstudio.ai/blog/claude-code-advisor-strategy-opus-sonnet-haiku and https://claude.com/resources/tutorials/choosing-the-right-claude-model

**When to use:** Multi-step agents where steps have genuinely different cognitive demands (planning vs typing). Anthropic's own "Opus-as-adviser, Sonnet-as-executor" pattern.
**When NOT to use:** Single-turn workloads; pipelines where context handoff between models loses too much signal.

**Tiny example:**
```yaml
# .claude/agents/feature-impl.yaml
planner:    { model: opus,   role: "design + review" }
implementer:{ model: sonnet, role: "write code" }
classifier: { model: haiku,  role: "label files / pick paths" }
```

---

## mm-04 — Small-model rerank before strong-model reasoning (two-stage retrieval)

**Rule:** Retrieve 50-200 candidates with a cheap embedding model, rerank with a small cross-encoder (Cohere rerank-3, BGE-reranker, Voyage rerank-2.5), pass top 5-10 to the expensive reasoner. Never feed raw vector-search top-K straight into the LLM.

**URL:** https://www.pinecone.io/learn/series/rag/rerankers/ and https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/ — "+15 pp retrieval accuracy on enterprise benchmarks."

**When to use:** Any RAG agent. Sweet spot: rerank 50-75 candidates.
**When NOT to use:** Tiny corpora (< 100 docs total); latency budget under 200ms where the rerank round-trip dominates.

**Tiny example:**
```
user → embed (text-embedding-3-small)
     → ANN top-100 (Pinecone)
     → cross-encoder rerank top-10 (Cohere rerank-3)
     → Opus answer with top-10 chunks
```

---

## mm-05 — Speculative decoding at the agent step level

**Rule:** For tool-call-heavy agents, pair a small "draft" model that proposes the next K tokens (or next tool call) with the big "target" model that verifies in parallel. Acceptance rate α determines speedup; tune draft to maximize α at lowest VRAM cost.

**URL:** https://research.google/blog/looking-back-at-speculative-decoding/ and https://www.bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding — typical 2-3× speedup, no quality loss.

**When to use:** Self-hosted inference (vLLM, TGI, TensorRT-LLM); long-form code or repetitive structured output where draft α is high; multi-turn agents where ITL × N steps dominates UX latency.
**When NOT to use:** API-only (OpenAI/Anthropic don't expose this); creative/open-ended generation where α is low and you pay for both models without speedup.

**Tiny example:**
```
vllm serve Qwen2.5-72B-Instruct \
  --speculative-model Qwen2.5-1.5B-Instruct \
  --num-speculative-tokens 5
# 2.6× decode speedup observed on agent-tool traces
```

---

## mm-06 — Mixture-of-Agents: parallel proposers + aggregator

**Rule:** Run N diverse open-source models in parallel as "proposers," feed all their drafts into a single strong "aggregator" model that synthesizes the final answer. Layer 2-4× for further gains. Caveat: 2025 follow-up showed Self-MoA (one strong model proposing N times) often beats heterogeneous MoA.

**URL:** https://arxiv.org/abs/2406.04692 (Together AI MoA) and https://arxiv.org/html/2502.00674v1 (Rethinking MoA, 2025) — "MoA open-source 65.1% AlpacaEval vs 57.5% GPT-4o."

**When to use:** Open-ended, high-stakes single answers (legal drafts, research syntheses, code review); you have budget to spend 5-10× tokens for top-quality.
**When NOT to use:** Latency-sensitive UX (proposers run in parallel but you still wait for slowest); high-volume cheap calls (cost explodes); when one model is clearly dominant — Self-MoA wins.

**Tiny example:**
```
Layer 1 proposers (parallel): Qwen2.5-72B, Llama-3.3-70B, Mistral-Large
Layer 2 aggregator: Claude Opus
→ aggregator sees all 3 drafts + original prompt, writes final.
```

---

## mm-07 — Local-model PII redaction → cloud-model reasoning

**Rule:** A small local model (Presidio + DistilBERT NER, or OpenAI Privacy Filter running on-device) runs first to detect/mask PII. Only the redacted text leaves the box to the cloud LLM. Reverse the mask on the response. Combined "route locally + redact + rephrase" stack achieves <1% PII leak.

**URL:** https://thenewstack.io/openai-privacy-filter-pii/ (OpenAI Privacy Filter, 96% F1, runs locally, 128k token bidirectional classifier) and https://arxiv.org/html/2604.12064 (LLM-Redactor 8-technique eval).

**When to use:** Healthcare, legal, HR, finance, EU/GDPR. Anything touching customer records.
**When NOT to use:** Public-data agents (news scraping, web research) where the redaction tax is pure overhead.

**Tiny example:**
```
input → presidio.analyze() → replace [PERSON_1], [EMAIL_1], [PHONE_1]
      → Claude API
      → response → re-substitute [PERSON_1] → real name → user
Audit log keeps both versions for 30 days.
```

---

## mm-08 — Cost-aware gateway with auto-router + fallback chain (OpenRouter pattern)

**Rule:** Don't hard-code the model. Hit a gateway that (a) auto-picks per-prompt from a curated set, (b) on provider error/timeout falls through an ordered list. Use `:floor` for cheapest, `:nitro` for fastest, explicit chain for SLA. Bill only successful runs.

**URL:** https://openrouter.ai/docs/features/model-routing and https://openrouter.ai/docs/guides/routing/model-fallbacks — Auto Router + Zero Completion Insurance.

**When to use:** Production with availability SLA; multi-region or rate-limited at single provider; team experimenting with new models without code change.
**When NOT to use:** Strict data-residency/compliance (gateway is a third party); when you need raw vendor SDK features (prompt caching, batch API, fine-tunes).

**Tiny example:**
```python
client.chat.completions.create(
    model="anthropic/claude-opus-4",
    extra_body={"models": [
        "anthropic/claude-opus-4",
        "openai/gpt-5",
        "google/gemini-2.5-pro"
    ]}
)
# fallback fires on 5xx/429/timeout
```

---

## mm-09 — Distillation for high-volume stable workloads (vs prompt-routing)

**Rule:** Once a routed cheap-model call accounts for >100k req/day **and** the prompt template is stable, distill the strong-model behavior into a fine-tuned small model. Replace the routing decision with one direct call. Accept this is a 1-shot bet — if the prompt drifts, redo it.

**URL:** https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/ and https://leanlm.ai/blog/llm-cost-optimization — "Sonnet-level accuracy at Haiku pricing, ~75% cost cut, payback ~60 days at 100k/day."

**When to use:** Stable narrow task (classification, extraction, named slot-filling, fixed-schema rewrite). Volume amortizes training cost.
**When NOT to use:** Open-ended task; prompt under active iteration; less than ~50k/day volume; multi-skill agent where you'd need to distill 20 things.

**Tiny example:**
```
Phase 1 (months 0-3): RouteLLM, log all (input, Opus output) pairs
Phase 2 (month 3): fine-tune Llama-3.1-8B on 50k pairs
Phase 3: serve Llama-8B for 92% of traffic, RouteLLM only for top 8% novel queries
```

---

## mm-10 — Voice-agent split: STT + LLM + TTS as three different models, streamed

**Rule:** For real-time voice, do NOT use a monolithic speech-to-speech model unless you need <500ms full-duplex. Cascade: faster-whisper-turbo (STT, local) → reasoning LLM (cloud) → Kokoro/Piper/ElevenLabs Turbo (TTS). Stream partial transcripts into LLM and stream LLM tokens into TTS so all three overlap.

**URL:** https://livekit.com/blog/voice-agent-architecture-stt-llm-tts-pipelines-explained and https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture — "<1s end-to-end with full streaming."

**When to use:** Phone bots, voice assistants, accessibility tools where you need to swap any of the three independently (different TTS voices per locale, cheaper STT for one language).
**When NOT to use:** True low-latency conversational interrupt-handling — use OpenAI Realtime / Gemini Live speech-to-speech instead.

**Tiny example:**
```
mic → faster-whisper-turbo (streaming partials every 200ms)
    → Sonnet (token streaming)
    → ElevenLabs Turbo v2.5 (streaming TTS, 75ms first byte)
    → speaker  ## total <800ms, swap any leg independently
```

---

## mm-11 — One big call vs many small calls (token-economic decision rule)

**Rule:** Default to ONE big call when (a) tasks share context (cache hit > 0.5), (b) tasks must be globally consistent (same plan), or (c) latency budget is tight. Default to MANY small calls when (a) tasks are embarrassingly parallel, (b) failure of one task shouldn't kill the others, or (c) per-task model choice differs (cheap for some, expensive for others). Prompt-cache the shared prefix in the many-small case.

**URL:** https://www.anthropic.com/news/prompt-caching and https://callsphere.tech/blog/ai-agent-cost-optimization-strategies-production — prompt caching gives 90% discount on cached input.

**When big-call wins:** Code refactor across 10 files needing global type-consistency; "review this PR" with 8 sub-checks; planning that downstream depends on.
**When small-calls win:** Process 200 emails in parallel; per-row enrichment; map step of map-reduce.

**Tiny example:**
```
BAD:  one 200k-token call to "review and label 200 emails"  → blocks 90s
GOOD: 200× 1k-token Haiku calls in parallel, shared system prompt cached
      → 6s total, 1/30th the cost, partial failures don't lose everything
```

---

## mm-12 — Vision-language perceiver + text-LLM reasoner split

**Rule:** A small VLM (Gemma-3-Vision, Moondream, Qwen2-VL-7B) extracts structured observations from an image into JSON/text. A larger text-only reasoner (Opus, GPT-5) reasons over that JSON. Don't pay vision-model premium for the reasoning step.

**URL:** https://landing.ai/blog/visionagent-an-agentic-approach-for-complex-visual-reasoning and https://openreview.net/forum?id=ncCuiD3KJQ ("Visual Agents as Fast and Slow Thinkers").

**When to use:** Document understanding, screenshot agents, robotics, content moderation pipelines where many images per query but reasoning is the bottleneck.
**When NOT to use:** Pure visual tasks (captioning, OCR, segmentation) where there's no symbolic reasoning step worth offloading; tasks where the perceiver loses too much detail to text.

**Tiny example:**
```
screenshot → Qwen2-VL-7B local: extract {buttons:[...], errors:[...], state:'..'}
          → Opus: "given that JSON, decide next click"
Per-frame cost ↓ ~80% vs running Opus-vision every frame.
```

---

## Sources

- [FrugalGPT (arXiv 2305.05176)](https://arxiv.org/abs/2305.05176)
- [RouteLLM paper (arXiv 2406.18665)](https://arxiv.org/abs/2406.18665)
- [RouteLLM GitHub (lm-sys)](https://github.com/lm-sys/RouteLLM)
- [LMSYS RouteLLM blog](https://www.lmsys.org/blog/2024-07-01-routellm/)
- [Mixture-of-Agents (arXiv 2406.04692)](https://arxiv.org/abs/2406.04692)
- [Rethinking MoA / Self-MoA (arXiv 2502.00674)](https://arxiv.org/html/2502.00674v1)
- [Together AI MoA docs](https://docs.together.ai/docs/mixture-of-agents)
- [Pinecone two-stage rerank guide](https://www.pinecone.io/learn/series/rag/rerankers/)
- [ZeroEntropy reranker guide 2026](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/)
- [Google Research speculative decoding retrospective](https://research.google/blog/looking-back-at-speculative-decoding/)
- [BentoML 3x faster speculative decoding](https://www.bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding)
- [OpenRouter model routing docs](https://openrouter.ai/docs/features/model-routing)
- [OpenRouter model fallbacks](https://openrouter.ai/docs/guides/routing/model-fallbacks)
- [OpenRouter Auto Router](https://openrouter.ai/docs/guides/routing/routers/auto-router)
- [Claude model selection (Anthropic)](https://claude.com/resources/tutorials/choosing-the-right-claude-model)
- [Claude Code advisor strategy (MindStudio)](https://www.mindstudio.ai/blog/claude-code-advisor-strategy-opus-sonnet-haiku)
- [OpenAI Privacy Filter (The New Stack)](https://thenewstack.io/openai-privacy-filter-pii/)
- [LLM-Redactor 8-technique eval (arXiv 2604.12064)](https://arxiv.org/html/2604.12064)
- [Kong AI gateway PII sanitization](https://konghq.com/blog/enterprise/building-pii-sanitization-for-llms-and-agentic-ai)
- [LiveKit voice agent architecture](https://livekit.com/blog/voice-agent-architecture-stt-llm-tts-pipelines-explained)
- [Softcery realtime vs cascading voice](https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture)
- [LandingAI VisionAgent](https://landing.ai/blog/visionagent-an-agentic-approach-for-complex-visual-reasoning)
- [Visual Agents Fast and Slow Thinkers (OpenReview)](https://openreview.net/forum?id=ncCuiD3KJQ)
- [AWS Bedrock cost optimization](https://aws.amazon.com/blogs/machine-learning/effective-cost-optimization-strategies-for-amazon-bedrock/)
- [LeanLM cost optimization](https://leanlm.ai/blog/llm-cost-optimization)
- [Anthropic prompt caching](https://www.anthropic.com/news/prompt-caching)
- [Martian LLM router (VentureBeat)](https://venturebeat.com/ai/why-accenture-and-martian-see-model-routing-as-key-to-enterprise-ai-success)
- [IBM Research LLM routers](https://research.ibm.com/blog/LLM-routers)
- [Microsoft BEST-Route (arXiv 2506.22716)](https://github.com/microsoft/best-route-llm)
- [RouterArena benchmark (arXiv 2510.00202)](https://arxiv.org/html/2510.00202v1)
- [NVIDIA LLM Router blueprint](https://github.com/NVIDIA-AI-Blueprints/llm-router)
- [Arize agent router best practices](https://arize.com/blog/best-practices-for-building-an-ai-agent-router/)
