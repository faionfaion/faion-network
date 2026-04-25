# Examples — Plan-Execute vs ReAct

## Example 1: Plan-Execute fits — code review pipeline

Goal: review PR #123. Sub-steps known: fetch diff → analyze each file → summarize → post comment.

Plan-Execute is right: each step is independent, parallelizable, the order is fixed, and the human reviewer can audit the plan before it runs.

## Example 2: ReAct fits — debugging a flaky test

Goal: figure out why test X flakes.

ReAct is right: the next action depends on what stack trace appears. Search → read file → grep → run test → check log. Each tool's output reshapes the next thought.

## Example 3: Hybrid fits — implement a feature from a spec

Plan: parse spec → for each requirement (1-N) → write code → write test → run tests → fix on failure → open PR.
Per-step ReAct: each sub-task has its own loop bounded to 5 turns; if a step's loop maxes out, a replan call decides whether to relax the requirement or escalate.

This is the Claude Code default for big tasks.

## Example 4: Anti-example — pure ReAct on a 30-step refactor

A 30-step framework migration done in raw ReAct goes off the rails:
- Loops on the same import 4 times before realizing the dependency renamed
- Forgets earlier decisions due to context compaction
- No human can review the trajectory because there's no plan to compare against

Fix: add a Plan call up front producing the migration steps; ReAct each step bounded.

## Example 5: Anti-example — Plan-Execute for web search

A research agent given "what is the current Anthropic pricing?" with a strict plan ["search → click first link → extract"] often fails: first link is wrong; extraction returns nothing. The right approach is ReAct, which adapts after each search.

## Example 6: Replan trigger

```
plan: [step1, step2, step3]

step1 succeeds
step2 fails with "schema mismatch"

→ trigger replan with state {"step1_done": True, "step2_error": "schema mismatch"}
→ new plan: [migrate_schema, retry_step2, step3]
```

Replan converts a stuck Plan-Execute into Plan-Execute-Plan. Don't replan on every step (that's just ReAct in costume).

## Example 7: faion-cli hybrid

Top-level: Plan (one Sonnet call) → 4 SDD tasks.
Per-task: ReAct (each task has its own subagent with 8-turn budget).
Aggregator: gathers results into `state.json`.
Replan trigger: a failed task's subagent reports `confidence: low` → orchestrator triggers replan with the failure context.

## Example 8: Audit trail

Plan-Execute's auditability is its biggest selling point. The plan document is immutable input to execution; it can be reviewed, signed off, and replayed. For regulated work (legal, finance, healthcare), this matters more than adaptability.
