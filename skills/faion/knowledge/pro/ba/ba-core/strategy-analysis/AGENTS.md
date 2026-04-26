# Strategy Analysis

## Summary

BABOK Knowledge Area 6: four sequential tasks — analyze current state, define future state, assess risks, define change strategy — each with a strict input/output contract. Every future-state goal must carry metric, baseline, target, and target date. Every change strategy must include a "do nothing" option. Produce four artifact files (current-state.json, future-state.json, risk-register.json, change-strategy.md) gated by a router agent that refuses to advance past a missing or stale task.

## Why

Initiatives that start without a validated current-state analysis and a measurable future state produce change strategies disconnected from real gaps. A KA-6 router that checks artifact presence and freshness (no artifact older than 90 days) prevents silently stale strategy work from driving budget decisions.

## When To Use

- Onboarding a BA agent to BABOK KA-6 layout — canonical map a routing agent uses to pick a sub-task
- Audit or gap-check of strategy artifacts: cross-checking that all four KA-6 tasks were performed
- Generating BABOK-aligned task scaffolding before deeper requirements work begins
- Mapping legacy strategy documents into BABOK terminology for Jama, Polarion, or Modern Requirements ingestion
- Training prompt grounding when a custom agent must reason in BABOK terms

## When NOT To Use

- A non-BABOK strategy framework is already in force (Wardley mapping, OKR-only, JTBD-driven) — do not retrofit KA-6 on top
- Single-team backlog refinement — KA-6 is heavyweight; a one-page problem statement is enough
- Pure product-discovery experiments before any commitment — use lean-canvas / opportunity-solution-trees first
- Engineering-only refactors with no business-state change — KA-6 business-need framing produces noise

## Content

| File | What's inside |
|------|---------------|
| `content/01-ka6-tasks.xml` | Four KA-6 tasks with input/output contracts, technique selection, and known limitations |
| `content/02-agentic.xml` | KA-6 router pattern, four sub-routine agents, prompt patterns, AI gotchas, human checkpoints |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-need-statement.md` | Business need statement with strategic alignment and success metrics |
| `templates/gap-analysis.md` | Gap analysis table across process, technology, people, and data |
| `templates/validate-ka6.sh` | Bash gate that validates all four KA-6 JSON artifacts against schemas before commit |
