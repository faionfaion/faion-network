# SDD Document Templates

## Summary

**One-sentence:** A collection of canonical templates for every SDD artifact: Constitution, Spec, Design, Implementation Plan, Task, Roadmap, Backlog Item, Confidence Check, Pattern Record, and Mistake Record.

**One-paragraph:** A collection of canonical templates for every SDD artifact: Constitution, Spec, Design, Implementation Plan, Task, Roadmap, Backlog Item, Confidence Check, Pattern Record, and Mistake Record. Use these as output schemas — provide a template in the system prompt, instruct the agent to fill each section, and enforce that no non-standard sections are added.

## Applies If (ALL must hold)

- Starting any SDD artifact from scratch — always start from the relevant template.
- Onboarding a new project: the Constitution template captures tech stack and standards before feature work begins.
- When a subagent must produce a spec, design, task, or implementation plan with consistent structure.
- Generating backlog items, roadmap entries, or confidence-check reports during planning sessions.

## Skip If (ANY kills it)

- When an SDD artifact already exists and only needs incremental updates — edit in place.
- For one-off notes or research spikes that do not feed into task execution.
- Generating freeform documentation not part of the SDD lifecycle.

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

- parent skill: `solo/sdd/sdd-planning/`
