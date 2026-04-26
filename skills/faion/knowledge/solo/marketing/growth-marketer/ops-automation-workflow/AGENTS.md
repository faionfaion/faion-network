# Automation and Workflow

## Summary

A methodology for identifying, prioritizing, and building business automations that
replace repetitive manual tasks. Covers a time-audit process, ROI prioritization
matrix, tool selection, and workflow design patterns for lead capture, onboarding,
content distribution, and reporting. The core rule: manually define and run a
process at least once before automating it — automating an undefined process
creates a faster path to wrong outcomes.

## Why

Repetitive tasks (lead capture, email sequences, social posting, data sync) compound
into hours of weekly overhead and introduce human errors. Automation converts these
to zero-marginal-cost operations, freeing capacity for strategy and relationships.
The ROI threshold is >5x return in year one: (time saved × occurrences/month) ÷
(build time + monthly maintenance).

## When To Use

- Identified repetitive tasks consuming 30+ minutes per day or 1+ hour per week
- Error-prone manual process where mistakes have downstream cost (payment, data sync)
- Customer lifecycle event (signup, purchase, milestone) that always triggers the same steps
- Weekly or daily reporting pulled manually from multiple tools
- Content distribution that follows the same steps after each new piece

## When NOT To Use

- Process not yet defined — automate only what has been run manually and understood
- Decision-heavy workflow requiring judgment — automation handles triggers, not strategy
- Rare task (less than monthly) where build time exceeds annual time savings
- Tool integrations are unstable or in active development — automation will break

## Content

| File | What's inside |
|------|---------------|
| `content/01-audit-and-prioritize.xml` | Time audit categories, automation ROI formula, prioritization matrix |
| `content/02-workflow-patterns.xml` | Lead capture, onboarding, content distribution, weekly reporting patterns |
| `content/03-robustness-and-tools.xml` | Error handling, notification patterns, tool comparison table, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/automation-audit.md` | Weekly time audit: daily tasks, event-based tasks, total manual hours |
| `templates/automation-design-doc.md` | Single automation spec: trigger, workflow steps, error handling, testing |
| `templates/automation-inventory.md` | Active automation registry: name, trigger, actions, status |
