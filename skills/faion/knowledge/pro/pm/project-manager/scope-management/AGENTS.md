---
slug: scope-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Define, baseline, validate, control project scope: scope statement + MoSCoW-prioritised requirements + RTM in source control. Write exclusions before inclusions; cap Must at 60%.
content_id: "76b52fc36a22aa4f"
complexity: medium
produces: spec
est_tokens: 4700
tags: [scope, requirements, change-control, traceability, scope-creep]
---
# Scope Management

## Summary

**One-sentence:** Define, baseline, validate, control project scope: scope statement + MoSCoW-prioritised requirements + RTM in source control. Write exclusions before inclusions; cap Must at 60%.

**One-paragraph:** Define, baseline, validate, and control project scope to prevent uncontrolled expansion. Produces: scope statement (objectives, deliverables, exclusions, constraints, assumptions), requirements document with MoSCoW priorities (Must ≤60%), and a Requirements Traceability Matrix (RTM) linking every requirement to design, build, and test — stored as YAML in source control, not a Word doc. Write exclusions before inclusions — explicit 'not in scope' prevents 80% of scope disputes. Baseline scope at end of planning; every subsequent change goes through Change Control with cost/schedule/risk delta.

**Ефективно для:**

- Project initiation: scope statement + requirements + baselining
- Mid-project CRs where impact assessment must precede approval
- Multi-stakeholder programs with conflicting priorities
- Contracted / fixed-price work where every out-of-scope item is a margin event

## Applies If (ALL must hold)

- Project initiation: drafting scope statement, requirement collection, baselining
- Mid-project change requests where impact assessment must precede approval
- Multi-stakeholder programs with conflicting priorities (MoSCoW + traceability)
- Contracted / fixed-price work where every out-of-scope item is a margin event
- Requirements traceability for regulated domains (medtech, fintech, government)

## Skip If (ANY kills it)

- Continuous-discovery agile product — use rolling outcomes instead of scope baselines
- Pure research / spike work where scope is the question
- Internal tools with fewer than 10 users where formal sign-off is theater
- Crisis incident response — scope is 'stop the bleeding'

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder inputs | Markdown / interviews / RFP | BA / sponsor |
| Requirement candidates | YAML / CSV | elicitation |
| Design and test refs | URLs | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-register]] | Source stakeholders ground requirement attribution |
| [[project-integration]] | Baseline feeds integrated plan |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: exclusions-before-inclusions, ac-per-must, baseline-then-cr, rtm-in-source-control, must-cap-60 | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-requirements` | sonnet | Bucket into business/stakeholder/solution/transition/NFR |
| `validate-acceptance-criteria` | haiku | Tautology detection + AC presence check |
| `change-impact` | sonnet | Cross-area delta for CR |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-doc.md` | Requirements document (business, stakeholder, functional, non-functional) |
| `templates/scope-statement.md` | Scope statement with deliverables, boundaries, constraints, assumptions |
| `templates/rtm.yaml` | Requirements Traceability Matrix YAML schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/trace-check.py` | Flag must-have requirements missing design/test coverage in RTM | Pre-merge; weekly |
| `scripts/moscow-lint.py` | Enforce MoSCoW invariants (no MUST without AC, no MUST+Wont, 60% cap) | Pre-commit |
| `scripts/validate-scope-management.py` | RTM schema lint + exclusions-before-inclusions check | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[stakeholder-register]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
