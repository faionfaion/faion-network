# Trajectory Evaluation with OTel GenAI Spans

**Category:** `eval-` (evaluation)

## The Rule

Score agent runs on **three axes simultaneously**: outcome (was the answer right?), trajectory (was the path optimal?), and resources (tokens, cost, steps). A single-axis eval misleads — an agent that always succeeds but burns 50× more tokens than necessary is a bad agent.

Capture trajectories using **OpenTelemetry GenAI semantic conventions** so traces flow uniformly to Langfuse, Phoenix, Datadog, Helicone, or any OTLP backend.

## Why It Works

LLM agents have a multi-dimensional cost surface. Two agents can both "succeed" but differ wildly:

| Agent | Outcome | Steps | Tokens | Cost | Latency |
|-------|---------|-------|--------|------|---------|
| A | Correct | 3 | 8K | $0.04 | 12s |
| B | Correct | 22 | 90K | $0.45 | 180s |

A single "% success" metric scores them identically; the multi-axis view scores B as 11× worse on resources and 7× worse on path-length.

OTel GenAI spans (`gen_ai.*` attributes, `gen_ai.completion.tokens`, `gen_ai.system`, `gen_ai.operation.name`) make this measurable across vendors. Each agent step → a span; each tool call → a child span; the full run → a trace.

## What to Capture per Span

For each LLM call:
- `gen_ai.system` — provider (anthropic, openai, google)
- `gen_ai.request.model` — exact model
- `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`
- `gen_ai.usage.cache_read_tokens` and `gen_ai.usage.cache_creation_tokens`
- `gen_ai.response.finish_reason` — end_turn, max_tokens, tool_use

For each tool call:
- Tool name
- Argument hash (for replay)
- Outcome (success | error | timeout)
- Duration

For the agent run as a whole:
- Goal (input)
- Outcome (success | failure | partial)
- Total turns
- Total cost
- Total latency
- Final-answer fingerprint (hash for dedup)

## When To Use

- Production agents where you need to debug regressions
- A/B comparing prompts, models, or trajectories
- Cost optimization (find which tasks burn the most)
- Compliance / audit (regulated industries need replayable traces)
- Multi-agent systems where you need to know which subagent did what

## When NOT To Use

- One-shot personal scripts where instrumenting takes longer than the script
- When telemetry would leak PII; redact at the span boundary or use a privacy-preserving collector
- When the OTel overhead matters in latency-critical paths (rare; instrumentation is usually < 1ms per span)

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Eval = "% correct" only | Add token, step, and latency axes |
| Span attributes drift between providers | Stick to OTel GenAI conventions; map vendor specifics in attributes |
| Tracing the LLM call but not the tool result | Tool spans capture the half of the trajectory you actually need to debug |
| Storing full prompts in spans | Hash long content; store full content in a side store referenced by hash |
| No replay capability | Each span should carry enough state to re-run the call |
| Eval suite that runs ad-hoc | Make eval a CI step; regress on cost just like on correctness |

## Composition

- + **stream-json-orchestration**: each stream event → one span
- + **subagent-as-context-firewall**: subagent runs are nested traces under the parent
- + **prompt-cache-prefix-order**: cache_read_tokens shows up in spans — hit-rate monitoring is a side benefit

## References

- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Langfuse OTel integration](https://langfuse.com/docs/opentelemetry/get-started)
- [Arize Phoenix — agent trajectory eval](https://docs.arize.com/phoenix/evaluation/concepts-evals/agent-evals)
- [Helicone (proxy-based observability)](https://docs.helicone.ai/)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
