# Templates — Plan-Execute vs ReAct

## Plan-Execute (Pydantic + Anthropic)

```python
from pydantic import BaseModel
from typing import Literal

class PlanStep(BaseModel):
    step_id: int
    action: Literal["search", "read_file", "write_file", "run_tests", "open_pr"]
    args: dict
    depends_on: list[int]   # for DAG ordering

class Plan(BaseModel):
    goal_restate: str
    constraints: list[str]
    plan_steps: list[PlanStep]

def plan_execute(goal: str) -> Result:
    # 1. Plan
    plan = sonnet_call(goal, response_schema=Plan)

    # 2. Validate
    if not validate_plan(plan):
        raise PlanInvalid(plan)

    # 3. Execute (DAG order)
    state = {}
    for step in topological_sort(plan.plan_steps):
        state[step.step_id] = run_step(step, state)

    return summarize(state)
```

## ReAct (minimal)

```python
def react_loop(goal: str, tools: list[Tool], max_turns: int = 10):
    messages = [{"role": "user", "content": goal}]
    for turn in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-...",
            tools=tools,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            return resp.content
        for block in resp.content:
            if block.type == "tool_use":
                result = call_tool(block.name, block.input)
                messages.append({"role": "assistant", "content": resp.content})
                messages.append({"role": "user", "content": [
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
                ]})
    raise MaxTurnsExceeded()
```

## Hybrid (Plan + per-step ReAct)

```python
def hybrid(goal: str):
    plan = plan_call(goal)
    state = {"goal": goal, "results": {}}

    for step in plan.plan_steps:
        try:
            result = react_loop(
                goal=step.action_description,
                tools=tools_for(step.action),
                max_turns=5,
            )
            state["results"][step.step_id] = result
        except (MaxTurnsExceeded, StepFailed):
            new_plan = replan_call(state, failed_step=step)
            state["results"][step.step_id] = react_loop(
                goal=new_plan.recovery_action,
                tools=tools,
                max_turns=5,
            )
    return state
```

## "Stuck" detector

```python
def detect_stuck(history: list[dict]) -> bool:
    last_three_actions = [
        msg["content"][0]["name"] + str(msg["content"][0]["input"])
        for msg in history[-3:]
        if msg["role"] == "assistant" and msg["content"][0]["type"] == "tool_use"
    ]
    return len(set(last_three_actions)) == 1   # all three identical
```

## Plan output schema (LangGraph style)

```python
from typing import Annotated
from pydantic import BaseModel

class Step(BaseModel):
    description: str
    tool: str
    expected_output: str

class Plan(BaseModel):
    rationale: str
    steps: Annotated[list[Step], "minimum 1, maximum 10"]
```
