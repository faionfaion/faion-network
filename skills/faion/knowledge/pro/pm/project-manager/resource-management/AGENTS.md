# Resource Management

## Summary

Identify required skills and quantities per work package, assess real availability (capped at 75-80% effective capacity), map resources to activities, level overloads via delay/split/add/cut options, and monitor utilization weekly against plan. Resources include human, physical, material, and financial — but human resource planning dominates and must never assume 100% capacity.

## Why

Bottlenecks from missing skills, uneven workload distribution, and schedule delays from unavailability trace back to plans built at 100% utilization that ignore meetings, interruptions, and PTO. Effective capacity for most knowledge workers is 75-80% of nominal hours; plans built above that ceiling always slip on the first sick week or sprint ceremony load.

## When To Use

- Multi-team programs where the same engineers are claimed by 2+ projects
- Onboarding or offboarding wave shifting skill mix within 30-60 days
- Agency or consulting context billing by utilization
- Mid-project resource crisis (key person quit, contractor delayed)
- Capacity planning ahead of quarterly OKR commitments

## When NOT To Use

- Stable single team under 8 people — informal allocation works; formal plans add overhead
- Pure agile teams committed to whole-team ownership — utilization tracking erodes psychological safety
- One-week sprint of throwaway research — over-planning waste
- Organisations where utilization % is used as a performance metric — creates burnout and gaming

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Resource categories, six-step process, leveling techniques, utilization guidelines |
| `content/02-workflow.xml` | Agentic capacity-planner and leveler pipeline, skill-matcher prompt, AI-agent gotchas |
| `content/03-tools-and-references.xml` | CLI tools, SaaS services, best practices, references |

## Templates

| File | Purpose |
|------|---------|
| `templates/resource-plan.md` | Resource plan with summary table, calendar grid, skill matrix, resource risks |
| `templates/resource-request.md` | Resource request form with role, skills, dates, justification, impact-if-not-filled |
| `templates/capacity.py` | Script: compute effective hours per person per week from roster, PTO, and meeting load |
