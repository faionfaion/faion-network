# Plan-Execute pattern with model tiering
# Opus for planning, Haiku for execution, Sonnet for synthesis

def plan_execute(goal: str, tools: dict, max_tasks: int = 10) -> str:
    # Expensive model for planning — decomposition requires deep task understanding
    plan = opus_call(f"Decompose into ordered tasks (max {max_tasks}): {goal}")
    tasks = parse_task_list(plan)

    # Validate plan has no circular dependencies before executing
    assert_no_cycles(tasks)

    results = []
    for task in tasks:
        # Cheap model for mechanical execution
        for attempt in range(3):
            result = haiku_call(
                f"Execute: {task.description}\nContext: {results}\nTools: {list(tools)}"
            )
            tool_result = run_tools_if_needed(result, tools)
            if tool_result is not None:
                results.append({"task": task.description, "result": tool_result})
                break
        else:
            # Three failures: return to planner
            plan = opus_call(
                f"Revise plan — task '{task.description}' failed 3 times.\n"
                f"Completed: {results}\nGoal: {goal}"
            )
            tasks = parse_task_list(plan)

    # Balanced model for synthesis
    return sonnet_call(f"Synthesize final answer from: {results}\nGoal: {goal}")
