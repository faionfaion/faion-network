# purpose: tool dispatcher wrapped in agent.tool.<name> child span
# consumes: tracer instance, agent runs, eval-set tasks
# produces: OTel spans / eval-report rows conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (three-axis-required, otel-genai-semconv, tool-span-required, hash-not-paste, ci-eval-gate)
# token-budget-impact: instrumentation overhead < 1ms / span; eval-report ~200 tokens / run
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
