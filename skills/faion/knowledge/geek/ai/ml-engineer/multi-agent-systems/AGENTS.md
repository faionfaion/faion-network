# Multi-Agent Systems

## Summary

Multi-agent systems coordinate multiple AI agents to solve tasks that exceed a single agent's context, parallelism, or role boundaries. Use the Claude Agent SDK's subagent primitive: parent spawns children with typed contracts, waits for structured results, routes to the next stage. Keep orchestrators stateless (routing only); push state to a shared file or queue. Test single-agent mode first — only add multi-agent when single-agent demonstrably fails.

## Why

Single agents fail when tasks exceed context windows (&gt;100K tokens of reasoning), require parallel specialized work, or have natural role boundaries (planner/executor/critic). Multi-agent systems distribute these concerns — but only when the coordination overhead is less than the gain. 72% of enterprise AI projects (2025-2026) use multi-agent architectures, making framework selection and state management patterns critical skills.

## When To Use

- Task requires parallel specialized work: research + coding + review happening simultaneously
- Problem is too large for a single context window
- Workflow has natural role boundaries (planner, executor, critic, verifier)
- Iterative refinement loops benefit from adversarial agents (generator vs. critic)
- Long-running pipelines where intermediate outputs need validation checkpoints

## When NOT To Use

- Simple, linear task a single agent completes in one pass
- Low latency required — multi-agent adds orchestration overhead (2-5x latency)
- Budget is tight — multiple agents multiply token spend
- Team lacks observability tooling — debugging multi-agent failures is hard without traces
- Task has tight coupling between steps where parallelization creates conflicts

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | Framework comparison (LangGraph, CrewAI, AutoGen, Swarm), architecture patterns, selection guide |
| `content/02-rules.xml` | State management rules, orchestrator constraints, failure modes, production gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/sequential-pipeline.py` | Minimal 3-agent sequential pipeline (researcher → writer → reviewer) |
| `templates/orchestrator-prompt.txt` | Stateless orchestrator system prompt pattern |
