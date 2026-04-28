def parent_agent(goal):
    with tracer.start_as_current_span("agent.run", attributes={"agent.goal": goal}):
        # subagent span will be a child automatically
        result = run_subagent("investigate")
        ...

def run_subagent(task):
    with tracer.start_as_current_span("agent.subagent", attributes={"agent.task": task}):
        ...
