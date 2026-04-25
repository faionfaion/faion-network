# Checklist — Trajectory Evaluation with OTel GenAI Spans

## Instrumentation

- [ ] Every LLM call wrapped in a span with `gen_ai.system`, `gen_ai.request.model`
- [ ] Token counts captured: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, cache read/create
- [ ] `gen_ai.response.finish_reason` recorded
- [ ] Every tool call wrapped in a child span with name, args hash, outcome, duration
- [ ] Agent run wrapped in a root span with goal, outcome, totals
- [ ] Subagent spans nested under parent agent's span

## Eval suite

- [ ] Eval scores on 3 axes minimum: outcome, trajectory (path length), resources (cost/tokens)
- [ ] Outcome scorer: rule-based or LLM-as-judge with structured rubric
- [ ] Trajectory scorer: count steps, detect loops, identify wasted work
- [ ] Resource scorer: tokens, cost, latency, cache hit rate
- [ ] Eval runs in CI on every prompt/model/tool change

## Backend

- [ ] OTLP exporter configured (gRPC or HTTP)
- [ ] Backend chosen: Langfuse, Phoenix, Datadog, Honeycomb, or self-hosted Jaeger
- [ ] PII redaction at the collector boundary
- [ ] Trace retention policy defined (typical: 7-30 days hot, longer in archive)

## Replay

- [ ] Spans carry enough info to replay the call (model, prompt hash, tool args)
- [ ] Replay tooling exists for at least the LLM-call spans
- [ ] Replay used for regression debugging (not just for live ops)

## Composition

- [ ] cache hit rate tracked over time as a regression signal
- [ ] Subagent depth tracked (deeper hierarchies often indicate poor decomposition)
- [ ] Cost per task type tracked (find expensive task templates and target optimization)
