# Prototyping

## Summary

A prototype is an interactive representation of a product that simulates the user experience before development. Choose fidelity (low/medium/high) based on what you need to learn — concept validation needs paper, flow testing needs clicks, experience testing needs high-fidelity. Always define learning objectives before choosing a tool.

## Why

Static designs cannot convey interactions. Usability issues stay hidden until development, when fixing them is expensive. Prototyping surfaces interaction gaps with real users before a single line of production code is written.

## When To Use

- Validating whether users can complete a critical flow before development starts
- Aligning stakeholders on how something will work, not just how it looks
- Testing a risky design assumption (navigation structure, onboarding, checkout)
- Deciding fidelity level given project constraints and open questions
- Generating a structured prototype plan and usability test script from a design brief

## When NOT To Use

- The interaction is motion-dependent or too nuanced for text-based planning (agent can plan, not build)
- A live coded prototype is required — that crosses from UX planning into implementation
- No clear testing hypothesis exists — prototyping without defined learning goals wastes cycles
- Post-launch optimization where A/B testing or analytics provide faster signal

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Fidelity decision matrix, five-step prototype process, handoff artifacts |
| `content/02-rules.xml` | Concrete rules for scope, testing, and agent-usage gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/prototype-plan.md` | Prototype plan: objectives, fidelity, scope, interactive elements, test script |
| `templates/testing-notes.md` | Per-session observation log: tasks, quotes, issues, recommendations |
| `templates/scaffold-prototype.sh` | Bash script to scaffold a minimal HTML click-through prototype |
