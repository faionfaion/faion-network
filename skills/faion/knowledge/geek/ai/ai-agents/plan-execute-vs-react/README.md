# Plan-Execute vs ReAct — Picking the Right Loop

**Category:** `lp-` (agent loops & control flow)

## The Rule

For tasks where the steps are **predictable from the goal**, use **Plan-Execute**: one big planning call produces a structured plan, then deterministic code (or a smaller agent per step) executes it. For tasks where the next step **depends on what you just learned**, use **ReAct** (or Reflexion): one model interleaving Thought → Action → Observation in a loop.

Mixing modes for the wrong job is the #1 cause of agent runs that meander or lock in early.

## Why It Works

- **Plan-Execute** front-loads reasoning. The plan is auditable BEFORE work starts; execution can be parallel; failures are localized to one step. But it cannot adapt — if reality differs from the plan's assumptions, the agent presses on regardless.
- **ReAct** adapts step-by-step. Each Action's Observation feeds the next Thought, so surprising tool outputs reshape the trajectory. But there's no plan to audit; loops can wander, retry, or hit max-turns.

The tradeoff is **adaptability vs auditability**. Pick by how much you can predict before starting.

## Decision Rule

| Signal | Use Plan-Execute | Use ReAct |
|--------|------------------|-----------|
| Goal decomposes into known sub-steps | ✅ | |
| Sub-steps are independent (parallelizable) | ✅ | |
| User wants to review the plan before run | ✅ | |
| Each step's input depends on previous output | | ✅ |
| Tool results often surprise (search, web, codebases) | | ✅ |
| Cost-bounded but exploratory | | ✅ (with max_turns) |
| Compliance/audit requirement on intermediate work | ✅ | |
| Long horizon, > 10 steps | Hybrid: plan top-level, ReAct each step | |

## Hybrid Pattern

The strongest production pattern is plan + ReAct-per-step:

1. Big-model **Plan** call: produce N structured sub-tasks
2. For each sub-task, spawn a small **ReAct** loop (max 5 turns) constrained to that sub-task
3. Each loop reports a slim result; aggregator updates a state document
4. Optional **Replan** call if a sub-task fails or surfaces a contradiction

This is what Claude Code, LangGraph supervisor+workers, and the deep-agents pattern all converge on.

## Anti-Patterns

| Anti-pattern | Why it hurts | Fix |
|--------------|--------------|-----|
| Pure ReAct on a 30-step goal | Loop wanders; no human can review trajectory | Add a planning step up front |
| Pure Plan-Execute on exploration | Plan is invented blind; first step's reality breaks the rest | Use ReAct or hybrid replan |
| ReAct without max_turns | Infinite loops on bad tool output | Always cap turns; surface "stuck" as a result |
| Plan-Execute that "plans inside execution" | Confusing trace; plan changes mid-run | Separate the calls: plan first, execute second |
| Replan every step | Same as ReAct but more expensive | Replan ONLY on failure or contradiction |

## Composition

- + **subagent-as-context-firewall**: each sub-task = subagent with isolated context
- + **stream-json-orchestration**: orchestrator watches stream events to decide replans
- + **schema-field-order**: planning-output schema = `[goal_restate, constraints, plan_steps]` (reasoning before answer)

## References

- [LangGraph Plan-and-Execute tutorial](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
- [ReAct: Synergizing Reasoning and Acting in Language Models (arxiv 2210.03629)](https://arxiv.org/abs/2210.03629)
- [Reflexion (arxiv 2303.11366)](https://arxiv.org/abs/2303.11366)
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/research/built-multi-agent-research-system)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
