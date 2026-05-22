---
slug: ops-automation-workflow
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for identifying, prioritizing, and building business automations that replace repetitive manual tasks.
content_id: "e4e2dcade5f66732"
tags: [automation, workflow, marketing-ops, roi, integration]
---
# Automation and Workflow

## Summary

**One-sentence:** A methodology for identifying, prioritizing, and building business automations that replace repetitive manual tasks.

**One-paragraph:** A methodology for identifying, prioritizing, and building business automations that replace repetitive manual tasks. Covers a time-audit process, ROI prioritization matrix, tool selection, and workflow design patterns for lead capture, onboarding, content distribution, and reporting. The core rule: manually define and run a process at least once before automating it — automating an undefined process creates a faster path to wrong outcomes.

## Applies If (ALL must hold)

- Identified repetitive tasks consuming 30+ minutes per day or 1+ hour per week
- Error-prone manual process where mistakes have downstream cost (payment, data sync)
- Customer lifecycle event (signup, purchase, milestone) that always triggers the same steps
- Weekly or daily reporting pulled manually from multiple tools
- Content distribution that follows the same steps after each new piece

## Skip If (ANY kills it)

- Process not yet defined — automate only what has been run manually and understood
- Decision-heavy workflow requiring judgment — automation handles triggers, not strategy
- Rare task (less than monthly) where build time exceeds annual time savings
- Tool integrations are unstable or in active development — automation will break

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

- parent skill: `solo/marketing/growth-marketer/`
