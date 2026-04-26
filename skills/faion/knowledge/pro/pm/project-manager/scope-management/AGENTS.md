# Scope Management

## Summary

Define, baseline, validate, and control project scope to prevent uncontrolled expansion. Scope management produces a scope statement (objectives, deliverables, exclusions, constraints, assumptions), a requirements document with MoSCoW priorities, and a traceability matrix linking every requirement to design, build, and test. The rule: write exclusions before inclusions — explicit "not in scope" prevents 80% of scope disputes.

## Why

Scope creep consumes budget and schedule while remaining invisible until too late. Without a baseline, there is no way to evaluate change requests objectively — every "small addition" appears free. A requirements traceability matrix (RTM) stored as YAML in source control (not a Word doc) stays live across the project and survives tool migrations.

## When To Use

- Project initiation: drafting scope statement, requirement collection, baselining
- Mid-project change requests where impact assessment must precede approval
- Multi-stakeholder programs with conflicting priorities (MoSCoW + traceability)
- Contracted/fixed-price work where every out-of-scope item is a margin event
- Requirements traceability for regulated domains (medtech, fintech, government)

## When NOT To Use

- Continuous-discovery agile product — use rolling outcomes instead of scope baselines
- Pure research/spike work where scope is the question, not the input
- Internal tools with < 10 users where formal sign-off is theater
- Crisis incident response — incident scope is "stop the bleeding", not a PMP doc

## Content

| File | What's inside |
|------|---------------|
| `content/01-scope-framework.xml` | Five-step scope process, requirement types, scope creep prevention rules |
| `content/02-traceability.xml` | RTM structure, MoSCoW invariants, agent gotchas for requirement extraction |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-doc.md` | Requirements document (business, stakeholder, functional, non-functional) |
| `templates/scope-statement.md` | Scope statement with deliverables, boundaries, constraints, assumptions |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/trace-check.py` | Flag must-have requirements missing design/test coverage in RTM CSV |
| `scripts/moscow-lint.py` | Enforce MoSCoW invariants (no MUST without AC, no MUST+Wont) |
