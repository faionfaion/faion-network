# Backlog Grooming and Roadmapping

## Summary

Backlog grooming is the weekly practice of scoring, reordering, and refining items in `.aidocs/backlog/` using RICE or MoSCoW frameworks. Roadmapping translates the groomed backlog into a Now/Next/Later horizon document. Agent-generated RICE scores are always marked `[estimate]` — they are hypotheses, not data. Never more than 3 items as P0. Use Now/Next/Later over date-based roadmaps to avoid false precision.

## Why

Ungroomed backlogs accumulate low-value items that block visibility of high-impact work. Without systematic prioritization, teams execute on interesting-but-low-value items while critical features wait. LLM agents cannot distinguish strategic P0s from tactical P0s without explicit business context — human validation of prioritization decisions is mandatory before items move to todo/.

## When To Use

- Weekly or monthly: agent-assisted grooming session to score and reorder `.aidocs/backlog/`
- When the backlog exceeds 20 items without re-prioritization in 2+ weeks
- Starting a new quarter: generate or update roadmap.md from current backlog state
- When performing MVP scoping: run MoSCoW analysis against a candidate feature set

## When NOT To Use

- As a replacement for human strategic decisions — P0 prioritization requires business context the agent lacks
- During active feature execution — grooming is planning work; mixing them degrades both
- When roadmap.md does not yet exist — create it with human-defined horizons first
- For items requiring stakeholder input the agent cannot simulate (pricing, partnerships)

## Content

| File | What's inside |
|------|---------------|
| `content/01-prioritization-frameworks.xml` | RICE scoring, MoSCoW, Value vs Effort matrix — when to use each |
| `content/02-roadmap-types.xml` | Now/Next/Later vs time-based vs theme-based roadmaps; why to avoid dates |
| `content/03-agent-limitations.xml` | AI confidence trap, score inflation, pruning failure, strategic blindness |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-item.md` | Spec stub with RICE fields for a new backlog feature |
| `templates/roadmap-skeleton.md` | Now/Next/Later roadmap structure with Won't-Do section |
