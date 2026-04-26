# Role-Specialized Models per Agent Step

## Summary

Assign different models to different cognitive ROLES, not different subtasks. The empirical split that works in production: planning and review get the strongest model, execution and code-writing get the mid model, and classification, slot-filling, and formatting get the smallest model. In Claude Code subagents this maps to `model:` per agent definition; in LangGraph/CrewAI it maps to per-node LLM. The split is by cognitive demand, not by which step happens to be next in the pipeline.

## Why

A single-model agent overpays on routine steps and underpays on hard reasoning. Anthropic's own "Opus-as-adviser, Sonnet-as-executor" pattern reports ~3x lower cost per shipped feature with no quality regression on internal eval suites. The mechanism is that planning steps consume a small fraction of total tokens (a 1k-token plan vs 50k tokens of execution) yet drive most of the quality, so spending the strongest model on the smallest token slice has outsized leverage. Conversely, classifying file paths or extracting names is a near-saturated capability where Opus and Haiku are within 1-2 pp of each other but Opus costs 60x more.

## When To Use

- Multi-step agents where steps have genuinely different cognitive demands (planning vs typing vs labelling).
- Claude Code projects where you can pin `model:` per subagent (`planner: opus`, `implementer: sonnet`, `classifier: haiku`).
- Pipelines with an explicit plan-execute-review loop — review is often the second-best place to spend the strong model.
- Workloads where token cost is dominated by a long execution step that does not require frontier reasoning.

## When NOT To Use

- Single-turn workloads where there is one cognitive role, one call.
- Pipelines with heavy state hand-off where model swap loses too much signal — switching mid-conversation drops the cheaper model into a context the stronger model populated.
- Cold starts and prototypes — pin everything to the strong model first, profile, then specialize roles where the data justifies it.
- Chains of equally hard steps (every step is reasoning) — the split has no leverage; routing or cascade is a better fit.

## Content

| File | What's inside |
|------|---------------|
| `content/01-role-split.xml` | The plan/execute/classify split, the cognitive-role taxonomy, and how to detect mis-assignments. |
| `content/02-handoff-rules.xml` | How to keep context coherent across model boundaries; what NOT to share; verification gates between roles. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agents.yaml` | Claude Code subagent definitions for planner / implementer / classifier with role-pinned models. |
