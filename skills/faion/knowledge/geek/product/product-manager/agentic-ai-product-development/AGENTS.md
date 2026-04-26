# Agentic AI Product Development

## Summary

A product methodology for designing and shipping autonomous AI systems — agents that act toward a goal without user-triggering each step. Replaces the MVP (Minimum Viable Product) frame with MVI (Minimum Viable Intelligence): scope is determined by the intelligence level the system must achieve, not by feature count. Every spec must enumerate autonomous actions explicitly, define machine-verifiable goal states, and document the human-in-the-loop model before engineering starts.

## Why

Traditional AI feature specs describe behavior in natural language ("the agent will handle complex cases"), which is not implementable. Agentic products require a different type of success metric (goal achievement rate, autonomy ratio, cost-per-task) and a different failure model (edge-case recovery paths, behavioral regression tests). 40% of agentic pilots fail to productionize — the failure point is usually not the model but the absence of a production-grade escalation path.

## When To Use

- Writing a product spec where the core delivery mechanism is an autonomous agent (not a user-triggered model call)
- Defining MVI scope: which capabilities are core intelligence vs deferred to v2
- Choosing success metrics for an agentic feature (goal achievement rate, escalation rate, autonomy ratio, cost-per-task)
- Documenting the human-in-the-loop model for stakeholders
- Deciding which use cases have sufficient goal clarity and data access to support autonomous action

## When NOT To Use

- The use case is a conversational assistant or copilot — use `ai-native-product-development` instead
- Success criteria require a human judge ("does this feel good?") — agentic systems need machine-verifiable success conditions
- Organization lacks engineering maturity to build and monitor agentic pipelines
- Regulatory constraints require human review of every AI-generated output before it reaches users

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Agentic vs traditional AI; MVI frame; design principles; cost structure |
| `content/02-spec-checklist.xml` | Required sections in an agentic product spec; escalation-first rule |
| `content/03-metrics.xml` | Goal achievement rate, autonomy ratio, cost-per-task definitions and targets |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-metrics.py` | Dataclass + summary function for autonomy ratio and goal achievement rate per sprint |
| `templates/prompt-spec-writer.txt` | Prompt for drafting an agentic product requirements document |
| `templates/prompt-spec-reviewer.txt` | Prompt for reviewing a spec for missing escalation triggers and failure modes |
