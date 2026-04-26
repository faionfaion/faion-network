# Checklist — Plan-Execute vs ReAct

## Decide which mode

- [ ] Listed 5-10 representative tasks the agent will face
- [ ] For each, marked predictable-vs-exploratory
- [ ] Counted: > 70% predictable → Plan-Execute baseline
- [ ] > 70% exploratory → ReAct baseline
- [ ] Mixed → Hybrid (plan top-level, ReAct per step)

## Plan-Execute setup

- [ ] Planning prompt produces a STRUCTURED plan (not free text)
- [ ] Plan schema has goal_restate before plan_steps (reasoning-before-answer)
- [ ] Each plan step is independently runnable
- [ ] Plan validation step (sanity check) before any execution
- [ ] Replan trigger defined (e.g., on step failure)

## ReAct setup

- [ ] Always set `max_turns` (typical: 5-15)
- [ ] Always set `max_total_tokens` budget
- [ ] Tool descriptions written for ReAct context (use-when/NOT-use-when)
- [ ] Loop emits structured Thought/Action/Observation events for tracing
- [ ] "Stuck" detection: same action 3x → break with diagnostic

## Hybrid setup

- [ ] Top-level plan is auditable BEFORE execution starts
- [ ] Per-step ReAct loops have small max_turns (3-5)
- [ ] Aggregator builds state document from per-step results
- [ ] Replan path is explicit (not implicit retry)

## Verify

- [ ] On 50 tasks, measured: success rate, avg turns, max turns
- [ ] No silent infinite loops
- [ ] Replan firing rate < 10% (otherwise the plan model is too weak)
- [ ] Auditability: can a human review the plan or trajectory after a failure?
