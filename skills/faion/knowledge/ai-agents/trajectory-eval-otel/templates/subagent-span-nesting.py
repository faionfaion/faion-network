# purpose: parent-agent → subagent span hierarchy pattern
# consumes: tracer instance, agent runs, eval-set tasks
# produces: OTel spans / eval-report rows conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (three-axis-required, otel-genai-semconv, tool-span-required, hash-not-paste, ci-eval-gate)
# token-budget-impact: instrumentation overhead < 1ms / span; eval-report ~200 tokens / run
def parent_agent(goal):
    with tracer.start_as_current_span("agent.run", attributes={"agent.goal": goal}):
        # subagent span will be a child automatically
        result = run_subagent("investigate")
        ...

def run_subagent(task):
    with tracer.start_as_current_span("agent.subagent", attributes={"agent.task": task}):
        ...
