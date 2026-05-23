# OpenAI Function Calling and Structured Outputs

## Summary

**One-sentence:** Disciplined caller for `client.chat.completions.create(tools=...)` and `client.beta.chat.completions.parse(response_format=Model)` — handles message order, parallel-tool coherence, refusals, and tool_choice gating.

**One-paragraph:** OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.beta.chat.completions.parse`, parallel tool calls, and multimodal extensions (DALL-E 3, Whisper, TTS). Primary distinction from generic tool use: structured outputs enforce schema compliance at the API level, not just by prompt instruction. Pipelines that drive external actions (writes, payments) must validate parallel tool calls for coherence before execution.

**Ефективно для:** AI-інженера, що під'єднує LLM до зовнішніх дій — закриває цикл tool_call → execute → result із гарантією схеми та порядку повідомлень.

## Applies If (ALL must hold)

- Reliable, schema-validated JSON extraction from unstructured text.
- Pipeline driving external actions (API calls, DB writes) triggered by model decisions.
- Multiple tools needed in one response (parallel tool calls) to cut round-trips.
- Image generation (DALL-E 3), speech-to-text (Whisper), or TTS alongside text LLM calls.
- Strict output enforcement where `json_object` mode alone is insufficient.

## Skip If (ANY kills it)

- Only need a JSON blob without schema strictness — `response_format={"type": "json_object"}` is simpler.
- Simple prompting + regex post-processing is sufficient.
- Schema is deeply nested (&gt;10 params) and the model mis-selects — simplify the schema first.
- Real-time audio generation at sub-200ms latency — TTS streaming is not suitable.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pydantic model | Python class | pipeline schema layer |
| Tool registry | dict[name, callable] | pipeline tools module |
| `OPENAI_API_KEY` | env var | vault / 1Password |
| Model id | string | gpt-4o or newer (parse requires it) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/openai-chat-completions` | Base SDK patterns (retry, finish_reason). |
| `geek/ai/llm-integration/tool-use-basics` | Generic tool-loop discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: message-order, parse-on-gpt-4o, refusal null-check, parallel-coherence, tool_choice gates, register-then-call | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one parse-record (model, parsed, refusal, tool_calls) + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair: wrong-order, refusal-ignored, parallel-contradiction, parse-on-old-model, missing-tool-result | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: define tools/model → call → branch tool_calls vs parsed → execute → append → final call | ~700 |
| `content/06-decision-tree.xml` | essential | Picks parse vs json_object vs free-form; tool_choice required vs auto | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-tool-schema` | sonnet | Per-domain tool schema authorship; balance verbosity with selection accuracy. |
| `extract-structured` | haiku | Per-call extraction with parse + Pydantic. |
| `audit-parallel-calls` | opus | Cross-call coherence when parallel writes contradict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pydantic-extraction.py` | Full structured-extraction caller with refusal handling and retry. |
| `templates/whisper-chunked.py` | Whisper transcription helper for &gt;25MB audio (chunked upload). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-function-calling.py` | Validate a parse/tool-call record JSON matches the output contract. | Post-call in pipeline; nightly audit. |

## Related

- [[openai-chat-completions]] — base SDK pattern.
- [[tool-use-basics]] — generic tool-loop discipline (provider-agnostic).
- [[structured-output-patterns]] — when parse is overkill.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks (a) `parse` vs `json_object` vs free-form by strictness need, (b) `tool_choice=required` vs `auto` by whether the pipeline depends on a tool result, and (c) parallel vs sequential by whether tool effects are commutative. Use it at every tool-using call site.
