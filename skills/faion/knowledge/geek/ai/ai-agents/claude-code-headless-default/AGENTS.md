# Claude Code Headless As Default Agent Runtime

## Summary

When you need an autonomous agent for a coding, devops, or research task, invoke `claude -p "<prompt>"` as a subprocess instead of writing a custom Agent SDK loop. The Claude Code CLI ships with a battle-tested harness — filesystem, bash, git, MCP, plan mode, sub-agents, hooks, skills, automatic compaction — already wired together. Drop down to the Claude Agent SDK only when you have a concrete reason the CLI cannot satisfy: a non-coding domain, custom tools beyond MCP, programmatic control of the inner loop, or embedding inside a SaaS product that cannot shell out.

## Why

The Claude Code harness encodes hundreds of engineering decisions (tool gating, retry policy, context compaction, sub-agent spawning, plan mode, hook execution order) that you would otherwise re-implement and re-debug in your own SDK loop. Anthropic ships and updates that harness; you inherit fixes for free. The CLI exposes the same agent through `-p` headless mode with `--output-format stream-json` for orchestration. Reaching for the SDK first is the default-overengineering trap — measure CLI before building.

## When To Use

- Coding, devops, refactoring, or research tasks runnable from a shell.
- Cron jobs, GitHub Actions, queue workers, internal automation.
- Any task that benefits from filesystem + git + bash context out of the box.
- Multi-agent pipelines where the orchestrator can shell out to subprocesses.
- Prototyping an agent before deciding whether a custom SDK loop is justified.

## When NOT To Use

- Non-coding business workflows (sales triage, claims, invoice routing) — Agent SDK + custom tools is leaner.
- SaaS product embedding where the host process cannot fork subprocesses.
- Custom inner-loop control (intercept every tool call, branch the conversation tree) — needs SDK.
- Domains needing non-MCP tools that cannot be expressed as MCP servers.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cli-vs-sdk-decision.xml` | The decision rule: default CLI, switch to SDK only on concrete trigger. |
| `content/02-invocation-shape.xml` | Canonical headless invocation flags and stream-json wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/run-headless.sh` | Reference shell wrapper for headless `claude -p` with allowlisted tools and budget cap. |
