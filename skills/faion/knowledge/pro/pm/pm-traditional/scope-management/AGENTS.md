# Scope Management

## Summary

Scope management defines, documents, and controls what a project will and will not deliver. It requires a written scope statement with explicit exclusions, a signed scope baseline, and a formal change-control gate — so every addition is evaluated for cost and schedule impact before it enters the project.

## Why

Scope creep is the leading cause of budget and schedule overrun. Without a locked baseline and a process to evaluate changes, teams absorb "small" additions until the project is unrecognizable. A written exclusions list closes the gap that vague deliverable language opens. Requirements traceability from source to test ensures nothing is forgotten and nothing unauthorized is built.

## When To Use

- Fixed-price or fixed-scope contracts where scope creep damages margin.
- Regulated programs (medical, finance, government) where scope is part of compliance evidence.
- Multi-vendor programs where contracted scope per vendor must compose into one deliverable.
- Strategic transformations (ERP, CRM, cloud migration) needing formal scope statement + WBS + validated deliverables.
- Projects showing scope creep symptoms: repeated re-baselining, "while you're in there" requests, confused acceptance criteria.

## When NOT To Use

- Pre-PMF startups iterating on hypotheses — strict scope control kills learning.
- Internal R&D or discovery sprints — locking scope before learning is anti-pattern.
- Pure agile teams with continuous discovery — backlog refinement replaces scope statements.
- One-person side projects — scope statement is overhead.
- When the root problem is unclear requirements or absent stakeholders; fix those first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Core concepts: product vs. project scope, scope baseline, scope creep, MoSCoW prioritization |
| `content/02-process.xml` | Five-step process: collect requirements, define scope, validate scope, control scope, requirements traceability |
| `content/03-rules.xml` | Concrete rules for scope creep prevention, acceptance criteria quality, and RTM coverage gates |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-doc.md` | Requirements documentation template (business, stakeholder, functional, non-functional) |
| `templates/scope-statement.md` | Project scope statement template with approval block |
| `templates/rtm-coverage.py` | Script: audits requirements traceability matrix coverage from YAML, exits non-zero on gaps |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/rtm_coverage.py` | Audit RTM YAML for design/build/test/accept coverage; exit non-zero on gaps |
