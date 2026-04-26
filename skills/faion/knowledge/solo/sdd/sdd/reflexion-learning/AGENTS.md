# Reflexion Learning

## Summary

Reflexion (NeurIPS 2023) is a verbal reinforcement learning paradigm where LLM agents improve through accumulated episodic memory rather than weight updates. Applied to SDD, it maps to the PDCA cycle: Plan (load patterns.md + mistakes.md), Do (execute with context), Check (evaluate against AC, generate verbal reflection), Act (write new PAT-NNN or MIS-NNN entries). External feedback signals — tests, linter, type checker — are mandatory; self-evaluation alone has a 64.5% blind-spot rate.

## Why

LLMs start fresh each session without memory of prior failures. Reflexion bridges this gap by maintaining persistent pattern and mistake files that are loaded at task start and updated at task end. Benchmark results: +10.9% on HumanEval, +22% on AlfWorld, +30% on HotpotQA compared to non-reflexion baselines. Gains come from the external feedback loop, not from self-evaluation.

## When To Use

- Any multi-task SDD workflow where agent quality must improve across tasks within a project
- When an agent has failed the same task type more than once
- Setting up a new project's `.aidocs/memory/` structure — Reflexion defines the memory architecture
- Unattended overnight agent batches where no human is available to correct mid-task failures

## When NOT To Use

- Single-shot one-off tasks with no follow-up — no memory to accumulate
- Tasks where external ground truth is unavailable (no tests, no linter, no type checker) — self-evaluation degrades quality
- Projects under 1 week old with fewer than 10 completed tasks — corpus too thin
- When PDCA overhead exceeds the value of the learning loop (very small tasks under ~5k tokens)

## Content

| File | What's inside |
|------|---------------|
| `content/01-pdca-cycle.xml` | PDCA phases, per-phase actions, integration with SDD quality gates |
| `content/02-memory-architecture.xml` | patterns.md, mistakes.md, session.md, decisions.md — structure and update rules |
| `content/03-confidence-calibration.xml` | Confidence scoring, update formula, decay rules, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-entry.md` | PAT-NNN entry template with confidence and metadata |
| `templates/update-confidence.py` | Python script to update a pattern's confidence score after task outcome |
