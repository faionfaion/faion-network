# Trajectory Evaluation with OTel GenAI Spans

## Summary

**One-sentence:** Score agent runs across outcome / trajectory / resources axes using OTel GenAI spans + tool child spans, validated by a per-run eval-report schema and gated in CI.

**One-paragraph:** Two agents can both succeed but burn 11x different resources and walk 7x different path lengths. Outcome-only eval ("% correct") hides cost and step regressions until the monthly bill arrives. This methodology forces OpenTelemetry GenAI semantic conventions on every LLM call, child spans on every tool dispatch, prompt content stored by SHA-256 hash with a side store, and a three-axis rubric (outcome, trajectory, resources) baked into the eval-report schema. CI gates PRs on regressions &gt; 25% on any axis. Replay-based debugging becomes trivial: spans carry enough state to re-run a failed call against a sandbox.

**Ефективно для:**

- Production-агенти з регресіями cost'у після model-bump'а — три-axis eval ловить ще до monthly bill'у.
- A/B prompts/моделей: outcome equal, але trajectory або resources показують справжній winner.
- Compliance / audit: replay-based debugging з spans = повне відтворення прод-помилки за хвилини.
- Subagent-architecture: span-nesting depth — рання попередження про неконтрольований fan-out.

## Applies If (ALL must hold)

- Agent runs in production or staging where regressions matter (cost, latency, correctness all observable).
- An OTLP backend exists or can be provisioned (Langfuse / Phoenix / Datadog / Helicone / open-source).
- An eval set of ≥50 representative tasks with ground-truth answers exists.

## Skip If (ANY kills it)

- One-shot personal scripts where instrumentation cost exceeds the run cost.
- Hard-PII contexts where redaction at the span boundary is not feasible (use a privacy-preserving collector first).
- Latency-critical sub-millisecond inference paths where even 1ms span overhead matters.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Application source | Python / TS / Go | repo |
| OTLP endpoint | URL + auth | observability backend |
| Eval set | 50+ task prompts + ground-truth answers | recorded user requests / synthetic set |
| Baseline scores | JSON | first eval run committed to repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[terse-default-tool-output]] | Verbose tool outputs are the most common cause of resource-axis regressions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-axis, otel-genai-semconv, tool-span, hash-not-paste, ci-eval-gate | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for eval-report (run_id, scores, raw, verdict, deltas) | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: outcome-only, ad-hoc-span-attrs, tool-blind-trace, inline-prompt-storage | 800 |
| `content/04-procedure.xml` | essential | 5-step setup: wire-tracer → instrument → rubric → run → ci-gate | 800 |
| `content/06-decision-tree.xml` | essential | Branches on regression class + loops + cache-hit drop | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wire_otel_tracer` | haiku | Boilerplate SDK setup; deterministic. |
| `instrument_llm_tools` | haiku | Wrapper-template application. |
| `outcome_judge` | sonnet | LLM-as-judge needs reasoning when ground truth is open-ended. |
| `regression_analyst` | opus | Cross-axis correlation + root-cause synthesis at release-gate time. |

## Templates

| File | Purpose |
|------|---------|
| `templates/python-instrument-anthropic.py` | OTel-instrumented Anthropic call with full `gen_ai.*` attribute set |
| `templates/python-instrument-tool.py` | Tool dispatcher wrapped in `agent.tool.&lt;name&gt;` child span |
| `templates/langfuse-decorator.py` | `@observe()` shortcut for Langfuse-OTel bridge |
| `templates/subagent-span-nesting.py` | Parent-agent → subagent span hierarchy pattern |
| `templates/eval-rubric.py` | Pydantic model for the 3-axis rubric + LLM-as-judge structured output |
| `templates/ci-eval-gate.yml` | GitHub Actions workflow gating PRs on the eval report |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trajectory-eval-otel.py` | Validate an eval-report JSON against the schema | CI on each eval run; pre-commit on baseline updates |

## Related

- [[terse-default-tool-output]] — resource-axis regressions usually trace to verbose tool outputs.
- [[tool-description-as-prompt]] — trajectory regressions often correlate with description drift.

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on which axis regressed &gt; 25% (outcome / trajectory / resources). For trajectory, it asks whether loops are present (same tool + args ≥3 times). For resources, it checks whether the cache hit ratio dropped (prompt-prefix change) or stayed flat (tool-verbosity growth). Each leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/python-instrument-anthropic.py`

```python
from opentelemetry import trace
from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as gai
from anthropic import Anthropic

tracer = trace.get_tracer("agent")
client = Anthropic()

def call_claude(messages, tools, model="claude-sonnet-..."):
    with tracer.start_as_current_span("agent.llm_call") as span:
        span.set_attribute(gai.GEN_AI_SYSTEM, "anthropic")
        span.set_attribute(gai.GEN_AI_REQUEST_MODEL, model)

        resp = client.messages.create(
            model=model, messages=messages, tools=tools, max_tokens=2048
        )

        span.set_attribute(gai.GEN_AI_USAGE_INPUT_TOKENS, resp.usage.input_tokens)
        span.set_attribute(gai.GEN_AI_USAGE_OUTPUT_TOKENS, resp.usage.output_tokens)
        span.set_attribute("gen_ai.usage.cache_read_tokens", resp.usage.cache_read_input_tokens or 0)
        span.set_attribute(gai.GEN_AI_RESPONSE_FINISH_REASONS, [resp.stop_reason])
        return resp
```

### `templates/python-instrument-tool.py`

```python
def run_tool(name: str, args: dict):
    with tracer.start_as_current_span(f"agent.tool.{name}") as span:
        span.set_attribute("agent.tool.name", name)
        span.set_attribute("agent.tool.args_hash", hash_args(args))
        try:
            result = TOOL_REGISTRY[name](**args)
            span.set_attribute("agent.tool.outcome", "success")
            return result
        except Exception as e:
            span.set_attribute("agent.tool.outcome", "error")
            span.record_exception(e)
            raise
```

### `templates/langfuse-decorator.py`

```python
from langfuse.decorators import observe

@observe()
def agent_step(input):
    # inputs/outputs auto-captured to Langfuse
    return llm_call(input)
```

### `templates/subagent-span-nesting.py`

```python
def parent_agent(goal):
    with tracer.start_as_current_span("agent.run", attributes={"agent.goal": goal}):
        # subagent span will be a child automatically
        result = run_subagent("investigate")
        ...

def run_subagent(task):
    with tracer.start_as_current_span("agent.subagent", attributes={"agent.task": task}):
        ...
```

### `templates/eval-rubric.py`

```python
from pydantic import BaseModel

class EvalRubric(BaseModel):
    outcome_score_0_to_1: float    # task-success
    trajectory_score_0_to_1: float # path optimality
    resource_score_0_to_1: float   # 1 - normalized_cost

def score_run(trace) -> EvalRubric:
    outcome = score_outcome_with_judge(trace.final_answer, trace.goal)
    trajectory = 1 - min(1, (trace.steps - optimal_steps) / 10)
    resource = 1 - min(1, trace.total_cost / max_acceptable_cost)
    return EvalRubric(
        outcome_score_0_to_1=outcome,
        trajectory_score_0_to_1=trajectory,
        resource_score_0_to_1=resource,
    )
```

### `templates/ci-eval-gate.yml`

```yaml
name: agent-eval
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - run: python -m agent.eval.run --suite golden_50 --otlp-endpoint=$LANGFUSE_OTLP
      - run: python -m agent.eval.gate --min-outcome=0.95 --max-cost-regression=0.10
```
