# Templates — Trajectory Evaluation with OTel GenAI Spans

## Python — instrument an Anthropic call

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

## Python — instrument a tool call

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

## Eval rubric (outcome + trajectory + resources)

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

## CI eval gate

```yaml
# .github/workflows/agent-eval.yml
name: agent-eval
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - run: python -m agent.eval.run --suite golden_50 --otlp-endpoint=$LANGFUSE_OTLP
      - run: python -m agent.eval.gate --min-outcome=0.95 --max-cost-regression=0.10
```

The gate fails the PR if outcome drops or cost regresses by > 10%.

## Subagent span nesting

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

## Langfuse decorator pattern

```python
from langfuse.decorators import observe

@observe()
def agent_step(input):
    # inputs/outputs auto-captured to Langfuse
    return llm_call(input)
```
