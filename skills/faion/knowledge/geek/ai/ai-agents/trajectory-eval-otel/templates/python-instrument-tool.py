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
