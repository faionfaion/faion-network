# Chaos-Eval — Fault Injection on Agent Tools

## Summary

A standard eval set runs tools that always succeed. Production tools fail: timeouts, 5xx errors, rate limits, corrupted return values, MCP server disconnects. Chaos-eval injects each failure mode at random points along the agent's trajectory and grades not "did it succeed?" but "did it recover, retry intelligently, escalate when blocked, or produce a confidently-wrong answer?". Without it, your reported success rate is a sunny-day distribution that lies the moment the network blinks.

## Why

ReliabilityBench (arXiv 2601.06112, 2026) and the agent-chaos benchmark show that agents which pass standard evals at 90%+ frequently collapse below 50% under realistic fault rates of 5-10%. The 2025 work on stress-testing LLM agents (arXiv 2505.03096) replicates this across six frameworks. Chaos-eval is the only way to measure the resilience axis before users do; it also produces the failure-mode catalogue that drives retry policy and escalation design.

## When To Use

- Any agent past prototype that depends on external tools, web APIs, MCP servers, or remote LLMs.
- Pre-launch readiness gate alongside outcome and trajectory evals.
- Regression suite when retry / circuit-breaker / fallback logic changes.
- Building a "graceful degradation" story for SLAs and post-mortems.

## When NOT To Use

- Air-gapped agents with only deterministic local tools (rare in practice).
- Pure prompt-only generators with zero tool use — there is nothing to fault-inject.
- Pre-prototype phase — wait until tool surface is stable before investing.
- Tools whose failure modes are already exercised by record/replay traces from production — chaos-eval is for failure modes you have not yet seen in prod.

## Content

| File | What's inside |
|------|---------------|
| `content/01-failure-taxonomy.xml` | The five canonical failure modes (timeout, error, rate-limit, corrupt-return, disconnect) and what to inject for each. |
| `content/02-recovery-grading.xml` | Recovery rubric: recovered / retried-intelligently / escalated-correctly / wrong-confident — with concrete pass/fail definitions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/chaos-config.json` | Reusable fault-injection config: per-fault probability, seed, scope (per-tool or global), recovery thresholds. |
