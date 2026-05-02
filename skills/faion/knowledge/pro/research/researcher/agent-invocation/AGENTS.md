# Agent Invocation Reference

## Summary

Reference for invoking faion-researcher agents from orchestrators. Covers two agents (`faion-research-agent` with 9 modes, `faion-domain-checker-agent`) and a sequential workflow pattern where each mode's output feeds the next. All outputs land in `.aidocs/product_docs/`.

## Why

The mode-dispatch pattern in the original README uses pseudocode that does not match Claude Code's actual `Task` tool semantics — `subagent_type` must match the literal `name:` in agent frontmatter, not a runtime string. This reference documents the correct invocation shape, sequential constraint, and output-path convention so orchestrators do not hallucinate mode routing or trigger rate-limit cascades from parallel calls.

## When To Use

- Orchestrating a multi-stage research run (ideas → market → competitors → pains → personas → validate → niche → pricing → names → domain-check).
- Picking the right mode for a user "research X" request without polluting parent context.
- Naming + domain-check workflows where `names` mode must chain to `faion-domain-checker-agent`.
- Ensuring outputs land deterministically in `.aidocs/product_docs/<file>.md` for downstream consumption by `faion-sdd` or `faion-product-manager`.

## When NOT To Use

- One-off factual lookup (single TAM number, single competitor URL) — call `WebSearch` directly; a research subagent costs 10x more tokens.
- Internal codebase research — use `Grep`/`Glob`/`Agent` instead; this agent is tuned for external web sources.
- Purely creative ideation (brand voice, copy variants) — use `brainstorm` instead of `mode: ideas`.
- Project already has fresh `market-research.md` / `competitive-analysis.md` — re-running burns budget; read existing files first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-modes.xml` | 9 research modes: agent, prompt pattern, required context, output file |
| `content/02-workflows.xml` | Multi-mode sequential workflow rules, error handling, output path map |
| `content/03-gotchas.xml` | Critical agent gotchas: subagent_type mismatch, sequential constraint, hallucinated URLs, context overflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/research-run.sh` | Bash dispatcher that drives modes sequentially with output-path tracking |

## Scripts

none
