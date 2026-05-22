---
slug: delivery-sop-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Template for writing a productized-service runbook that lets a senior contractor execute a recurring service end-to-end without founder QA on every step.
content_id: "65fbde79d967f930"
tags: [pm, sop, runbook, productized-service, agency, delegation]
---

# Service Delivery SOP Template

## Summary

**One-sentence:** A template for writing operational SOPs / runbooks that productize a custom service into a repeatable, delegate-able offer with defined inputs, steps, decision points, deliverables, and quality gates.

**One-paragraph:** Solves the micro-agency bottleneck where every engagement requires founder QA because the work is implicit. Mechanism: take a service the founder currently executes manually, decompose into 5-15 named steps with explicit input requirements, decision points (with branch conditions), tool-by-tool actions, and quality gates per step, then ship the SOP as a versioned document that a senior contractor can execute with no clarification calls. Primary output: a runbook with success-criteria + a defined escalation path for edge cases.

## Applies If (ALL must hold)

- service has been delivered manually by the founder >= 5 times
- median delivery is now consistent enough that founder can predict 80% of the work
- founder is the constraint — backlog grows because only founder can execute
- target operator is a senior contractor / employee, NOT a junior who needs training material

## Skip If (ANY kills it)

- service delivered fewer than 5 times — no stable pattern to codify yet; deliver more first
- service is fundamentally creative / strategic (brand identity work, exec coaching) — SOP destroys quality
- founder cannot articulate the steps without "it depends" on every decision — service is not yet productizable
- target operator is junior who needs hand-holding — write a training manual, not an SOP

## Prerequisites

- list of past engagements (>= 5) with start/end dates + outputs delivered
- founder available for 2-3h to walk through one delivery while operator-or-PM records every action
- decision points where founder said "it depends" must be captured with what made it depend
- definition of success per engagement type (what client paid for, what passed acceptance)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-operations/process-mapping` | SOP is a process map with branches; consume the mapping notation |
| `pro/pm/project-manager/escalation-protocol` | Edge-case escalation path is a sub-document referenced by SOP |
| `solo/sdd/sdd/raci-matrix` | SOP must name owner per step — derive RACI from the matrix not redefine |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: input-defined-per-step, decision-with-branch-conditions, quality-gate-per-step, escalation-path-defined, time-budget-per-step | ~900 |
| `content/02-output-contract.xml` | essential | SOP structure contract (step record schema, gate fields, escalation links) + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (it-depends-cop-out, gate-without-criteria, missing-edge-case-branch, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `step_decomposition_draft` | sonnet | Convert founder walkthrough transcript into named steps |
| `decision_branch_extraction` | sonnet | Find "it depends" moments, formalize as branch with condition |
| `quality_gate_synthesis` | opus | Cross-step synthesis — gates must compose into engagement-level acceptance |
| `escalation_path_template_fill` | haiku | Fill the named-escalation-owner template per step |

## Templates

| File | Purpose |
|------|---------|
| `templates/sop.md` | Runbook document template with frontmatter + 15-step skeleton |
| `templates/step-record.json` | JSON Schema for a single SOP step (input / action / decision / output / gate) |
| `templates/escalation-map.md` | Edge-case branch -> named escalation owner map |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sop.py` | Validates SOP against step-record schema + gate completeness | Before handing SOP to a contractor for first execution |
| `scripts/audit-sop-execution.py` | Compares actual delivery log vs SOP, flags steps that drifted | After first 2-3 executions, to refine SOP |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `productization-roadmap`, `subcontractor-onboarding`, `service-pricing-model`
- external: [E-Myth Revisited (Gerber)](https://en.wikipedia.org/wiki/The_E-Myth_Revisited) · [Productize Your Service (Eisenberg)](https://www.amazon.com/Productize-Service/dp/) · [SweetProcess SOP Patterns](https://www.sweetprocess.com/sop/)
