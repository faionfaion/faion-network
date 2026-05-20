---
slug: role-specialized-models
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Assign different models to different cognitive ROLES, not different subtasks.
content_id: "f95cb4f5c3c16e31"
tags: [models, cost-optimization, multi-agent, claude, role-specialization]
---
# Role-Specialized Models per Agent Step

## Summary

**One-sentence:** Assign different models to different cognitive ROLES, not different subtasks.

**One-paragraph:** Assign different models to different cognitive ROLES, not different subtasks. The empirical split that works in production: planning and review get the strongest model, execution and code-writing get the mid model, and classification, slot-filling, and formatting get the smallest model. In Claude Code subagents this maps to `model:` per agent definition; in LangGraph/CrewAI it maps to per-node LLM. The split is by cognitive demand, not by which step happens to be next in the pipeline.

## Applies If (ALL must hold)

- Multi-step agents where steps have genuinely different cognitive demands (planning vs typing vs labelling).
- Claude Code projects where you can pin `model:` per subagent (`planner: opus`, `implementer: sonnet`, `classifier: haiku`).
- Pipelines with an explicit plan-execute-review loop — review is often the second-best place to spend the strong model.
- Workloads where token cost is dominated by a long execution step that does not require frontier reasoning.

## Skip If (ANY kills it)

- Single-turn workloads where there is one cognitive role, one call.
- Pipelines with heavy state hand-off where model swap loses too much signal — switching mid-conversation drops the cheaper model into a context the stronger model populated.
- Cold starts and prototypes — pin everything to the strong model first, profile, then specialize roles where the data justifies it.
- Chains of equally hard steps (every step is reasoning) — the split has no leverage; routing or cascade is a better fit.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
