# purpose: @observe() shortcut for Langfuse-OTel bridge
# consumes: tracer instance, agent runs, eval-set tasks
# produces: OTel spans / eval-report rows conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (three-axis-required, otel-genai-semconv, tool-span-required, hash-not-paste, ci-eval-gate)
# token-budget-impact: instrumentation overhead < 1ms / span; eval-report ~200 tokens / run
from langfuse.decorators import observe

@observe()
def agent_step(input):
    # inputs/outputs auto-captured to Langfuse
    return llm_call(input)
