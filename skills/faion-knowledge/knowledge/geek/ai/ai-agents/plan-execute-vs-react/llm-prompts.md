# LLM Prompts — Plan-Execute vs ReAct

## Prompt 1: Decide the mode

```
Given this task description, decide whether to use Plan-Execute, ReAct, or Hybrid.

Output STRICT JSON:
{
  "rationale": "...",
  "predictability_score_0_to_5": 0-5,
  "exploration_score_0_to_5": 0-5,
  "audit_required": bool,
  "recommended_mode": "plan_execute" | "react" | "hybrid",
  "max_turns_if_react": int
}

Task:
{task description}
```

## Prompt 2: Planner (Plan-Execute mode)

```
You are a planner. Produce a STRUCTURED plan for the task below.

Schema:
{
  "goal_restate": "1 sentence",
  "constraints": ["list"],
  "plan_steps": [
    {"step_id": 1, "action": "...", "args": {...}, "depends_on": []}
  ]
}

Rules:
- Each step is independently runnable
- depends_on enables DAG order
- Max 10 steps; if more needed, say so in goal_restate
- Tool names limited to: {available_tools}

Task:
{task}
```

## Prompt 3: ReAct system prompt

```
You operate in a Thought → Action → Observation loop.

After each tool call, observe the result and reflect:
- Did this match expectations?
- Has the goal been reached?
- What's the next concrete step?

If you find yourself repeating the same action with no progress, output `<stuck>` and explain.

You have at most {max_turns} turns. Use them sparingly.
```

## Prompt 4: Replan trigger

```
A Plan-Execute run hit a failure. Decide whether to retry, replan, or escalate.

State:
{state}

Failed step:
{step}

Error:
{error}

Output:
{
  "decision": "retry" | "replan" | "escalate",
  "rationale": "...",
  "new_plan_if_replan": [...]   // only if decision == "replan"
}
```

## Prompt 5: Trajectory reviewer

After a ReAct run, review the trajectory:

```
Review this trajectory. For each step, mark:
- on_path | exploring | wandering | stuck

Then summarize: was this trajectory efficient? Could a Plan-Execute version have been better?

Trajectory:
{thoughts/actions/observations}
```
